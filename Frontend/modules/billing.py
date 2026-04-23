# modules/billing.py
# ============================================
# NexaAI Billing System
# Plans: Free | Pro (monthly) | Max (yearly)
# ============================================

import streamlit as st
import requests
from datetime import datetime, date

BACKEND_URL = "http://localhost:8000"

# ============================================
# PLAN DEFINITIONS
# ============================================
PLANS = {
    "Free": {
        "price": "₹0",
        "period": "Forever free",
        "color": "#8B949E",
        "features": [
            "✓ AtlasAI — Course-based RAG (Full Access)",
            "✓ EchoAI — Limited 10 queries/day",
            "✓ Basic AI Insights",
            "✓ Profile & Activity Log",
            "✓ Community Support",
        ],
        "limits": {
            "echoai_daily": 10,
            "atlasai": "unlimited",
            "insights": "basic",
        }
    },
    "Plus": {   # 🔁 Pro → Plus
        "price": "₹199",
        "period": "per month",
        "color": "#8B949E",
        "features": [
            "✓ Everything in Free, plus:",
            "✓ AtlasAI — Unlimited RAG queries",
            "✓ EchoAI — 100 queries/day (all speeds)",
            "✓ Advanced AI Insights",
            "✓ Priority Support",
            "✓ Profile Insights Analytics",
        ],
        "limits": {
            "echoai_daily": 100,
            "atlasai": "unlimited",
            "insights": "advanced",
        }
    },
    "Pro": {   # 🔁 Max → Pro
        "price": "₹2,499",
        "period": "per year (save 58%)",
        "color": "#8B949E",
        "features": [
            "✓ Everything in Plus, plus:",
            "✓ EchoAI — Unlimited queries (all speeds)",
            "✓ Smart Mode — Full Access",
            "✓ Early Access to New AI Features",
            "✓ Dedicated Support",
            "✓ Annual billing — Best value",
        ],
        "limits": {
            "echoai_daily": "unlimited",
            "atlasai": "unlimited",
            "insights": "advanced",
        }
    }
}

# ============================================
# PLAN LIMITS ENFORCER
# ============================================
def check_echoai_limit() -> tuple[bool, str]:
    """
    Returns (allowed: bool, message: str)
    Call this before every EchoAI request in llm_ui.py
    """
    plan = st.session_state.get("plan", "Free")
    today = str(date.today())

    # Init daily counter
    if "echoai_usage" not in st.session_state:
        st.session_state.echoai_usage = {"date": today, "count": 0}

    # Reset counter if new day
    if st.session_state.echoai_usage["date"] != today:
        st.session_state.echoai_usage = {"date": today, "count": 0}

    limit = PLANS[plan]["limits"]["echoai_daily"]

    if limit == "unlimited":
        st.session_state.echoai_usage["count"] += 1
        return True, ""

    if st.session_state.echoai_usage["count"] >= limit:
        return False, f"Daily EchoAI limit reached ({limit} queries). Upgrade your plan for more."

    st.session_state.echoai_usage["count"] += 1
    return True, ""

def get_remaining_echoai() -> str:
    """Returns remaining EchoAI queries for today"""
    plan = st.session_state.get("plan", "Free")
    limit = PLANS[plan]["limits"]["echoai_daily"]
    if limit == "unlimited":
        return "Unlimited"
    today = str(date.today())
    usage = st.session_state.get("echoai_usage", {})
    if usage.get("date") != today:
        return str(limit)
    used = usage.get("count", 0)
    return str(max(0, limit - used))

