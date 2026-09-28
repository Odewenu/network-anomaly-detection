# Network Traffic Anomaly Detection

Group 16 project: detecting anomalies (attacks) in network traffic using machine learning.

## Dataset
UNSW-NB15 (Moustafa & Slay, 2015), using the Kaggle upload by dhoogla:
https://www.kaggle.com/datasets/dhoogla/unswnb15

## Project structure
- `data/raw/` - column schemas of the original data
- `data/processed/` - cleaned data ready for model training
- `notebooks/01_data_cleaning_clean.ipynb` - data cleaning (Phase 1)

## Phase 1: Data cleaning (done)
- Removed duplicate rows (train: 175,341 to 96,822; test: 82,332 to 49,971)
- Removed 1,571 test rows that also appeared in train (test: 48,400)
- Added 6 engineered features (totals, ratios, bytes per packet)
- Analysed outliers and kept them, since extreme values are often attacks (see `outlier_summary.csv`)
- Log-transformed 25 heavily skewed columns
- Grouped rare protocols into "other" and one-hot encoded `proto`, `service` and `state`
- Scaled 36 numeric columns with StandardScaler (fitted on train only)
- Saved `attack_cat` separately so it cannot be used as a model input

## Using the cleaned data
```python
import pandas as pd
train = pd.read_parquet("data/processed/train_clean.parquet")
test = pd.read_parquet("data/processed/test_clean.parquet")
```
- Target column: `label` (0 = normal, 1 = attack)
- `attack_cat` has already been removed from these files. It is saved in `train_attack_cat.parquet` and `test_attack_cat.parquet` (same row order) for error analysis only. Never use it as a model input.
- `scaler.pkl` must be reused when scaling new data in deployment.
