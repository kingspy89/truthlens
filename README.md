# 🔍 TruthLens - AI-Powered Misinformation Detection System

**Version:** 2.0.0  
**Platform:** Streamlit Web Application  
**Purpose:** Forensic-level misinformation detection and fact-checking system

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation & Setup](#installation--setup)
4. [Project Structure](#project-structure)
5. [File Documentation](#file-documentation)
6. [API Services](#api-services)
7. [User Interfaces](#user-interfaces)
8. [Configuration](#configuration)
9. [Usage Guide](#usage-guide)
10. [Development](#development)

---

## 🎯 Project Overview

TruthLens is an advanced AI-powered misinformation detection system designed for both public users and authority personnel. It combines multiple AI services, news aggregation, and forensic analysis techniques to identify and combat misinformation in real-time.

### Key Capabilities:
- **Text Analysis**: Deep forensic analysis of text content for misinformation patterns
- **Image Analysis**: Detection of manipulated or fake images
- **News Verification**: Real-time news aggregation and verification
- **Authority Dashboard**: Specialized interface for law enforcement and authorities
- **Analytics Center**: Comprehensive data analysis and trend monitoring
- **Educational Hub**: Digital literacy training and resources

---

## ✨ Features

### 🔍 Core Analysis Features
- **Forensic Text Analysis**: AI-powered content analysis with manipulation tactic detection
- **Image Authenticity Detection**: Advanced image manipulation detection
- **Real-time News Verification**: Live news aggregation and fact-checking
- **Source Traceability**: Origin tracking and source credibility assessment
- **Threat Level Assessment**: Risk scoring and threat classification

### 👮 Authority Features
- **Live Dashboard**: Real-time monitoring of misinformation threats
- **Alert System**: Automated threat detection and notification
- **Investigation Tools**: Advanced forensic analysis tools
- **Report Generation**: Comprehensive analysis reports
- **User Activity Monitoring**: Track and analyze user behavior

### 📊 Analytics & Intelligence
- **Trend Analysis**: Misinformation pattern identification
- **Source Intelligence**: Deep dive into content sources
- **Performance Metrics**: System performance monitoring
- **User Behavior Analysis**: Usage pattern insights

### 🎓 Educational Features
- **Learning Modules**: Interactive digital literacy training
- **Case Studies**: Real-world misinformation examples
- **Interactive Quizzes**: Knowledge testing and validation
- **Resource Library**: Comprehensive educational materials

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Internet connection for API services

### Quick Start

1. **Clone/Download the project**
   ```bash
   # Navigate to project directory
   cd TruthLens_Old_Streamlit_Backup
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Access the Application**
   - Open your browser to `http://localhost:8501`
   - For admin access: `http://localhost:8501?admin=true`

### Environment Variables (Optional)
Create a `.env` file for custom API keys:
```env
GEMINI_API_KEY=your_gemini_api_key
NEWSAPI_KEY=your_newsapi_key
FIREBASE_API_KEY=your_firebase_key
```

---

## 📁 Project Structure

```
TruthLens_Old_Streamlit_Backup/
├── app.py                          # Main application entry point
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── README.md                       # This documentation
├── ADMIN_ACCESS.md                 # Admin access documentation
├── cleanup_old_files.bat          # Cleanup utility script
│
├── pages/                          # User interface modules
│   ├── __init__.py
│   ├── admin.py                    # Admin interface
│   ├── analytics.py                # Analytics dashboard
│   ├── authority.py                # Authority control center
│   └── education.py                # Educational resources
│
├── utils/                          # Core service modules
│   ├── __init__.py
│   ├── ai_services.py              # AI and ML services
│   ├── database.py                 # Database operations
│   ├── news_services.py            # News aggregation
│   ├── security.py                 # Security and authentication
│   ├── email_service.py            # Email notifications
│   └── google_cloud_services.py    # Google Cloud integration
│
├── assets/                         # Static assets
│   └── styles.css                  # Custom CSS styles
│
└── __pycache__/                    # Python cache files
```

---

## 📄 File Documentation

### Core Application Files

#### `app.py` (1,360 lines)
**Main application entry point and orchestrator**

**Key Functions:**
- `main()`: Primary application controller
- `load_custom_css()`: UI styling management
- `check_authentication()`: User authentication system
- `text_analyzer_interface()`: Text analysis UI
- `image_analysis_interface()`: Image analysis UI
- `news_center_interface()`: News verification UI
- `display_api_status()`: API connectivity monitoring
- `load_demo_data()`: Demo data population

**Features:**
- Multi-interface routing system
- Real-time API status monitoring
- Demo data loading functionality
- Responsive UI with custom styling
- Authentication and authorization

#### `config.py` (50 lines)
**Centralized configuration management**

**Key Classes:**
- `Config`: Main configuration class
- `setup_page_config()`: Streamlit page configuration

**Configuration Areas:**
- API keys (Gemini, NewsAPI, Firebase)
- Google Cloud settings
- Application metadata
- Environment variable management

### Service Modules (`utils/`)

#### `ai_services.py` (274 lines)
**AI and machine learning services**

**Key Classes:**
- `GeminiService`: Google Gemini AI integration
- `FactCheckService`: Google Fact Check Tools API

**GeminiService Methods:**
- `forensic_analysis()`: Deep content analysis with manipulation detection
- `trace_origin()`: Content origin tracing
- `analyze_context()`: Missing context analysis
- `extract_sources_and_reporting()`: Source extraction and reporting info
- `test_connection()`: API connectivity testing

**FactCheckService Methods:**
- `search_claims()`: Fact-checked claims search
- `test_connection()`: API connectivity testing

#### `database.py` (216 lines)
**Database operations and data management**

**Key Class:**
- `FirebaseService`: Firebase database simulation

**Key Methods:**
- `save_analysis()`: Save text analysis results
- `save_image_analysis()`: Save image analysis results
- `get_statistics()`: Retrieve system statistics
- `get_recent_analyses()`: Get recent analysis history
- `get_trending_threats()`: Get trending threat topics
- `get_analytics_data()`: Get analytics data for charts
- `populate_demo_data()`: Load demo data

#### `news_services.py` (152 lines)
**News aggregation and verification**

**Key Class:**
- `NewsAggregator`: News API integration

**Key Methods:**
- `get_breaking_news()`: Fetch breaking news headlines
- `search_news()`: Search for specific news topics
- `verify_article()`: Article verification
- `get_trending_topics()`: Extract trending topics
- `test_connection()`: API connectivity testing

#### `security.py` (306 lines)
**Security and authentication services**

**Key Class:**
- `SecurityService`: Security management

**Key Methods:**
- `verify_authority_credentials()`: Authority user authentication
- `get_authority_info()`: Get user information
- `analyze_content_safety()`: Content safety analysis
- `detect_manipulation_tactics()`: Manipulation tactic detection
- `generate_security_report()`: Security report generation
- `check_content_flags()`: Content flag checking

### User Interface Modules (`pages/`)

#### `authority.py` (646 lines)
**Authority control center and monitoring dashboard**

**Key Functions:**
- `authority_interface()`: Main authority dashboard
- `live_dashboard()`: Real-time monitoring
- `alert_system()`: Threat alert management
- `analytics_center()`: Authority analytics
- `investigation_tools()`: Forensic investigation tools
- `reports_logs()`: Report generation and logging

**Features:**
- Real-time threat monitoring
- Advanced investigation tools
- Comprehensive reporting system
- User activity tracking
- Alert management system

#### `analytics.py` (472 lines)
**Advanced analytics and data visualization**

**Key Functions:**
- `analytics_interface()`: Main analytics dashboard
- `trend_analysis()`: Misinformation trend analysis
- `content_analytics()`: Content analysis metrics
- `source_intelligence()`: Source analysis and intelligence
- `user_behavior_analysis()`: User behavior insights
- `performance_metrics()`: System performance monitoring

**Features:**
- Interactive data visualizations
- Trend forecasting
- Source credibility analysis
- User behavior tracking
- Performance metrics dashboard

#### `education.py` (660 lines)
**Educational resources and training modules**

**Key Functions:**
- `educational_interface()`: Main education hub
- `learning_modules()`: Interactive learning modules
- `interactive_quiz()`: Knowledge testing system
- `case_studies()`: Real-world case studies
- `training_center()`: Professional training
- `educational_resources()`: Resource library

**Features:**
- Multi-level learning paths
- Interactive quizzes and assessments
- Real-world case studies
- Professional training modules
- Comprehensive resource library

---

## 🔌 API Services

### Google Gemini AI
- **Purpose**: Advanced content analysis and misinformation detection
- **Models Used**: gemini-1.5-pro, gemini-1.5-flash
- **Features**: Forensic analysis, origin tracing, context analysis

### Google Fact Check Tools
- **Purpose**: Fact-checked claims verification
- **Features**: Claims search, publisher verification, verdict checking

### NewsAPI
- **Purpose**: Real-time news aggregation
- **Features**: Breaking news, news search, article verification

### Firebase (Simulated)
- **Purpose**: Data storage and analytics
- **Features**: Analysis storage, statistics tracking, user management

---

## 🎨 User Interfaces

### 1. 🔍 Text Analyzer
- **Purpose**: Analyze text content for misinformation
- **Features**: 
  - Forensic-level content analysis
  - Manipulation tactic detection
  - Source credibility assessment
  - Risk scoring and threat classification

### 2. 🖼️ Image Analysis
- **Purpose**: Detect manipulated or fake images
- **Features**:
  - Image authenticity verification
  - Manipulation detection
  - Metadata analysis
  - Visual forensics

### 3. 📰 News Center
- **Purpose**: Real-time news verification and aggregation
- **Features**:
  - Breaking news headlines
  - News search and filtering
  - Article verification
  - Source credibility checking

### 4. 👮 Authority Dashboard
- **Purpose**: Specialized interface for authorities and law enforcement
- **Features**:
  - Real-time threat monitoring
  - Advanced investigation tools
  - Alert management system
  - Comprehensive reporting

### 5. 📊 Analytics
- **Purpose**: Data analysis and trend monitoring
- **Features**:
  - Trend analysis and forecasting
  - Content analytics
  - Source intelligence
  - User behavior analysis

### 6. 🎓 Education
- **Purpose**: Digital literacy training and education
- **Features**:
  - Interactive learning modules
  - Case studies and examples
  - Knowledge testing
  - Resource library

---

## ⚙️ Configuration

### API Keys Required
- **Gemini API Key**: For AI content analysis
- **NewsAPI Key**: For news aggregation
- **Firebase Keys**: For data storage (optional)

### Environment Variables
```env
GEMINI_API_KEY=your_gemini_key
NEWSAPI_KEY=your_newsapi_key
FIREBASE_API_KEY=your_firebase_key
FIREBASE_AUTH_DOMAIN=your_domain
FIREBASE_PROJECT_ID=your_project_id
```

---

## 📖 Usage Guide

### For Public Users
1. **Launch the application**: `streamlit run app.py`
2. **Select Text Analyzer**: Analyze suspicious text content
3. **Use Image Analysis**: Check images for manipulation
4. **Browse News Center**: Verify news articles
5. **Access Education**: Learn about misinformation

### For Authority Personnel
1. **Access Authority Dashboard**: Select from sidebar
2. **Enter credentials**: Use provided authority credentials
3. **Monitor threats**: Use live dashboard for real-time monitoring
4. **Investigate cases**: Use investigation tools for deep analysis
5. **Generate reports**: Create comprehensive analysis reports

### For Administrators
1. **Access admin panel**: Navigate to `?admin=true`
2. **Manage system**: Configure settings and monitor performance
3. **View analytics**: Access comprehensive system analytics
4. **Manage users**: Handle user accounts and permissions

---

## 🛠️ Development

### Adding New Features
1. **Create new page**: Add to `pages/` directory
2. **Add service**: Create in `utils/` directory
3. **Update routing**: Modify `app.py` main function
4. **Add configuration**: Update `config.py` if needed

### Testing
- **API Testing**: Use built-in connection tests
- **Demo Data**: Load demo data for testing
- **Error Handling**: Comprehensive error handling throughout

### Dependencies
- **Core**: Streamlit, Pandas, NumPy
- **AI/ML**: Google Generative AI, Transformers, PyTorch
- **Data**: Plotly, Matplotlib, Seaborn
- **APIs**: Requests, HTTPX, BeautifulSoup
- **Cloud**: Google Cloud services, Firebase
- **Security**: Cryptography, BCrypt

---

## 🚨 Important Notes

### Security Considerations
- **API Keys**: Store securely, never commit to version control
- **Authority Access**: Use strong credentials for authority accounts
- **Data Privacy**: Ensure compliance with data protection regulations

### Performance
- **API Limits**: Be aware of API rate limits
- **Caching**: Implement caching for better performance
- **Error Handling**: Robust error handling for production use

### Scalability
- **Database**: Consider real Firebase implementation for production
- **Caching**: Implement Redis or similar for caching
- **Load Balancing**: Use multiple instances for high traffic

---

## 📞 Support & Contact

For technical support, feature requests, or bug reports:
- **GitHub Issues**: Create an issue in the repository
- **Documentation**: Refer to this README and code comments
- **API Documentation**: Check individual service documentation

---

## 📄 License

This project is developed for educational and research purposes. Please ensure compliance with all applicable laws and regulations when using this system.

---

**TruthLens v2.0.0** - Advanced AI-Powered Misinformation Detection System
