import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load trained model and feature names
model = joblib.load("fraud_detection_model.pkl")  # Your trained pipeline (Scaler + Model)
feature_names = joblib.load("feature_names.pkl")  # List of expected feature names

st.title("Fraud Detection System - PaySim Dataset")
st.subheader("Enter transaction details:")

# Collect user inputs
step = st.number_input("Step (Time Step)", value=1)
amount = st.number_input("Transaction Amount", value=0.0)
oldbalanceOrg = st.number_input("Old Balance of Sender", value=0.0)
newbalanceOrig = st.number_input("New Balance of Sender", value=0.0)
oldbalanceDest = st.number_input("Old Balance of Receiver", value=0.0)
newbalanceDest = st.number_input("New Balance of Receiver", value=0.0)

transaction_type = st.selectbox("Transaction Type", ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'])

# Prepare input dictionary with required features
input_dict = {
    'step': step,
    'amount': amount,
    'oldbalanceOrg': oldbalanceOrg,
    'newbalanceOrig': newbalanceOrig,
    'oldbalanceDest': oldbalanceDest,
    'newbalanceDest': newbalanceDest,
    'type_CASH_IN': 0,
    'type_CASH_OUT': 0,
    'type_DEBIT': 0,
    'type_PAYMENT': 0,
    'type_TRANSFER': 0,
    'isFlaggedFraud': 0  # Default to 0 unless flagged transactions are required
}

# Set the correct transaction type flag
input_dict[f'type_{transaction_type}'] = 1

# Add any missing features expected by the model with default 0
for col in feature_names:
    if col not in input_dict:
        input_dict[col] = 0

# Arrange input in correct column order
input_df = pd.DataFrame([input_dict])[feature_names]

# Prediction button
if st.button("Predict Fraud"):
    prediction = model.predict(input_df)

    if prediction[0] == 1:
        st.error("⚠ Fraudulent Transaction Detected!")
    else:
        st.success("✅ Transaction appears genuine.")