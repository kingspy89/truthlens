import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration management"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDCGUgJR20zmhvlrkYVa4HUDE-W_Wk7Tbs")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", GEMINI_API_KEY)
    
    # News APIs
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "27fc63acd5064608a6a1387488c7208b")
    NEWSDATA_KEY = os.getenv("NEWSDATA_API_KEY", "ub_5b6d7697fe6c4f9d8cb9ce964f292760")
    
    # Firebase (for backend)
    FIREBASE_CONFIG = {
        "apiKey": os.getenv("FIREBASE_API_KEY", ""),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": os.getenv("FIREBASE_PROJECT_ID", "truthlens-2025"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId": os.getenv("FIREBASE_APP_ID", "")
    }
    
    # Google Cloud
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "misinformation-detector-2025")
    
    # App Settings
    APP_NAME = "TruthLens"
    VERSION = "2.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

def setup_page_config():
    """Setup Streamlit page configuration"""
    st.set_page_config(
        page_title=f"{Config.APP_NAME} - AI Misinformation Detector",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-username/truthlens',
            'Report a bug': 'https://github.com/your-username/truthlens/issues',
            'About': f"# {Config.APP_NAME} v{Config.VERSION}\nForensic-level misinformation detection system powered by AI"
        }
    )
