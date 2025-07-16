import uuid
import random
import os
from datetime import datetime
import pandas as pd
import faker

# Khởi tạo Faker
fake = faker.Faker()

# ────────────────────────────────────────
# ⚙️ Config số lượng dữ liệu
# ────────────────────────────────────────
NUM_CUSTOMERS = 100
NUM_DEVICES = 80
NUM_ACCOUNTS = 200
NUM_TRANSACTIONS = 800
NUM_AUTH_LOGS = 600

# ────────────────────────────────────────
# 🔧 Helper functions
# ────────────────────────────────────────
def generate_uuid():
    return str(uuid.uuid4())

def random_enum(enum_list):
    return random.choice(enum_list)

# ────────────────────────────────────────
# 📂 Chuẩn hóa đường dẫn export
# ────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # src/
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "data")              # data/
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ────────────────────────────────────────
# 👤 CUSTOMER
# ────────────────────────────────────────
customers = []
for _ in range(NUM_CUSTOMERS):
    customer_id = generate_uuid()
    customers.append({
        'customer_id': customer_id,
        'full_name': fake.name(),
        'gender': random_enum(['male', 'female']),
        'national_id': random_enum(['CCCD', 'PASSPORT']),
        'national_number': fake.unique.random_number(digits=12),
        'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=70),
        'country': fake.country(),
        'address': fake.address(),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'created_at': fake.date_time_this_year()
    })

# ────────────────────────────────────────
# 💻 DEVICE
# ────────────────────────────────────────
devices = []
for _ in range(NUM_DEVICES):
    devices.append({
        'device_id': generate_uuid(),
        'device_code': fake.sha256(),
        'is_verified': random.choice([True, False]),
        'created_at': fake.date_time_this_year()
    })

# ────────────────────────────────────────
# 💳 ACCOUNT
# ────────────────────────────────────────
accounts = []
for _ in range(NUM_ACCOUNTS):
    customer = random.choice(customers)
    accounts.append({
        'account_id': generate_uuid(),
        'customer_id': customer['customer_id'],
        'account_type': random_enum(['SAVINGS', 'CURRENT', 'CREDIT']),
        'balance': round(random.uniform(1000, 100_000_000), 2),
        'status': random_enum(['ACTIVE', 'INACTIVE', 'BLOCKED']),
        'created_at': fake.date_time_this_year()
    })

# ────────────────────────────────────────
# 💰 TRANSACTION
# ────────────────────────────────────────
transactions = []
for _ in range(NUM_TRANSACTIONS):
    account = random.choice(accounts)
    device = random.choice(devices)
    amount = round(random.uniform(1000, 50_000_000), 2)
    transactions.append({
        'transaction_id': generate_uuid(),
        'account_id': account['account_id'],
        'device_id': device['device_id'],
        'amount': amount,
        'transaction_type': random_enum(['TRANSFER', 'PAYMENT', 'WITHDRAWAL', 'TOPUP']),
        'state': random_enum(['PENDING', 'COMPLETED', 'FAILED']),
        'timestamp': fake.date_time_this_year()
    })

# ────────────────────────────────────────
# 🔐 AUTH LOG
# ────────────────────────────────────────
auth_logs = []
for _ in range(NUM_AUTH_LOGS):
    transaction = random.choice(transactions)
    auth_logs.append({
        'auth_log_id': generate_uuid(),
        'transaction_id': transaction['transaction_id'],
        'auth_method': random_enum(['OTP', 'BIOMETRIC']),
        'auth_success': random.choice([True, False]),
        'auth_timestamp': transaction['timestamp']
    })

# ────────────────────────────────────────
# 🔄 CUSTOMER-DEVICE
# ────────────────────────────────────────
customer_device = []
for _ in range(NUM_CUSTOMERS * 3):
    customer = random.choice(customers)
    device = random.choice(devices)
    customer_device.append({
        'customer_id': customer['customer_id'],
        'device_id': device['device_id'],
        'is_trusted': random.choice([True, False]),
        'added_at': fake.date_time_this_year()
    })

# ────────────────────────────────────────
# 📤 EXPORT CSVs
# ────────────────────────────────────────
def export_csv(data, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    pd.DataFrame(data).to_csv(path, index=False, date_format="%Y-%m-%d %H:%M:%S")
    print(f"✅ Exported: {filename}")

export_csv(customers, "customers.csv")
export_csv(devices, "devices.csv")
export_csv(accounts, "accounts.csv")
export_csv(transactions, "transactions.csv")
export_csv(auth_logs, "auth_logs.csv")
export_csv(customer_device, "customer_device.csv")
