from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

app = Flask(__name__)
MODEL_FILE = "model.pkl"
ENCODERS_FILE = "encoders.pkl"

# Columns expected
CATEGORICAL_COLS = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
NUMERIC_COLS = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']

# Preprocess function
def preprocess(df, is_training=True):
    # Fill numeric missing values with median
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Fill categorical missing values with mode
    for col in CATEGORICAL_COLS:
        if col in df.columns:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Encode categorical features
    encoders = {}
    if is_training:
        for col in CATEGORICAL_COLS:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                encoders[col] = le
        # Save encoders
        with open(ENCODERS_FILE, 'wb') as f:
            pickle.dump(encoders, f)
    else:
        # Load encoders
        with open(ENCODERS_FILE, 'rb') as f:
            encoders = pickle.load(f)
        for col in CATEGORICAL_COLS:
            if col in df.columns and col in encoders:
                df[col] = encoders[col].transform(df[col])
    
    # Encode target if exists
    if 'Loan_Status' in df.columns:
        df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})
    
    return df

# Train endpoint
@app.route('/train', methods=['POST'])
def train():
    file = request.files['file']
    df = pd.read_csv(file)
    df = preprocess(df, is_training=True)

    X = df.drop(['Loan_ID', 'Loan_Status'], axis=1)
    y = df['Loan_Status']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)

    accuracy = model.score(X_test, y_test)

    return jsonify({"message": "Model trained successfully!", "accuracy": accuracy})

# Test endpoint
@app.route('/test', methods=['POST'])
def test():
    if not os.path.exists(MODEL_FILE) or not os.path.exists(ENCODERS_FILE):
        return jsonify({"error": "Model not trained yet!"})
    
    file = request.files['file']
    df = pd.read_csv(file)
    df = preprocess(df, is_training=False)

    X_test = df.drop(['Loan_ID', 'Loan_Status'], axis=1)
    y_test = df['Loan_Status']

    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)

    y_pred = model.predict(X_test)
    accuracy = (y_pred == y_test).mean()

    return jsonify({"accuracy": accuracy})

# Predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    if not os.path.exists(MODEL_FILE) or not os.path.exists(ENCODERS_FILE):
        return jsonify({"error": "Model not trained yet!"})
    
    data = request.get_json()
    df = pd.DataFrame([data])
    df = preprocess(df, is_training=False)

    # Keep only model features
    X = df[[col for col in df.columns if col in NUMERIC_COLS + CATEGORICAL_COLS]]

    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)

    pred = model.predict(X)[0]
    result = "Approved" if pred == 1 else "Rejected"

    return jsonify({"prediction": result})

if __name__ == '__main__':
    app.run(debug=True)
