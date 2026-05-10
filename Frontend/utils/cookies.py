import os
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st
load_dotenv()

cookies = EncryptedCookieManager(
    prefix="nexa_ai_",
    password=os.getenv("SECRET_KEY")
)

if not cookies.ready():
    if not cookies.ready():
        st.stop()
    raise Exception("Cookies not ready")