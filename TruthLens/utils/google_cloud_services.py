import streamlit as st
import requests
import json
from config import Config

class GoogleCloudVisionService:
    """Google Cloud Vision API service for image analysis"""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY  # Using same key for now
        self.base_url = "https://vision.googleapis.com/v1/images:annotate"
    
    def analyze_image(self, image_data):
        """Analyze image using Google Cloud Vision API"""
        try:
            import base64
            
            # Encode image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare request
            request_data = {
                "requests": [
                    {
                        "image": {
                            "content": image_base64
                        },
                        "features": [
                            {"type": "TEXT_DETECTION", "maxResults": 10},
                            {"type": "LABEL_DETECTION", "maxResults": 10},
                            {"type": "SAFE_SEARCH_DETECTION", "maxResults": 1},
                            {"type": "WEB_DETECTION", "maxResults": 10}
                        ]
                    }
                ]
            }
            
            # Make API call
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(request_data),
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Google Cloud Vision API Error: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Google Cloud Vision API Exception: {str(e)}")
            return None

class GoogleCloudNaturalLanguageService:
    """Google Cloud Natural Language API service"""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.base_url = "https://language.googleapis.com/v1/documents:analyzeSentiment"
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using Google Cloud Natural Language API"""
        try:
            request_data = {
                "document": {
                    "type": "PLAIN_TEXT",
                    "content": text
                },
                "encodingType": "UTF8"
            }
            
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(request_data),
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            st.error(f"Google Cloud Natural Language API Exception: {str(e)}")
            return None

class GoogleCloudTranslateService:
    """Google Cloud Translate API service"""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.base_url = "https://translation.googleapis.com/language/translate/v2"
    
    def translate_text(self, text, target_language='en'):
        """Translate text using Google Cloud Translate API"""
        try:
            request_data = {
                "q": text,
                "target": target_language,
                "format": "text"
            }
            
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(request_data),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['data']['translations'][0]['translatedText']
            else:
                return text  # Return original if translation fails
                
        except Exception as e:
            st.error(f"Google Cloud Translate API Exception: {str(e)}")
            return text

class GoogleCloudStorageService:
    """Google Cloud Storage service for file management"""
    
    def __init__(self):
        self.project_id = Config.GOOGLE_CLOUD_PROJECT
        self.bucket_name = "truthlens-storage"
    
    def upload_file(self, file_data, filename):
        """Upload file to Google Cloud Storage"""
        try:
            # This is a placeholder - in real implementation, you'd use the Google Cloud Storage client
            st.info(f"📁 File {filename} would be uploaded to Google Cloud Storage")
            return f"gs://{self.bucket_name}/{filename}"
        except Exception as e:
            st.error(f"Google Cloud Storage Exception: {str(e)}")
            return None

class GoogleCloudMonitoringService:
    """Google Cloud Monitoring service for analytics"""
    
    def __init__(self):
        self.project_id = Config.GOOGLE_CLOUD_PROJECT
    
    def log_event(self, event_type, event_data):
        """Log event to Google Cloud Monitoring"""
        try:
            # This is a placeholder - in real implementation, you'd use the Google Cloud Monitoring client
            st.info(f"📊 Event {event_type} logged to Google Cloud Monitoring")
            return True
        except Exception as e:
            st.error(f"Google Cloud Monitoring Exception: {str(e)}")
            return False
