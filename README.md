# Banking Data Quality and Risk Detection Platform

**Candidate**: Nguyen Duy Hai  
**Submission for**: Case Study Assignment - Data Engineer Intern at Timo

---

## 1. Project Overview

This project simulates a secure banking data pipeline that:

- Generates synthetic data for banking operations: customers, devices, accounts, transactions, authentication logs.
- Performs data quality validation.
- Detects potential violations based on compliance rules from Decision **2345/QĐ-NHNN (2023)**.
- Logs violations and prepares insights for downstream analysis.

---

## 2. System Architecture

- **Data Generation**: `generate_data.py`
- **Data Quality Validation**: `data_quality_standards.py`
- **Risk & Compliance Monitoring**: `monitoring_audit.py`
- **Workflow Orchestration**: Apache Airflow DAG (`banking_dq_dag.py`)
- **Visualization (Optional)**: Superset dashboard
- **Logs Output**: Stored in `logs/` and `data/violations/`

---

## 3. Risk Detection Rules (Based on 2345/QĐ-NHNN)

The following rules are enforced only for `INDIVIDUAL` customer type:

| Transaction Type | Minimum Required Authentication Methods |
|------------------|-------------------------------------------|
| **A** (< 5M)     | PASSWORD or any higher-level method       |
| **B** (5M - 20M) | OTP_SMS, OTP_EMAIL, MATRIX_CARD, SOFT_OTP_BASIC, SOFT_OTP_ADV, FIDO, BIOMETRIC |
| **C** (> 20M - 1.5B) | BIOMETRIC_CCCD, BIOMETRIC_EID, BIOMETRIC_DB, SOFT_OTP_ADV, TWO_FACTOR |
| **D** (> 1.5B)   | BIOMETRIC_* combined with SOFT_OTP_ADV / FIDO / SIGNATURE |

Additional checks:

- ✅ High-value daily transactions (> 20M VND) must include at least one **strong authentication method** (e.g., biometric, soft/hard token).
- ✅ All transactions must originate from a **trusted & verified device**.
- ✅ Transactions must not exceed account balances.

---

## 4. Data Quality Checks

- ✅ Null and missing value validation
- ✅ Uniqueness constraints (e.g., customer_id, transaction_id)
- ✅ CCCD must have exactly 12 digits (no letters/symbols)
- ✅ Foreign key integrity between tables (e.g., transaction → account → customer)

---

## 5. Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for manual execution if needed)

### Step 1: Clone the repository
```bash
git clone https://github.com/elsaconbo/banking-data-assignment.git
cd banking-data-assignment
```

### Step 2: Start Docker Compose
```bash
docker-compose up --build
```

### Access Tools
- Airflow: [http://localhost:8085](http://localhost:8085)
- Superset (optional): [http://localhost:8088](http://localhost:8088)

---

## 6. How to Run in Airflow

Main DAG: `banking_data_quality_dag`

Sequential Tasks:
1. `generate_data`: generate sample data for testing
2. `data_quality_check`: validate quality rules
3. `risk_based_check`: detect rule violations

Trigger the DAG:
```bash
airflow dags trigger banking_data_quality_dag
```

---

## 7. Repository Structure
```
banking-data-assignment/
├── sql/
│   └── schema.sql
├── src/
│   ├── generate_data.py
│   ├── data_quality_standards.py
│   └── monitoring_audit.py
├── dags_or_jobs/
│   └── banking_dq_dag.py
├── data/
│   ├── *.csv
│   └── violations/
├── logs/
├── docker-compose.yml
└── README.md
```

---

## 8. Assumptions & Notes

- All compliance logic is scoped for `INDIVIDUAL` customer types only.
- Synthetic data respects constraints from Decision 2345/QĐ-NHNN.
- Valid authentication methods are carefully mapped to transaction categories.
- Higher-level auth methods (e.g., category D) can be used for lower-level transactions (e.g., A/B).
- CSV files serve as the core data medium; relational database is optional.

---

## 9. Contact
Nguyen Duy Hai  
📧 Email: nguyenduyhai1502@gmail.com  
Looking forward to your feedback in the interview process.