# ============================================
# BILLING UI
# ============================================
def render_billing():
    st.markdown("""
        <style>
        .plan-card {
            background-color: #0E1117;
            border: 1px solid #30363D;
            border-radius: 15px;
            padding: 30px;
            min-height: 520px;
            transition: transform 0.3s;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .plan-card:hover {
            border: 2px solid #3b82f6 !important;
            transform: translateY(-5px);
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        }
        .plan-card.active-plan {
            border: 2px solid #10b981 !important;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }
        .price-text {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 0px;
        }
        .feature-list {
            font-size: 14px;
            color: #8B949E;
            margin-top: 20px;
            line-height: 2.0;
        }
        </style>
    """, unsafe_allow_html=True)

    if "plan" not in st.session_state:
        st.session_state.plan = "Free"

    current_plan = st.session_state.plan

    st.markdown("<h1 style='text-align:center; font-size:48px;'>Explore Plans</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8B949E;'>Choose the plan that fits your learning journey.</p>", unsafe_allow_html=True)

    # ---- CURRENT PLAN BANNER ----
    plan_info = PLANS[current_plan]
    remaining = get_remaining_echoai()
    st.markdown(f"""
        <div style='background:#111; border:1px solid #222; border-radius:12px;
             padding:16px 24px; margin:20px 0; display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <span style='color:#10b981; font-weight:700;'>
    Current Plan: {current_plan}
</span>
                <span style='color:#8B949E; font-size:13px; margin-left:12px;'>{plan_info["price"]} {plan_info["period"]}</span>
            </div>
            <div style='color:#8B949E; font-size:13px;'>
                EchoAI today: <b style='color:#f3f4f6;'>{remaining}</b> queries remaining
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("##")
    col1, col2, col3 = st.columns(3)

    # ---- FREE ----
    with col1:
        is_current = current_plan == "Free"
        border_cls = "active-plan" if is_current else ""
        p = PLANS["Free"]
        features_html = "".join([f"{f}<br>" for f in p["features"]])
        st.markdown(f"""
            <div class="plan-card {border_cls}">
                <div>
                    <h2 style='color:{p["color"]};'>Free</h2>
                    <p style='color:#8B949E;'>Basic access for students</p>
                    <p class='price-text'>{p['price']}</p>
                    <p style='color:#8B949E; font-size:12px;'>{p['period']}</p>
                    <div class='feature-list'>{features_html}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if is_current:
            st.button("Current Plan ✓", key="free_btn", use_container_width=True, disabled=True)
        else:
            if st.button("Downgrade to Free", key="free_btn", use_container_width=True):
                st.session_state.plan = "Free"
                st.success("Downgraded to Free plan.")
                st.rerun()

    # ---- Plus ----
    with col2:
        is_current = current_plan == "Plus"
        border_cls = "active-plan" if is_current else ""
        p = PLANS["Plus"]
        features_html = "".join([f"{f}<br>" for f in p["features"]])
        st.markdown(f"""
            <div class="plan-card {border_cls}">
                <div>
                    <h2 style='color:{p["color"]};'>Plus</h2>
                    <p style='color:#8B949E;'>For serious learners</p>
                    <p class='price-text'>{p['price']}</p>
                    <p style='color:#8B949E; font-size:12px;'>{p['period']}</p>
                    <div class='feature-list'>{features_html}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if is_current:
            st.button("Current Plan ✓", key="plus_current_btn", use_container_width=True, disabled=True)
        else:
            if st.button("Upgrade to Plus", key="upgrade_plus_btn", type="primary", use_container_width=True):
                st.session_state.pending_plan = "Plus"
                st.session_state.view = "Plus_Payment"
                st.rerun()

    # ---- PRo ----
    with col3:
        is_current = current_plan == "Pro"
        border_cls = "active-plan" if is_current else ""
        p = PLANS["Pro"]
        features_html = "".join([f"{f}<br>" for f in p["features"]])
        st.markdown(f"""
            <div class="plan-card {border_cls}">
                <div>
                    <h2 style='color:{p["color"]};'>Pro</h2>
                    <p style='color:#8B949E;'>For power users</p>
                    <p class='price-text'>{p['price']}</p>
                    <p style='color:#8B949E; font-size:12px;'>{p['period']}</p>
                    <div class='feature-list'>{features_html}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if is_current:
            st.button("Current Plan ✓", key="pro_current_btn", use_container_width=True, disabled=True)
        else:
            if st.button("Upgrade to Pro", key="upgrade_pro_btn", use_container_width=True):
                st.session_state.pending_plan ="Pro"
                st.session_state.view = "Pro_Payment"
                st.rerun()

    


# ============================================
# PAYMENT PAGES
# ============================================
def render_plus_payment():
    st.title("Plus Plan Checkout")
    st.caption("Monthly billing — cancel anytime")
    st.divider()

    st.subheader("Plan Summary")
    st.info("Plus Plan — ₹199/month | Billed monthly")

    col_feat, col_pay = st.columns([1, 1])

    with col_feat:
        st.markdown("**What you get:**")
        for f in PLANS["Plus"]["features"]:
            st.markdown(f"- {f.replace('✓ ', '')}")

    with col_pay:
        st.subheader("Billing Details")
        name  = st.text_input("Full Name",  value=st.session_state.profile_data.get("name", ""))
        email = st.text_input("Email",       value=st.session_state.profile_data.get("email", ""))

        st.subheader("Payment Method")
        method = st.radio("Choose method", ["UPI", "Card", "Net Banking"], horizontal=True)

        if method == "UPI":
            upi_id = st.text_input("Enter UPI ID", placeholder="yourname@upi")

        elif method == "Card":
            st.text_input("Card Number", placeholder="•••• •••• •••• ••••", max_chars=19)
            c1, c2, c3 = st.columns(3)
            with c1: st.text_input("Expiry MM", max_chars=2)
            with c2: st.text_input("Expiry YY", max_chars=2)
            with c3: st.text_input("CVV", max_chars=3, type="password")

        elif method == "Net Banking":
            st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB"])

    st.divider()
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Back", use_container_width=True):
            st.session_state.view = "Billing"
            st.rerun()
    with b2:
        if st.button("Pay ₹199/month", type="primary", use_container_width=True):
            if not name or not email:
                st.error("Please fill billing details.")
            else:
                # ✅ Activate Plus plan
                st.session_state.plan = "Plus"
                st.session_state.plan_start = str(date.today())
                # Reset daily counter
                st.session_state.echoai_usage = {"date": str(date.today()), "count": 0}
                from user_profile import add_activity
                add_activity("💳", "Upgraded to Plus", f"Plus plan activated for {email}")
                st.success("Payment Successful! Plus Plan Activated")
                st.balloons()
                import time; time.sleep(2)
                st.session_state.view = "Billing"
                st.rerun()


def render_pro_payment():
    st.title("Pro Plan Checkout")
    st.caption("Yearly billing — best value, save 58%")
    st.divider()

    st.subheader("Plan Summary")
    st.success("Pro Plan — ₹2,499/year | Save ₹6,989 vs monthly Pro")

    col_feat, col_pay = st.columns([1, 1])

    with col_feat:
        st.markdown("**What you get:**")
        for f in PLANS["Pro"]["features"]:
            st.markdown(f"- {f.replace('✓ ', '')}")

    with col_pay:
        st.subheader("Billing Details")
        name  = st.text_input("Full Name",  value=st.session_state.profile_data.get("name", ""))
        email = st.text_input("Email",       value=st.session_state.profile_data.get("email", ""))

        st.subheader("Payment Method")
        method = st.radio("Choose method", ["UPI", "Card", "Net Banking"], horizontal=True)

        if method == "UPI":
            st.text_input("Enter UPI ID", placeholder="yourname@upi")

        elif method == "Card":
            st.text_input("Card Number", placeholder="•••• •••• •••• ••••", max_chars=19)
            c1, c2, c3 = st.columns(3)
            with c1: st.text_input("Expiry MM", max_chars=2)
            with c2: st.text_input("Expiry YY", max_chars=2)
            with c3: st.text_input("CVV", max_chars=3, type="password")

        elif method == "Net Banking":
            st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB"])

    st.divider()
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Back", use_container_width=True):
            st.session_state.view = "Billing"
            st.rerun()
    with b2:
        if st.button("Pay ₹2,499/year", type="primary", use_container_width=True):
            if not name or not email:
                st.error("Please fill billing details.")
            else:
                # ✅ Activate Max plan
                st.session_state.plan = "Pro"
                st.session_state.plan_start = str(date.today())
                # Reset daily counter
                st.session_state.echoai_usage = {"date": str(date.today()), "count": 0}
                from user_profile import add_activity
                add_activity("💳", "Upgraded to Pro", f"Pro plan activated for {email}")
                st.success("Payment Successful! Pro Plan Activated ")
                st.balloons()
                import time; time.sleep(2)
                st.session_state.view = "Billing"
                st.rerun()
