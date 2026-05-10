# backend/api/eval.py
# ═══════════════════════════════════════════════════════════════
# LLM Evaluation API
# Evaluates EchoAI and AtlasAI responses across 4 metrics:
#   1. Relevance   — does the answer address the question?
#   2. Accuracy    — is the answer factually correct?
#   3. Fluency     — is the language natural and clear?
#   4. Groundedness— (AtlasAI only) is answer based on context?
#
# Routes:
#   POST /eval/response      — evaluate a single response
#   POST /eval/batch         — evaluate multiple at once
#   GET  /eval/history       — get eval logs for current user
# ═══════════════════════════════════════════════════════════════

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json
import uuid

from db.database import get_db
from dependencies.auth import get_current_user
from models.user import User
from core.llm_engine import generate_echo_response, generate_echo_stream
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


# ═══════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════
class EvalRequest(BaseModel):
    question:   str
    response:   str
    context:    Optional[str] = None   # AtlasAI: retrieved RAG context
    mode:       str = "EchoAI"         # "EchoAI" | "AtlasAI"

class EvalResult(BaseModel):
    relevance:     float   # 0.0 – 1.0
    accuracy:      float
    fluency:       float
    groundedness:  Optional[float] = None   # AtlasAI only
    overall:       float
    feedback:      str
    evaluated_at:  str

class BatchEvalRequest(BaseModel):
    items: List[EvalRequest]

class BatchEvalResult(BaseModel):
    results:      List[EvalResult]
    avg_overall:  float


# ═══════════════════════════════════════════════════════════════
# EVAL PROMPT BUILDER
# ═══════════════════════════════════════════════════════════════
def _build_eval_prompt(req: EvalRequest) -> str:
    context_section = ""
    groundedness_section = ""

    if req.mode == "AtlasAI" and req.context:
        context_section = f"\nContext (retrieved from course):\n{req.context}\n"
        groundedness_section = (
            '  "groundedness": <float 0.0-1.0 — is the response based only on the provided context?>,\n'
        )

    return f"""You are an LLM evaluator. Score the AI response below on the following metrics.
Return ONLY valid JSON — no explanation outside the JSON.

Question: {req.question}
{context_section}
AI Response: {req.response}

Score each metric from 0.0 (worst) to 1.0 (best):
{{
  "relevance":    <float — does the response address the question?>,
  "accuracy":     <float — is the information factually correct?>,
  "fluency":      <float — is the language natural, clear, and grammatically correct?>,
{groundedness_section}  "overall":      <float — weighted average of all scores>,
  "feedback":     "<one sentence of constructive feedback>"
}}

Rules:
- Return ONLY the JSON object, no markdown fences, no extra text.
- All float values must be between 0.0 and 1.0.
- Be strict and calibrated — a score of 0.9+ means near-perfect.
"""


# ═══════════════════════════════════════════════════════════════
# CORE EVALUATOR
# ═══════════════════════════════════════════════════════════════
def _run_eval(req: EvalRequest) -> EvalResult:
    """
    Sends evaluation prompt to the LLM (using fast/phi3 model).
    Parses JSON response and returns EvalResult.
    """
    prompt   = _build_eval_prompt(req)
    messages = [{"role": "user", "content": prompt}]

    raw = "".join(
    generate_echo_stream(
        messages,
        speed="fast",
        request_id=f"eval-{uuid.uuid4()}"   # 👈 IMPORTANT
    )
)

    # Strip markdown fences if model wrapped in ```json ... ```
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.error(f"[EVAL] JSON parse failed: {raw[:200]}")
        raise HTTPException(
            status_code=500,
            detail="LLM returned invalid JSON during evaluation."
        )

    # Clamp all floats to [0.0, 1.0]
    def _clamp(v, default=0.5):
        try: return max(0.0, min(1.0, float(v)))
        except: return default

    relevance    = _clamp(data.get("relevance",    0.5))
    accuracy     = _clamp(data.get("accuracy",     0.5))
    fluency      = _clamp(data.get("fluency",      0.5))
    groundedness = (_clamp(data.get("groundedness")) 
                    if req.mode == "AtlasAI" and "groundedness" in data 
                    else None)
    overall      = _clamp(data.get("overall", (relevance + accuracy + fluency) / 3))
    feedback     = str(data.get("feedback", "No feedback provided."))[:500]

    return EvalResult(
        relevance    = relevance,
        accuracy     = accuracy,
        fluency      = fluency,
        groundedness = groundedness,
        overall      = overall,
        feedback     = feedback,
        evaluated_at = datetime.utcnow().isoformat(),
    )


