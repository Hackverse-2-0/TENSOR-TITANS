# 🚀 PDS LEAK DETECTION PLATFORM - SETUP & INSTALLATION GUIDE

**For Judges & Evaluators**

---

## 📋 TABLE OF CONTENTS
1. [System Requirements](#system-requirements)
2. [Quick Start (5 Minutes)](#quick-start-5-minutes)
3. [Detailed Installation](#detailed-installation)
4. [Running the Application](#running-the-application)
5. [Testing the Features](#testing-the-features)
6. [Default Credentials](#default-credentials)
7. [Troubleshooting](#troubleshooting)
8. [Project Structure](#project-structure)

---

## 🖥️ SYSTEM REQUIREMENTS

### Minimum Requirements:
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **Python**: 3.9 or higher
- **RAM**: 2GB minimum
- **Disk Space**: 500MB
- **Network**: Local network access (localhost)

### Recommended:
- **Python**: 3.11+
- **RAM**: 4GB+
- **CPU**: Multi-core processor
- **Ports Available**: 5000 (backend), 8000 (frontend)

---

## ⚡ QUICK START (5 MINUTES)

### Step 1: Navigate to Project Directory
```bash
cd "c:\Users\USER\OneDrive\Desktop\pds leak detection"
```

### Step 2: Activate Virtual Environment
**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r backend/requirements_no_psycopg.txt
```

### Step 4: Start Backend Server (Open Terminal 1)
```bash
cd backend
python main.py
```
✅ **Wait for**: `Running on http://0.0.0.0:5000`

### Step 5: Start Frontend Server (Open Terminal 2)
```bash
cd frontend
python -m http.server 8000
```
✅ **Wait for**: `Serving HTTP on 0.0.0.0 port 8000`

### Step 6: Access the Platform
**Open in Browser:**
```
http://localhost:8000/login.html
```

✅ **DONE! Platform is LIVE!**

---

## 📦 DETAILED INSTALLATION

### Step 1: Clone/Download Project
```bash
# If downloaded as ZIP, extract it
# Otherwise, navigate to project directory
cd "pds leak detection"
```

### Step 2: Verify Python Installation
```bash
python --version
# Output should be 3.9 or higher
```

### Step 3: Create Virtual Environment (if not exists)
```bash
python -m venv .venv
```

### Step 4: Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Expected Output**: `(.venv)` prefix in terminal

### Step 5: Install Backend Dependencies
```bash
cd backend
pip install -r requirements_no_psycopg.txt
```

**This installs:**
- Flask 2.3.2 (Web framework)
- Flask-JWT-Extended 4.4.4 (Authentication)
- Flask-CORS 4.0.0 (API security)
- SQLAlchemy 2.0.19 (Database ORM)
- scikit-learn 1.3.0 (ML algorithms)
- XGBoost 2.0.0 (Advanced ML)
- pandas 2.0.3 (Data processing)
- numpy 1.24.3 (Numerical computing)

⏱️ **Installation Time**: 2-5 minutes (depends on internet speed)

### Step 6: Verify Installation
```bash
python -c "import flask; import sqlalchemy; print('✅ All dependencies installed successfully!')"
```

---

## 🎯 RUNNING THE APPLICATION

### Terminal 1 - Backend API Server
```bash
cd "c:\Users\USER\OneDrive\Desktop\pds leak detection\backend"
python main.py
```

**Expected Output:**
```
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Terminal 2 - Frontend Web Server
```bash
cd "c:\Users\USER\OneDrive\Desktop\pds leak detection\frontend"
python -m http.server 8000
```

**Expected Output:**
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

### Terminal 3 (Optional) - Monitoring
```bash
# Keep this open to monitor requests
# No command needed - just for reference
```

---

## 🌐 ACCESSING THE PLATFORM

### Login Page
```
http://localhost:8000/login.html
```

### Dashboard (After Login)
```
http://localhost:8000/dashboard.html
```

### API Documentation
```
http://localhost:5000/api/v1
```

### Health Check
```
http://localhost:5000/api/v1/health
```

---

## 🧪 TESTING THE FEATURES

### Step 1: Register a Test Account

1. **Open**: `http://localhost:8000/login.html`
2. **Click**: "Register" link
3. **Fill Form:**
   ```
   Username: testuser
   Email: test@example.com
   Password: TestPass123!
   Role: Admin (for full access)
   ```
4. **Click**: Submit
5. **See**: "Registration successful" message

### Step 2: Login
1. **Enter Credentials:**
   ```
   Email: test@example.com
   Password: TestPass123!
   ```
2. **Click**: Login
3. **See**: Dashboard with statistics

### Step 3: Test Data Ingestion
1. **Click**: "📤 Ingest Data" on dashboard
2. **Select**: "Stock Data" tab
3. **Fill:**
   - Shop: Select Shop #1 (or create one first)
   - Item: Rice
   - Quantity: 100
4. **Click**: Submit
5. **See**: Success notification

### Step 4: Test Anomaly Detection
1. **Click**: "🔍 View Anomalies"
2. **Ingest some mismatched data** to trigger anomalies
3. **See**: Anomalies listed with severity

### Step 5: Test Shop Management
1. **Click**: "🏪 Manage Shops"
2. **Click**: "+ Create New Shop"
3. **Fill:**
   - Shop Code: SHOP001
   - Shop Name: Test Fair Price Shop
   - Location: Test City
4. **Click**: Create
5. **See**: Shop added to list

### Step 6: Test Admin Panel
1. **Click**: "⚙️ Admin Panel"
2. **See**: User management interface
3. **Click**: "Users" tab
4. **See**: All registered users listed

### Step 7: Test Logout with Notification
1. **Click**: "← Back & Logout" button
2. **See**: Logout notification popup
3. **See**: Auto-redirect to login page after 2 seconds

### Step 8: Test Security (Try Back Button)
1. **Login again**
2. **Press**: Browser back button
3. **See**: Automatic logout with notification
4. **Result**: Redirect to login page (Cannot access cached dashboard)

### Step 9: Test Tab Switching
1. **Login to dashboard**
2. **Open new tab** with different website
3. **Come back to dashboard tab**
4. **See**: Automatic logout (security feature)

---

## 👤 DEFAULT CREDENTIALS

### Admin Account (Pre-created in database)
```
Email: admin@pds.gov.in
Password: Admin@123
Role: Admin
```

### Test Account (Create during first use)
```
Email: test@example.com
Password: TestPass123!
Role: Admin
```

### Test Shop Manager Account
```
Email: shopmanager@pds.gov.in
Password: ShopMgr@123
Role: Shop Manager
Shop ID: 1
```

---

## 🐛 TROUBLESHOOTING

### Issue 1: Port Already in Use

**Problem**: `Address already in use` error

**Solution**:
```bash
# Windows - Find and kill process using port
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Issue 2: Python Not Found

**Problem**: `python: command not found`

**Solution**:
```bash
# Check Python installation
python --version

# If not found, install Python 3.9+
# Or use full path
C:\Python311\python.exe main.py
```

### Issue 3: Virtual Environment Issues

**Problem**: Virtual environment won't activate

**Solution**:
```bash
# Delete old venv
rmdir /s /q .venv

# Create new one
python -m venv .venv

# Activate
.venv\Scripts\activate

# Reinstall dependencies
pip install -r backend/requirements_no_psycopg.txt
```

### Issue 4: Database Locked

**Problem**: `Database is locked` error

**Solution**:
```bash
# Delete the database file
cd backend
del pds_leak_detection.db

# Restart backend
python main.py
```

### Issue 5: Dependencies Won't Install

**Problem**: pip install fails

**Solution**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Clear pip cache
pip cache purge

# Try install again
pip install -r backend/requirements_no_psycopg.txt --no-cache-dir
```

### Issue 6: CORS Errors in Console

**Problem**: "Access-Control-Allow-Origin" errors

**Solution**:
- This is normal during development
- CORS is configured in backend
- Refresh page to retry

### Issue 7: Cannot Connect to Backend

**Problem**: 404 or connection refused errors

**Solution**:
1. Ensure backend is running on port 5000
2. Check terminal for error messages
3. Restart backend:
```bash
cd backend
python main.py
```
4. Wait 3-5 seconds for startup
5. Refresh frontend page

---

## 📁 PROJECT STRUCTURE

```
pds leak detection/
├── backend/                          # Flask API Server
│   ├── main.py                       # Application entry point
│   ├── config.py                     # Configuration settings
│   ├── models.py                     # Database models
│   ├── requirements_no_psycopg.txt   # Python dependencies
│   ├── pds_leak_detection.db         # SQLite database (auto-created)
│   ├── api/
│   │   ├── auth_routes.py            # Authentication endpoints
│   │   ├── auth.py                   # Auth service logic
│   │   ├── data_routes.py            # Data ingestion endpoints
│   │   ├── anomaly_routes.py         # Anomaly detection endpoints
│   │   ├── shop_routes.py            # Shop management endpoints
│   │   └── database_routes.py        # Data retrieval endpoints
│   ├── ml_models/
│   │   └── anomaly_detector.py       # ML algorithm implementation
│   └── pipelines/
│       └── data_pipeline.py          # Data processing pipeline
│
├── frontend/                         # Web Interface
│   ├── login.html                    # Login & registration
│   ├── dashboard.html                # Main dashboard
│   ├── anomalies.html                # Anomaly viewer
│   ├── data-ingestion.html           # Data input forms
│   ├── shops.html                    # Shop management
│   ├── admin.html                    # Admin panel
│   ├── data-viewer.html              # Database viewer
│   ├── js/
│   │   ├── api.js                    # API client
│   │   └── utils.js                  # Utility functions
│   └── css/
│       └── styles.css                # Styling
│
├── SETUP_INSTRUCTIONS.md             # This file
├── PLATFORM_LIVE.md                  # Features & endpoints
├── IMPLEMENTATION_COMPLETE.md        # Technical documentation
└── QUICK_TEST_GUIDE.md               # Quick testing guide
```

---

## ✅ VERIFICATION CHECKLIST

Before demonstrating to judges, verify:

- [ ] **Backend Running**: Terminal shows `Running on http://0.0.0.0:5000`
- [ ] **Frontend Running**: Terminal shows `Serving HTTP on 0.0.0.0 port 8000`
- [ ] **Can Open Login**: `http://localhost:8000/login.html` loads
- [ ] **Can Register**: New account creation works
- [ ] **Can Login**: Authentication successful with created account
- [ ] **Dashboard Loads**: Statistics and data appear
- [ ] **Can Ingest Data**: Data submission works and returns success
- [ ] **Can View Anomalies**: Anomalies page loads (may need test data first)
- [ ] **Can Create Shops**: New shop creation works
- [ ] **API Health**: `http://localhost:5000/api/v1/health` returns OK
- [ ] **Security Works**: Back button triggers logout
- [ ] **Logout Works**: "Back & Logout" shows notification

---

## 📊 PERFORMANCE NOTES

### Expected Response Times:
- **Login**: < 1 second
- **Dashboard Load**: < 2 seconds
- **Data Ingestion**: < 1.5 seconds
- **Anomaly Detection**: < 3 seconds
- **Shop Creation**: < 1 second

### Database Status:
- Created automatically on first run
- File: `backend/pds_leak_detection.db`
- Type: SQLite (no external server needed)
- Size: ~5-10 MB (grows with data)

---

## 🔧 ADVANCED CONFIGURATION

### Change Backend Port
Edit `backend/main.py` (last lines):
```python
app.run(
    host='0.0.0.0',
    port=5001,  # Change this number
    debug=True
)
```

### Change Frontend Port
```bash
cd frontend
python -m http.server 8001  # Different port
```

### Enable Debug Logging
Add to `backend/main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📞 SUPPORT INFO

### Common Issues Contact Info:
- **Database Issues**: Check `backend/pds_leak_detection.db` exists
- **Port Issues**: Verify no other apps on 5000/8000
- **Import Errors**: Reinstall requirements: `pip install -r backend/requirements_no_psycopg.txt`
- **Connection Issues**: Check both terminals are running

### Logs Location:
- **Backend**: Console output
- **Frontend**: Browser console (F12)
- **Database**: `backend/pds_leak_detection.db`

---

## 🎓 DEMO SCRIPT FOR JUDGES

### Recommended Demonstration Flow (10 minutes):

1. **Show Startup (1 min)**
   - Run both servers
   - Show they're running on ports 5000 & 8000

2. **Show Registration (1 min)**
   - Open login page
   - Register new test user
   - Show success message

3. **Show Login & Dashboard (1 min)**
   - Login with new credentials
   - Show dashboard with statistics

4. **Show Data Ingestion (2 min)**
   - Ingest sample stock data
   - Ingest biometric logs
   - Ingest delivery schedules
   - Show success notifications

5. **Show Anomaly Detection (2 min)**
   - Navigate to anomalies page
   - Show anomaly detection with severity levels
   - Explain AI model (Isolation Forest + XGBoost)

6. **Show Security Features (2 min)**
   - Press back button → Shows auto-logout
   - Show logout notification
   - Try to access cached dashboard → Fails (auto-logout)

7. **Show Admin Panel (1 min)**
   - Navigate to admin panel
   - Show user management

---

## 🎉 YOU'RE READY!

Your PDS Leak Detection Platform is now fully set up and ready for demonstration!

**Questions?** Refer to individual markdown files for detailed feature documentation.

**Ready to impress?** 🚀

