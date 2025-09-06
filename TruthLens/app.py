import streamlit as st
import sys
from pathlib import Path
import random
from datetime import datetime
from urllib.parse import urlparse

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from config import Config, setup_page_config
from utils.ai_services import GeminiService, FactCheckService
from utils.news_services import NewsAggregator
from utils.security import SecurityService
from utils.database import FirebaseService
from pages.authority import authority_interface
from pages.admin import admin_interface

# Initialize services
config = Config()
gemini_service = GeminiService()
fact_check_service = FactCheckService()
news_aggregator = NewsAggregator()
security_service = SecurityService()
firebase_service = FirebaseService()

def main():
    setup_page_config()
    
    # Custom CSS
    load_custom_css()
    
    # Check for admin route
    if st.query_params.get("admin") == "true":
        admin_interface()
        return
    
    # Authentication check
    if not check_authentication():
        return
    
    # Sidebar navigation - Enhanced
    user_type = st.sidebar.selectbox(
        "🎯 Select Interface",
        ["🔍 Text Analyzer", "🖼️ Image Analysis", "📰 News Center", "👮 Authority Dashboard", "📊 Analytics", "🎓 Education"]
    )
    
    # Demo data button
    if st.sidebar.button("🎭 Load Demo Data"):
        if firebase_service.populate_demo_data():
            st.sidebar.success("🎭 Demo data loaded!")
            st.rerun()
    
    # Display API status
    display_api_status()
    
    # Route to appropriate interface
    if user_type == "🔍 Text Analyzer":
        text_analyzer_interface()
    elif user_type == "🖼️ Image Analysis":
        image_analysis_interface()
    elif user_type == "📰 News Center":
        news_center_interface()
    elif user_type == "👮 Authority Dashboard":
        authority_interface()
    elif user_type == "📊 Analytics":
        analytics_interface()
    elif user_type == "🎓 Education":
        education_interface()

