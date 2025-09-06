import streamlit as st
from datetime import datetime, timedelta
import uuid
import random

class FirebaseService:
    """Firebase database service simulation"""
    
    def __init__(self):
        # Initialize session state for data storage
        if 'firebase_data' not in st.session_state:
            st.session_state.firebase_data = {
                'analyses': [],
                'users': [],
                'statistics': {
                    'analyzed_today': 1247,
                    'flagged_content': 156,
                    'verified_claims': 891,
                    'accuracy_rate': 94.2
                },
                'trending_threats': [],
                'analytics_data': {}
            }
    
    def test_connection(self):
        """Test database connection"""
        return True
    
    def save_analysis(self, content, results):
        """Save analysis results to database"""
        try:
            analysis_id = str(uuid.uuid4())[:8]
            
            analysis_record = {
                'id': analysis_id,
                'content_preview': content[:100] + "..." if len(content) > 100 else content,
                'full_content': content,
                'risk_score': results['risk_score'],
                'credibility_score': results['credibility_score'],
                'threat_level': 'HIGH' if results['risk_score'] > 70 else 'MEDIUM' if results['risk_score'] > 40 else 'LOW',
                'manipulation_tactics': results['manipulation_tactics'],
                'timestamp': datetime.now().isoformat(),
                'user_type': st.session_state.get('user_type', 'public')
            }
            
            st.session_state.firebase_data['analyses'].append(analysis_record)
            
            # Update statistics
            st.session_state.firebase_data['statistics']['analyzed_today'] += 1
            if results['risk_score'] > 70:
                st.session_state.firebase_data['statistics']['flagged_content'] += 1
            
            return analysis_id
            
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return None
    
    def save_image_analysis(self, image_name, results):
        """Save image analysis results"""
        try:
            analysis_id = str(uuid.uuid4())[:8]
            
            analysis_record = {
                'id': analysis_id,
                'content_preview': f"Image: {image_name}",
                'type': 'image',
                'risk_score': results['manipulation_score'],
                'authenticity_score': results['authenticity_score'],
                'threat_level': 'HIGH' if results['manipulation_score'] > 70 else 'MEDIUM' if results['manipulation_score'] > 40 else 'LOW',
                'timestamp': datetime.now().isoformat(),
                'user_type': st.session_state.get('user_type', 'public')
            }
            
            st.session_state.firebase_data['analyses'].append(analysis_record)
            return analysis_id
            
        except Exception as e:
            return None
    
    def get_statistics(self):
        """Get system statistics"""
        return st.session_state.firebase_data['statistics']
    
    def get_recent_analyses(self, limit=10):
        """Get recent analyses"""
        analyses = st.session_state.firebase_data['analyses']
        
        # Sort by timestamp (most recent first)
        sorted_analyses = sorted(analyses, key=lambda x: x['timestamp'], reverse=True)
        
        return sorted_analyses[:limit]
    
    def get_trending_threats(self):
        """Get trending threat topics"""
        if not st.session_state.firebase_data['trending_threats']:
            # Generate sample trending threats
            st.session_state.firebase_data['trending_threats'] = [
                {'topic': 'Health Misinformation', 'count': 234, 'growth': '+12%', 'risk': 'HIGH'},
                {'topic': 'Election Fraud Claims', 'count': 189, 'growth': '+8%', 'risk': 'HIGH'},
                {'topic': 'Climate Change Denial', 'count': 156, 'growth': '+5%', 'risk': 'MEDIUM'},
                {'topic': 'Vaccine Misinformation', 'count': 123, 'growth': '+15%', 'risk': 'HIGH'},
                {'topic': 'Economic Conspiracy', 'count': 98, 'growth': '+3%', 'risk': 'MEDIUM'},
                {'topic': 'Social Media Rumors', 'count': 87, 'growth': '+7%', 'risk': 'LOW'},
                {'topic': 'Celebrity Death Hoax', 'count': 65, 'growth': '+2%', 'risk': 'LOW'}
            ]
        
        return st.session_state.firebase_data['trending_threats']
    
    def get_analytics_data(self):
        """Get analytics data for charts"""
        if not st.session_state.firebase_data['analytics_data']:
            # Generate sample analytics data
            st.session_state.firebase_data['analytics_data'] = {
                'risk_distribution': {
                    'High': 25,
                    'Medium': 35, 
                    'Low': 40
                },
                'daily_counts': [120, 134, 156, 143, 167, 145, 189],
                'threat_sources': {
                    'Social Media': 45,
                    'News Sites': 25,
                    'Messaging Apps': 15,
                    'Forums': 10,
                    'Other': 5
                },
                'hourly_activity': [12, 8, 5, 3, 2, 4, 8, 15, 25, 35, 42, 48, 52, 55, 53, 48, 45, 42, 38, 32, 28, 22, 18, 15],
                'top_tactics': [
                    'Emotional Appeal',
                    'False Urgency', 
                    'Cherry Picking',
                    'Appeal to Fear',
                    'Bandwagon Effect'
                ],
                'user_types': {
                    'Public': 78,
                    'Authority': 22
                }
            }
        
        return st.session_state.firebase_data['analytics_data']
    
    def get_user_activity(self):
        """Get user activity logs"""
        # Generate sample user activity
        activities = []
        for i in range(10):
            activities.append({
                'timestamp': (datetime.now() - timedelta(hours=i)).isoformat(),
                'user_type': random.choice(['public', 'authority']),
                'action': random.choice(['content_analysis', 'image_analysis', 'login', 'report_generated'])
            })
        
        return activities
    
    def populate_demo_data(self):
        """Populate database with demo data"""
        try:
            # Sample analyses
            demo_analyses = [
                {
                    'id': 'DEMO001',
                    'content_preview': 'BREAKING: Scientists discover shocking truth about vaccines...',
                    'risk_score': 85,
                    'credibility_score': 15,
                    'threat_level': 'HIGH',
                    'manipulation_tactics': ['Emotional Appeal', 'False Urgency', 'Conspiracy Theory'],
                    'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
                    'user_type': 'public'
                },
                {
                    'id': 'DEMO002', 
                    'content_preview': 'New study shows correlation between social media and...',
                    'risk_score': 35,
                    'credibility_score': 75,
                    'threat_level': 'LOW',
                    'manipulation_tactics': ['None Detected'],
                    'timestamp': (datetime.now() - timedelta(hours=4)).isoformat(),
                    'user_type': 'authority'
                },
                {
                    'id': 'DEMO003',
                    'content_preview': 'URGENT: Share before it gets deleted! Government hiding...',
                    'risk_score': 92,
                    'credibility_score': 8,
                    'threat_level': 'HIGH',
                    'manipulation_tactics': ['False Urgency', 'Conspiracy Theory', 'Appeal to Fear'],
                    'timestamp': (datetime.now() - timedelta(hours=6)).isoformat(),
                    'user_type': 'public'
                },
                {
                    'id': 'DEMO004',
                    'content_preview': 'According to recent research published in Nature...',
                    'risk_score': 15,
                    'credibility_score': 85,
                    'threat_level': 'LOW',
                    'manipulation_tactics': ['None Detected'],
                    'timestamp': (datetime.now() - timedelta(hours=8)).isoformat(),
                    'user_type': 'public'
                }
            ]
            
            # Add demo data to session state
            st.session_state.firebase_data['analyses'].extend(demo_analyses)
            
            # Update statistics
            st.session_state.firebase_data['statistics']['analyzed_today'] += len(demo_analyses)
            st.session_state.firebase_data['statistics']['flagged_content'] += 2  # High risk items
            
            return True
            
        except Exception as e:
            st.error(f"Failed to load demo data: {str(e)}")
            return False
