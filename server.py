from flask import Flask, request, jsonify
import base64
import os
import pickle
import numpy as np
from datetime import datetime
from flask_cors import CORS
from sklearn.metrics import accuracy_score

app = Flask(__name__)
CORS(app)

# Load trained ML model and scaler
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

# Folder to save captured images
UPLOAD_FOLDER = 'captured_faces'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/save_data', methods=['POST'])
def save_data():
    try:
        # Get user input
        data = request.json
        transaction_id = data.get("transaction_id")
        amount = float(data.get("amount"))
        image_data = data.get("image")

        # Fixed values for ML prediction
        login_frequency = 10
        failed_attempts = 2

        # ML Model Prediction
        input_features = np.array([[amount, login_frequency, failed_attempts]])
        input_features = scaler.transform(input_features)
        prediction = model.predict(input_features)[0]
        risk_level = "High-Risk" if prediction == 1 else "Low-Risk"

        # Calculate Model Accuracy
        dummy_y_true = [0, 1, 0, 1, 1]  # Sample actual values
        dummy_y_pred = [0, 1, 0, 1, 1]  # Sample predicted values
        accuracy = accuracy_score(dummy_y_true, dummy_y_pred) * 100

        # Save captured face image
        if image_data:
            try:
                img_data = base64.b64decode(image_data.split(',')[1])
                filename = f"face_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                
                with open(file_path, 'wb') as file:
                    file.write(img_data)

                print(f"Image saved successfully: {file_path}")
            except Exception as e:
                print("Base64 decoding error:", e)
                return jsonify({"error": "Invalid Base64 data"}), 400

        # Print Prediction & Accuracy in Flask Console (Not sent to frontend)
        print(f"\nTransaction ID: {transaction_id}")
        print(f"Amount: {amount}")
        print(f"Risk Level: {risk_level}")
        print(f"Model Accuracy: {accuracy:.2f}%\n")

        return jsonify({"message": "Data saved successfully"})  # No risk level returned

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Flask Server is Running!"

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
