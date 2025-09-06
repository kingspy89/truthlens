# 🔐 TruthLens Admin Panel Access

## 🚀 How to Access Admin Panel

### **Secret URL Access:**
```
http://localhost:8501/?admin=true
```

### **Admin Credentials:**
- **Username:** `admin`
- **Password:** `truthlens2024`

## 🎯 Admin Panel Features

### **📊 Live Dashboard**
- Real-time system metrics
- Live activity monitoring
- Recent alerts and notifications
- 24-hour activity graphs

### **📋 User Reports Management**
- View all user reports
- Filter by status, priority, and date
- Action buttons for each report:
  - ✅ Resolve reports
  - 📧 Send to email
  - 🔍 View details
  - ❌ Reject reports

### **🤖 AI Responses Monitoring**
- Monitor all AI analyses
- View AI verdicts and confidence scores
- Track response times
- Email AI responses to admin

### **📧 Email Center**
- Email settings configuration
- Send test emails
- Email statistics
- Auto-email reports

### **⚙️ System Settings**
- Change admin password
- Configure system settings
- Auto-email preferences
- User limits

## 📧 Email Functionality

### **Automatic Email Reports:**
- All user reports are automatically formatted for email
- Beautiful HTML email templates
- Includes all report details and AI analysis
- Direct links to admin panel

### **Email Templates:**
- **Report Alerts:** Complete report details with AI analysis
- **AI Response Alerts:** AI analysis results and confidence scores
- **Test Emails:** System configuration verification

## 🔒 Security Features

### **Hidden Access:**
- No buttons or links to admin panel in main app
- Only accessible via secret URL parameter
- Secure authentication required
- Session-based access control

### **Admin Controls:**
- Change admin password
- Monitor all user activity
- Access to all reports and AI responses
- System configuration management

## 🎨 Admin Panel UI

### **Beautiful Design:**
- Gradient backgrounds and modern cards
- Real-time metrics and charts
- Interactive tables and forms
- Color-coded status indicators
- Responsive design

### **Live Updates:**
- Real-time data refresh
- Live activity monitoring
- Dynamic content updates
- Instant feedback on actions

## 📱 How to Use

1. **Start the app:** `streamlit run app.py`
2. **Access admin:** Go to `http://localhost:8501/?admin=true`
3. **Login:** Use credentials `admin` / `truthlens2024`
4. **Monitor:** View all user reports and AI responses
5. **Email:** Send reports to `malav0003@gmail.com`

## 🔧 Customization

### **Change Admin Credentials:**
Edit `pages/admin.py`:
```python
ADMIN_USERNAME = "your_username"
ADMIN_PASSWORD = "your_password"
```

### **Change Admin Email:**
Edit `pages/admin.py`:
```python
ADMIN_EMAIL = "your_email@gmail.com"
```

### **Email Configuration:**
Edit `utils/email_service.py` for SMTP settings:
```python
self.smtp_server = "smtp.gmail.com"
self.smtp_port = 587
```

## 🎉 Features Summary

✅ **Secret admin panel** - Hidden from regular users
✅ **Secure authentication** - Username/password protection
✅ **Live dashboard** - Real-time monitoring
✅ **User reports management** - View and manage all reports
✅ **AI responses monitoring** - Track AI analysis
✅ **Email functionality** - Send reports to admin email
✅ **Beautiful UI** - Modern, responsive design
✅ **Real-time updates** - Live data and metrics

## 🚀 Ready to Use!

Your admin panel is now fully functional and ready to monitor all TruthLens activity!
