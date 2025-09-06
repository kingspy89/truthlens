import requests
import streamlit as st
from config import Config

class GeminiService:
    """Enhanced Gemini AI service with specialized prompts"""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def test_connection(self):
        """Test if Gemini API is working"""
        try:
            response = self._make_request("Hello", model="gemini-1.5-flash")
            return response is not None
        except:
            return False
    
    def forensic_analysis(self, text, language="en"):
        """Specialized forensic analysis prompt"""
        prompt = f"""
        As a digital forensics expert, analyze this content for misinformation:
        
        CONTENT: "{text}"
        
        IMPORTANT: Start your VERACITY ASSESSMENT with one of these clear statements:
        - "FALSE INFORMATION" if the content is factually incorrect
        - "MISLEADING" if the content is partially true but deceptive
        - "TRUE" if the content is factually accurate
        - "UNVERIFIED" if you cannot determine accuracy
        
        Provide analysis in this format:
        
        🔍 VERACITY ASSESSMENT:
        [Start with FALSE INFORMATION/MISLEADING/TRUE/UNVERIFIED, then explain why]
        
        🧬 MANIPULATION TACTICS:
        [What psychological tricks are used?]
        
        📊 EVIDENCE EVALUATION:
        [What evidence supports/contradicts this? Include specific sources, studies, or articles]
        
        🎯 TARGET ANALYSIS:
        [Who is this meant to influence and how?]
        
        ⚠️ HARM POTENTIAL:
        [What damage could this cause if it spreads?]
        
        🛡️ COUNTER-NARRATIVE:
        [What's the accurate information? Include links to credible sources]
        
        📋 VERIFICATION STEPS:
        [How can users verify this themselves? Include specific websites and search terms]
        
        🔗 SOURCE LINKS & ARTICLES:
        [Provide 3-5 credible source links that refute or support this claim. Format as:
        - Source Name: [Brief description] - [URL or searchable reference]
        - Example: "Snopes Fact Check: Debunks this claim" - "https://snopes.com/fact-check/..."
        - Example: "Reuters Investigation: Confirms this is false" - "https://reuters.com/..."]
        
        📧 REPORTING INFORMATION:
        [If this is false/misleading content, provide relevant reporting emails:
        - Platform Reporting: [email addresses for social media platforms]
        - Fact-Check Organizations: [emails for fact-checking bodies]
        - Government Agencies: [relevant authorities for this type of content]
        - Example: "Report to Facebook: report@facebook.com"
        - Example: "Report to Snopes: tips@snopes.com"]
        
        Language: {language}
        Be specific, cite sources with links, use emojis for readability.
        """
        
        return self._make_request(prompt, model="gemini-1.5-pro")
    
    def extract_sources_and_reporting(self, ai_response):
        """Extract source links and reporting information from AI response"""
        if not ai_response:
            return {'sources': [], 'reporting_emails': []}
        
        sources = []
        reporting_emails = []
        
        # Extract source links
        source_section = self._extract_section(ai_response, "🔗 SOURCE LINKS & ARTICLES:")
        if source_section:
            lines = source_section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-') and ':' in line:
                    # Parse format: "- Source Name: [description] - [URL]"
                    parts = line[1:].split(':', 1)
                    if len(parts) == 2:
                        source_name = parts[0].strip()
                        description_url = parts[1].strip()
                        
                        # Split description and URL
                        if ' - ' in description_url:
                            desc, url = description_url.rsplit(' - ', 1)
                            sources.append({
                                'name': source_name,
                                'description': desc.strip(),
                                'url': url.strip()
                            })
                        else:
                            sources.append({
                                'name': source_name,
                                'description': description_url,
                                'url': None
                            })
        
        # Extract reporting emails
        reporting_section = self._extract_section(ai_response, "📧 REPORTING INFORMATION:")
        if reporting_section:
            lines = reporting_section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-') and '@' in line:
                    # Parse format: "- Description: email@domain.com"
                    if ':' in line:
                        desc, email = line[1:].split(':', 1)
                        reporting_emails.append({
                            'description': desc.strip(),
                            'email': email.strip()
                        })
        
        return {
            'sources': sources,
            'reporting_emails': reporting_emails
        }
    
    def _extract_section(self, text, section_header):
        """Extract a specific section from AI response"""
        lines = text.split('\n')
        in_section = False
        section_content = []
        
        for line in lines:
            if section_header in line:
                in_section = True
                continue
            elif in_section and line.startswith('🔍') or line.startswith('🧬') or line.startswith('📊') or line.startswith('🎯') or line.startswith('⚠️') or line.startswith('🛡️') or line.startswith('📋'):
                break
            elif in_section:
                section_content.append(line)
        
        return '\n'.join(section_content).strip()
    
    def trace_origin(self, text):
        """Attempt to trace content origins"""
        prompt = f"""
        As a digital investigator, analyze the potential origins of this content:
        
        CONTENT: "{text}"
        
        Analyze:
        🕵️ LINGUISTIC PATTERNS: [Writing style, grammar, vocabulary clues]
        📅 TEMPORAL CLUES: [References to dates, events, timing]
        🌍 GEOGRAPHIC INDICATORS: [Location references, cultural context]
        📱 PLATFORM INDICATORS: [Formatting, hashtags, platform-specific language]
        🔄 PROPAGATION PATTERN: [How this might spread, typical vectors]
        
        Provide your best assessment of where/when this originated.
        """
        
        return self._make_request(prompt, model="gemini-1.5-pro")
    
    def analyze_context(self, text):
        """Analyze missing context"""
        prompt = f"""
        As a context analyst, identify what crucial context is missing from this content:
        
        CONTENT: "{text}"
        
        Identify:
        📚 MISSING BACKGROUND: [What background info is needed?]
        📊 MISSING DATA: [What statistics or data are omitted?]
        ⏰ MISSING TIMELINE: [What timeline context is missing?]
        🔗 MISSING CONNECTIONS: [What related events/facts aren't mentioned?]
        📝 CHERRY-PICKING: [What contradictory evidence might exist?]
        
        Explain why this missing context matters for understanding the truth.
        """
        
        return self._make_request(prompt, model="gemini-1.5-flash")
    
    def _make_request(self, prompt, model="gemini-1.5-flash"):
        """Make request to Gemini API"""
        try:
            url = f"{self.base_url}/{model}:generateContent"
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            }
            
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                # Correct path to access the generated text from Gemini API response
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                st.error(f"Gemini API Error: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Gemini API Exception: {str(e)}")
            return None


class FactCheckService:
    """Google Fact Check Tools API service"""
    
    def __init__(self):
        self.api_key = Config.GOOGLE_API_KEY
        self.base_url = "https://factchecktools.googleapis.com/v1alpha1"
    
    def test_connection(self):
        """Test fact check API"""
        try:
            result = self.search_claims("test")
            return True
        except:
            return False
    
    def search_claims(self, query):
        """Search for fact-checked claims"""
        try:
            url = f"{self.base_url}/claims:search"
            params = {
                'query': query[:100],
                'key': self.api_key,
                'languageCode': 'en'
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_fact_checks(data)
            else:
                return []
                
        except Exception as e:
            st.warning(f"Fact check failed: {str(e)}")
            return []
    
    def _parse_fact_checks(self, data):
        """Parse fact check response"""
        results = []
        
        if 'claims' in data:
            for claim in data['claims'][:5]:
                for review in claim.get('claimReview', []):
                    results.append({
                        'title': review.get('title', 'No title'),
                        'url': review.get('url', ''),
                        'publisher': review.get('publisher', {}).get('name', 'Unknown'),
                        'verdict': review.get('textualRating', 'No verdict'),
                        'date': review.get('reviewDate', 'Unknown date')
                    })
        
        return results
