import sqlite3
import mysql.connector
from datetime import datetime

# MySQL Connection Function (Centralized Bank Storage)
def connect_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ullas@0202",  # Your MySQL Root Password
        database="banking_system"
    )

# SQLite Database File (Edge Storage)
EDGE_DB = "edge_transactions.db"

# Create SQLite Table if Not Exists
def setup_sqlite():
    conn = sqlite3.connect(EDGE_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            recipient TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Create MySQL Database and Table if Not Exists
def setup_mysql():
    conn = connect_mysql()
    cursor = conn.cursor()

    # Create Database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS banking_system")
    cursor.execute("USE banking_system")

    # Create Table for High-Risk Transactions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HighRiskTransactions (
            tx_id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10,2) NOT NULL,
            recipient VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Function to Store Low-Risk Transactions in SQLite
def store_edge_transaction(amount, recipient):
    conn = sqlite3.connect(EDGE_DB)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO Transactions (amount, recipient, timestamp) VALUES (?, ?, ?)",
                   (amount, recipient, timestamp))
    conn.commit()
    conn.close()
    print(f"✅ Low-Risk Transaction Stored in SQLite: ₹{amount} to {recipient}")

# Function to Store High-Risk Transactions in MySQL
def store_high_risk_transaction(amount, recipient):
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO HighRiskTransactions (amount, recipient) VALUES (%s, %s)",
                   (amount, recipient))
    conn.commit()
    conn.close()
    print(f"🚀 High-Risk Transaction Stored in MySQL: ₹{amount} to {recipient}")

# AI-Based Risk Classification (Decide Edge vs Centralized Storage)
def classify_transaction(amount):
    return "Low-Risk" if amount < 100000 else "High-Risk"

# Function to Process Transactions
def process_transaction(amount, recipient):
    transaction_type = classify_transaction(amount)

    if transaction_type == "Low-Risk":
        store_edge_transaction(amount, recipient)  # Store in Edge (SQLite)
    else:
        store_high_risk_transaction(amount, recipient)  # Store in Centralized DB (MySQL)

# Retrieve & Display Edge (SQLite) Transactions
def display_edge_transactions():
    conn = sqlite3.connect(EDGE_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transactions")
    transactions = cursor.fetchall()
    conn.close()
    
    print("\n Edge Transactions (Low-Risk):")
    for tx in transactions:
        print(tx)

# Retrieve & Display Central (MySQL) Transactions
def display_central_transactions():
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HighRiskTransactions")
    transactions = cursor.fetchall()
    conn.close()
    
    print("\n Central Transactions (High-Risk):")
    for tx in transactions:
        print(tx)

# Setup Databases & Tables
setup_sqlite()
setup_mysql()

# Example Transactions
process_transaction(500, "Alice")        # Low-Risk → Stored in SQLite
process_transaction(200000, "Bob")       # High-Risk → Stored in MySQL

# Display Transactions
display_edge_transactions()
display_central_transactions()


def sync_edge_transactions():
    conn = sqlite3.connect(EDGE_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transactions")
    transactions = cursor.fetchall()
    conn.close()

    for tx in transactions:
        store_high_risk_transaction(tx[1], tx[2])
    print(" Edge Transactions Synced with Centralized MySQL Database")