# services/rag_service.py
# atlasAI - RAG (Retrieval-Augmented Generation) Service
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests

# ✅ Load once (important for performance)
df = joblib.load('LLM/embeddings.joblib')


def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    return r.json()["embeddings"]


def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    })
    return r.json()


def generate_rag_response(user_query: str):
    try:
        # 🔹 Step 1: Create embedding
        question_embedding = create_embedding([user_query])[0]

        # 🔹 Step 2: Similarity search
        similarities = cosine_similarity(
            np.vstack(df['embedding']),
            [question_embedding]
        ).flatten()

        top_results = 3
        max_indx = similarities.argsort()[::-1][:top_results]

        new_df = df.loc[max_indx]

        # 🔹 Step 3: Prompt creation
        prompt = f"""
        I am teaching web development using Sigma web development course.

        Here are relevant video chunks:
        {new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

        ---------------------------------
        Question: "{user_query}"

        Instructions:
        - Answer in a human-friendly way
        - Mention video number and timestamp
        - Guide user to correct video
        - If unrelated, say you only answer course-related questions
        """

        # 🔹 Step 4: LLM call
        response = inference(prompt)["response"]

        return response
    
    except Exception as e:
        return f"RAG Error: {str(e)}"

