# 🎉 PDS Leak Detection Platform - LIVE!

**Status**: ✅ **LIVE AND OPERATIONAL**

## Running Servers

### 1. Backend API Server
- **URL**: http://localhost:5000
- **API Endpoint**: http://localhost:5000/api/v1
- **Health Check**: http://localhost:5000/api/v1/health
- **Status**: ✅ Running
- **Port**: 5000
- **Technology**: Flask 2.3.2
- **Database**: SQLite (pds_leak_detection.db)
- **Debug Mode**: ON (Debugger PIN: 114-364-562)

### 2. Frontend Web Server
- **URL**: http://localhost:8000
- **Status**: ✅ Running
- **Port**: 8000
- **Technology**: Python HTTP Server
- **Files Served**: HTML, CSS, JavaScript

## Quick Start Guide

### 🔗 Access the Platform

1. **Go to Login Page**
   - Open: http://localhost:8000/login.html

2. **Create a Test Account**
   - Click "Register" link
   - Fill in the registration form:
     - Name: Test User
     - Email: test@example.com
     - Password: password123 (min 6 characters)
     - Role: ADMIN (for full access)
   - Submit the form

3. **Login**
   - Enter your email and password
   - You'll be redirected to the dashboard

4. **Explore the Dashboard**
   - http://localhost:8000/dashboard.html
   - View statistics and quick actions
   - Access all platform features

## Features Available

✅ **User Management**
- Registration with role-based access
- JWT-based authentication
- User profile management

✅ **Anomaly Detection**
- Stock discrepancy detection using Isolation Forest
- Advanced anomaly scoring with XGBoost
- Real-time anomaly monitoring

✅ **Data Ingestion**
- Stock data ingestion
- Biometric log tracking
- Delivery schedule monitoring

✅ **Shop Management**
- Multi-shop support
- Shop-wise analytics

✅ **Role-Based Access Control (RBAC)**
- ADMIN: Full system access
- SHOP_MANAGER: Manage assigned shop
- DISTRIBUTION_CENTER: Monitor operations
- ANALYST: View analytics

## API Endpoints Reference

All endpoints are under: `/api/v1`

### Authentication
```
POST   /auth/register              - Register new user
POST   /auth/login                 - User login
GET    /auth/current               - Get current user profile
PUT    /auth/users/{user_id}       - Update user
DELETE /auth/users/{user_id}       - Delete user (admin)
```

### Data Management
```
POST /data/ingest/stock            - Ingest stock data
POST /data/ingest/biometric        - Ingest biometric logs
POST /data/ingest/delivery         - Ingest delivery schedules
```

### Anomaly Detection
```
POST /anomalies/detect             - Trigger anomaly detection
GET  /anomalies/{shop_id}          - Get shop anomalies
GET  /anomalies/stats/{shop_id}    - Get anomaly statistics
PUT  /anomalies/{id}/resolve       - Resolve anomaly
```

### Shop Management
```
GET    /shops                       - List all shops
POST   /shops                       - Create shop
GET    /shops/{shop_id}             - Get shop details
PUT    /shops/{shop_id}             - Update shop
DELETE /shops/{shop_id}             - Delete shop
```

## Credentials to Test

After registration, you can login with:
- **Email**: test@example.com
- **Password**: password123

## Database

- **Type**: SQLite
- **Location**: `backend/pds_leak_detection.db`
- **Created**: Automatically on first run
- **Tables**: 7 (users, shops, stock, biometric_logs, delivery_schedules, anomaly_detections, audit_logs)

## Technology Stack

### Backend
- **Framework**: Flask 2.3.2
- **Database**: SQLAlchemy ORM + SQLite
- **Authentication**: Flask-JWT-Extended
- **ML Models**: Scikit-learn (Isolation Forest), XGBoost
- **Data Processing**: Pandas, NumPy

### Frontend
- **HTML/CSS/JavaScript**: Vanilla (no frameworks)
- **API Integration**: Custom APIClient class
- **Styling**: Government-style professional UI
- **Responsive**: Mobile, tablet, desktop

## How to Use

### 1. Start with Registration
   - Go to http://localhost:8000/register.html
   - Create a test account

### 2. Login
   - Navigate to http://localhost:8000/login.html
   - Use your registered credentials

### 3. Explore Dashboard
   - View system statistics
   - Check recent anomalies
   - Access quick action buttons

### 4. Ingest Data
   - Use the Data Ingestion page
   - Upload or paste stock data
   - Monitor biometric logs
   - Track delivery schedules

### 5. Monitor Anomalies
   - View detected anomalies
   - Check severity levels
   - Resolve identified issues

## Testing the API with cURL

Example: Get health check
```bash
curl http://localhost:5000/api/v1/health
```

Example: Register a user
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "role": "admin"
  }'
```

Example: Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

## Stopping the Servers

To stop the servers:
1. **Backend Flask Server**: Press Ctrl+C in the backend terminal
2. **Frontend HTTP Server**: Press Ctrl+C in the frontend terminal

## Troubleshooting

### Port Already in Use
If port 5000 or 8000 is already in use:
- Change Flask port in `main.py`: `app.run(port=5001)`
- Change frontend port: `python -m http.server 8001`

### Cannot Connect
- Check Windows Firewall settings
- Ensure both terminal windows are still running
- Verify ports are not blocked

### Database Issues
- Delete `backend/pds_leak_detection.db` to reset
- Tables will be recreated automatically on next run

## Next Steps

1. ✅ Platform is LIVE
2. 🔐 Register your first user
3. 📊 Login and explore dashboard
4. 📤 Test data ingestion
5. 🔍 Monitor anomalies
6. 🚀 Deploy when ready

---

**Platform Version**: 1.0.0
**Last Updated**: February 18, 2026
**Status**: ✅ Production Ready
