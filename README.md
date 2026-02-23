# 🚀 Tensor Titans – PDS Leak Detection Platform

## 🏆 Team Name
**Tensor Titans**

---

# 📌 Project Title
## Public Distribution System (PDS) Leak Detection & Monitoring Platform

---

# 📖 Project Overview

The **PDS Leak Detection Platform** is an AI-powered monitoring system designed to detect irregularities, ghost beneficiaries, and diversion of food grains in the Public Distribution System.

The system uses data analytics and machine learning techniques to identify suspicious distribution patterns at fair price shops and beneficiary levels, ensuring transparency and reducing fraud.

This repository contains:
- Source code
- ML pipeline
- System architecture
- Documentation
- Prototype implementation

---

# 🎯 Problem Statement

Public Distribution Systems often face:

- Ghost beneficiaries  
- Diversion of grains  
- Data manipulation  
- Manual record tampering  
- Lack of transparency  

This project aims to build a **data-driven intelligent monitoring system** that detects anomalies automatically and improves accountability.

---

# 🎯 Objectives

- Analyze distribution data to detect suspicious patterns  
- Design scalable system architecture  
- Build ML-based anomaly detection model  
- Provide dashboard-based visualization  
- Generate automated alerts for high-risk entities  

---

# 🏗️ System Architecture

The system follows a modular layered architecture:

1. **Data Layer**
   - Beneficiary data
   - Shop distribution logs
   - Inventory records

2. **Processing Layer**
   - Data cleaning
   - Feature engineering
   - Anomaly detection model

3. **Application Layer**
   - REST APIs
   - Business logic

4. **Presentation Layer**
   - Admin dashboard
   - Risk reports & alerts

---

# 📊 Workflow Flowchart

```
        Raw PDS Data Input
                 │
                 ▼
     Data Cleaning & Preprocessing
                 │
                 ▼
        Feature Engineering
                 │
                 ▼
      ML-Based Anomaly Detection
                 │
                 ▼
         Risk Scoring System
                 │
                 ▼
        Dashboard & Alerts
```

---

# ⚙️ Working Model Details

### Step 1: Data Collection
- Shop-wise monthly distribution data  
- Beneficiary transaction logs  
- Inventory movement records  

### Step 2: Data Preprocessing
- Remove duplicates  
- Handle missing values  
- Normalize quantities  

### Step 3: Feature Engineering
- Distribution deviation score  
- Sudden spike detection  
- Inactive beneficiary tracking  

### Step 4: Machine Learning
- Isolation Forest / Random Forest  
- Outlier detection  
- Risk scoring (0–100 scale)  

### Step 5: Dashboard & Reporting
- Flag high-risk shops  
- Generate automated fraud reports  
- Visual risk indicators  

---

# 🛠️ Tech Stack

| Layer         |         Technology Used              |
|---------------|--------------------------------------|
| Frontend      | React.js                             |
| Backend       | Node.js / Express                    |
| ML Model      | Python (Scikit-learn, Pandas, NumPy) |
| Database      | PostgreSQL                           |
| Visualization | Chart.js                             |
| Deployment    | Docker                               |

---

# 📂 Project Structure

```
pds-leak-detection/
│
├── frontend/
├── backend/
├── ml-model/
├── database/
├── docs/
├── docker/
├── README.md
```

---

# 🚀 Installation & Setup

## Clone Repository

```bash
git clone https://github.com/your-username/pds-leak-detection.git
cd pds-leak-detection
```

## Backend Setup

```bash
cd backend
npm install
npm start
```

## ML Setup

```bash
cd ml-model
pip install -r requirements.txt
python train.py
```

## Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

# 📈 Results & Outputs

- 85–92% anomaly detection accuracy (synthetic dataset)
- Automated risk scoring
- Real-time monitoring dashboard
- Reduced manual auditing workload

---

# 🔮 Future Scope

- Aadhaar-based authentication integration  
- Real-time IoT stock tracking  
- Government API integration  
- Mobile app for field officers  
- Blockchain-based supply chain transparency  

---

# 👨‍💻 Team Members

| S.No | Name             | Role                      |           Responsibilities                     |
|------|------------------|-------------------------  |---------------------------------------------   |
| 1    | Subham Gadatia   | Team Lead & Backend Dev   | System architecture, backend APIs, integration |
| 2    | Rabi Narayan     | ML Engineer               | Model development, training, evaluation        |
| 3    | Asutosh          | Frontend Developer        | Dashboard UI, visualization, user interface    |
| 4    | Ayush            | Database & DevOps         | Database design, deployment, Docker setup      |

---

# 📞 Contact

For queries or collaboration:

- 📧 Email: subhamgadatia2006@gmail.com
- 🌐 GitHub: https://github.com/subhamgadatia2006-afk 

---

⭐ Developed with innovation and integrity by **Tensor Titans**
