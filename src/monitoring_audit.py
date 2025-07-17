import os
import uuid
import json
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

transactions = pd.read_csv(os.path.join(DATA_DIR, "transactions.csv"))
auth_logs = pd.read_csv(os.path.join(DATA_DIR, "auth_logs.csv"))
devices = pd.read_csv(os.path.join(DATA_DIR, "devices.csv"))
accounts = pd.read_csv(os.path.join(DATA_DIR, "accounts.csv"))
customer_device = pd.read_csv(os.path.join(DATA_DIR, "customer_device.csv"))

log_results = []
risk_results = []

def log_risk_result(check_name, df, risk_rule, risk_reason):
    status = "FAIL" if not df.empty else "PASS"
    log_results.append({
        "check_name": check_name,
        "risk_rule": risk_rule,
        "status": status,
        "affected_rows": len(df),
        "sample_transaction_ids": json.dumps(df['transaction_id'].unique().tolist()[:5]) if not df.empty else None,
        "message": risk_reason if status == "FAIL" else "No violation",
        "detected_at": datetime.now().isoformat()
    })
    if status == "FAIL":
        df['risk_rule'] = risk_rule
        df['risk_reason'] = risk_reason
        df['check_name'] = check_name
        risk_results.append(df)

check_trans10M = transactions.merge(auth_logs, on="transaction_id", how="left")
check_trans10M = check_trans10M.merge(accounts[['account_id', 'customer_id']], on='account_id', how='left')
check_trans10M = check_trans10M[check_trans10M['amount'] >= 10_000_000]

rule1 = check_trans10M[
    ~check_trans10M['auth_method'].isin(['OTP', 'BIOMETRIC'])
][['transaction_id', 'customer_id', 'account_id', 'device_id', 'timestamp']].copy()

log_risk_result(
    check_name="high_value_no_auth",
    df=rule1,
    risk_rule="MISSING_STRONG_AUTH",
    risk_reason="Transaction >= 10M VND must use OTP or biometric authentication"
)

check_dev = transactions.merge(devices[['device_id', 'is_verified']], on="device_id", how="left")
check_dev = check_dev.merge(accounts[['account_id', 'customer_id']], on="account_id", how="left")
check_dev = check_dev.merge(customer_device[['customer_id', 'device_id', 'is_trusted']],
                            on=['customer_id', 'device_id'], how="left")

rule2 = check_dev[
    (check_dev['is_verified'] != True) | (check_dev['is_trusted'] != True)
][['transaction_id', 'customer_id', 'account_id', 'device_id', 'timestamp']].copy()

log_risk_result(
    check_name="device_not_verified_or_trusted",
    df=rule2,
    risk_rule="UNVERIFIED_OR_UNTRUSTED_DEVICE",
    risk_reason="Transaction used unverified or untrusted device"
)

check_trans20M = transactions.merge(auth_logs, on="transaction_id", how="left")
check_trans20M = check_trans20M.merge(accounts[['account_id', 'customer_id']], on='account_id', how='left')
check_trans20M['timestamp'] = pd.to_datetime(check_trans20M['timestamp'])
check_trans20M['date_only'] = check_trans20M['timestamp'].dt.date

daily_sum = check_trans20M.groupby(['customer_id', 'date_only'])['amount'].sum().reset_index()
daily_sum = daily_sum[daily_sum['amount'] > 20_000_000]

strong_auth = check_trans20M[check_trans20M['auth_method'].isin(['OTP', 'BIOMETRIC'])]
strong_auth = strong_auth[['customer_id', 'date_only']].drop_duplicates()

high_risk_days = daily_sum.merge(strong_auth, on=['customer_id', 'date_only'], how='left', indicator=True)
high_risk_days = high_risk_days[high_risk_days['_merge'] == 'left_only'][['customer_id', 'date_only']]

violated_transactions = check_trans20M.merge(
    high_risk_days,
    on=['customer_id', 'date_only'],
    how='inner'
)[['transaction_id', 'customer_id', 'account_id', 'device_id', 'timestamp']].copy()

log_risk_result(
    check_name="daily_sum_no_auth",
    df=violated_transactions,
    risk_rule="NO_STRONG_AUTH_IN_HIGH_VOLUME_DAY",
    risk_reason="Total transaction > 20M/day but no OTP/BIOMETRIC used"
)

log_df = pd.DataFrame(log_results)
log_df.to_csv(os.path.join(LOG_DIR, "risk_check_log.csv"), index=False)

if risk_results:
    risk_df = pd.concat(risk_results, ignore_index=True)
    risk_df["risk_id"] = [str(uuid.uuid4()) for _ in range(len(risk_df))]
    risk_df["created_at"] = datetime.now().isoformat()
    risk_tag_df = risk_df[[
        "risk_id",
        "transaction_id",
        "customer_id",
        "account_id",
        "device_id",
        "timestamp",
        "risk_rule",
        "risk_reason",
        "created_at"
    ]]
    risk_tag_df.to_csv(os.path.join(LOG_DIR, "risk_tag_table.csv"), index=False)

if log_df[log_df['status'] == 'FAIL'].empty:
    print("No risky behavior detected.")
else:
    print("Risky behavior detected. See logs/risk_check_log.csv and risk_tag_table.csv")
