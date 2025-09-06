import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.database import FirebaseService

def analytics_interface():
    """Advanced analytics and data visualization interface"""
    
    st.title("📊 TruthLens Analytics Center")
    st.markdown("**Advanced data analytics and trend analysis for misinformation patterns**")
    
    firebase_service = FirebaseService()
    
    # Analytics tabs
    tabs = st.tabs([
        "📈 Trend Analysis",
        "🎯 Content Analytics", 
        "🌐 Source Intelligence",
        "👥 User Behavior",
        "📊 Performance Metrics"
    ])
    
    with tabs:
        trend_analysis(firebase_service)
    
    with tabs:
        content_analytics(firebase_service)
    
    with tabs:
        source_intelligence(firebase_service)
    
    with tabs:
        user_behavior_analysis(firebase_service)
    
    with tabs:
        performance_metrics(firebase_service)

def trend_analysis(firebase_service):
    """Trend analysis and forecasting"""
    st.subheader("📈 Misinformation Trend Analysis")
    
    # Time range selector
    col1, col2 = st.columns([1, 3])
    
    with col1:
        time_range = st.selectbox("Time Range", ["Last 7 Days", "Last 30 Days", "Last 3 Months", "Last Year"])
        analysis_type = st.selectbox("Analysis Type", ["Volume Trends", "Risk Patterns", "Topic Evolution"])
    
    # Get analytics data
    analytics_data = firebase_service.get_analytics_data()
    
    # Trend visualization
    if analysis_type == "Volume Trends":
        st.write("**📊 Content Volume Trends**")
        
        # Create sample trend data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        volume_data = pd.DataFrame({
            'Date': dates,
            'Total_Content': [100 + i*2 + (i%7)*10 for i in range(len(dates))],
            'High_Risk': [20 + i*0.5 + (i%5)*3 for i in range(len(dates))],
            'Verified': [60 + i*1.2 + (i%6)*5 for i in range(len(dates))]
        })
        
        fig = px.line(volume_data, x='Date', y=['Total_Content', 'High_Risk', 'Verified'],
                     title="Content Analysis Volume Over Time")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
    elif analysis_type == "Risk Patterns":
        st.write("**⚠️ Risk Level Patterns**")
        
        # Risk pattern heatmap
        risk_data = [[20, 35, 45, 25, 15, 30, 40],
                    [25, 40, 55, 30, 20, 35, 45],
                    [30, 45, 60, 35, 25, 40, 50],
                    [35, 50, 65, 40, 30, 45, 55]]
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=risk_data,
            x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            y=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            colorscale='Reds'
        ))
        fig_heatmap.update_layout(title="Risk Levels by Day and Week", height=400)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Trending topics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🔥 Trending Misinformation Topics**")
        trending = firebase_service.get_trending_threats()
        
        for i, topic in enumerate(trending, 1):
            st.write(f"{i}. **{topic['topic']}**")
            st.write(f"   📊 {topic['count']} mentions ({topic['growth']})")
            
            # Growth indicator
            growth_val = float(topic['growth'].replace('%', '').replace('+', ''))
            st.progress(min(growth_val / 100, 1.0))
    
    with col2:
        st.write("**📊 Topic Distribution**")
        
        topic_data = {topic['topic']: topic['count'] for topic in trending}
        
        fig_pie = px.pie(
            values=list(topic_data.values()),
            names=list(topic_data.keys()),
            title="Distribution of Misinformation Topics"
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

def content_analytics(firebase_service):
    """Content-focused analytics"""
    st.subheader("🎯 Content Analysis Deep Dive")
    
    # Content metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Text Analyses", "12,450", "+234")
    with col2:
        st.metric("🖼️ Image Analyses", "3,890", "+89")
    with col3:
        st.metric("🔗 URL Investigations", "2,340", "+45")
    with col4:
        st.metric("📰 News Verifications", "5,670", "+123")
    
    # Content type analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Content Type Distribution**")
        
        content_types = {
            'Social Media Posts': 45,
            'News Articles': 25,
            'Messaging Apps': 15,
            'Forums/Blogs': 10,
            'Other': 5
        }
        
        fig_bar = px.bar(
            x=list(content_types.keys()),
            y=list(content_types.values()),
            title="Content Sources",
            color=list(content_types.values()),
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.write("**⚡ Manipulation Tactic Frequency**")
        
        tactics = ['Emotional Appeal', 'False Urgency', 'Cherry Picking', 'Ad Hominem', 'Strawman', 'Bandwagon']
        frequencies = [320, 280, 240, 180, 160, 140]
        
        fig_horizontal = px.bar(
            x=frequencies,
            y=tactics,
            orientation='h',
            title="Most Common Manipulation Tactics",
            color=frequencies,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_horizontal, use_container_width=True)
    
    # Risk score distribution
    st.write("**📊 Risk Score Distribution Analysis**")
    
    # Generate sample risk score data
    import numpy as np
    risk_scores = np.random.beta(2, 5, 1000) * 100  # Beta distribution for realistic risk scores
    
    fig_hist = px.histogram(
        x=risk_scores,
        nbins=20,
        title="Distribution of Risk Scores",
        labels={'x': 'Risk Score', 'y': 'Frequency'}
    )
    fig_hist.add_vline(x=np.mean(risk_scores), line_dash="dash", line_color="red", 
                      annotation_text=f"Mean: {np.mean(risk_scores):.1f}")
    st.plotly_chart(fig_hist, use_container_width=True)

def source_intelligence(firebase_service):
    """Source and platform intelligence"""
    st.subheader("🌐 Source Intelligence & Platform Analysis")
    
    # Platform comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📱 Platform Risk Assessment**")
        
        platform_data = {
            'Platform': ['Twitter/X', 'Facebook', 'Instagram', 'TikTok', 'WhatsApp', 'Telegram'],
            'Risk_Score': [75, 68, 45, 82, 58, 71],
            'Volume': [1200, 980, 560, 890, 340, 420]
        }
        
        df_platforms = pd.DataFrame(platform_data)
        
        fig_scatter = px.scatter(
            df_platforms, 
            x='Volume', 
            y='Risk_Score',
            size='Volume',
            color='Risk_Score',
            hover_name='Platform',
            title="Platform Risk vs Volume Analysis",
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.write("**🏢 Domain Credibility Scores**")
        
        domain_data = {
            'Domain': ['legitimate-news.com', 'questionable-source.net', 'fake-news-site.org', 'reliable-media.com', 'conspiracy-hub.info'],
            'Credibility': [92, 35, 15, 88, 22],
            'Frequency': [150, 89, 234, 120, 178]
        }
        
        df_domains = pd.DataFrame(domain_data)
        
        fig_bubble = px.scatter(
            df_domains,
            x='Frequency',
            y='Credibility', 
            size='Frequency',
            color='Credibility',
            hover_name='Domain',
            title="Domain Credibility Analysis",
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_bubble, use_container_width=True)
    
    # Geographic analysis
    st.write("**🌍 Geographic Distribution of Threats**")
    
    geo_data = {
        'Country': ['United States', 'India', 'Brazil', 'United Kingdom', 'Germany', 'France', 'Canada', 'Australia'],
        'Threat_Count': [450, 320, 280, 180, 160, 140, 120, 90],
        'Risk_Level': ['High', 'High', 'Medium', 'Medium', 'Low', 'Low', 'Low', 'Low']
    }
    
    df_geo = pd.DataFrame(geo_data)
    
    fig_map = px.bar(
        df_geo,
        x='Country',
        y='Threat_Count',
        color='Risk_Level',
        title="Misinformation Threats by Country",
        color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'}
    )
    fig_map.update_xaxes(tickangle=45)
    st.plotly_chart(fig_map, use_container_width=True)

def user_behavior_analysis(firebase_service):
    """User behavior and engagement analysis"""
    st.subheader("👥 User Behavior & Engagement Analysis")
    
    # User engagement metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👤 Active Users", "8,450", "+320")
    with col2:
        st.metric("🔄 Avg. Session Time", "12m 34s", "+1m 23s")
    with col3:
        st.metric("📊 Analyses per User", "3.2", "+0.4")
    
    # User activity patterns
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**⏰ User Activity by Hour**")
        
        hours = list(range(24))
        activity = [45, 32, 28, 25, 30, 45, 67, 89, 120, 145, 160, 170, 
                   165, 155, 140, 125, 135, 150, 145, 120, 98, 75, 60, 52]
        
        fig_activity = px.line(
            x=hours,
            y=activity,
            title="Hourly User Activity Pattern",
            labels={'x': 'Hour of Day', 'y': 'Active Users'}
        )
        fig_activity.update_traces(line_color='#667eea', line_width=3)
        st.plotly_chart(fig_activity, use_container_width=True)
    
    with col2:
        st.write("**👥 User Type Distribution**")
        
        user_types = {'Public Users': 78, 'Authority Users': 22}
        
        fig_donut = px.pie(
            values=list(user_types.values()),
            names=list(user_types.keys()),
            hole=0.4,
            title="User Base Composition"
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    # Feature usage analysis
    st.write("**🔧 Feature Usage Statistics**")
    
    feature_data = {
        'Feature': ['Text Analysis', 'Image Analysis', 'URL Investigation', 'News Verification', 'Social Media Scan'],
        'Usage_Count': [5420, 1890, 1340, 2670, 890],
        'Success_Rate': [94.2, 87.5, 91.3, 89.7, 85.2]
    }
    
    df_features = pd.DataFrame(feature_data)
    
    fig_features = px.bar(
        df_features,
        x='Feature',
        y='Usage_Count',
        color='Success_Rate',
        title="Feature Usage and Success Rates",
        color_continuous_scale='Greens'
    )
    fig_features.update_xaxes(tickangle=45)
    st.plotly_chart(fig_features, use_container_width=True)

def performance_metrics(firebase_service):
    """System performance and efficiency metrics"""
    st.subheader("📊 System Performance Metrics")
    
    # System health overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⚡ Avg Response Time", "1.24s", "-0.05s")
    with col2:
        st.metric("🎯 Accuracy Rate", "94.2%", "+0.3%")
    with col3:
        st.metric("🔄 Uptime", "99.8%", "+0.1%")
    with col4:
        st.metric("💾 Data Processed", "2.4TB", "+120GB")
    
    # Performance trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**⚡ Response Time Trends**")
        
        days = list(range(1, 31))
        response_times = [1.2 + 0.1 * (i % 7) + 0.05 * np.random.randn() for i in days]
        
        fig_response = px.line(
            x=days,
            y=response_times,
            title="Average Response Time (Last 30 Days)",
            labels={'x': 'Day', 'y': 'Response Time (seconds)'}
        )
        fig_response.add_hline(y=1.5, line_dash="dash", line_color="red", 
                              annotation_text="Target: 1.5s")
        st.plotly_chart(fig_response, use_container_width=True)
    
    with col2:
        st.write("**🎯 Accuracy Rate by Analysis Type**")
        
        accuracy_data = {
            'Analysis Type': ['Text Forensics', 'Image Analysis', 'URL Investigation', 'News Verification'],
            'Accuracy': [94.2, 87.5, 91.3, 89.7]
        }
        
        fig_accuracy = px.bar(
            accuracy_data,
            x='Analysis Type',
            y='Accuracy',
            title="Accuracy Rates by Feature",
            color='Accuracy',
            color_continuous_scale='Greens'
        )
        fig_accuracy.update_xaxes(tickangle=45)
        st.plotly_chart(fig_accuracy, use_container_width=True)
    
    # API performance
    st.write("**🔌 API Performance Statistics**")
    
    api_data = {
        'API': ['Gemini AI', 'Fact Check', 'News API', 'Image Analysis', 'Security Scanner'],
        'Avg_Response_Time': [0.85, 1.2, 0.95, 2.1, 0.65],
        'Success_Rate': [98.5, 94.2, 96.8, 91.3, 99.1],
        'Daily_Calls': [1250, 890, 670, 340, 1100]
    }
    
    df_api = pd.DataFrame(api_data)
    
    # Create subplot with multiple metrics
    fig_api = px.scatter(
        df_api,
        x='Avg_Response_Time',
        y='Success_Rate',
        size='Daily_Calls',
        color='API',
        title="API Performance Overview",
        labels={'Avg_Response_Time': 'Average Response Time (s)', 'Success_Rate': 'Success Rate (%)'}
    )
    st.plotly_chart(fig_api, use_container_width=True)
    
    # Resource utilization
    st.write("**💻 Resource Utilization**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**CPU Usage**")
        cpu_usage = 67
        fig_cpu = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = cpu_usage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CPU %"},
            gauge = {'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "red"}],
                    'threshold': {'line': {'color': "red", 'width': 4},
                                'thickness': 0.75, 'value': 90}}))
        fig_cpu.update_layout(height=250)
        st.plotly_chart(fig_cpu, use_container_width=True)
    
    with col2:
        st.write("**Memory Usage**")
        memory_usage = 45
        fig_memory = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = memory_usage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Memory %"},
            gauge = {'axis': {'range': [None, 100]},
                    'bar': {'color': "green"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "red"}],
                    'threshold': {'line': {'color': "red", 'width': 4},
                                'thickness': 0.75, 'value': 90}}))
        fig_memory.update_layout(height=250)
        st.plotly_chart(fig_memory, use_container_width=True)
    
    with col3:
        st.write("**Storage Usage**")
        storage_usage = 23
        fig_storage = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = storage_usage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Storage %"},
            gauge = {'axis': {'range': [None, 100]},
                    'bar': {'color': "purple"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "red"}],
                    'threshold': {'line': {'color': "red", 'width': 4},
                                'thickness': 0.75, 'value': 90}}))
        fig_storage.update_layout(height=250)
        st.plotly_chart(fig_storage, use_container_width=True)
