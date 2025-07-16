import os
import pandas as pd
from datetime import datetime

# ────────────────────────────────────────
# 📂 Chuẩn hóa đường dẫn
# ────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))        # /src
DATA_DIR = os.path.join(BASE_DIR, "..", "data")              # /data
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")               # /logs
os.makedirs(LOG_DIR, exist_ok=True)

# ────────────────────────────────────────
# 📥 Load dữ liệu
# ────────────────────────────────────────
customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
devices = pd.read_csv(os.path.join(DATA_DIR, "devices.csv"))
accounts = pd.read_csv(os.path.join(DATA_DIR, "accounts.csv"))
transactions = pd.read_csv(os.path.join(DATA_DIR, "transactions.csv"))
auth_logs = pd.read_csv(os.path.join(DATA_DIR, "auth_logs.csv"))
customer_device = pd.read_csv(os.path.join(DATA_DIR, "customer_device.csv"))

results = []

# ────────────────────────────────────────
# 🧾 Hàm ghi log kiểm tra
# ────────────────────────────────────────
def log_result(check_name, table, column, status, affected_rows=0, sample_values=None, message=""):
    log_entry = {
        "check_time": datetime.now().isoformat(),
        "check_name": check_name,
        "table": table,
        "column": column,
        "status": status,
        "affected_rows": affected_rows,
        "sample_values": str(sample_values[:5]) if sample_values else None,
        "message": message
    }

    if status == "FAIL":
        results.append(log_entry)
    else:
        print(f"✅ {check_name} passed for {table}.{column}")

# ────────────────────────────────────────
# ✅ Check 1: Null
# ────────────────────────────────────────
def check_nulls(df, df_name):
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            sample_ids = df[df[col].isnull()].index.tolist()
            log_result("null_check", df_name, col, "FAIL", count, sample_ids, f"{count} nulls in '{col}'")
        else:
            log_result("null_check", df_name, col, "PASS")

# ✅ Check 2: Uniqueness
def check_unique(df, df_name, column):
    dup_df = df[df.duplicated(subset=[column], keep=False)]
    if not dup_df.empty:
        log_result("uniqueness_check", df_name, column, "FAIL", len(dup_df), dup_df[column].unique().tolist(),
                   f"{len(dup_df)} duplicate values in '{column}'")
    else:
        log_result("uniqueness_check", df_name, column, "PASS")

# ✅ Check 3: CCCD định dạng 12 chữ số
def check_cccd_format(df):
    if "national_id" in df.columns and "national_number" in df.columns:
        invalid = df[(df["national_id"] == "CCCD") &
                     (~df["national_number"].astype(str).str.match(r"^\d{12}$"))]
        if not invalid.empty:
            log_result("regex_check_cccd", "Customer", "national_number", "FAIL", len(invalid),
                       invalid["national_number"].tolist(), "Invalid CCCD format (not 12 digits)")
        else:
            log_result("regex_check_cccd", "Customer", "national_number", "PASS")

# ✅ Check 4: Foreign Key
def check_fk(child_df, parent_df, child_col, parent_col, child_table, parent_table):
    unmatched = ~child_df[child_col].isin(parent_df[parent_col])
    if unmatched.any():
        bad_values = child_df.loc[unmatched, child_col].unique().tolist()
        log_result("foreign_key_check", child_table, child_col, "FAIL", unmatched.sum(), bad_values,
                   f"{unmatched.sum()} FK violations: values in '{child_col}' not in {parent_table}")
    else:
        log_result("foreign_key_check", child_table, child_col, "PASS")

# ────────────────────────────────────────
# 🔍 Chạy tất cả các kiểm tra
# ────────────────────────────────────────

# Null checks
for df, name in [(customers, "Customer"), (devices, "Device"), (accounts, "Account"),
                 (transactions, "Transaction"), (auth_logs, "AuthLog"), (customer_device, "CustomerDevice")]:
    check_nulls(df, name)

# Uniqueness checks
check_unique(customers, "Customer", "national_number")
check_unique(customers, "Customer", "customer_id")
check_unique(devices, "Device", "device_id")
check_unique(accounts, "Account", "account_id")
check_unique(transactions, "Transaction", "transaction_id")
check_unique(auth_logs, "AuthLog", "auth_log_id")

# Format / Regex check
check_cccd_format(customers)

# Foreign key checks
check_fk(accounts, customers, "customer_id", "customer_id", "Account", "Customer")
check_fk(transactions, accounts, "account_id", "account_id", "Transaction", "Account")
check_fk(transactions, devices, "device_id", "device_id", "Transaction", "Device")
check_fk(auth_logs, transactions, "transaction_id", "transaction_id", "AuthLog", "Transaction")
check_fk(customer_device, customers, "customer_id", "customer_id", "CustomerDevice", "Customer")
check_fk(customer_device, devices, "device_id", "device_id", "CustomerDevice", "Device")

# ────────────────────────────────────────
# 📄 Export log kết quả
# ────────────────────────────────────────
dq_result = pd.DataFrame(results)

if dq_result.empty or all(dq_result["status"] == "PASS"):
    print("✅ No data quality issues found.")
else:
    print("❌ Data quality issues found:")
    print(dq_result[["check_name", "table", "column", "status", "affected_rows", "message"]])

dq_result.to_csv(os.path.join(LOG_DIR, "data_quality_log.csv"), index=False)
