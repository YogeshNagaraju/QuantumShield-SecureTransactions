import sqlite3

EDGE_DB = "edge_transactions.db"

# Create SQLite database for edge storage
def create_edge_database():
    conn = sqlite3.connect(EDGE_DB)
    cursor = conn.cursor()

    # Create table for low-risk transactions
    cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL,
                        recipient TEXT,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

# Initialize Edge Storage
create_edge_database()