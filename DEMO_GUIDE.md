# 🎯 FEATURE DEMONSTRATION GUIDE FOR JUDGES

**Complete walkthrough of all platform features with expected outcomes**

---

## 📋 TABLE OF CONTENTS

1. [Authentication Features](#1-authentication-features)
2. [Dashboard & Statistics](#2-dashboard--statistics)
3. [Data Ingestion](#3-data-ingestion)
4. [Anomaly Detection](#4-anomaly-detection)
5. [Shop Management](#5-shop-management)
6. [Admin Panel](#6-admin-panel)
7. [Security Features](#7-security-features)
8. [Data Viewer](#8-data-viewer)

---

## 1️⃣ AUTHENTICATION FEATURES

### Feature 1.1: User Registration

**What to Test:**
1. Open `http://localhost:8000/login.html`
2. Click **"Register"** link
3. Fill in the form:
   - Username: `judge_user_123`
   - Email: `judge@example.com`
   - Password: `JudgePass@123`
   - Role: **Admin** (for full access)
4. Click **"Register"**

**Expected Outcome:**
- ✅ Success notification appears
- ✅ Form clears
- ✅ Automatically redirects to login after 2 seconds
- ✅ User data persists in database

**What It Demonstrates:**
- Input validation
- Database persistence
- User role assignment
- Client-side feedback

---

### Feature 1.2: User Login

**What to Test:**
1. After registration, enter credentials:
   - Email: `judge@example.com`
   - Password: `JudgePass@123`
2. Click **"Login Securely"**

**Expected Outcome:**
- ✅ "Authenticating..." loading state
- ✅ Redirects to dashboard.html
- ✅ Hello message shows username
- ✅ All menu items available (for Admin role)

**Security Demonstrated:**
- ✅ JWT token generation
- ✅ Secure password handling
- ✅ Session initialization
- ✅ Role-based menu display

---

### Feature 1.3: Rate Limiting & Account Lockout

**What to Test:**
1. Click Login form and clear password field
2. Try 5 times with wrong password
3. On 6th attempt, observe lockout

**Expected Outcome:**
- ✅ After 5 failed attempts: Message "Too many login attempts"
- ✅ Account locked for 15 minutes
- ✅ Counter shows "4 attempts remaining" (decreasing)
- ✅ Login button disabled during lockout

**Security Demonstrated:**
- ✅ Brute force attack prevention
- ✅ Progressive lockout mechanism
- ✅ Automatic unlock after timeout
- ✅ User feedback on attempts

---

## 2️⃣ DASHBOARD & STATISTICS

### Feature 2.1: Real-time Dashboard

**What to Test:**
1. Login successfully
2. Observe dashboard.html page

**Expected Outcome:**
- ✅ Statistics cards show:
  - Total Shops
  - Active Anomalies
  - Critical Alerts
  - Data Records
- ✅ Numbers are **live-updating** (refreshes every 30 seconds)
- ✅ Recent anomalies table shows latest detections
- ✅ System status shows API, Database, and Load status

**What It Demonstrates:**
- ✅ Real-time data aggregation
- ✅ Multi-source data integration
- ✅ Responsive UI with live updates
- ✅ Administrator overview capability

---

### Feature 2.2: Quick Actions Menu

**What to Test:**
1. On dashboard, see the "Quick Actions" section
2. Observe all action buttons:
   - 📤 Ingest Data
   - 🔍 View Anomalies
   - 🏪 Manage Shops
   - ⚙️ Admin Panel

**Expected Outcome:**
- ✅ All buttons are clickable
- ✅ Each navigates to correct page
- ✅ Seamless navigation between features

**What It Demonstrates:**
- ✅ User-friendly interface
- ✅ Easy feature discovery
- ✅ Navigation hierarchy

---

## 3️⃣ DATA INGESTION

### Feature 3.1: Stock Data Ingestion

**What to Test:**
1. Click **"📤 Ingest Data"** from dashboard
2. On Stock Data tab, fill:
   - Shop: Select a shop (or create one first under Shops menu)
   - Item Name: `Rice`
   - Quantity Received: `1000`
   - Quantity Sold: `800`
   - Quantity Remaining: `200`
   - Expected Quantity: `200`
3. Click **"Add Item"** to add more items (optional)
4. Click **"Submit"**

**Expected Outcome:**
- ✅ Green success notification
- ✅ Form clears
- ✅ Message: "Stock data ingested successfully"
- ✅ Data persists in database

**What It Demonstrates:**
- ✅ Dynamic form handling
- ✅ Multi-item batch processing
- ✅ Real-time validation
- ✅ Data persistence
- ✅ User feedback system

**Backend Processing:**
- Stores in `stocks` table
- Validates quantity logic
- Creates audit trail

---

### Feature 3.2: Biometric Log Ingestion

**What to Test:**
1. Stay on data-ingestion.html
2. Click **"Biometric Logs"** tab
3. Fill:
   - Shop: Select same shop
   - Employee Name: `John Doe`
   - Check-in Time: `08:00 AM`
   - Check-out Time: `05:00 PM`
   - Status: `Present`
4. Click **"Add Employee"** for more (optional)
5. Click **"Submit"**

**Expected Outcome:**
- ✅ Success notification
- ✅ Data stored in database
- ✅ Form resets for next entry

**What It Demonstrates:**
- ✅ Employee tracking capability
- ✅ Attendance automation
- ✅ Multi-employee batch processing
- ✅ Time validation

**Use Case:**
- Prevents ghost employees (fake attendance)
- Tracks labor costs
- Detects suspicious patterns

---

### Feature 3.3: Delivery Schedule Ingestion

**What to Test:**
1. Click **"Delivery Schedules"** tab
2. Fill:
   - Shop: Select shop
   - Item: `Rice`
   - Scheduled Delivery: `50 units`
   - Actual Delivery: `48 units`
   - Delivery Date: (today)
   - Status: `Delivered`
3. Click **"Submit"**

**Expected Outcome:**
- ✅ Success notification
- ✅ Discrepancies automatically detected
- ✅ Can view in Anomalies page

**What It Demonstrates:**
- ✅ Delivery tracking
- ✅ Scheduled vs. Actual comparison
- ✅ Automatic anomaly trigger (if mismatch)
- ✅ Supply chain monitoring

---

## 4️⃣ ANOMALY DETECTION

### Feature 4.1: View Anomalies

**What to Test:**
1. Click **"🔍 View Anomalies"** from dashboard
2. Observe anomalies list

**Expected Outcome:**
- ✅ Table shows anomalies with:
  - Shop ID
  - Anomaly Type (Stock Discrepancy, Delivery Delay, etc.)
  - Severity (Critical, High, Medium, Low)
  - Score (0-100)
  - Detection Date
  - Current Status (Open, Resolved, Under Investigation)
- ✅ Color-coded severity badges
- ✅ Most recent at top

**What It Demonstrates:**
- ✅ ML model in action (Isolation Forest + XGBoost)
- ✅ Real-time anomaly scoring
- ✅ Severity classification
- ✅ Timestamp tracking

---

### Feature 4.2: Filter Anomalies

**What to Test:**
1. On anomalies page, use filters:
   - **Severity Filter**: Select "Critical"
   - **Status Filter**: Select "Open"
   - **Type Filter**: Select "Stock Discrepancy"
   - **Time Range**: Last 7 days
2. Click **"Apply Filters"**

**Expected Outcome:**
- ✅ Table updates to show only matching anomalies
- ✅ Count decreases based on filters
- ✅ Reset button clears all filters
- ✅ Instant filtering (no page reload)

**What It Demonstrates:**
- ✅ Advanced filtering capability
- ✅ Real-time data manipulation
- ✅ User control over data view
- ✅ Quick search/analysis

---

### Feature 4.3: Resolve Anomalies

**What to Test:**
1. On anomalies page, click **"Resolve"** on any anomaly
2. Fill resolution form:
   - Status: `Resolved`
   - Notes: `Investigated and corrected the stock discrepancy`
3. Click **"Submit"**

**Expected Outcome:**
- ✅ Status changes to "Resolved"
- ✅ Anomaly moves to resolved section
- ✅ Details show resolution notes
- ✅ Timestamp records when resolved

**What It Demonstrates:**
- ✅ Complete anomaly lifecycle management
- ✅ Audit trail for compliance
- ✅ Problem tracking and closure
- ✅ Investigation documentation

---

## 5️⃣ SHOP MANAGEMENT

### Feature 5.1: Create New Shop

**What to Test:**
1. Click **"🏪 Manage Shops"** from dashboard
2. Click **"+ Create New Shop"** button
3. Fill form:
   - Shop Code: `SHOP_JUDGE_001`
   - Shop Name: `Judge's Fair Price Shop`
   - Location: `Test City`
   - Latitude: `28.6139` (Delhi example)
   - Longitude: `77.2090`
4. Click **"Create Shop"**

**Expected Outcome:**
- ✅ Success notification
- ✅ New shop appears in shops list
- ✅ Can view shop details immediately
- ✅ Can assign to users

**What It Demonstrates:**
- ✅ Multi-shop network support
- ✅ Geographic tracking capability
- ✅ Shop hierarchy management
- ✅ Dynamic data entry

---

### Feature 5.2: Edit Shop Details

**What to Test:**
1. Click on any shop in the list
2. Click **"Edit Shop"** button
3. Modify:
   - Shop Name: Add " - Test"
   - Location: Add " (Primary)"
4. Click **"Update"**

**Expected Outcome:**
- ✅ Success confirmation
- ✅ Details update in real-time
- ✅ Audit log records change

**What It Demonstrates:**
- ✅ Shop maintenance capability
- ✅ Data modification control
- ✅ Change tracking for compliance

---

### Feature 5.3: View Shop Statistics

**What to Test:**
1. Click on any shop
2. Observe statistics section showing:
   - Total Stock Items
   - Active Anomalies
   - Average Discrepancy
   - Recent Deliveries
   - Employee Count

**Expected Outcome:**
- ✅ Real-time statistics
- ✅ Aggregated data from ingested records
- ✅ Performance metrics

**What It Demonstrates:**
- ✅ Shop-level analytics
- ✅ Performance monitoring
- ✅ Multi-dimensional insights

---

## 6️⃣ ADMIN PANEL

### Feature 6.1: User Management

**What to Test:**
1. Click **"⚙️ Admin Panel"** from dashboard
2. Click **"Users"** tab
3. Observe:
   - All registered users listed
   - User details (Username, Email, Role, Status)
   - Action buttons (Edit, Deactivate, Delete)

**Expected Outcome:**
- ✅ All users displayed
- ✅ Role labels visible
- ✅ Status indicators
- ✅ Action buttons functional

**What It Demonstrates:**
- ✅ User administration capability
- ✅ Role oversight
- ✅ Access control management

---

### Feature 6.2: System Status

**What to Test:**
1. On Admin Panel, click **"System Status"** tab
2. Observe:
   - API Server Status (Online)
   - Database Connection (Connected)
   - Total Users Count
   - Total Shops Count
   - Data Records Count
   - Last Backup Time

**Expected Outcome:**
- ✅ All systems show green (Online/Connected)
- ✅ Counters reflect actual data
- ✅ Real-time monitoring dashboard

**What It Demonstrates:**
- ✅ System health monitoring
- ✅ Administrative oversight
- ✅ Data volume tracking

---

## 7️⃣ SECURITY FEATURES

### Feature 7.1: Session Timeout

**What to Test:**
1. Login and stay idle for 30+ minutes (or set timer)
2. Try to interact with page after timeout

**Expected Outcome:**
- ✅ Automatic logout triggered
- ✅ Logout notification appears
- ✅ Redirects to login page
- ✅ Session data cleared

**What It Demonstrates:**
- ✅ Session security
- ✅ Idle timeout protection
- ✅ Automatic cleanup

---

### Feature 7.2: Back Button Protection

**What to Test:**
1. Login to dashboard
2. Press **browser back button** (← in browser)

**Expected Outcome:**
- ✅ **Automatic logout triggered**
- ✅ Logout notification appears
- ✅ Redirects to login page
- ✅ Cannot access cached dashboard
- ✅ Session completely cleared

**What It Demonstrates:**
- ✅ Advanced security mechanism
- ✅ Cache protection
- ✅ Unauthorized access prevention

---

### Feature 7.3: Tab Switching Security

**What to Test:**
1. Login to dashboard
2. Open a different website in another tab
3. Switch tabs multiple times
4. Switch **back to dashboard tab**

**Expected Outcome:**
- ✅ **Automatic logout on tab return**
- ✅ Logout notification appears
- ✅ Must login again
- ✅ Session invalidated

**What It Demonstrates:**
- ✅ Multi-tab security
- ✅ Session hijacking prevention
- ✅ Browser switching detection

---

### Feature 7.4: Logout Notification

**What to Test:**
1. Click **"← Back & Logout"** button on dashboard
2. Observe notification

**Expected Outcome:**
- ✅ Elegant popup notification appears
- ✅ Shows: "Logged Out Successfully"
- ✅ Personalized message: "Goodbye, [Username]!"
- ✅ Wave emoji animation (👋)
- ✅ Auto-redirects after 2 seconds
- ✅ All data cleared

**What It Demonstrates:**
- ✅ Professional UX design
- ✅ User feedback system
- ✅ Graceful logout handling
- ✅ Session management

---

### Feature 7.5: HTTPS Headers (Backend)

**What to Test:**
1. Open browser Dev Tools (F12)
2. Go to Network tab
3. Send any request to backend
4. Click on response, view Headers

**Expected Outcome:**
See security headers:
- `Cache-Control: no-cache, no-store, must-revalidate`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `X-Frame-Options: DENY`
- `Content-Security-Policy: default-src 'self'...`

**What It Demonstrates:**
- ✅ Enterprise-grade security headers
- ✅ OWASP compliance
- ✅ XSS prevention
- ✅ Clickjacking prevention
- ✅ MIME sniffing prevention

---

## 8️⃣ DATA VIEWER

### Feature 8.1: View Ingested Stock Data

**What to Test:**
1. Click **"Data Viewer"** from dashboard
2. Click **"Stocks"** tab
3. Observe all ingested stock records

**Expected Outcome:**
- ✅ Table shows all stocks with:
  - Shop ID
  - Item Name
  - Quantity Received
  - Quantity Sold
  - Remaining
  - Expected
  - Discrepancy (calculated)
  - Ingestion Date
- ✅ Pagination works (10 items per page)
- ✅ Can export data

**What It Demonstrates:**
- ✅ Data persistence
- ✅ Historical tracking
- ✅ Report generation capability

---

### Feature 8.2: View Biometric Logs

**What to Test:**
1. On Data Viewer, click **"Biometric Logs"** tab
2. Observe employee attendance records

**Expected Outcome:**
- ✅ Table shows:
  - Shop ID
  - Employee Name
  - Check-in Time
  - Check-out Time
  - Status (Present, Absent, Late, Leave)
  - Duration (calculated)
  - Date
- ✅ Can sort by columns
- ✅ Pagination works

**What It Demonstrates:**
- ✅ Attendance tracking
- ✅ Labor management
- ✅ Data aggregation

---

### Feature 8.3: View Delivery Records

**What to Test:**
1. On Data Viewer, click **"Deliveries"** tab
2. Observe delivery history

**Expected Outcome:**
- ✅ Table shows:
  - Shop ID
  - Item Name
  - Scheduled Quantity
  - Actual Quantity
  - Difference (calculated)
  - Status
  - Delivery Date
- ✅ Can identify delays/shortages
- ✅ Historical comparison

**What It Demonstrates:**
- ✅ Supply chain tracking
- ✅ Performance analysis
- ✅ Trend identification

---

### Feature 8.4: Export Data

**What to Test:**
1. On any Data Viewer tab
2. Click **"Export"** button

**Expected Outcome:**
- ✅ CSV file downloads
- ✅ Contains all visible data
- ✅ Opens in Excel/Sheets
- ✅ Properly formatted

**What It Demonstrates:**
- ✅ Data interoperability
- ✅ Report generation
- ✅ External integration support

---

## 🎬 COMPLETE DEMO FLOW (10 minutes)

### Recommended sequence for judges:

```
⏱️ 0:00 - Start: Show login page
⏱️ 0:30 - Register new test user
⏱️ 1:30 - Login with new credentials
⏱️ 2:00 - Show Dashboard with live statistics
⏱️ 2:30 - Ingest sample data (stock + biometric)
⏱️ 4:00 - Show Anomaly Detection results
⏱️ 5:00 - Create new shop in Shop Management
⏱️ 6:00 - Show Admin Panel & System Status
⏱️ 7:00 - Demonstrate Security:
        - Press back button → Auto-logout
        - Show logout notification
⏱️ 8:00 - Show Data Viewer with ingested data
⏱️ 9:00 - Export report as CSV
⏱️ 10:00 - Summary & Q&A
```

---

## ✅ EVALUATION CHECKLIST

### Judges can verify:
- [ ] Registration works
- [ ] Login with authentication works
- [ ] Dashboard shows real-time data
- [ ] Data ingestion accepts all three types
- [ ] Anomaly detection identifies patterns
- [ ] Shop management allows CRUD operations
- [ ] Admin panel shows system status
- [ ] Back button triggers logout
- [ ] Tab switching causes logout
- [ ] Logout notification appears
- [ ] Security headers present
- [ ] Data persists after refresh
- [ ] Role-based access control works
- [ ] Rate limiting prevents brute force
- [ ] Export functionality works

---

## 🎯 KEY TALKING POINTS

1. **Real-Time Anomaly Detection**: AI-powered (Isolation Forest + XGBoost)
2. **Comprehensive Security**: Enterprise-grade authentication & session management
3. **Multi-Shop Support**: Scalable across thousands of distribution centers
4. **Complete Data Pipeline**: Automated ingestion & processing
5. **Admin Oversight**: Dashboard for monitoring entire network
6. **Data Persistence**: SQLite database with audit trails
7. **User Experience**: Government-compliant design
8. **Production Ready**: Deployable on any OS with Python

