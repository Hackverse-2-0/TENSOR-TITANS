# PDS Leak Detection Platform

A comprehensive platform for detecting and preventing stock leaks in Public Distribution Systems using ML-based anomaly detection.

## Features

- **Data Ingestion Pipelines**: Ingest shop-wise stock data, biometric logs, and delivery schedules
- **Anomaly Detection**: Uses Isolation Forest and ML algorithms to detect:
  - Stock discrepancies
  - Suspicious attendance patterns
  - Delivery delays and anomalies
- **Role-Based Access Control**: ADMIN, SHOP_MANAGER, DISTRIBUTION_CENTER, ANALYST
- **Audit Logging**: Complete audit trail of all user actions
- **REST API**: Complete REST API for all operations

## Tech Stack

- **Python 3.8+**
- **Flask**: Web framework
- **SQLAlchemy**: ORM
- **Scikit-learn**: Isolation Forest for anomaly detection
- **XGBoost**: Advanced ML for anomaly scoring
- **Pandas & NumPy**: Data processing
- **JWT**: Authentication & authorization
- **PostgreSQL/SQLite**: Database

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd pds-leak-detection
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
export FLASK_ENV=development
export JWT_SECRET_KEY=your-secret-key-here
# For production with PostgreSQL:
# export DATABASE_URL=postgresql://user:password@localhost/pds_leak_detection
```

5. **Run the application**
```bash
python main.py
```

The server will start on `http://localhost:5000`

## API Documentation

### Authentication

#### Register User
```
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "shop_manager",
  "shop_id": 1
}
```

**Roles**: `admin`, `shop_manager`, `distribution_center`, `analyst`

#### Login
```
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword"
}

Response:
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

#### Get Current User
```
GET /api/v1/auth/me
Authorization: Bearer {access_token}
```

### Shops

#### Create Shop (ADMIN only)
```
POST /api/v1/shops
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "shop_code": "SHOP001",
  "shop_name": "Central Distribution Shop",
  "location": "Mumbai, MH",
  "latitude": 19.0760,
  "longitude": 72.8777
}
```

#### List Shops
```
GET /api/v1/shops?limit=50&offset=0
Authorization: Bearer {access_token}
```

#### Get Shop Details
```
GET /api/v1/shops/{shop_id}
Authorization: Bearer {access_token}
```

#### Get Shop Statistics
```
GET /api/v1/shops/{shop_id}/stats
Authorization: Bearer {access_token}
```

### Data Ingestion

#### Ingest Stock Data
```
POST /api/v1/data/ingest/stock
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

#### Ingest Biometric Logs
```
POST /api/v1/data/ingest/biometric
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "shop_id": 1,
  "biometric_logs": [
    {
      "employee_id": "EMP001",
      "employee_name": "John Doe",
      "check_in_time": "2026-02-17T08:30:00",
      "check_out_time": "2026-02-17T16:30:00",
      "status": "present"
    }
  ]
}
```

#### Ingest Delivery Schedules
```
POST /api/v1/data/ingest/delivery
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "shop_id": 1,
  "deliveries": [
    {
      "delivery_id": "DEL001",
      "item_code": "RICE001",
      "item_name": "Rice 10kg",
      "scheduled_quantity": 100,
      "scheduled_date": "2026-02-17T09:00:00",
      "delivered_quantity": 100,
      "actual_delivery_date": "2026-02-17T09:30:00",
      "status": "delivered"
    }
  ]
}
```

### Anomaly Detection

#### Run Anomaly Detection
```
POST /api/v1/anomalies/detect/{shop_id}
Authorization: Bearer {access_token}

Response:
{
  "success": true,
  "shop_id": 1,
  "total_anomalies": 3,
  "stock_discrepancies": [...],
  "suspicious_attendance": [...],
  "delivery_anomalies": [...]
}
```

