# PDS Leak Detection Platform - Getting Started

## Platform is Now Live! 🚀

Your PDS Leak Detection Platform is running on your local machine with both backend and frontend servers active.

### Access Points

- **Frontend (Web Interface)**: http://localhost:8000
- **Backend API**: http://localhost:5000/api/v1
- **Health Check**: http://localhost:5000/api/v1/health

### Available Pages

1. **Login Page** - http://localhost:8000/login.html
2. **Register Page** - http://localhost:8000/register.html
3. **Dashboard** - http://localhost:8000/dashboard.html (requires login)

### Getting Started

1. **Create an Account**
   - Go to http://localhost:8000/register.html
   - Fill in the registration form with:
     - Name
     - Email
     - Password (minimum 6 characters)
     - Role (choose from ADMIN, SHOP_MANAGER, DISTRIBUTION_CENTER, ANALYST)
     - Shop ID (optional, required for SHOP_MANAGER role)
   - Click "Register"

2. **Login**
   - Navigate to http://localhost:8000/login.html
   - Enter your email and password
   - You should be redirected to the dashboard

3. **Access Dashboard**
   - View statistics on anomalies, shops, and data records
   - Access quick actions to:
     - Ingest Data
     - View Anomalies
     - Manage Shops
     - Access Admin Panel

### API Endpoints

All API endpoints are prefixed with `/api/v1`

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/current` - Get current user
- `PUT /auth/users/{user_id}` - Update user profile
- `DELETE /auth/users/{user_id}` - Delete user (admin only)

#### Data Ingestion
- `POST /data/ingest/stock` - Ingest stock data
- `POST /data/ingest/biometric` - Ingest biometric logs
- `POST /data/ingest/delivery` - Ingest delivery schedules

#### Anomaly Detection
- `POST /anomalies/detect` - Trigger anomaly detection
- `GET /anomalies/{shop_id}` - Get anomalies for a shop
- `GET /anomalies/stats/{shop_id}` - Get anomaly statistics
- `PUT /anomalies/{anomaly_id}/resolve` - Resolve an anomaly

#### Shops
- `GET /shops` - List all shops
- `POST /shops` - Create new shop
- `GET /shops/{shop_id}` - Get shop details
- `PUT /shops/{shop_id}` - Update shop
- `DELETE /shops/{shop_id}` - Delete shop

### Database

The platform uses **SQLite** for development, with the database file stored at:
```
backend/pds_leak_detection.db
```

The following tables are automatically created:
- users
- shops
- stock
- biometric_logs
- delivery_schedules
- anomaly_detections
- audit_logs

### System Features

#### Machine Learning Models
- **Isolation Forest**: Anomaly detection for stock discrepancies
- **XGBoost**: Advanced anomaly scoring and prediction

#### Role-Based Access Control
- **ADMIN**: Full system access
- **SHOP_MANAGER**: Manage their assigned shop's data
- **DISTRIBUTION_CENTER**: Monitor distribution center operations
- **ANALYST**: View-only access to analytics and reports

#### Data Pipelines
1. **Stock Pipeline**: Ingest shop inventory data
2. **Biometric Pipeline**: Track staff attendance via biometric logs
3. **Delivery Pipeline**: Monitor delivery schedules and completion

### Troubleshooting

1. **Cannot connect to backend**
   - Ensure Flask server is running on http://localhost:5000
   - Check that port 5000 is not blocked by firewall

2. **Cannot access frontend**
   - Ensure HTTP server is running on http://localhost:8000
   - Check that port 8000 is not blocked by firewall

3. **Database errors**
   - The SQLite database is automatically created on first run
   - Database file: `backend/pds_leak_detection.db`

4. **Import errors in Flask**
   - Verify all packages are installed: `pip install -r requirements-dev.txt`
   - Ensure you're using the configured Python environment

### Next Steps

1. Register a test user
2. Login to the platform
3. Explore the dashboard
4. Try the data ingestion features
5. Monitor anomaly detection results

### Server Status

Both servers are configured to auto-restart and reload on file changes during development.

- Flask Debug Mode: **ENABLED** (Debugger PIN shown in terminal)
- Frontend Server: **Python HTTP Server on Port 8000**
- Database: **SQLite (Development)**

---

**Built with**:
- Python Flask 2.3.2
- SQLAlchemy ORM
- Scikit-learn & XGBoost ML
- Flask-JWT for authentication
- Vanilla JavaScript frontend

**Status**: ✅ Platform Live and Operational
