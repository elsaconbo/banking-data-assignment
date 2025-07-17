# Banking Data Quality and Risk Detection Platform

**Candidate**: Nguyen Duy Hai &#x20;
**Submission for**: Case Study Assignment - Data Engineer Intern at Timo

---

## Project Overview

This project simulates a mock banking transaction system that automatically:

* Generates synthetic banking data: customers, accounts, devices, transactions, and auth\_logs
* Performs data quality checks
* Detects risky or fraudulent transactions based on business rules
* Exports violation logs and displays results via dashboard (Superset)

The entire workflow is orchestrated using a DAG in Apache Airflow.

---

## System Architecture

* Data generation: `generate_data.py`
* Data quality checks: `data_quality_standards.py`
* Risk detection: `monitoring_audit.py`
* Logs stored as CSV files in `/logs`
* Superset dashboard for visualization

---

## Features Implemented

### Risk Detection Rules

* Transactions >= 10 million VND without OTP/biometric authentication
* Transactions from devices that are unverified or untrusted
* Customer transacts > 20 million VND in a day without any strong authentication

### Data Quality Checks

* Null checks, uniqueness checks
* Format validation: CCCD must be exactly 12 digits
* Foreign key checks between related tables

---

## Setup Instructions

### Prerequisites

* Docker & Docker Compose
* Python 3.9+ (for manual execution if needed)

### Step 1: Clone the repository

```bash
git clone https://github.com/elsaconbo/banking-data-assignment.git
cd banking-data-assignment
```

### Step 2: Start Docker

```bash
docker-compose up --build
```

Access:

* Airflow: [http://localhost:8085](http://localhost:8085)
* Superset: [http://localhost:8088](http://localhost:8088)

---

## Running the DAG in Airflow

Main DAG: `banking_data_quality_dag`

It contains 3 sequential tasks:

1. `generate_data`: generates transaction data
2. `data_quality_check`: performs data quality validations
3. `risk_based_check`: detects transaction risks

Trigger DAG:

```bash
airflow dags trigger banking_data_quality_dag
```

---

## Superset Dashboard

Superset access: [http://localhost:8088](http://localhost:8088)

The dashboard displays:

* Number of risky transactions
* Number of data quality issues by category
* Count of unverified devices by customer

(can filter by time periods)
![superset](https://github.com/user-attachments/assets/f37c5a21-69e9-4b53-838f-c0335694c31d)

---

## Repository Structure

```
banking-data-assignment/
├── sql/
│   ├── schema.sql
├── src/
│   ├── generate_data.py
│   ├── data_quality_standards.py
│   └── monitoring_audit.py
├── dags_or_jobs/
│   └── banking_dq_dag.py
├── data/         
├── logs/         
├── visualization/
├── docker-compose.yml
└── README.md
```

---

## Assumptions

* CCCD must be exactly 12 numeric digits
* Each transaction has exactly one associated auth log
* CSV files are the primary data source
* MySQL is optional for visualization, not required

---

## Contact

Nguyen Duy Hai &#x20;
Email: \[nguyenduyhai1502@gmail.com] &#x20;
Looking forward to receiving feedback from Timo during the interview.
