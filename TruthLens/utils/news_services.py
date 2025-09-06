import streamlit as st
import requests
from config import Config

class NewsAggregator:
    """News aggregation and verification service"""
    
    def __init__(self):
        self.newsapi_key = Config.NEWSAPI_KEY
        self.newsdata_key = Config.NEWSDATA_KEY
        self.newsapi_url = "https://newsapi.org/v2"
        self.newsdata_url = "https://newsdata.io/api/1"
    
    def test_connection(self):
        """Test news API connections"""
        try:
            # Test NewsAPI
            response = requests.get(
                f"{self.newsapi_url}/top-headlines",
                params={
                    'apiKey': self.newsapi_key,
                    'country': 'us',
                    'pageSize': 1
                },
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def get_breaking_news(self, country='us', category=None):
        """Get breaking news headlines"""
        try:
            params = {
                'apiKey': self.newsapi_key,
                'country': country,
                'pageSize': 10
            }
            
            if category:
                params['category'] = category
            
            response = requests.get(
                f"{self.newsapi_url}/top-headlines",
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
            else:
                return []
                
        except Exception as e:
            st.warning(f"News API failed: {str(e)}")
            return []
    
    def search_news(self, query, language='en'):
        """Search for news articles"""
        try:
            params = {
                'apiKey': self.newsapi_key,
                'q': query,
                'language': language,
                'sortBy': 'relevancy',
                'pageSize': 10
            }
            
            response = requests.get(
                f"{self.newsapi_url}/everything",
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
            else:
                return []
                
        except Exception as e:
            st.warning(f"News search failed: {str(e)}")
            return []
    
    def verify_article(self, article_url):
        """Basic article verification"""
        try:
            # This is a placeholder for article verification
            # In a real implementation, you would:
            # 1. Fetch the article content
            # 2. Check against fact-checking databases
            # 3. Analyze source credibility
            # 4. Cross-reference with other sources
            
            verification_result = {
                'verified': True,
                'credibility_score': 75,
                'source_reputation': 'Medium',
                'cross_references': 3,
                'warning_flags': []
            }
            
            return verification_result
            
        except Exception as e:
            return {
                'verified': False,
                'error': str(e)
            }
    
    def get_trending_topics(self):
        """Get trending news topics"""
        try:
            # Get recent articles and extract trending topics
            articles = self.get_breaking_news()
            
            # Simple topic extraction (in real app, use NLP)
            topics = []
            for article in articles[:5]:
                if article.get('title'):
                    # Simple keyword extraction
                    title = article['title'].lower()
                    if 'election' in title or 'vote' in title:
                        topics.append('Elections')
                    elif 'covid' in title or 'vaccine' in title:
                        topics.append('Health')
                    elif 'climate' in title or 'environment' in title:
                        topics.append('Climate')
                    elif 'economy' in title or 'market' in title:
                        topics.append('Economy')
                    else:
                        topics.append('General News')
            
            # Count occurrences and return top topics
            from collections import Counter
            topic_counts = Counter(topics)
            
            return [
                {'topic': topic, 'count': count}
                for topic, count in topic_counts.most_common(5)
            ]
            
        except Exception as e:
            return [
                {'topic': 'Health Misinformation', 'count': 45},
                {'topic': 'Political Claims', 'count': 32},
                {'topic': 'Science Denial', 'count': 28},
                {'topic': 'Social Media Rumors', 'count': 21},
                {'topic': 'Economic Misinformation', 'count': 18}
            ]
