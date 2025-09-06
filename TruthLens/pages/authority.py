import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.database import FirebaseService
from utils.security import SecurityService

def authority_interface():
    """Professional authority dashboard with real-time monitoring"""
    
    if st.session_state.get('user_type') != 'authority':
        st.error("🚫 Access Denied - Authority credentials required")
        return
    
    # Get services
    firebase_service = FirebaseService()
    security_service = SecurityService()
    
    # Header with user info
    username = st.session_state.get('authority_username', 'Unknown')
    user_info = security_service.get_authority_info(username)
    
    st.title("👮‍♂️ TruthLens Authority Control Center")
    st.markdown(f"""
    **Welcome, {user_info['role']} {username}** | 
    **Department:** {user_info['department']} | 
    **Clearance:** {user_info['clearance']}
    """)
    
    # Main dashboard tabs
    tabs = st.tabs([
        "📊 Live Dashboard",
        "🚨 Alert System", 
        "📈 Analytics Center",
        "🔍 Investigation Tools",
        "📋 Reports & Logs"
    ])
    
    with tabs:
        live_dashboard(firebase_service, security_service)
    
    with tabs:
        alert_system(firebase_service, security_service)
    
    with tabs:
        analytics_center(firebase_service)
    
    with tabs:
        investigation_tools(firebase_service, security_service)
    
    with tabs:
        reports_and_logs(firebase_service, security_service)

def live_dashboard(firebase_service, security_service):
    """Real-time threat monitoring dashboard"""
    st.subheader("🔴 Live Threat Monitoring")
    
    # Auto-refresh option
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Real-time misinformation detection and threat assessment**")
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Real-time metrics
    stats = firebase_service.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🚨 High Risk Detected", 
            stats['flagged_content'], 
            delta="+12",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "⚡ Processing Queue", 
            "23", 
            delta="-8",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "🌐 Active Sources", 
            "156", 
            delta="+12"
        )
    
    with col4:
        st.metric(
            "👥 Active Users", 
            stats['analyzed_today'], 
            delta="+89"
        )
    
    # Threat Level Overview
    st.subheader("🎯 Current Threat Level Assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Threat level gauge
        current_threat_level = "MEDIUM"  # This would be calculated from real data
        threat_colors = {"LOW": "green", "MEDIUM": "orange", "HIGH": "red", "CRITICAL": "darkred"}
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 65,  # Current threat level (0-100)
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Overall Threat Level"},
            delta = {'reference': 60},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "yellow"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.markdown("**🔥 Trending Threats:**")
        trending = firebase_service.get_trending_threats()
        
        for threat in trending[:5]:
            risk_icon = "🔴" if threat['risk'] == 'HIGH' else "🟡" if threat['risk'] == 'MEDIUM' else "🟢"
            st.write(f"{risk_icon} **{threat['topic']}**")
            st.write(f"   📊 {threat['count']} mentions ({threat['growth']})")
            st.progress(min(threat['count'] / 200, 1.0))
    
    # Live activity feed
    st.subheader("📺 Live Content Feed")
    
    # Get recent analyses
    recent_analyses = firebase_service.get_recent_analyses(limit=10)
    
    if recent_analyses:
        for analysis in recent_analyses[:8]:  # Show top 8
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 1])
                
                with col1:
                    st.write(f"📝 {analysis['content_preview']}")
                
                with col2:
                    risk_color = "🔴" if analysis['threat_level'] == 'HIGH' else "🟡" if analysis['threat_level'] == 'MEDIUM' else "🟢"
                    st.write(f"{risk_color} {analysis['threat_level']}")
                
                with col3:
                    st.write(f"Risk: {analysis['risk_score']}")
                
                with col4:
                    time_str = datetime.fromisoformat(analysis['timestamp']).strftime('%H:%M')
                    st.write(f"⏰ {time_str}")
                
                with col5:
                    if st.button(f"🔍", key=f"inv_{analysis['id']}", help="Investigate"):
                        st.session_state.investigation_target = analysis
                        st.info(f"📋 Investigation opened for analysis #{analysis['id']}")
                
                st.markdown("---")
    else:
        st.info("🔍 No recent analyses to display. System is monitoring...")

