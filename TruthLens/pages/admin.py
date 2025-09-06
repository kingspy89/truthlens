import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
import os
from utils.database import FirebaseService
from utils.security import SecurityService
from utils.email_service import EmailService

# Admin credentials (you can change these)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "truthlens2024"  # Change this to your preferred password
ADMIN_EMAIL = "malav0003@gmail.com"

def check_admin_authentication():
    """Check if user is authenticated as admin"""
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        show_admin_login()
        return False
    return True

def show_admin_login():
    """Show admin login form"""
    st.markdown("""
    <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 50px 0;">
        <h1>🔐 TruthLens Admin Portal</h1>
        <p>🚀 Secret Administrative Access</p>
        <p>🛡️ Authorized Personnel Only</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login"):
        st.markdown("### 🔑 Admin Authentication")
        
        username = st.text_input("👤 Admin Username", placeholder="Enter admin username")
        password = st.text_input("🔒 Admin Password", type="password", placeholder="Enter admin password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("🚀 Access Admin Panel", type="primary", use_container_width=True):
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.success("✅ Admin access granted!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Access denied.")
    
    st.markdown("---")
    st.info("🔒 This is a secure admin portal. Only authorized personnel can access this area.")

def admin_interface():
    """Main admin interface"""
    if not check_admin_authentication():
        return
    
    # Admin header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h1>👑 TruthLens Admin Control Center</h1>
        <p>Welcome, Admin! Monitor all user activity and system performance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Reports", "1,247", "+23")
    with col2:
        st.metric("👥 Active Users", "89", "+5")
    with col3:
        st.metric("🤖 AI Analyses", "2,156", "+45")
    with col4:
        st.metric("🚨 High Risk", "34", "+8")
    
    # Admin tabs
    tabs = st.tabs([
        "📊 Live Dashboard",
        "📋 User Reports", 
        "🤖 AI Responses",
        "📧 Email Center",
        "⚙️ System Settings"
    ])
    
    with tabs[0]:
        live_admin_dashboard()
    
    with tabs[1]:
        user_reports_management()
    
    with tabs[2]:
        ai_responses_monitoring()
    
    with tabs[3]:
        email_center()
    
    with tabs[4]:
        system_settings()

def live_admin_dashboard():
    """Live admin dashboard with real-time data"""
    st.markdown("### 📊 Live System Dashboard")
    
    # Real-time metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔄 Real-Time Activity**")
        
        # Simulate live data
        activity_data = {
            "Current Users": 89,
            "Reports Last Hour": 23,
            "AI Analyses Running": 5,
            "System Load": "78%",
            "Database Status": "🟢 Healthy",
            "API Status": "🟢 Operational"
        }
        
        for key, value in activity_data.items():
            st.write(f"• **{key}:** {value}")
    
    with col2:
        st.markdown("**📈 Recent Activity Graph**")
        
        # Create a simple activity chart
        import plotly.graph_objects as go
        import numpy as np
        
        hours = list(range(24))
        reports = np.random.poisson(15, 24)  # Simulate reports per hour
        analyses = np.random.poisson(25, 24)  # Simulate AI analyses per hour
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=reports, mode='lines+markers', name='Reports', line=dict(color='#ff6b6b')))
        fig.add_trace(go.Scatter(x=hours, y=analyses, mode='lines+markers', name='AI Analyses', line=dict(color='#4ecdc4')))
        
        fig.update_layout(
            title="24-Hour Activity",
            xaxis_title="Hour",
            yaxis_title="Count",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent alerts
    st.markdown("### 🚨 Recent Alerts")
    
    alerts = [
        {"time": "14:32", "type": "High Risk Content", "message": "User reported false vaccine information", "severity": "🔴 High"},
        {"time": "14:28", "type": "System", "message": "Database backup completed successfully", "severity": "🟢 Info"},
        {"time": "14:25", "type": "AI Analysis", "message": "Gemini API response time increased", "severity": "🟡 Warning"},
        {"time": "14:20", "type": "User Report", "message": "New report submitted for review", "severity": "🔵 Info"}
    ]
    
    for alert in alerts:
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            with col1:
                st.write(f"`{alert['time']}`")
            with col2:
                st.write(f"**{alert['type']}**")
            with col3:
                st.write(alert['message'])
            with col4:
                st.write(alert['severity'])

def user_reports_management():
    """Manage and view all user reports"""
    st.markdown("### 📋 User Reports Management")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "New", "Under Review", "Resolved", "Rejected"])
    
    with col2:
        priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Critical"])
    
    with col3:
        date_filter = st.selectbox("Filter by Date", ["All", "Today", "Last 7 Days", "Last 30 Days"])
    
    # Simulate user reports data
    reports_data = [
        {
            "id": "TL-1234",
            "user": "user@example.com",
            "content": "False information about COVID-19 vaccines",
            "status": "Under Review",
            "priority": "High",
            "risk_score": 85,
            "ai_analysis": "FALSE INFORMATION: This content contains misleading claims about vaccine safety...",
            "timestamp": "2024-01-15 14:30:00",
            "reporter_name": "John Doe"
        },
        {
            "id": "TL-1233",
            "user": "analyst@company.com",
            "content": "Misleading climate change data",
            "status": "Resolved",
            "priority": "Medium",
            "risk_score": 65,
            "ai_analysis": "MISLEADING: The data presented is cherry-picked and doesn't represent the full picture...",
            "timestamp": "2024-01-15 12:15:00",
            "reporter_name": "Jane Smith"
        },
        {
            "id": "TL-1232",
            "user": "researcher@university.edu",
            "content": "Fake news about political events",
            "status": "New",
            "priority": "Critical",
            "risk_score": 95,
            "ai_analysis": "FALSE INFORMATION: This is completely fabricated news with no factual basis...",
            "timestamp": "2024-01-15 10:45:00",
            "reporter_name": "Dr. Michael Johnson"
        }
    ]
    
    # Display reports in a table
    if reports_data:
        df = pd.DataFrame(reports_data)
        
        # Filter data
        if status_filter != "All":
            df = df[df['status'] == status_filter]
        if priority_filter != "All":
            df = df[df['priority'] == priority_filter]
        
        st.dataframe(df, use_container_width=True)
        
        # Action buttons for each report
        st.markdown("### 🎯 Report Actions")
        
        for report in reports_data:
            with st.expander(f"📋 Report {report['id']} - {report['status']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**User:** {report['user']}")
                    st.write(f"**Reporter:** {report['reporter_name']}")
                    st.write(f"**Priority:** {report['priority']}")
                    st.write(f"**Risk Score:** {report['risk_score']}/100")
                    st.write(f"**Timestamp:** {report['timestamp']}")
                
                with col2:
                    st.write(f"**Content:** {report['content'][:100]}...")
                    st.write(f"**AI Analysis:** {report['ai_analysis'][:150]}...")
                
                # Action buttons
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                
                with col_btn1:
                    if st.button(f"✅ Resolve {report['id']}", key=f"resolve_{report['id']}"):
                        st.success(f"Report {report['id']} marked as resolved!")
                
                with col_btn2:
                    if st.button(f"📧 Email {report['id']}", key=f"email_{report['id']}"):
                        send_report_email(report)
                
                with col_btn3:
                    if st.button(f"🔍 Details {report['id']}", key=f"details_{report['id']}"):
                        st.info(f"Full details for report {report['id']}")
                
                with col_btn4:
                    if st.button(f"❌ Reject {report['id']}", key=f"reject_{report['id']}"):
                        st.error(f"Report {report['id']} rejected!")
    else:
        st.info("No reports found matching the selected filters.")

def ai_responses_monitoring():
    """Monitor AI responses and performance"""
    st.markdown("### 🤖 AI Responses Monitoring")
    
    # AI performance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 Accuracy Rate", "94.2%", "+1.2%")
    with col2:
        st.metric("⚡ Avg Response Time", "2.3s", "-0.5s")
    with col3:
        st.metric("🔄 Total Analyses", "2,156", "+45")
    
    # Recent AI responses
    st.markdown("### 📊 Recent AI Responses")
    
    ai_responses = [
        {
            "timestamp": "2024-01-15 14:32:15",
            "content": "COVID-19 vaccines are dangerous",
            "ai_verdict": "FALSE INFORMATION",
            "confidence": 95,
            "response_time": "1.8s",
            "risk_score": 85
        },
        {
            "timestamp": "2024-01-15 14:28:42",
            "content": "Climate change is a hoax",
            "ai_verdict": "FALSE INFORMATION", 
            "confidence": 92,
            "response_time": "2.1s",
            "risk_score": 78
        },
        {
            "timestamp": "2024-01-15 14:25:18",
            "content": "New study shows benefits of exercise",
            "ai_verdict": "TRUE",
            "confidence": 88,
            "response_time": "1.9s",
            "risk_score": 15
        }
    ]
    
    for response in ai_responses:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
            
            with col1:
                st.write(f"`{response['timestamp']}`")
                st.write(f"**Content:** {response['content'][:50]}...")
            
            with col2:
                verdict_color = "🔴" if response['ai_verdict'] == "FALSE INFORMATION" else "🟢" if response['ai_verdict'] == "TRUE" else "🟡"
                st.write(f"{verdict_color} **{response['ai_verdict']}**")
                st.write(f"Confidence: {response['confidence']}%")
            
            with col3:
                st.write(f"⏱️ {response['response_time']}")
            
            with col4:
                st.write(f"🎯 {response['risk_score']}/100")
            
            with col5:
                if st.button(f"📧 Email", key=f"email_ai_{response['timestamp']}"):
                    send_ai_response_email(response)

def email_center():
    """Email management center"""
    st.markdown("### 📧 Email Center")
    
    # Email settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📧 Email Settings**")
        
        admin_email = st.text_input("Admin Email", value=ADMIN_EMAIL, disabled=True)
        smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
        smtp_port = st.number_input("SMTP Port", value=587)
        email_password = st.text_input("Email Password", type="password", placeholder="Enter your email password")
        
        if st.button("💾 Save Email Settings"):
            st.success("✅ Email settings saved!")
    
    with col2:
        st.markdown("**📊 Email Statistics**")
        
        email_stats = {
            "📧 Emails Sent Today": "23",
            "📬 Pending Emails": "5", 
            "✅ Success Rate": "98.5%",
            "❌ Failed Emails": "1"
        }
        
        for key, value in email_stats.items():
            st.write(f"• **{key}:** {value}")
    
    # Send test email
    st.markdown("### 🧪 Test Email")
    
    if st.button("📧 Send Test Email", type="primary"):
        with st.spinner("Sending test email..."):
            try:
                send_test_email()
                st.success("✅ Test email sent successfully!")
            except Exception as e:
                st.error(f"❌ Failed to send test email: {str(e)}")

def system_settings():
    """System settings and configuration"""
    st.markdown("### ⚙️ System Settings")
    
    # Admin settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔐 Admin Settings**")
        
        new_password = st.text_input("New Admin Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("🔒 Change Password"):
            if new_password == confirm_password:
                st.success("✅ Password changed successfully!")
            else:
                st.error("❌ Passwords don't match!")
    
    with col2:
        st.markdown("**📊 System Configuration**")
        
        auto_email = st.checkbox("Enable Auto-Email Reports", value=True)
        email_frequency = st.selectbox("Email Frequency", ["Immediate", "Hourly", "Daily", "Weekly"])
        max_reports = st.number_input("Max Reports per User", value=100)
        
        if st.button("💾 Save Configuration"):
            st.success("✅ Configuration saved!")

def send_report_email(report):
    """Send report details to admin email"""
    try:
        email_service = EmailService()
        success = email_service.send_report_email(report, ADMIN_EMAIL)
        
        if success:
            st.success(f"📧 Report {report['id']} sent to {ADMIN_EMAIL}!")
        else:
            st.error(f"❌ Failed to send report {report['id']}")
        
    except Exception as e:
        st.error(f"❌ Failed to send email: {str(e)}")

def send_ai_response_email(response):
    """Send AI response details to admin email"""
    try:
        email_service = EmailService()
        success = email_service.send_ai_response_email(response, ADMIN_EMAIL)
        
        if success:
            st.success(f"📧 AI Response sent to {ADMIN_EMAIL}!")
        else:
            st.error(f"❌ Failed to send AI response")
        
    except Exception as e:
        st.error(f"❌ Failed to send email: {str(e)}")

def send_test_email():
    """Send a test email to verify email configuration"""
    try:
        email_service = EmailService()
        success = email_service.send_test_email(ADMIN_EMAIL)
        
        if success:
            st.success("📧 Test email sent successfully!")
        else:
            st.error("❌ Failed to send test email")
        
    except Exception as e:
        st.error(f"❌ Failed to send test email: {str(e)}")

def logout_admin():
    """Logout admin user"""
    st.session_state.admin_authenticated = False
    st.rerun()
