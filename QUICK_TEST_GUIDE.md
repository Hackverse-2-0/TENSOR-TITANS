# Quick Test & Deployment Guide

## 🚀 Quick Start

### Server Status
- **Backend**: http://localhost:5000 ✅
- **Frontend**: http://localhost:8000 ✅
- **Database**: SQLite (auto-created) ✅

---

## 👤 Testing Accounts

### Create Your First Account
1. Go to: **http://localhost:8000/register.html**
2. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
   - Role: `Admin` (for full access)
3. Click "Register"

### Login
1. Go to: **http://localhost:8000/login.html**
2. Enter credentials created above
3. Click "Login"
4. You'll be redirected to Dashboard

---

## 📋 Module Testing Checklist

### ✅ Module 1: Data Ingestion
**URL**: http://localhost:8000/data-ingestion.html

**Test Stock Data:**
1. Fill Shop ID: `1`
2. Add Stock Item:
   - Item Code: `RICE001`
   - Item Name: `Rice 10kg`
   - Qty Received: `100`
   - Qty Sold: `45`
   - Qty Remaining: `55`
   - Expected: `60`
3. Click "Submit Stock Data"
4. Verify: `✅ Success notification`

**Test Biometric Data:**
1. Fill Shop ID: `1`
2. Add Employee:
   - Employee ID: `EMP001`
   - Name: `John Doe`
   - Check-in: `2026-02-18 08:30`
   - Check-out: `2026-02-18 17:30`
   - Status: `Present`
3. Click "Submit Biometric Data"
4. Verify: `✅ Success notification`

**Test Delivery Data:**
1. Fill Shop ID: `1`
2. Add Delivery:
   - Delivery ID: `DEL001`
   - Item Code: `RICE001`
   - Item Name: `Rice 10kg`
   - Scheduled Qty: `100`
   - Delivered Qty: `100`
   - Status: `Delivered`
3. Click "Submit Delivery Data"
4. Verify: `✅ Success notification`

---

### ✅ Module 2: View Anomalies
**URL**: http://localhost:8000/anomalies.html

**Setup:**
1. First ingest some data using data-ingestion module
2. Note if anomalies appear (may need to intentionally create ones)

**Test Anomaly Viewing:**
1. Page should load with any existing anomalies
2. Apply Filters:
   - Severity: `High`
   - Type: `Stock Discrepancy`
   - Status: `Open`
3. Click "Apply Filters"
4. Verify: `✅ Filtered results shown`

**Test Anomaly Resolution:**
1. Click "View" on any anomaly
2. In modal, click "Mark as Resolved"
3. Select Status: `Resolved`
4. Add Notes: `Issue investigated`
5. Click "Submit Resolution"
6. Verify: `✅ Success notification`

**Test Run Detection:**
1. Click "⚡ Run Detection" button
2. Wait for processing
3. Verify: `✅ Detection completed`

---

### ✅ Module 3: Manage Shops
**URL**: http://localhost:8000/shops.html

**Create Shop:**
1. Fill Create New Shop form:
   - Shop Code: `SHOP002`
   - Shop Name: `North Distribution Center`
   - Location: `Delhi, ND`
   - Latitude: `28.6139` (optional)
   - Longitude: `77.2090` (optional)
2. Click "+ Create Shop"
3. Verify: `✅ Shop appears in list`

**Edit Shop:**
1. Click "Edit" on any shop
2. Change Shop Name: `North Delhi Distribution`
3. Click "Update Shop"
4. Verify: `✅ Name updated in list`

**View Shop Details:**
1. Click "View" on any shop
2. See shop details in modal
3. Close modal
4. Verify: `✅ Modal closes properly`

**Delete Shop:**
1. Click "Delete" on the shop you created
2. Confirm deletion
3. Verify: `✅ Shop removed from list`

**Search & Filter:**
1. Type in search box: `Shop`
2. Click "🔍 Search"
3. Verify: `✅ Results filtered`

**Sort:**
1. Select "Name (A-Z)" from sort dropdown
2. Click "🔍 Search"
3. Verify: `✅ Shops sorted by name`

---

### ✅ Module 4: Admin Panel
**URL**: http://localhost:8000/admin.html

**Requirements**: Must be logged in as Admin user

**Test User Management:**
1. Go to Admin Panel
2. Create User:
   - Username: `newanalyst`
   - Email: `analyst@example.com`
   - Password: `password123`
   - Role: `Analyst`
3. Click "+ Create User"
4. Verify: `✅ User appears in list`

**View Users:**
1. System displays all users
2. Filter by Role: `Shop Manager`
3. Click "🔍 Filter"
4. Verify: `✅ Only shop managers shown`

**Deactivate User:**
1. Click "Deactivate" on any active user
2. Verify: `✅ Status changed to Inactive`

**View System Settings:**
1. Click "⚙️ System Settings" tab
2. See:
   - Database Type: SQLite
   - API Version: v1
   - ML Models: Active (Isolation Forest, XGBoost)
3. Click "🔌 Test Backend Connection"
4. Verify: `✅ Backend connection confirmed`