# ═══════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════

# ── 1. Single evaluation ────────────────────────────────────────
@router.post("/response", response_model=EvalResult)
async def evaluate_response(
    data: EvalRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Evaluate a single AI response.

    Example body:
    {
        "question": "What is the CSS Box Model?",
        "response": "The CSS Box Model consists of content, padding, border, and margin.",
        "mode": "EchoAI"
    }
    """
    logger.info(f"[EVAL] Single eval | user={current_user.id} | mode={data.mode}")

    result = _run_eval(data)

    # Optionally save to DB (simple log table — extend if needed)
    _log_eval(db, current_user.id, data, result)

    logger.info(
        f"[EVAL] Result | user={current_user.id} | "
        f"overall={result.overall:.2f} | relevance={result.relevance:.2f}"
    )
    return result


# ── 2. Batch evaluation ─────────────────────────────────────────
@router.post("/batch", response_model=BatchEvalResult)
async def evaluate_batch(
    data: BatchEvalRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Evaluate multiple responses at once.
    Returns individual results + average overall score.
    """
    if not data.items:
        raise HTTPException(status_code=400, detail="No items to evaluate.")
    if len(data.items) > 20:
        raise HTTPException(status_code=400, detail="Max 20 items per batch.")

    logger.info(f"[EVAL] Batch eval | user={current_user.id} | count={len(data.items)}")

    results = []
    for item in data.items:
        try:
            r = _run_eval(item)
            results.append(r)
            _log_eval(db, current_user.id, item, r)
        except Exception as e:
            logger.error(f"[EVAL] Batch item failed: {e}")
            # Add a failed placeholder so indices stay aligned
            results.append(EvalResult(
                relevance=0.0, accuracy=0.0, fluency=0.0,
                overall=0.0, feedback=f"Evaluation failed: {e}",
                evaluated_at=datetime.utcnow().isoformat()
            ))

    avg = sum(r.overall for r in results) / len(results)

    return BatchEvalResult(results=results, avg_overall=round(avg, 4))


# ── 3. Eval history ─────────────────────────────────────────────
@router.get("/history")
def eval_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns the last {limit} evaluation logs for the current user.
    """
    from models.eval_log import EvalLog
    logs = (
        db.query(EvalLog)
        .filter(EvalLog.user_id == current_user.id)
        .order_by(EvalLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id":           l.id,
            "mode":         l.mode,
            "question":     l.question[:80],
            "overall":      l.overall,
            "relevance":    l.relevance,
            "accuracy":     l.accuracy,
            "fluency":      l.fluency,
            "groundedness": l.groundedness,
            "feedback":     l.feedback,
            "created_at":   str(l.created_at),
        }
        for l in logs
    ]


# ═══════════════════════════════════════════════════════════════
# DB LOG HELPER
# ═══════════════════════════════════════════════════════════════
def _log_eval(db: Session, user_id: int, req: EvalRequest, result: EvalResult):
    try:
        from models.eval_log import EvalLog
        log = EvalLog(
            user_id      = user_id,
            mode         = req.mode,
            question     = req.question[:500],
            response     = req.response[:1000],
            relevance    = result.relevance,
            accuracy     = result.accuracy,
            fluency      = result.fluency,
            groundedness = result.groundedness,
            overall      = result.overall,
            feedback     = result.feedback,
        )
        db.add(log)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"[EVAL] Log save error: {e}")
        
# ─────────────────────────────────────────────
# INTERNAL AUTO EVAL FUNCTION
# Used by chat.py and rag.py
# ─────────────────────────────────────────────
def auto_eval_and_log(
    db: Session,
    user_id: int,
    question: str,
    response: str,
    mode: str,
    context: str = None,
):
    """
    Internal helper:
    evaluates response automatically and stores result in DB.
    """

    try:
        req = EvalRequest(
            question=question,
            response=response,
            context=context,
            mode=mode,
        )

        result = _run_eval(req)

        _log_eval(
            db=db,
            user_id=user_id,
            req=req,
            result=result,
        )

        logger.info(
            f"[AUTO EVAL] Saved | user={user_id} | overall={result.overall}"
        )

    except Exception as e:
        logger.error(f"[AUTO EVAL] Failed: {e}")