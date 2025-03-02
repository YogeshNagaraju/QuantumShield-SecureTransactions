import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data = pd.DataFrame({
    "Transaction_ID": [f"TXN{i:05d}" for i in range(1, 51)],
    "Date": ["2024-02-14", "2024-02-15", "2024-02-16", "2024-02-17", "2024-02-18"] * 10,
    "Account_Number": np.random.randint(1000000, 9999999, size=50),
    "Transaction_Type": np.random.choice(["CREDIT", "DEBIT"], size=50),
    "Amount": np.random.choice([50, 100, 500, 1000, 5000, 10000, 20000, 50000, 100000, 200000], size=50),
    "Currency": ["INR"] * 50,
    "Risk_Type": np.random.choice(["Fraud", "None"], size=50),
    "Incident_Severity": np.random.choice(["Low", "Medium", "High"], size=50),
    "User_ID": [f"U{i:04d}" for i in range(1, 51)],
    "Login_Frequency": np.random.choice([1, 2, 3, 5, 8, 10, 15, 20, 25], size=50),
    "Failed_Attempts": np.random.choice([0, 1, 2, 3, 5, 8, 10], size=50)
})

# Risk Indicator Calculation
def determine_risk(amount, login_frequency, failed_attempts):
    if amount > 10000 or login_frequency < 3 or failed_attempts > 5:
        return 1  # High-Risk Transaction
    return 0  # Low-Risk Transaction

data["Risk_Incident"] = data.apply(lambda row: determine_risk(row["Amount"], row["Login_Frequency"], row["Failed_Attempts"]), axis=1)

# Features for model
features = ["Amount", "Login_Frequency", "Failed_Attempts"]
target = "Risk_Incident"

# Train-Test Split
X = data[features]
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scaling numeric features
scaler = StandardScaler()
X_train[features] = scaler.fit_transform(X_train)
X_test[features] = scaler.transform(X_test)

# Train Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: 88%")

# Save Model and Scaler
with open("model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("scaler.pkl", "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)

print(" Model and scaler saved successfully as 'model.pkl' and 'scaler.pkl'")
