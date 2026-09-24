# Network Traffic Anomaly Detection

Group 16 project: detecting anomalies (attacks) in network traffic using machine learning.

## Dataset
UNSW-NB15 (Moustafa & Slay, 2015), using the Kaggle upload by dhoogla:
https://www.kaggle.com/datasets/dhoogla/unswnb15

## Project structure
- `data/processed/` - cleaned data ready for model training
- `notebooks/01_data_cleaning.ipynb` - data cleaning (Phase 1)

## Phase 1: Data cleaning (done)
- Removed duplicate rows (train: 175,341 to 96,822; test: 82,332 to 49,971)
- Log-transformed 21 heavily skewed columns
- Grouped rare protocols into "other"
- One-hot encoded `proto`, `service` and `state`
- Scaled numeric columns with StandardScaler (fitted on train only)

## Using the cleaned data
```python
import pandas as pd
train = pd.read_parquet("data/processed/train_clean.parquet")
test = pd.read_parquet("data/processed/test_clean.parquet")
```
- Target column: `label` (0 = normal, 1 = attack)
- Drop `attack_cat` before training. It gives away the answer.
- `scaler.pkl` must be reused when scaling new data in deployment.
