-- CUSTOMER
CREATE TABLE Customer (
    customer_id CHAR(36) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    gender ENUM('male','female') NOT NULL,
    national_id ENUM('CCCD', 'PASSPORT') NOT NULL,
    national_number VARCHAR(20) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    country VARCHAR(50),
    address VARCHAR (255),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ACCOUNT
CREATE TABLE Account (
    account_id CHAR(36) PRIMARY KEY,
    customer_id CHAR(36) NOT NULL,
    account_type ENUM('SAVINGS', 'CURRENT', 'CREDIT') NOT NULL,
    balance DECIMAL(18,2) DEFAULT 0.00,
    status ENUM('ACTIVE', 'INACTIVE', 'BLOCKED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);
CREATE INDEX idx_account_customer_id ON Account(customer_id);

-- DEVICE
CREATE TABLE Device (
    device_id CHAR(36) PRIMARY KEY,
    device_code VARCHAR(100) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TRANSACTION
CREATE TABLE Transaction (
    transaction_id CHAR(36) PRIMARY KEY,
    account_id CHAR(36) NOT NULL,
    device_id CHAR(36) NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    transaction_type ENUM('TRANSFER', 'PAYMENT', 'WITHDRAWAL', 'TOPUP') NOT NULL,
    state ENUM ('PENDING', 'COMPLETED', 'FAILED') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Account(account_id),
    FOREIGN KEY (device_id) REFERENCES Device(device_id)
);
CREATE INDEX idx_transaction_account_id ON Transaction(account_id);
CREATE INDEX idx_transaction_device_id ON Transaction(device_id);

CREATE TABLE AuthLog (
    auth_log_id CHAR(36) PRIMARY KEY,
    transaction_id CHAR(36) NOT NULL,
    auth_method ENUM(
        'PASSWORD',
        'OTP_SMS', 'OTP_VOICE', 'OTP_EMAIL',
        'MATRIX_CARD',
        'SOFT_OTP_BASIC', 'SOFT_OTP_ADV',
        'FIDO', 'SIGNATURE',
        'BIOMETRIC_CCCD', 'BIOMETRIC_EID', 'BIOMETRIC_DB'
    ) NOT NULL,
    auth_success BOOLEAN DEFAULT TRUE,
    biometric_verified BOOLEAN DEFAULT FALSE,
    biometric_source ENUM('CCCD_CHIP', 'ELECTRONIC_ID', 'BANK_DATABASE', 'NONE') DEFAULT 'NONE',
    auth_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id)
);

CREATE INDEX idx_authlog_transaction_id ON AuthLog(transaction_id);


-- CUSTOMER - DEVICE (many-to-many)
CREATE TABLE CustomerDevice (
    customer_id CHAR(36) NOT NULL,
    device_id CHAR(36) NOT NULL,
    is_trusted BOOLEAN DEFAULT FALSE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id, device_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (device_id) REFERENCES Device(device_id)
);
CREATE INDEX idx_custdev_customer_id ON CustomerDevice(customer_id);
CREATE INDEX idx_custdev_device_id ON CustomerDevice(device_id);

-- RISK TAG
CREATE TABLE RiskTag (
    risk_id CHAR(36) PRIMARY KEY,          -- UUID hoặc auto-gen
    transaction_id CHAR(36) NOT NULL,
    customer_id CHAR(36),
    account_id CHAR(36),
    device_id CHAR(36),
    timestamp TIMESTAMP,
    risk_rule VARCHAR(100),
    risk_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (account_id) REFERENCES Account(account_id),
    FOREIGN KEY (device_id) REFERENCES Device(device_id)
);
