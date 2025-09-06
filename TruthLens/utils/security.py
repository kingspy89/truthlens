import streamlit as st
import hashlib
import hmac
import re
from datetime import datetime
from config import Config

class SecurityService:
    """Security and authentication service"""
    
    def __init__(self):
        # Sample authority credentials (in real app, use proper auth)
        self.authority_users = {
            'admin': 'admin123',
            'officer1': 'secure456',
            'analyst': 'analyze789',
            'detective': 'investigate321',
            'supervisor': 'supervise654'
        }
        
        # Dangerous keywords for content safety
        self.dangerous_keywords = [
            'violence', 'harm', 'attack', 'bomb', 'weapon', 'kill', 'murder', 
            'terrorist', 'extremist', 'suicide', 'self-harm', 'drug dealing',
            'illegal weapons', 'assassination', 'kidnapping'
        ]
        
        # Manipulation indicators
        self.manipulation_indicators = {
            'sensational': ['shocking', 'unbelievable', 'amazing', 'incredible', 'mind-blowing'],
            'urgency': ['urgent', 'quickly', 'immediately', 'before it\'s too late', 'act now', 'limited time'],
            'conspiracy': ['they don\'t want you to know', 'hidden truth', 'cover-up', 'secret agenda'],
            'emotional': ['outrageous', 'disgusting', 'terrifying', 'heartbreaking', 'infuriating'],
            'authority_undermining': ['mainstream media lies', 'experts are wrong', 'don\'t trust'],
            'false_scarcity': ['going viral', 'before it gets deleted', 'share before removed']
        }
    
    def verify_authority_credentials(self, username, password):
        """Verify authority login credentials"""
        if username in self.authority_users:
            return self.authority_users[username] == password
        return False
    
    def get_authority_info(self, username):
        """Get authority user information"""
        authority_info = {
            'admin': {'role': 'System Administrator', 'department': 'IT Security', 'clearance': 'Level 5'},
            'officer1': {'role': 'Senior Officer', 'department': 'Cybercrime Unit', 'clearance': 'Level 3'},
            'analyst': {'role': 'Intelligence Analyst', 'department': 'Threat Analysis', 'clearance': 'Level 4'},
            'detective': {'role': 'Detective', 'department': 'Investigation Unit', 'clearance': 'Level 3'},
            'supervisor': {'role': 'Supervisor', 'department': 'Operations', 'clearance': 'Level 4'}
        }
        return authority_info.get(username, {'role': 'User', 'department': 'Unknown', 'clearance': 'Level 1'})
    
    def hash_content(self, content):
        """Generate hash for content tracking"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def check_content_safety(self, content):
        """Basic content safety check"""
        content_lower = content.lower()
        flagged_words = []
        
        for word in self.dangerous_keywords:
            if word in content_lower:
                flagged_words.append(word)
        
        risk_level = 'LOW'
        if len(flagged_words) > 3:
            risk_level = 'CRITICAL'
        elif len(flagged_words) > 1:
            risk_level = 'HIGH'
        elif len(flagged_words) > 0:
            risk_level = 'MEDIUM'
        
        return {
            'is_safe': len(flagged_words) == 0,
            'flagged_words': flagged_words,
            'risk_level': risk_level,
            'safety_score': max(0, 100 - (len(flagged_words) * 25))
        }
    
    def detect_manipulation_patterns(self, content):
        """Detect manipulation patterns in content"""
        content_lower = content.lower()
        detected_patterns = {}
        total_score = 0
        
        for category, keywords in self.manipulation_indicators.items():
            matches = []
            for keyword in keywords:
                if keyword in content_lower:
                    matches.append(keyword)
            
            if matches:
                detected_patterns[category] = {
                    'matches': matches,
                    'count': len(matches),
                    'severity': self._calculate_pattern_severity(category, len(matches))
                }
                total_score += len(matches) * self._get_category_weight(category)
        
        return {
            'patterns': detected_patterns,
            'total_indicators': sum(p['count'] for p in detected_patterns.values()),
            'manipulation_score': min(100, total_score * 5),  # Scale to 0-100
            'risk_assessment': self._assess_manipulation_risk(total_score)
        }
    
    def _calculate_pattern_severity(self, category, count):
        """Calculate severity of detected pattern"""
        if count >= 3:
            return 'HIGH'
        elif count >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _get_category_weight(self, category):
        """Get weight for different manipulation categories"""
        weights = {
            'conspiracy': 4,
            'urgency': 3,
            'sensational': 2,
            'emotional': 2,
            'authority_undermining': 3,
            'false_scarcity': 2
        }
        return weights.get(category, 1)
    
    def _assess_manipulation_risk(self, score):
        """Assess overall manipulation risk"""
        if score >= 15:
            return 'CRITICAL'
        elif score >= 10:
            return 'HIGH'
        elif score >= 5:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def analyze_text_structure(self, content):
        """Analyze text structure for suspicious patterns"""
        analysis = {
            'excessive_caps': self._check_excessive_caps(content),
            'excessive_punctuation': self._check_excessive_punctuation(content),
            'suspicious_urls': self._check_suspicious_urls(content),
            'emotional_language': self._check_emotional_language(content),
            'readability_score': self._calculate_readability(content)
        }
        
        # Calculate overall structure score
        structure_score = 0
        if analysis['excessive_caps']:
            structure_score += 20
        if analysis['excessive_punctuation']:
            structure_score += 15
        if analysis['suspicious_urls']:
            structure_score += 25
        if analysis['emotional_language'] > 5:
            structure_score += 20
        
        analysis['structure_risk_score'] = min(100, structure_score)
        return analysis
    
    def _check_excessive_caps(self, content):
        """Check for excessive capital letters"""
        if len(content) < 10:
            return False
        caps_count = sum(1 for c in content if c.isupper())
        caps_ratio = caps_count / len(content)
        return caps_ratio > 0.3  # More than 30% caps
    
    def _check_excessive_punctuation(self, content):
        """Check for excessive punctuation"""
        punctuation_count = len(re.findall(r'[!?]{2,}', content))
        return punctuation_count > 3
    
    def _check_suspicious_urls(self, content):
        """Check for suspicious URLs"""
        # Simple URL detection
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        
        suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'short.link', 'click.here',
            'suspicious-news.com', 'fake-facts.org'
        ]
        
        for url in urls:
            for domain in suspicious_domains:
                if domain in url:
                    return True
        return False
    
    def _check_emotional_language(self, content):
        """Count emotional language usage"""
        emotional_words = [
            'shocking', 'outrageous', 'disgusting', 'terrifying', 'amazing',
            'incredible', 'unbelievable', 'devastating', 'heartbreaking', 'infuriating'
        ]
        
        content_lower = content.lower()
        count = 0
        for word in emotional_words:
            count += content_lower.count(word)
        
        return count
    
    def _calculate_readability(self, content):
        """Simple readability score (0-100, higher is more readable)"""
        if len(content) < 10:
            return 50
        
        sentences = len(re.findall(r'[.!?]+', content))
        words = len(content.split())
        
        if sentences == 0:
            return 30  # No proper sentence structure
        
        avg_words_per_sentence = words / sentences
        
        # Simple readability metric
        if avg_words_per_sentence > 25:
            return 40  # Too complex
        elif avg_words_per_sentence < 5:
            return 45  # Too simple, might be manipulative
        else:
            return 80  # Good readability
    
    def generate_report_id(self):
        """Generate unique report ID"""
        import time
        import random
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        return f"TL-{timestamp}-{random_num}"
    
    def log_security_event(self, event_type, details):
        """Log security events"""
        if 'security_logs' not in st.session_state:
            st.session_state.security_logs = []
        
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details,
            'user_type': st.session_state.get('user_type', 'unknown'),
            'session_id': st.session_state.get('session_id', 'unknown')
        }
        
        st.session_state.security_logs.append(event)
    
    def get_security_logs(self, limit=50):
        """Get recent security logs"""
        if 'security_logs' not in st.session_state:
            return []
        return list(reversed(st.session_state.security_logs[-limit:]))
    
    def validate_input(self, text, max_length=10000):
        """Validate user input"""
        if not text or not text.strip():
            return False, "Input cannot be empty"
        
        if len(text) > max_length:
            return False, f"Input too long. Maximum {max_length} characters allowed"
        
        # Check for potentially malicious patterns
        malicious_patterns = [
            r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>',  # Script tags
            r'javascript:',  # JavaScript URLs
            r'on\w+\s*=',  # Event handlers
        ]
        
        for pattern in malicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False, "Input contains potentially malicious content"
        
        return True, "Valid input"
    
    def sanitize_input(self, text):
        """Sanitize user input"""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def test_connection(self):
        """Test security service"""
        return True
    
    def get_threat_level_color(self, threat_level):
        """Get color code for threat levels"""
        colors = {
            'LOW': '#28a745',      # Green
            'MEDIUM': '#ffc107',   # Yellow
            'HIGH': '#fd7e14',     # Orange
            'CRITICAL': '#dc3545'  # Red
        }
        return colors.get(threat_level, '#6c757d')  # Default gray