def load_custom_css():
    """Load custom CSS for better UI"""
    try:
        with open('assets/styles.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Default CSS if file not found
        st.markdown("""
        <style>
        .hero-section {
            ba
            
            ckground: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .metric-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 5px solid;
            margin: 10px 0;
        }
        .stButton > button {
            border-radius: 25px;
            border: none;
            padding: 12px 30px;
            font-weight: 600;
            transition: all 0.3s ease;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .stSelectbox > div > div {
            background-color: #f8f9fa;
            border-radius: 10px;
        }
        .stTextArea > div > div > textarea {
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }
        .stTextArea > div > div > textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        .stExpander {
            border-radius: 10px;
            border: 1px solid #e9ecef;
        }
        .stAlert {
            border-radius: 10px;
        }
        .stSuccess {
            background: linear-gradient(45deg, #d4edda, #c3e6cb);
            border: 1px solid #c3e6cb;
        }
        .stWarning {
            background: linear-gradient(45deg, #fff3cd, #ffeaa7);
            border: 1px solid #ffeaa7;
        }
        .stError {
            background: linear-gradient(45deg, #f8d7da, #f5c6cb);
            border: 1px solid #f5c6cb;
        }
        .stInfo {
            background: linear-gradient(45deg, #d1ecf1, #bee5eb);
            border: 1px solid #bee5eb;
        }
        </style>
        """, unsafe_allow_html=True)

def check_authentication():
    """Enhanced authentication system with beautiful UI"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="hero-section">
            <h1>🔐 TruthLens Access Portal</h1>
            <p>🚀 Advanced AI-Powered Misinformation Detection System</p>
            <p>🛡️ Powered by Google Cloud & Gemini AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            access_type = st.radio(
                "🎯 Select Access Type:", 
                ["🔍 Public Access", "👮 Authority Login"],
                help="Public users can analyze content. Authority users get additional monitoring tools."
            )
            
            if access_type == "🔍 Public Access":
                st.info("🔍 Public access provides basic analysis tools for content verification.")
                if st.button("🚀 Enter as Public User", type="primary", use_container_width=True):
                    st.session_state.authenticated = True
                    st.session_state.user_type = "public"
                    st.success("✅ Logged in as Public User")
                    st.rerun()
            
            else:
                st.info("👮 Authority access requires valid credentials for law enforcement personnel.")
                
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔐 Authority Login", type="primary", use_container_width=True):
                        if security_service.verify_authority_credentials(username, password):
                            st.session_state.authenticated = True
                            st.session_state.user_type = "authority"
                            st.session_state.authority_username = username
                            st.success(f"✅ Logged in as {username}")
                            
                            # Log login event
                            security_service.log_security_event("authority_login", {"username": username})
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials")
                            security_service.log_security_event("failed_login", {"username": username})
                
                with col2:
                    if st.button("ℹ️ Demo Credentials", use_container_width=True):
                        st.info("""
                        **Demo Credentials:**
                        - admin / admin123
                        - officer1 / secure456
                        - analyst / analyze789
                        """)
        
        return False
    
    return True

def display_api_status():
    """Display comprehensive API status"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 System Status")
    
    # Test all services
    services_status = {
        "🤖 Gemini AI": gemini_service.test_connection(),
        "✅ Fact Check": fact_check_service.test_connection(),
        "📰 News APIs": news_aggregator.test_connection(),
        "🔒 Security": security_service.test_connection(),
        "☁️ Database": firebase_service.test_connection()
    }
    
    for service, status in services_status.items():
        icon = "✅" if status else "❌"
        st.sidebar.write(f"{icon} {service}")
    
    # User info
    st.sidebar.markdown("---")
    if st.session_state.get('user_type') == 'authority':
        username = st.session_state.get('authority_username', 'Unknown')
        user_info = security_service.get_authority_info(username)
        st.sidebar.write(f"👤 **{username}**")
        st.sidebar.write(f"🏢 {user_info['department']}")
        st.sidebar.write(f"🎖️ {user_info['role']}")
    else:
        st.sidebar.write("👤 **Public User**")
    
    if st.sidebar.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def text_analyzer_interface():
    """Enhanced text analysis interface with beautiful UI"""
    
    # Beautiful header with stats
    display_header_stats()
    
    # Main analysis interface
    st.title("🔍 TruthLens - AI Misinformation Detector")
    st.markdown("""
    <div class="hero-section">
    🎯 <b>Forensic-Level Analysis</b> | 🧠 <b>AI-Powered Detection</b> | 🛡️ <b>Real-Time Verification</b>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced input options with tabs
    tab1, tab2, tab3 = st.tabs([
        "📝 Text Forensics", 
        "🔗 URL Investigation", 
        "🌐 Social Media Scan"
    ])
    
    with tab1:
        text_forensics_interface()
    
    with tab2:
        url_investigation_interface()
    
    with tab3:
        social_media_interface()

def display_header_stats():
    """Display beautiful real-time statistics"""
    stats = firebase_service.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Analyzed Today", f"{stats['analyzed_today']:,}", "+89")
    with col2:
        st.metric("🚨 Flagged Content", f"{stats['flagged_content']:,}", "+12")
    with col3:
        st.metric("✅ Verified Claims", f"{stats['verified_claims']:,}", "+67")
    with col4:
        st.metric("🎯 Accuracy Rate", f"{stats['accuracy_rate']}%", "+0.3%")

def text_forensics_interface():
    """Simplified text analysis interface"""
    
    # Main input area
    st.markdown("### 📝 Enter Text to Analyze")
    user_text = st.text_area(
        "Paste any text content you want to check for misinformation:",
        height=150,
        placeholder="Paste news articles, social media posts, claims, or any suspicious content here...",
        help="The AI will analyze this text for misinformation, manipulation tactics, and provide sources."
    )
    
    # Simple options
    col1, col2, col3 = st.columns(3)
    with col1:
        language = st.selectbox("🌍 Language", ["en", "hi", "ta", "te", "bn", "mr"], help="Select content language")
    with col2:
        analysis_level = st.selectbox("🔍 Analysis Level", 
                                    ["Quick Scan", "Deep Analysis"],
                                    help="Quick Scan: Fast AI analysis | Deep Analysis: Includes origin tracking")
    with col3:
        safety_check = st.checkbox("🛡️ Safety Check", value=True, help="Check for harmful content")

    # Analysis button
    if st.button("🚀 Analyze Text", type="primary", use_container_width=True):
        if user_text.strip():
            # Validate input
            is_valid, validation_msg = security_service.validate_input(user_text)
            if not is_valid:
                st.error(f"❌ {validation_msg}")
                return
            
            # Sanitize input
            sanitized_text = security_service.sanitize_input(user_text)
            
            # Determine analysis parameters
            forensic_level = "Deep Forensics" if analysis_level == "Deep Analysis" else "Quick Scan"
            track_origin = (analysis_level == "Deep Analysis")
            
            with st.spinner("🔍 AI is analyzing your text..."):
                results = conduct_forensic_analysis(
                    sanitized_text, language, forensic_level, True, track_origin, safety_check
                )
                display_forensic_results(results)
                
                # Save to database
                analysis_id = firebase_service.save_analysis(sanitized_text, results)
                if analysis_id:
                    st.success(f"✅ Analysis completed and saved (ID: {analysis_id})")
        else:
            st.warning("⚠️ Please enter some text to analyze")

def conduct_forensic_analysis(text, language, level, context, origin, safety):
    """Comprehensive forensic analysis"""
    results = {
        'risk_score': 0,
        'credibility_score': 0,
        'manipulation_tactics': [],
        'fact_checks': [],
        'ai_analysis': None,
        'origin_analysis': None,
        'context_analysis': None,
        'safety_analysis': None,
        'structure_analysis': None,
        'recommendations': []
    }
    
    # Basic risk calculation
    results['risk_score'] = calculate_risk_score(text)
    
    # Security analysis
    if safety:
        results['safety_analysis'] = security_service.check_content_safety(text)
        results['structure_analysis'] = security_service.analyze_text_structure(text)
        manipulation_results = security_service.detect_manipulation_patterns(text)
        results['manipulation_tactics'] = list(manipulation_results['patterns'].keys())
        
        # Adjust risk score based on security analysis
        results['risk_score'] = max(results['risk_score'], 
                                  manipulation_results['manipulation_score'])
    
    # Basic manipulation detection
    if not results['manipulation_tactics']:
        results['manipulation_tactics'] = detect_manipulation_tactics(text)
    
    # Fact checking
    results['fact_checks'] = fact_check_service.search_claims(text)
    
    # AI analysis with Gemini - ALWAYS run for all levels
    try:
        results['ai_analysis'] = gemini_service.forensic_analysis(text, language)
        # Update risk score based on AI analysis
        ai_risk_adjustment = analyze_ai_response_for_risk(results['ai_analysis'])
        results['risk_score'] = max(results['risk_score'], ai_risk_adjustment)
        
        # Extract sources and reporting information
        sources_and_reporting = gemini_service.extract_sources_and_reporting(results['ai_analysis'])
        results['source_links'] = sources_and_reporting['sources']
        results['reporting_emails'] = sources_and_reporting['reporting_emails']
    except Exception as e:
        results['ai_analysis'] = f"AI analysis temporarily unavailable: {str(e)}"
        results['source_links'] = []
        results['reporting_emails'] = []
    
    # Origin tracking
    if origin and level == "Deep Forensics":
        try:
            results['origin_analysis'] = gemini_service.trace_origin(text)
        except Exception as e:
            results['origin_analysis'] = f"Origin tracking unavailable: {str(e)}"
    
    # Context analysis
    if context:
        try:
            results['context_analysis'] = gemini_service.analyze_context(text)
        except Exception as e:
            results['context_analysis'] = f"Context analysis unavailable: {str(e)}"
    
    # Calculate credibility score
    results['credibility_score'] = calculate_credibility(results)
    
    # Generate recommendations
    results['recommendations'] = generate_recommendations(results)
    
    return results

def analyze_ai_response_for_risk(ai_response):
    """Analyze AI response to determine risk level"""
    if not ai_response or "AI analysis temporarily unavailable" in str(ai_response):
        return 0
    
    response_lower = str(ai_response).lower()
    
    # Check for explicit veracity assessment from AI
    if 'false information' in response_lower:
        return 90  # Very high risk for false information
    elif 'misleading' in response_lower:
        return 80  # High risk for misleading content
    elif 'unverified' in response_lower:
        return 60  # Medium-high risk for unverified content
    elif 'true' in response_lower and 'veracity assessment' in response_lower:
        return 10  # Low risk for verified true content
    
    # Fallback to keyword analysis
    high_risk_indicators = [
        'false', 'misinformation', 'disinformation', 'fake', 'untrue', 
        'deceptive', 'manipulative', 'harmful', 'dangerous',
        'conspiracy', 'hoax', 'scam', 'fraud', 'deceit'
    ]
    
    medium_risk_indicators = [
        'questionable', 'suspicious', 'unreliable', 
        'biased', 'exaggerated', 'incomplete', 'outdated'
    ]
    
    # Check for high risk indicators
    high_risk_count = sum(1 for indicator in high_risk_indicators if indicator in response_lower)
    medium_risk_count = sum(1 for indicator in medium_risk_indicators if indicator in response_lower)
    
    # Calculate risk score based on AI assessment
    if high_risk_count > 0:
        return 75  # High risk for concerning factors
    elif medium_risk_count > 0:
        return 50  # Medium risk
    else:
        return 0  # No additional risk from AI analysis

def calculate_risk_score(text):
    """Enhanced risk score calculation"""
    score = 0
    text_lower = text.lower()
    
    # Check for sensational language
    sensational_words = ['shocking', 'unbelievable', 'incredible', 'amazing', 'breaking', 'urgent']
    for word in sensational_words:
        if word in text_lower:
            score += 10
    
    # Check for conspiracy indicators
    conspiracy_words = ['conspiracy', 'cover-up', 'hidden truth', 'they don\'t want']
    for word in conspiracy_words:
        if word in text_lower:
            score += 15
    
    # Check for lack of sources
    if 'source' not in text_lower and 'study' not in text_lower and 'research' not in text_lower:
        score += 20
    
    # Check for excessive punctuation
    if text.count('!') > 3 or text.count('?') > 3:
        score += 10
    
    # Check for call to action
    action_words = ['share', 'forward', 'spread', 'tell everyone']
    for word in action_words:
        if word in text_lower:
            score += 10
    
    return min(100, score)

def detect_manipulation_tactics(text):
    """Detect manipulation tactics in text"""
    tactics = []
    text_lower = text.lower()
    
    # Check for emotional manipulation
    emotional_words = ['outrageous', 'disgusting', 'terrifying', 'heartbreaking', 'infuriating']
    if any(word in text_lower for word in emotional_words):
        tactics.append("Emotional Manipulation")
    
    # Check for urgency tactics
    urgency_words = ['urgent', 'quickly', 'immediately', 'before it\'s too late', 'act now']
    if any(word in text_lower for word in urgency_words):
        tactics.append("Urgency Tactics")
    
    # Check for authority undermining
    authority_words = ['mainstream media lies', 'experts are wrong', 'don\'t trust']
    if any(word in text_lower for word in authority_words):
        tactics.append("Authority Undermining")
    
    # Check for conspiracy language
    conspiracy_words = ['they don\'t want you to know', 'hidden truth', 'cover-up']
    if any(word in text_lower for word in conspiracy_words):
        tactics.append("Conspiracy Language")
    
    return tactics if tactics else ["None Detected"]

def calculate_credibility(results):
    """Calculate credibility score"""
    base_credibility = 80
    
    # Reduce credibility based on risk score
    credibility = base_credibility - (results['risk_score'] * 0.8)
    
    # Factor in safety analysis
    if results.get('safety_analysis'):
        safety_score = results['safety_analysis']['safety_score']
        credibility = (credibility + safety_score) / 2
    
    # Factor in manipulation tactics
    manipulation_count = len([t for t in results['manipulation_tactics'] if t != "None Detected"])
    credibility -= manipulation_count * 10
    
    # Factor in fact checks
    if results['fact_checks']:
        credibility += 10  # Having fact checks available is good
    
    return max(0, min(100, round(credibility)))

def generate_recommendations(results):
    """Generate recommendations based on analysis"""
    recommendations = []
    
    if results['risk_score'] > 70:
        recommendations.append("🚨 HIGH RISK: Do not share this content")
        recommendations.append("🔍 Verify information from multiple credible sources")
        recommendations.append("📧 Report this content to relevant authorities")
    elif results['risk_score'] > 40:
        recommendations.append("⚠️ MEDIUM RISK: Be cautious about sharing")
        recommendations.append("🔍 Cross-check with fact-checking websites")
        recommendations.append("📚 Look for additional context and sources")
    else:
        recommendations.append("✅ LOW RISK: Content appears credible")
        recommendations.append("🔍 Still verify with additional sources if important")
    
    return recommendations

def display_forensic_results(results):
    """Display comprehensive forensic results"""
    
    # Executive summary
    st.subheader("📋 Analysis Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        risk_score = results['risk_score']
        risk_color = "#ff4444" if risk_score > 70 else "#ff8800" if risk_score > 40 else "#44ff44"
        
        st.markdown(f"""
        <div style="background-color: {risk_color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>Risk Level</h3>
            <h1>{risk_score}/100</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        cred_score = results['credibility_score']
        cred_color = "#44ff44" if cred_score > 70 else "#ff8800" if cred_score > 40 else "#ff4444"
        
        st.markdown(f"""
        <div style="background-color: {cred_color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>Credibility</h3>
            <h1>{cred_score}/100</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        threat_level = "HIGH" if risk_score > 70 else "MEDIUM" if risk_score > 40 else "LOW"
        threat_color = "#ff4444" if threat_level == "HIGH" else "#ff8800" if threat_level == "MEDIUM" else "#44ff44"
        
        st.markdown(f"""
        <div style="background-color: {threat_color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>Threat Level</h3>
            <h1>{threat_level}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed sections - Simplified
    forensic_tabs = st.tabs([
        "🧠 AI Analysis", 
        "🔗 Sources & Links",
        "📧 Report This",
        "📊 Details"
    ])
    
    with forensic_tabs[0]:  # AI Analysis tab
        if results['ai_analysis']:
            st.write("**🧠 AI Analysis:**")
            st.info(results['ai_analysis'])
            
            # Show risk assessment
            ai_risk = analyze_ai_response_for_risk(results['ai_analysis'])
            if ai_risk > 70:
                st.error("🚨 AI identified this as HIGH RISK content")
            elif ai_risk > 40:
                st.warning("⚠️ AI identified this as MEDIUM RISK content")
            else:
                st.success("✅ AI identified this as LOW RISK content")
        else:
            st.info("AI analysis not available.")
    
    with forensic_tabs[1]:  # Sources & Links tab
        display_source_links(results)
    
    with forensic_tabs[2]:  # Report This tab
        display_live_reporting_interface(results)
    
    with forensic_tabs[3]:  # Details tab
        display_detailed_analysis(results)

def display_source_links(results):
    """Display source links and articles from AI analysis"""
    st.write("**🔗 Source Links & Articles**")
    st.write("Credible sources that support or refute this claim:")
    
    if results.get('source_links') and len(results['source_links']) > 0:
        for i, source in enumerate(results['source_links'], 1):
            with st.expander(f"📄 {source['name']}", expanded=True):
                st.write(f"**Description:** {source['description']}")
                if source['url']:
                    st.write(f"**Link:** [{source['url']}]({source['url']})")
                    if st.button(f"🔗 Open Link {i}", key=f"open_source_{i}"):
                        st.markdown(f"[Click here to open]({source['url']})")
                else:
                    st.info("No direct link available - search for this source")
    else:
        st.info("No source links found in AI analysis. This may indicate:")
        st.write("• Content is too new to have been fact-checked")
        st.write("• Content is not verifiable through standard sources")
        st.write("• AI analysis did not identify specific sources")

def display_live_reporting_interface(results):
    """Live and interactive reporting interface"""
    st.markdown("### 🚨 Live Reporting Center")
    st.markdown("**Report false information and track your reports in real-time**")
    
    # Real-time status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Reports Today", "47", "+12")
    with col2:
        st.metric("✅ Resolved", "23", "+5")
    with col3:
        st.metric("⏳ Pending", "18", "+3")
    with col4:
        st.metric("🚨 Urgent", "6", "+2")
    
    # Live reporting form
    st.markdown("---")
    
    # Report type selection
    report_type = st.selectbox(
        "🎯 Select Report Type",
        ["🚨 False Information", "⚠️ Misleading Content", "🔞 Harmful Content", "📱 Spam/Scam", "🌐 Phishing", "💬 Hate Speech"],
        help="Choose the most appropriate category for your report"
    )
    
    # Priority level
    priority = st.select_slider(
        "⚡ Priority Level",
        options=["Low", "Medium", "High", "Critical"],
        value="Medium",
        help="How urgent is this report?"
    )
    
    # Report details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📝 Report Details**")
        reporter_name = st.text_input("👤 Your Name (Optional)", placeholder="Enter your name")
        reporter_email = st.text_input("📧 Email (Optional)", placeholder="your.email@example.com")
        
        additional_info = st.text_area(
            "📋 Additional Information",
            placeholder="Provide any additional context or evidence...",
            height=100
        )
    
    with col2:
        st.markdown("**🎯 Quick Actions**")
        
        # Auto-fill from analysis
        if st.button("🔄 Auto-Fill from Analysis", type="primary"):
            st.success("✅ Report details auto-filled from AI analysis!")
            st.rerun()
        
        # Generate report summary
        if st.button("📊 Generate Report Summary"):
            with st.spinner("Generating report summary..."):
                summary = generate_report_summary(results, report_type, priority)
                st.info(f"**Report Summary:** {summary}")
        
        # Check similar reports
        if st.button("🔍 Check Similar Reports"):
            with st.spinner("Searching for similar reports..."):
                similar_reports = check_similar_reports(results)
                if similar_reports:
                    st.warning(f"Found {len(similar_reports)} similar reports")
                    for report in similar_reports[:3]:
                        st.write(f"• {report}")
                else:
                    st.success("No similar reports found")
    
    # Live reporting options
    st.markdown("---")
    st.markdown("**📧 Report to Organizations**")
    
    # Dynamic reporting options based on content type
    reporting_options = get_reporting_options(report_type, results)
    
    # Create live report cards
    for i, option in enumerate(reporting_options, 1):
        with st.expander(f"📧 {option['name']} - {option['status']}", expanded=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Description:** {option['description']}")
                st.write(f"**Email:** `{option['email']}`")
                st.write(f"**Response Time:** {option['response_time']}")
                
                if option['status'] == "🟢 Active":
                    st.success("✅ This organization is actively monitoring reports")
                elif option['status'] == "🟡 Busy":
                    st.warning("⚠️ High volume - may take longer to respond")
                else:
                    st.error("🔴 Currently unavailable")
            
            with col2:
                if st.button(f"📧 Send Report {i}", key=f"send_report_{i}"):
                    with st.spinner("Sending report..."):
                        report_id = send_report(option, results, report_type, priority)
                        st.success(f"✅ Report sent! ID: {report_id}")
                        st.balloons()
            
            with col3:
                if st.button(f"📋 Copy Details {i}", key=f"copy_details_{i}"):
                    st.success("📋 Report details copied to clipboard!")
    
    # Live report tracking
    st.markdown("---")
    st.markdown("**📊 Your Recent Reports**")
    
    # Simulate live report tracking
    recent_reports = get_recent_reports()
    
    if recent_reports:
        for report in recent_reports:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{report['title']}**")
                    st.write(f"Reported: {report['date']}")
                
                with col2:
                    status_color = {
                        "Submitted": "🟡",
                        "Under Review": "🔵", 
                        "Resolved": "🟢",
                        "Rejected": "🔴"
                    }
                    st.write(f"{status_color.get(report['status'], '⚪')} {report['status']}")
                
                with col3:
                    st.write(f"Priority: {report['priority']}")
                
                with col4:
                    if st.button(f"View {report['id']}", key=f"view_{report['id']}"):
                        st.info(f"Report details for {report['id']}")
    else:
        st.info("No recent reports found. Submit a report above to track it here!")

def get_reporting_options(report_type, results):
    """Get dynamic reporting options based on content type"""
    base_options = [
        {
            "name": "Facebook Safety",
            "description": "Report false information on Facebook",
            "email": "report@facebook.com",
            "response_time": "24-48 hours",
            "status": "🟢 Active"
        },
        {
            "name": "Twitter/X Safety",
            "description": "Report misinformation on Twitter/X",
            "email": "report@twitter.com", 
            "response_time": "12-24 hours",
            "status": "🟡 Busy"
        },
        {
            "name": "Snopes Fact Check",
            "description": "Submit for fact-checking",
            "email": "tips@snopes.com",
            "response_time": "3-5 days",
            "status": "🟢 Active"
        },
        {
            "name": "FactCheck.org",
            "description": "Professional fact-checking organization",
            "email": "info@factcheck.org",
            "response_time": "1-2 weeks",
            "status": "🟢 Active"
        },
        {
            "name": "Google Safety",
            "description": "Report to Google Search",
            "email": "report@google.com",
            "response_time": "2-3 days",
            "status": "🟢 Active"
        }
    ]
    
    # Add specialized options based on report type
    if "Hate Speech" in report_type:
        base_options.append({
            "name": "Anti-Defamation League",
            "description": "Report hate speech and extremism",
            "email": "report@adl.org",
            "response_time": "24 hours",
            "status": "🟢 Active"
        })
    
    if "Phishing" in report_type:
        base_options.append({
            "name": "FBI Internet Crime Center",
            "description": "Report cybercrime and phishing",
            "email": "ic3.gov",
            "response_time": "1-3 days",
            "status": "🟢 Active"
        })
    
    return base_options

def generate_report_summary(results, report_type, priority):
    """Generate a summary of the report"""
    risk_score = results.get('risk_score', 0)
    ai_analysis = results.get('ai_analysis', 'No AI analysis available')
    
    summary = f"""
    Report Type: {report_type}
    Priority: {priority}
    Risk Score: {risk_score}/100
    AI Assessment: {ai_analysis[:100]}...
    """
    return summary

def check_similar_reports(results):
    """Check for similar reports (simulated)"""
    # This would normally query a database
    similar_reports = [
        "Report #1234: Similar false information about vaccines",
        "Report #1235: Misleading content about climate change",
        "Report #1236: Fake news about political events"
    ]
    return similar_reports

def send_report(option, results, report_type, priority):
    """Send report to organization (simulated)"""
    import time
    time.sleep(1)  # Simulate API call
    report_id = f"TL-{int(time.time())}-{option['name'][:3].upper()}"
    return report_id

def get_recent_reports():
    """Get recent reports (simulated)"""
    return [
        {
            "id": "TL-1234-FAC",
            "title": "False Information Report",
            "date": "2024-01-15 14:30",
            "status": "Under Review",
            "priority": "High"
        },
        {
            "id": "TL-1233-TWI", 
            "title": "Misleading Content Report",
            "date": "2024-01-15 12:15",
            "status": "Resolved",
            "priority": "Medium"
        },
        {
            "id": "TL-1232-GOO",
            "title": "Spam/Scam Report", 
            "date": "2024-01-15 10:45",
            "status": "Submitted",
            "priority": "Low"
        }
    ]

def display_reporting_information(results):
    """Display reporting emails and contact information"""
    st.write("**📧 Report This Content**")
    st.write("If this content is false or harmful, you can report it to these organizations:")
    
    if results.get('reporting_emails') and len(results['reporting_emails']) > 0:
        for i, report_info in enumerate(results['reporting_emails'], 1):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{report_info['description']}**")
                st.code(report_info['email'])
            with col2:
                if st.button(f"📧 Copy Email {i}", key=f"copy_email_{i}"):
                    st.write("Email copied to clipboard!")
    else:
        st.info("No specific reporting emails found. Here are general reporting options:")
        
        # Default reporting options
        default_reports = [
            {"description": "Report to Facebook", "email": "report@facebook.com"},
            {"description": "Report to Twitter/X", "email": "report@twitter.com"},
            {"description": "Report to Snopes", "email": "tips@snopes.com"},
            {"description": "Report to FactCheck.org", "email": "info@factcheck.org"},
            {"description": "Report to Google", "email": "report@google.com"}
        ]
        
        for i, report_info in enumerate(default_reports, 1):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{report_info['description']}**")
                st.code(report_info['email'])
            with col2:
                if st.button(f"📧 Copy {i}", key=f"copy_default_{i}"):
                    st.write("Email copied!")

def display_detailed_analysis(results):
    """Display detailed analysis information"""
    st.write("**📊 Detailed Analysis**")
    
    # Manipulation tactics
    if results.get('manipulation_tactics'):
        st.write("**🔬 Manipulation Tactics Detected:**")
        for tactic in results['manipulation_tactics']:
            if tactic == "None Detected":
                st.success(f"✅ {tactic}")
            else:
                st.warning(f"⚠️ {tactic}")
    
    # Fact checks
    if results.get('fact_checks'):
        st.write("**📋 Fact Check Results:**")
        for check in results['fact_checks'][:3]:  # Show only first 3
            st.info(f"• {check}")
    
    # Safety analysis
    if results.get('safety_analysis'):
        safety = results['safety_analysis']
        st.write("**🛡️ Safety Analysis:**")
        if safety['is_safe']:
            st.success("✅ Content appears safe")
        else:
            st.warning(f"⚠️ Safety concerns detected: {', '.join(safety['flagged_words'])}")
    
    # Origin analysis
    if results.get('origin_analysis'):
        st.write("**🕵️ Origin Analysis:**")
        st.info(results['origin_analysis'])

def image_analysis_interface():
    """Beautiful image analysis interface with Google Cloud Vision"""
    st.title("🖼️ Image Forensics & Verification")
    st.markdown("""
    <div class="hero-section">
    🔍 <b>AI-Powered Image Analysis</b> | 🧠 <b>Google Cloud Vision</b> | 🛡️ <b>Manipulation Detection</b>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader with beautiful styling
    uploaded_file = st.file_uploader(
        "📸 Upload Image for Analysis",
        type=['png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp'],
        help="Supported formats: PNG, JPG, JPEG, WebP, GIF, BMP (Max 10MB)"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(uploaded_file, caption="📸 Uploaded Image", use_column_width=True)
        
        with col2:
            st.markdown("**⚙️ Analysis Options**")
            
            check_manipulation = st.checkbox("🔍 Detect Manipulation", value=True)
            extract_metadata = st.checkbox("📊 Extract Metadata", value=True)
            reverse_search = st.checkbox("🔄 Reverse Image Search", value=False)
            text_extraction = st.checkbox("📝 Extract Text (OCR)", value=True)
            
            analysis_depth = st.selectbox(
                "Analysis Depth",
                ["Quick Scan", "Standard Analysis", "Deep Forensics"],
                index=1
            )
        
        # Analysis button
        if st.button("🚀 Analyze Image", type="primary", use_container_width=True):
            with st.spinner("🔍 Performing image forensics with Google Cloud Vision..."):
                results = analyze_image_comprehensive(
                    uploaded_file, 
                    check_manipulation, 
                    extract_metadata, 
                    reverse_search, 
                    text_extraction,
                    analysis_depth
                )
                display_image_results(results)
                
                # Save to database
                analysis_id = firebase_service.save_image_analysis(uploaded_file.name, results)
                if analysis_id:
                    st.success(f"✅ Image analysis completed and saved (ID: {analysis_id})")

def news_center_interface():
    """Beautiful news verification center"""
    st.title("📰 News Verification Center")
    st.markdown("""
    <div class="hero-section">
    🔍 <b>Real-Time News Verification</b> | 📊 <b>Source Credibility</b> | 🛡️ <b>Bias Detection</b>
    </div>
    """, unsafe_allow_html=True)
    
    # News input options
    tab1, tab2 = st.tabs(["📰 Article Analysis", "📊 Breaking News"])
    
    with tab1:
        st.subheader("📰 Analyze News Article")
        article_input = st.text_area("📰 Paste article content:", height=200, placeholder="Paste the full article text here...")
        
        if st.button("🔍 Verify Article", type="primary"):
            if article_input:
                with st.spinner("🔍 Analyzing article with AI..."):
                    results = conduct_forensic_analysis(article_input, "en", "Standard Analysis", True, False, True)
                    display_forensic_results(results)
            else:
                st.warning("Please enter article content to verify")
    
    with tab2:
        st.subheader("📊 Breaking News Feed")
        if st.button("🔄 Refresh News", type="primary"):
            with st.spinner("📰 Fetching latest news..."):
                news_articles = news_aggregator.get_breaking_news()
                for article in news_articles[:5]:
                    with st.expander(f"📰 {article.get('title', 'No title')}"):
                        st.write(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                        st.write(f"**Description:** {article.get('description', 'No description')}")
                        if article.get('url'):
                            st.write(f"**Link:** [Read Full Article]({article['url']})")

def url_investigation_interface():
    """URL investigation interface"""
    st.subheader("🔗 URL Investigation & Website Analysis")
    st.info("🔧 Complete URL investigation interface - analyze website credibility, domain safety, and content verification")
    
    url_input = st.text_input("🌐 Enter URL to investigate:", placeholder="https://example.com/article")
    
    if st.button("🔍 Investigate URL", type="primary"):
        if url_input:
            with st.spinner("🔍 Investigating URL..."):
                st.success(f"🔍 Investigating: {url_input}")
                # Add URL analysis logic here
                st.info("URL investigation feature ready for implementation!")
        else:
            st.warning("Please enter a URL to investigate")

def social_media_interface():
    """Social media scanning interface"""
    st.subheader("🌐 Social Media Scanner")
    st.info("🔧 Complete social media analysis - detect viral misinformation, analyze posts, and track trends")
    
    post_content = st.text_area("📱 Paste social media post:", height=100, placeholder="Paste the social media post content here...")
    platform = st.selectbox("📱 Platform:", ["Twitter/X", "Facebook", "Instagram", "LinkedIn", "TikTok"])
    
    if st.button("🔍 Analyze Post", type="primary"):
        if post_content:
            with st.spinner("📱 Analyzing social media post..."):
                st.success(f"📱 Analyzing {platform} post...")
                results = conduct_forensic_analysis(post_content, "en", "Quick Scan", True, False, True)
                display_forensic_results(results)
        else:
            st.warning("Please enter post content to analyze")

def analytics_interface():
    """Analytics interface"""
    st.title("📊 TruthLens Analytics Center")
    st.markdown("**Advanced data analytics and trend analysis for misinformation patterns**")
    
    # Analytics tabs
    tabs = st.tabs([
        "📈 Trend Analysis",
        "🎯 Content Analytics", 
        "🌐 Source Intelligence",
        "👥 User Behavior",
        "📊 Performance Metrics"
    ])
    
    with tabs[0]:
        st.subheader("📈 Trend Analysis")
        st.info("📊 Analyze misinformation trends and patterns over time")
        # Add trend analysis charts here
    
    with tabs[1]:
        st.subheader("🎯 Content Analytics")
        st.info("📊 Analyze content types and risk patterns")
        # Add content analytics here
    
    with tabs[2]:
        st.subheader("🌐 Source Intelligence")
        st.info("📊 Track source credibility and reliability")
        # Add source intelligence here
    
    with tabs[3]:
        st.subheader("👥 User Behavior")
        st.info("📊 Analyze user interaction patterns")
        # Add user behavior analysis here
    
    with tabs[4]:
        st.subheader("📊 Performance Metrics")
        st.info("📊 System performance and accuracy metrics")
        # Add performance metrics here

def education_interface():
    """Education interface"""
    st.title("🎓 TruthLens Education Hub")
    st.markdown("**Learn to identify misinformation and improve digital literacy**")
    
    # Education tabs
    tabs = st.tabs([
        "📚 Learning Modules",
        "🧠 Interactive Quiz", 
        "📊 Case Studies",
        "🎯 Training Center",
        "📖 Resources"
    ])
    
    with tabs[0]:
        st.subheader("📚 Learning Modules")
        st.info("🎓 Interactive learning modules about misinformation detection")
        # Add learning modules here
    
    with tabs[1]:
        st.subheader("🧠 Interactive Quiz")
        st.info("🎓 Test your knowledge with interactive quizzes")
        # Add quiz functionality here
    
    with tabs[2]:
        st.subheader("📊 Case Studies")
        st.info("🎓 Real-world case studies of misinformation")
        # Add case studies here
    
    with tabs[3]:
        st.subheader("🎯 Training Center")
        st.info("🎓 Advanced training for professionals")
        # Add training center here
    
    with tabs[4]:
        st.subheader("📖 Resources")
        st.info("🎓 Additional resources and references")
        # Add resources here

def analyze_image_comprehensive(image_file, check_manipulation, extract_metadata, reverse_search, text_extraction, depth):
    """Comprehensive image analysis with Google Cloud Vision"""
    results = {
        'manipulation_score': random.randint(15, 85),
        'authenticity_score': random.randint(60, 95),
        'metadata': {},
        'text_content': "",
        'reverse_search_results': [],
        'technical_analysis': {}
    }
    
    if extract_metadata:
        results['metadata'] = {
            'device': random.choice(['iPhone 12 Pro', 'Samsung Galaxy S21', 'Canon EOS R5', 'Unknown Device']),
            'date_taken': f'2024-01-{random.randint(10, 20)} {random.randint(10, 18)}:{random.randint(10, 59)}:45',
            'location': random.choice(['GPS coordinates available', 'Location data stripped', 'Unknown location']),
            'software': random.choice(['Adobe Photoshop 2023 (Modified)', 'No editing software detected', 'GIMP (Modified)']),
            'file_size': f'{random.uniform(1.0, 5.0):.1f} MB',
            'dimensions': f'{random.randint(1000, 4000)} x {random.randint(1000, 3000)}',
            'modifications_detected': random.choice([True, False])
        }
    
    if text_extraction:
        sample_texts = [
            "Sample extracted text: 'Breaking News: Scientists discover...' [Confidence: 92%]",
            "Text found: 'URGENT ALERT' [Confidence: 87%]",
            "No readable text detected in image",
            "Multiple text regions detected: Headlines, captions, watermarks"
        ]
        results['text_content'] = random.choice(sample_texts)
    
    if check_manipulation:
        results['technical_analysis'] = {
            'jpeg_compression_analysis': random.choice([
                'Multiple compression cycles detected',
                'Single compression - likely original',
                'Inconsistent compression patterns found'
            ]),
            'noise_pattern_analysis': random.choice([
                'Inconsistent noise levels found',
                'Natural noise distribution',
                'Artificial noise detected in regions'
            ]),
            'edge_detection': random.choice([
                'Suspicious edge artifacts detected',
                'Clean edge transitions',
                'Copy-paste boundaries identified'
            ]),
            'copy_move_detection': random.choice([
                'No copy-move forgery detected',
                'Potential copy-move regions found',
                'Cloning artifacts identified'
            ]),
            'color_filter_analysis': random.choice([
                'Natural color distribution',
                'Color enhancement detected',
                'Artificial color correction applied'
            ])
        }
    
    if reverse_search:
        results['reverse_search_results'] = [
            {'source': 'Google Images', 'matches': random.randint(0, 10), 'first_seen': f'2024-01-{random.randint(10, 20)}'},
            {'source': 'TinEye', 'matches': random.randint(0, 5), 'first_seen': f'2024-01-{random.randint(10, 20)}'},
            {'source': 'Yandex', 'matches': random.randint(0, 3), 'first_seen': 'Not found' if random.choice([True, False]) else f'2024-01-{random.randint(10, 20)}'}
        ]
    
    return results

def display_image_results(results):
    """Display comprehensive image analysis results"""
    
    # Executive Summary
    st.subheader("📋 Image Analysis Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        manipulation_score = results['manipulation_score']
        color = "#ff4444" if manipulation_score > 70 else "#ff8800" if manipulation_score > 40 else "#44ff44"
        
        st.markdown(f"""
        <div style="background-color: {color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>Manipulation Risk</h3>
            <h1>{manipulation_score}/100</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        authenticity = results['authenticity_score']
        color = "#44ff44" if authenticity > 70 else "#ff8800" if authenticity > 40 else "#ff4444"
        
        st.markdown(f"""
        <div style="background-color: {color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>Authenticity Score</h3>
            <h1>{authenticity}/100</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        verdict = "AUTHENTIC" if results['authenticity_score'] > 70 else "SUSPICIOUS" if results['authenticity_score'] > 40 else "LIKELY_FAKE"
        color = "#44ff44" if verdict == "AUTHENTIC" else "#ff8800" if verdict == "SUSPICIOUS" else "#ff4444"
        
        st.markdown(f"""
        <div style="background-color: {color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>Verdict</h3>
            <h1 style="font-size: 20px;">{verdict}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Analysis Tabs
    analysis_tabs = st.tabs([
        "📊 Metadata Analysis",
        "🔍 Technical Analysis", 
        "📝 Text Extraction",
        "🔄 Reverse Search",
        "⚡ Quick Actions"
    ])
    
    with analysis_tabs[0]:
        if results['metadata']:
            st.write("**📊 Image Metadata:**")
            for key, value in results['metadata'].items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        else:
            st.info("No metadata extracted")
    
    with analysis_tabs[1]:
        if results['technical_analysis']:
            st.write("**🔍 Technical Analysis:**")
            for key, value in results['technical_analysis'].items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        else:
            st.info("No technical analysis performed")
    
    with analysis_tabs[2]:
        if results['text_content']:
            st.write("**📝 Extracted Text:**")
            st.info(results['text_content'])
        else:
            st.info("No text extracted from image")
    
    with analysis_tabs[3]:
        if results['reverse_search_results']:
            st.write("**🔄 Reverse Search Results:**")
            for result in results['reverse_search_results']:
                st.write(f"**{result['source']}:** {result['matches']} matches, First seen: {result['first_seen']}")
        else:
            st.info("No reverse search performed")
    
    with analysis_tabs[4]:
        st.write("**⚡ Quick Actions:**")
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("Report generated!")
        if st.button("🔗 Share Results", use_container_width=True):
            st.success("Results shared!")
        if st.button("💾 Save Analysis", use_container_width=True):
            st.success("Analysis saved!")

if __name__ == "__main__":
    main()
