CREATE DATABASE IF NOT EXISTS banking_system;

USE banking_system;

DROP TABLE IF EXISTS HighRiskTransactions;

-- Create the table for high-risk transactions
CREATE TABLE HighRiskTransactions (
    tx_id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(10,2) NOT NULL,
    recipient VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    zkp_proof TEXT NOT NULL
);