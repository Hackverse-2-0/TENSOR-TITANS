# 🚀 QUICK REFERENCE - 5 MINUTE SETUP

## **FASTEST WAY TO GET RUNNING:**

### Copy & Paste These Commands:

```bash
# 1. Navigate to project
cd "c:\Users\USER\OneDrive\Desktop\pds leak detection"

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Install dependencies (if not done)
pip install -r backend/requirements_no_psycopg.txt

# 4. Terminal 1: Start Backend
cd backend
python main.py

# 5. Terminal 2: Start Frontend (NEW TERMINAL)
cd frontend
python -m http.server 8000

# 6. Open Browser
# http://localhost:8000/login.html
```

---

## **WHAT YOU'LL SEE:**

✅ **Terminal 1 Output:**
```
 * Running on http://0.0.0.0:5000
```

✅ **Terminal 2 Output:**
```
Serving HTTP on 0.0.0.0 port 8000
```

✅ **Browser**: Login page with government styling

---

## **QUICK TEST FLOW:**

1. **Register**: Click "Register" → Fill form → Submit
2. **Login**: Use registered credentials
3. **Dashboard**: See statistics and options
4. **Data**: Click "📤 Ingest Data" → Add sample data
5. **Anomalies**: Click "🔍 View Anomalies" → See detected anomalies
6. **Security**: Click "← Back & Logout" → See logout notification
7. **Back Button**: Press browser back → Auto-logout (security!)

---

## **URLS TO ACCESS:**

| Page | URL |
|------|-----|
| Login | `http://localhost:8000/login.html` |
| Dashboard | `http://localhost:8000/dashboard.html` |
| Anomalies | `http://localhost:8000/anomalies.html` |
| Data Ingestion | `http://localhost:8000/data-ingestion.html` |
| Shops | `http://localhost:8000/shops.html` |
| Admin | `http://localhost:8000/admin.html` |
| API Health | `http://localhost:5000/api/v1/health` |

---

## **PORT ISSUES?**

```bash
# Windows: Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux: 
lsof -i :5000
kill -9 <PID>
```

---

## **DEMO WITH DEFAULT ACCOUNT:**

```
Email: admin@pds.gov.in
Password: Admin@123
Role: Admin
```

---

**NOTES:**
- ✅ Both terminals must keep running
- ✅ Database auto-creates on first run
- ✅ No external database needed
- ✅ Data persists in `backend/pds_leak_detection.db`
- ✅ Close both terminals to stop (Ctrl+C)