#### Get Anomalies
```
GET /api/v1/anomalies/{shop_id}?severity=high&status=open&limit=50
Authorization: Bearer {access_token}
```

Query parameters:
- `severity`: low, medium, high, critical
- `anomaly_type`: stock_discrepancy, suspicious_activity, delivery_delay
- `status`: open, investigating, resolved
- `limit`: Number of records (max 500)
- `offset`: Pagination offset

#### Resolve Anomaly
```
POST /api/v1/anomalies/{anomaly_id}/resolve
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "resolved",
  "resolution_notes": "Issue investigated and cleared"
}
```

#### Get Anomaly Statistics
```
GET /api/v1/anomalies/stats/{shop_id}
Authorization: Bearer {access_token}

Response:
{
  "success": true,
  "total_anomalies": 5,
  "severity_distribution": {
    "critical": 1,
    "high": 2,
    "medium": 1,
    "low": 1
  },
  "anomaly_type_distribution": {...},
  "status_distribution": {...}
}
```

## Access Control

### Role Permissions

| Role | Stock Ingestion | Biometric Ingestion | Delivery Ingestion | Anomaly Detection | View Anomalies | Resolve Anomalies |
|------|---|---|---|---|---|---|
| Admin | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Shop Manager | ✗ | ✓ | ✗ | ✓* | ✓* | ✗ |
| Distribution Center | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ |
| Analyst | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |

*Shop Managers can only access their own shop's data

## Anomaly Detection Methods

### 1. Stock Discrepancy Detection
- Uses **Isolation Forest** algorithm
- Detects discrepancies between expected and actual stock
- Calculates discrepancy ratio and severity

### 2. Suspicious Attendance Detection
- Analyzes biometric patterns
- Detects unusual working hours/durations
- Identifies anomalous check-in patterns

### 3. Delivery Anomaly Detection
- Tracks delivery delays and quantity variances
- Uses Isolation Forest for pattern analysis
- Identifies late or incorrect deliveries

## Database Schema

### Key Tables

- **users**: User accounts with roles
- **shops**: Distribution shop information
- **stocks**: Shop stock records
- **biometric_logs**: Employee attendance logs
- **delivery_schedules**: Delivery tracking
- **anomaly_detections**: Detected anomalies with scoring
- **audit_logs**: Complete audit trail

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python main.py
```

### Running Tests
```bash
pytest tests/
```

### Database Migrations
```bash
# If using Alembic:
flask db upgrade
```

## Production Deployment

1. **Use PostgreSQL instead of SQLite**
2. **Set strong JWT_SECRET_KEY**
3. **Use gunicorn/uwsgi for WSGI server**
4. **Enable HTTPS/SSL**
5. **Set FLASK_ENV=production**
6. **Configure proper logging**

Example production run:
```bash
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:password@host/pds_leak_detection
gunicorn -w 4 -b 0.0.0.0:5000 'main:create_app()'
```

## Monitoring & Logging

- All API requests and user actions are logged
- Audit trail maintained in `audit_logs` table
- Anomaly scores and evidence stored for investigation
- Health check endpoint: `GET /api/v1/health`

## Performance Tuning

- Isolation Forest contamination: 0.1 (adjust based on baseline anomaly rate)
- Stock data lookback: 100 records (configurable)
- Biometric data lookback: 200 records (configurable)
- Database indexes on frequently queried columns recommended

## Troubleshooting

### Database Connection Issues
- Check DATABASE_URL environment variable
- Verify PostgreSQL service is running
- Check user permissions

### JWT Token Issues
- Verify JWT_SECRET_KEY is set
- Check token expiration (24 hours default)
- Ensure Authorization header format: `Bearer {token}`

### Anomaly Detection Not Running
- Verify sufficient data in database
- Check minimum record requirements (10+ stock, 20+ biometric)
- Review logs for error messages

## Support & Contributing

For issues or contributions, please contact the development team.

## License

Proprietary - Government of India PDS Project