def alert_system(firebase_service, security_service):
    """Alert management system"""
    st.subheader("🚨 Alert Management Center")
    
    # Alert configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⚙️ Alert Configuration**")
        
        with st.form("alert_settings"):
            high_risk_threshold = st.slider("High Risk Threshold", 50, 100, 70)
            auto_flag = st.checkbox("Auto-flag content above threshold", True)
            email_alerts = st.checkbox("Send email alerts", True)
            sms_alerts = st.checkbox("Send SMS alerts", False)
            alert_frequency = st.selectbox("Alert Frequency", ["Immediate", "Every 5 minutes", "Every 15 minutes", "Hourly"])
            
            if st.form_submit_button("💾 Save Alert Settings", type="primary"):
                st.success("✅ Alert settings saved successfully!")
                security_service.log_security_event("alert_settings_updated", {
                    "threshold": high_risk_threshold,
                    "auto_flag": auto_flag,
                    "frequency": alert_frequency
                })
    
    with col2:
        st.markdown("**📊 Alert Statistics (Last 24h)**")
        
        alert_stats = {
            "🔴 Critical Alerts": 23,
            "🟡 Warning Alerts": 67,
            "🟢 Info Alerts": 134,
            "📧 Emails Sent": 45,
            "📱 SMS Sent": 12,
            "⚡ Auto-Actions": 8
        }
        
        for alert_type, count in alert_stats.items():
            st.metric(alert_type, count)
    
    # Recent alerts
    st.subheader("📋 Recent Alerts & Notifications")
    
    sample_alerts = [
        {"time": "14:23:45", "type": "🔴 CRITICAL", "message": "Mass misinformation campaign detected", "source": "Social Media Monitor", "action": "Auto-flagged"},
        {"time": "14:15:22", "type": "🟡 WARNING", "message": "Suspicious claim verification failed", "source": "News Analyzer", "action": "Under Review"},
        {"time": "14:08:11", "type": "🔴 CRITICAL", "message": "High-risk content from verified account", "source": "Account Monitor", "action": "Escalated"},
        {"time": "13:55:33", "type": "🟡 WARNING", "message": "Image manipulation detected", "source": "Image Analyzer", "action": "Flagged"},
        {"time": "13:45:12", "type": "🟢 INFO", "message": "Routine fact-check completed", "source": "Fact Checker", "action": "Verified"},
    ]
    
    for alert in sample_alerts:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 3, 2, 1])
            
            with col1:
                st.write(f"⏰ {alert['time']}")
            
            with col2:
                st.write(alert['type'])
            
            with col3:
                st.write(alert['message'])
            
            with col4:
                st.write(f"📡 {alert['source']}")
            
            with col5:
                st.write(f"⚡ {alert['action']}")
        
        st.markdown("---")
    
    # Alert actions
    st.subheader("⚡ Quick Alert Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚨 Trigger Test Alert", use_container_width=True):
            st.success("🚨 Test alert triggered successfully!")
    
    with col2:
        if st.button("📢 Broadcast Warning", use_container_width=True):
            st.info("📢 Public warning broadcast initiated!")
    
    with col3:
        if st.button("🔒 Emergency Lock", use_container_width=True):
            st.warning("🔒 Emergency protocols activated!")
    
    with col4:
        if st.button("📊 Generate Alert Report", use_container_width=True):
            st.success("📊 Alert report generated!")

