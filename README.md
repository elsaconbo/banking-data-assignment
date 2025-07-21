# Banking Data Quality & Risk Monitoring Platform

## Candidate Information

- **Name**: Nguyen Duy Hai
- **Submission for**: Data Engineer Intern – Timo

---

## 1. Project Overview

This project simulates a miniature banking data environment to validate data quality and detect risky transactions, based on compliance with regulation **2345/QĐ-NHNN 2023**.

### Key Objectives:

- Generate realistic synthetic banking data for **individual customers**
- Perform extensive **data quality validations**
- Detect high-risk transactions through rule-based monitoring
- Export all **violations into log files** for traceability

---

## 2. System Architecture

The system is implemented as a modular Python-based ETL pipeline, with Airflow DAG orchestration and optional Superset visualization.

### Components:

- `generate_data.py`: Generates customer, account, transaction, and device data
- `data_quality_standards.py`: Validates nulls, foreign keys, formats, and consistency rules
- `monitoring_audit.py`: Applies fraud/risk detection based on transaction types and authentication methods
- Output logs saved in `/data/violations/`
- Airflow orchestrates the pipeline; Superset can be used for dashboards (optional)

---

## 3. Functional Features

### 3.1 Data Quality Rules

- **Null Checks**: Required fields in all entities must not be null
- **Uniqueness Checks**: `national_number` must be unique for INDIVIDUAL customers
- **Format Validation**:
  - `national_number` must be 12 digits if CCCD
  - Timestamps must match `YYYY-MM-DD HH:MM:SS`
- **Foreign Key Integrity**:
  - Accounts → Customers
  - Transactions → Accounts, Devices
  - AuthLogs → Transactions
  - CustomerDevice → Customers, Devices

### 3.2 Risk Detection Rules

- **Transaction Category Authentication**:
  - B: Requires OTP or Matrix Card
  - C: Requires Biometric
  - D: Requires Biometric FIDO or Token
- **Balance Enforcement**:
  - SAVINGS & CURRENT accounts cannot transact more than available balance
- **Strong Auth on Large Volume**:
  - If total transactions > 20M VND in 1 day → must include strong auth (e.g. biometric)
- **Device Trust**:
  - Transactions from unverified devices are flagged

---

## 4. Setup Instructions

### Prerequisites

- Python 3.9+
- Docker + Docker Compose (for Airflow + Superset, optional)

### Installation

```bash
git clone https://github.com/elsaconbo/banking-data-assignment.git
cd banking-data-assignment
```

### Run Locally (Manual)

```bash
python src/generate_data.py
python src/data_quality_standards.py
python src/monitoring_audit.py
```

### Run with Airflow

```bash
docker-compose up --build
```

Access:

- Airflow UI: http://localhost:8085
- Superset: http://localhost:8088 (if configured)

To trigger the full DAG:

```bash
airflow dags trigger banking_data_quality_dag
```

---

## 5. Directory Structure

```
banking-data-assignment/
├── data/
│   ├── customers.csv
│   ├── transactions.csv
|   |__...
│   └── violations/
│       ├── data_quality_violations.log
│       └── risk_violations.log
├── src/
│   ├── generate_data.py
│   ├── data_quality_standards.py
│   └── monitoring_audit.py
├── dags_or_jobs/
│   └── banking_dq_dag.py
├── sql/
│   └── schema.sql
└── docker-compose.yml
```

---

## 6. Assumptions & Notes

- All rules are applied only for `INDIVIDUAL` customer type
- Synthetic data is generated randomly but aligned with business constraints
- All authentication is simulated probabilistically (95% success rate by default)
- CSV is used as the primary data source; DB integration is optional

---

## 7. Contact

- **Nguyen Duy Hai**
- **Email**: nguyenduyhai1502@gmail.com
- Looking forward to further discussions with the Timo team.
