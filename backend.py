# {
#  "cells": [],
#  "metadata": {
#   "language_info": {
#    "name": "python"
#   }
#  },
#  "nbformat": 4,
#  "nbformat_minor": 5
# }

# backend.py
import numpy as np
import pandas as pd
import joblib
import streamlit as st

# 1. Load the master pipeline bundle once with caching
@st.cache_resource
def load_production_pipeline():
    return joblib.load("models/network_pipeline.pkl")

pipeline = load_production_pipeline()

# 2. Dynamic Preprocessing Engine
def process_runtime_traffic(input_data_dict):
    scaler = pipeline["scaler"]
    skewed_cols = pipeline["skewed_features"]
    cat_cols = pipeline["categorical_features"]
    expected_order = pipeline["expected_features_order"]
    
    # Convert input dict to a single-row DataFrame
    df = pd.DataFrame([input_data_dict])
    
    # --- Feature Engineering ---
    if "sbytes" in df.columns and "dbytes" in df.columns:
        df["total_bytes"] = df["sbytes"] + df["dbytes"]
        df["byte_ratio"] = df["sbytes"] / (df["dbytes"] + 1)
    if "spkts" in df.columns and "dpkts" in df.columns:
        df["total_packets"] = df["spkts"] + df["dpkts"]
        df["packet_ratio"] = df["spkts"] / (df["dpkts"] + 1)
    if "sbytes" in df.columns and "spkts" in df.columns:
        df["source_bytes_per_packet"] = df["sbytes"] / (df["spkts"] + 1)
    if "dbytes" in df.columns and "dpkts" in df.columns:
        df["destination_bytes_per_packet"] = df["dbytes"] / (df["dpkts"] + 1)
        
    # --- Dynamic Log Transformations ---
    for col in skewed_cols:
        if col in df.columns:
            df[col] = np.log1p(df[col])
            
    # --- Dynamic One-Hot Encoding and Column Reindexing ---
    df = pd.get_dummies(df, columns=cat_cols, dtype=int)
    df = df.reindex(columns=expected_order, fill_value=0)
    
    # --- Dynamic Scaling ---
    to_scale = [c for c in df.columns if df[c].nunique() > 2]
    if len(to_scale) > 0:
        df[to_scale] = scaler.transform(df[to_scale])
        
    return df

# 3. Dynamic Prediction Engine
def evaluate_traffic_anomaly(processed_row_df):
    model = pipeline["model"]
    prediction = model.predict(processed_row_df)
    probability = model.predict_proba(processed_row_df)[:, 1] if hasattr(model, "predict_proba") else None
    return prediction, probability