**View Reports:**
1. Click "📊 Reports" tab
2. See statistics:
   - Total Users
   - Users by Role
   - Active Sessions
   - Total Anomalies
3. Verify: `✅ Numbers displayed`

---

## 🧪 Backend API Testing

### Test with cURL or Postman

**Health Check (No Auth Required):**
```bash
GET http://localhost:5000/api/v1/health
```
Expected: `{"status": "healthy", "version": "1.0.0"}`

**Register User:**
```bash
POST http://localhost:5000/api/v1/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "role": "admin"
}
```

**Login User:**
```bash
POST http://localhost:5000/api/v1/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```
Expected: `{"access_token": "...", "user": {...}}`

**Get Current User (Requires Token):**
```bash
GET http://localhost:5000/api/v1/auth/me
Authorization: Bearer {access_token}
```

**Create Shop:**
```bash
POST http://localhost:5000/api/v1/shops
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "shop_code": "SHOP003",
  "shop_name": "Test Shop",
  "location": "Test Location"
}
```

**List Shops:**
```bash
GET http://localhost:5000/api/v1/shops?limit=50
Authorization: Bearer {access_token}
```

**Ingest Stock Data:**
```bash
POST http://localhost:5000/api/v1/data/ingest/stock
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "shop_id": 1,
  "stocks": [
    {
      "item_code": "RICE001",
      "item_name": "Rice 10kg",
      "quantity_received": 100,
      "quantity_sold": 45,
      "quantity_remaining": 55,
      "expected_quantity": 60
    }
  ]
}
```

**Run Anomaly Detection:**
```bash
POST http://localhost:5000/api/v1/anomalies/detect/1
Authorization: Bearer {access_token}
```

**Get Anomalies:**
```bash
GET http://localhost:5000/api/v1/anomalies/1?limit=50
Authorization: Bearer {access_token}
```

**Resolve Anomaly:**
```bash
POST http://localhost:5000/api/v1/anomalies/{anomaly_id}/resolve
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "resolved",
  "resolution_notes": "Issue resolved"
}
```

---

## 🔄 Complete User Flow Test

### Scenario: Complete PDS Operations

**Step 1: Register & Login**
- Register as Admin user
- Login to platform
- Land on Dashboard

**Step 2: Create Infrastructure**
- Go to Shops page
- Create 3 test shops
- Verify shops in list

**Step 3: Ingest Data**
- Go to Data Ingestion
- Add stock for Shop 1
- Add biometric logs for Shop 1
- Add deliveries for Shop 1
- Repeat for other shops

**Step 4: Monitor Anomalies**
- Go to Anomalies page
- Run Detection
- Review detected anomalies
- Filter by severity/type
- Resolve a critical anomaly

**Step 5: Admin Operations**
- Go to Admin Panel
- Create new Analyst user
- View all users
- Check system settings
- Run backend test
- Review statistics

**Expected Result**: `✅ All operations successful`

---

## 📦 File Verification

Verify all files are in place:

```
frontend/
├── login.html                 ✅
├── register.html              ✅
├── dashboard.html             ✅
├── data-ingestion.html       ✅
├── anomalies.html            ✅
├── shops.html                ✅
├── admin.html                ✅
├── css/styles.css            ✅
└── js/
    ├── api.js                ✅
    └── utils.js              ✅

backend/
├── main.py                   ✅
├── config.py                 ✅
├── models.py                 ✅
├── requirements-dev.txt      ✅
├── api/
│   ├── auth.py               ✅
│   ├── auth_routes.py        ✅
│   ├── data_routes.py        ✅
│   ├── anomaly_routes.py     ✅
│   └── shop_routes.py        ✅ (with DELETE)
└── pipelines/
    └── data_pipeline.py      ✅
```

---

## 🐛 Troubleshooting

### Frontend Not Loading
```bash
# Start frontend server (if not running)
cd frontend
python -m http.server 8000
```

### Backend Not Responding
```bash
# Check if backend is running
python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/api/v1/health').status)"

# If not running, start it
cd backend
python main.py
```

### Database Issues
```bash
# Reset database
rm backend/pds_leak_detection.db
# Restart backend - database will be recreated
```

### Token Issues
```bash
# Clear browser cache/localStorage
# Re-login
# Token will be refreshed
```

---

## ✅ Deployment Readiness

- [x] Backend API fully functional
- [x] Frontend pages complete
- [x] All API endpoints tested
- [x] Database schema verified
- [x] Authentication working
- [x] ML models active
- [x] Error handling in place
- [x] Form validation working
- [x] UI responsive
- [x] Documentation complete

**Status**: 🟢 **READY FOR PRODUCTION**

---

## 📞 Support Information

If you encounter issues:
1. Check terminal output for error messages
2. Verify both servers are running
3. Clear browser cache if needed
4. Review API response in browser console
5. Check database connectivity
6. Ensure all Python packages are installed

---

**Last Updated**: February 18, 2026
**Platform Version**: 1.0.0 (Complete)
**Status**: ✅ Operational