def analytics_center(firebase_service):
    """Comprehensive analytics dashboard"""
    st.subheader("📈 Analytics & Intelligence Center")
    
    # Get analytics data
    analytics_data = firebase_service.get_analytics_data()
    
    # Time period selector
    col1, col2 = st.columns([1, 3])
    
    with col1:
        time_period = st.selectbox(
            "📅 Time Period", 
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom Range"]
        )
    
    with col2:
        st.markdown("**📊 Advanced analytics for threat intelligence and pattern recognition**")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk distribution pie chart
        fig_pie = px.pie(
            values=list(analytics_data['risk_distribution'].values()),
            names=list(analytics_data['risk_distribution'].keys()),
            title="🎯 Threat Level Distribution",
            color_discrete_map={'High': '#ff4444', 'Medium': '#ff8800', 'Low': '#44ff44'}
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Daily activity chart
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=list(range(7)),
            y=analytics_data['daily_counts'],
            mode='lines+markers',
            name='Daily Analyses',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        fig_line.update_layout(
            title="📊 7-Day Activity Trend", 
            xaxis_title="Days Ago", 
            yaxis_title="Number of Analyses",
            height=400
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Threat sources
        fig_bar = px.bar(
            x=list(analytics_data['threat_sources'].keys()),
            y=list(analytics_data['threat_sources'].values()),
            title="🌐 Threat Sources Distribution",
            color=list(analytics_data['threat_sources'].values()),
            color_continuous_scale='Reds'
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Hourly activity heatmap
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=[analytics_data['hourly_activity']],
            x=list(range(24)),
            y=['Activity'],
            colorscale='Reds',
            showscale=True
        ))
        fig_heatmap.update_layout(
            title="🕒 24-Hour Activity Heatmap",
            xaxis_title="Hour of Day",
            height=200
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Analysis breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🧠 Top Manipulation Tactics Detected**")
        for i, tactic in enumerate(analytics_data['top_tactics'], 1):
            progress_value = 0.9 - (i * 0.15)
            st.write(f"{i}. {tactic}")
            st.progress(progress_value)
    
    with col2:
        st.markdown("**👥 User Type Distribution**")
        user_types = analytics_data['user_types']
        fig_donut = px.pie(
            values=list(user_types.values()),
            names=list(user_types.keys()),
            hole=0.4,
            color_discrete_map={'Public': '#36a2eb', 'Authority': '#ff6384'}
        )
        fig_donut.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig_donut, use_container_width=True)

def investigation_tools(firebase_service, security_service):
    """Investigation and case management tools"""
    st.subheader("🔍 Investigation & Case Management")
    
    # Investigation tools
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**🔎 Content Investigation**")
        
        search_query = st.text_input(
            "🔍 Search analyses by content, ID, or keywords:",
            placeholder="Enter search terms..."
        )
        
        col1a, col1b = st.columns(2)
        with col1a:
            search_type = st.selectbox("Search Type", ["Content", "Analysis ID", "User Type", "Threat Level"])
        with col1b:
            date_filter = st.selectbox("Date Range", ["All Time", "Today", "Last Week", "Last Month"])
        
        if st.button("🔍 Search Database", type="primary") and search_query:
            with st.spinner("🔍 Searching database..."):
                # Get recent analyses for demo
                analyses = firebase_service.get_recent_analyses(limit=20)
                
                # Filter based on search query (simplified)
                filtered_results = []
                for analysis in analyses:
                    if search_query.lower() in analysis['content_preview'].lower():
                        filtered_results.append(analysis)
                
                st.success(f"🔍 Found {len(filtered_results)} results for '{search_query}'")
                
                for result in filtered_results[:5]:  # Show top 5
                    with st.expander(f"📄 Analysis ID: {result['id']} (Risk: {result['risk_score']})"):
                        st.write(f"**Content:** {result['content_preview']}")
                        st.write(f"**Risk Score:** {result['risk_score']}/100")
                        st.write(f"**Threat Level:** {result['threat_level']}")
                        st.write(f"**Timestamp:** {result['timestamp']}")
                        st.write(f"**Manipulation Tactics:** {', '.join(result['manipulation_tactics'])}")
                        
                        if st.button(f"📋 Open Full Investigation", key=f"full_inv_{result['id']}"):
                            st.info(f"📋 Full investigation opened for Analysis {result['id']}")
    
    with col2:
        st.markdown("**📊 Investigation Templates**")
        
        investigation_types = [
            "🔍 Standard Content Review",
            "🚨 High-Priority Threat Assessment", 
            "📊 Pattern Analysis Investigation",
            "🌐 Cross-Platform Verification",
            "📈 Trend Impact Analysis",
            "⚖️ Legal Evidence Collection"
        ]
        
        selected_template = st.selectbox("Select Investigation Type:", investigation_types)
        
        if st.button("📄 Create New Investigation", type="primary"):
            investigation_id = security_service.generate_report_id()
            st.success(f"📄 Investigation {investigation_id} created!")
            st.info(f"Template: {selected_template}")
    
    # Active investigations
    st.subheader("📁 Active Investigations")
    
    investigation_data = {
        'Investigation ID': ['INV-2024-001', 'INV-2024-002', 'INV-2024-003', 'INV-2024-004', 'INV-2024-005'],
        'Type': ['Misinformation Campaign', 'Fake News Network', 'Manipulated Media', 'Bot Activity', 'Coordinated Attack'],
        'Status': ['In Progress', 'Under Review', 'Evidence Collection', 'Escalated', 'Completed'],
        'Priority': ['High', 'Critical', 'Medium', 'High', 'Low'],
        'Assigned Officer': ['Officer Smith', 'Detective Johnson', 'Analyst Brown', 'Supervisor Davis', 'Officer Wilson'],
        'Created': ['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12', '2024-01-10']
    }
    
    df = pd.DataFrame(investigation_data)
    
    # Make it interactive
    selected_investigation = st.selectbox("Select Investigation to View:", df['Investigation ID'])
    
    if selected_investigation:
        selected_row = df[df['Investigation ID'] == selected_investigation].iloc
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Priority", selected_row['Priority'])
        with col2:
            st.metric("Status", selected_row['Status'])
        with col3:
            st.metric("Days Active", "5")
        
        st.write(f"**Type:** {selected_row['Type']}")
        st.write(f"**Assigned Officer:** {selected_row['Assigned Officer']}")
        st.write(f"**Created:** {selected_row['Created']}")
    
    st.dataframe(df, use_container_width=True)

def reports_and_logs(firebase_service, security_service):
    """Reports generation and system logs"""
    st.subheader("📋 Reports & System Logs")
    
    # Report generation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Report Generation**")
        
        with st.form("report_generation"):
            report_type = st.selectbox("Report Type", [
                "Daily Threat Summary",
                "Weekly Analytics Report", 
                "Investigation Case File",
                "Public Safety Alert",
                "Trend Analysis Report",
                "System Performance Report",
                "User Activity Report"
            ])
            
            report_format = st.selectbox("Format", ["PDF", "Excel", "CSV", "Word Document"])
            
            include_charts = st.checkbox("Include Charts & Graphs", value=True)
            include_raw_data = st.checkbox("Include Raw Data", value=False)
            
            if st.form_submit_button("📄 Generate Report", type="primary"):
                with st.spinner("📄 Generating report..."):
                    report_id = security_service.generate_report_id()
                    st.success(f"✅ Report generated successfully!")
                    st.info(f"Report ID: {report_id}")
                    
                    # Simulate download
                    sample_report = f"""
TRUTHLENS AUTHORITY REPORT
Report Type: {report_type}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Report ID: {report_id}

EXECUTIVE SUMMARY:
- Total Analyses: {firebase_service.get_statistics()['analyzed_today']}
- High-Risk Content: {firebase_service.get_statistics()['flagged_content']}
- System Accuracy: {firebase_service.get_statistics()['accuracy_rate']}%

DETAILED ANALYSIS:
[Report content would be generated here based on selected parameters]

---
Generated by TruthLens Authority System v2.0.0
                    """
                    
                    st.download_button(
                        label="⬇️ Download Report",
                        data=sample_report,
                        file_name=f"truthlens_{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
    
    with col2:
        st.markdown("**⚙️ Report Schedule**")
        
        with st.form("report_schedule"):
            auto_reports = st.checkbox("Enable Automatic Reports", value=True)
            
            if auto_reports:
                schedule_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
                schedule_time = st.time_input("Delivery Time", value=datetime.strptime("09:00", "%H:%M").time())
                recipients = st.text_area("Email Recipients", placeholder="officer1@agency.gov\nanalyst@agency.gov")
            
            if st.form_submit_button("💾 Save Schedule"):
                st.success("✅ Report schedule saved!")
    
    # System logs
    st.subheader("📋 System Activity Logs")
    
    log_tabs = st.tabs(["🔒 Security Logs", "👤 User Activity", "⚡ System Events", "🚨 Alert History"])
    
    with log_tabs:
        security_logs = security_service.get_security_logs()
        
        if security_logs:
            st.write("**🔒 Recent Security Events:**")
            for log in security_logs[:10]:
                col1, col2, col3, col4 = st.columns([2, 1, 2, 3])
                
                with col1:
                    timestamp = datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    st.write(timestamp)
                
                with col2:
                    st.write(log['user_type'])
                
                with col3:
                    st.write(log['event_type'])
                
                with col4:
                    st.write(str(log['details'])[:50] + "..." if len(str(log['details'])) > 50 else str(log['details']))
        else:
            st.info("No security logs available")
    
    with log_tabs:
        user_activity = firebase_service.get_user_activity()
        
        if user_activity:
            st.write("**👤 Recent User Activity:**")
            for activity in user_activity[:10]:
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    timestamp = datetime.fromisoformat(activity['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    st.write(timestamp)
                
                with col2:
                    st.write(activity['user_type'])
                
                with col3:
                    st.write(activity['action'])
        else:
            st.info("No user activity logs available")
    
    with log_tabs:
        st.write("**⚡ System Events:**")
        
        sample_events = [
            {"time": "2024-01-15 14:30:00", "event": "System Health Check", "status": "✅ Passed"},
            {"time": "2024-01-15 14:25:00", "event": "Database Backup", "status": "✅ Completed"},
            {"time": "2024-01-15 14:20:00", "event": "API Rate Limit Check", "status": "✅ Normal"},
            {"time": "2024-01-15 14:15:00", "event": "Memory Usage Alert", "status": "⚠️ Warning"},
            {"time": "2024-01-15 14:10:00", "event": "User Session Cleanup", "status": "✅ Completed"}
        ]
        
        for event in sample_events:
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                st.write(event["time"])
            
            with col2:
                st.write(event["event"])
            
            with col3:
                st.write(event["status"])
    
    with log_tabs:
        st.write("**🚨 Alert History:**")
        
        sample_alert_history = [
            {"time": "14:23:45", "type": "Critical", "message": "Mass misinformation detected", "resolved": "Yes"},
            {"time": "13:45:22", "type": "Warning", "message": "Suspicious pattern identified", "resolved": "Yes"},
            {"time": "12:30:15", "type": "Info", "message": "Routine scan completed", "resolved": "N/A"},
            {"time": "11:15:30", "type": "Critical", "message": "High-risk content flagged", "resolved": "Under Investigation"},
        ]
        
        for alert in sample_alert_history:
            col1, col2, col3, col4 = st.columns([2, 1, 3, 1])
            
            with col1:
                st.write(alert["time"])
            
            with col2:
                color = "🔴" if alert["type"] == "Critical" else "🟡" if alert["type"] == "Warning" else "🟢"
                st.write(f"{color} {alert['type']}")
            
            with col3:
                st.write(alert["message"])
            
            with col4:
                st.write(alert["resolved"])
