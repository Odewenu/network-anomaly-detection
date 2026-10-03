## Phase 2: Model Training

This phase builds, tunes and tests the model that separates normal network traffic from attacks, using the cleaned UNSW-NB15 data from Phase 1.

**Notebook:** [`notebooks/02_model_training_final.ipynb`](notebooks/02_model_training_final.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Odewenu/network-anomaly-detection/blob/main/notebooks/02_model_training_final.ipynb)

### What was done

1. Loaded the cleaned train and test files from Phase 1 (`data/processed/`).
2. Held out 20% of the training data as a validation set. The test set was kept untouched until the final evaluation.
3. Trained four baseline models and compared them on the validation set: Logistic Regression, Decision Tree, Random Forest and XGBoost.
4. Trained an Isolation Forest on normal traffic only, as an unsupervised comparison.
5. Tuned the best model (XGBoost) with `RandomizedSearchCV` (20 combinations, 3-fold stratified cross-validation, scored on F1).
6. Retrained the tuned model on all training data and evaluated it once on the test set.
7. Checked detection rates per attack type and the most important features.
8. Saved the model and the files Phase 3 needs.

### Results

Validation set (used to choose the model):

| Model | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|
| Logistic Regression | [fill in] | [fill in] | [fill in] | [fill in] |
| Decision Tree | [fill in] | [fill in] | [fill in] | [fill in] |
| Random Forest | [fill in] | [fill in] | [fill in] | [fill in] |
| XGBoost | [fill in] | [fill in] | [fill in] | [fill in] |

Final model on the test set:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| XGBoost (tuned) | [fill in] | [fill in] | [fill in] | [fill in] | [fill in] |

Best settings found: `[paste from models/best_params.json]`

The full comparison of all models on the test set is in `results/test_comparison_all_models.csv`.

### Files added in this phase

```
notebooks/
  02_model_training_final.ipynb
models/
  xgb_model.pkl              trained XGBoost model
  feature_columns.json       column names, in the exact order the model expects
  test_metrics.json          final test scores
  best_params.json           tuned settings
  baseline_comparison.csv    validation comparison of the baseline models
results/
  baseline_comparison.png
  confusion_matrix.png
  roc_curve.png
  feature_importance.png
  per_attack_detection.csv
  test_comparison_all_models.csv
```

### How to reproduce

1. Run `notebooks/01_data_cleaning_clean.ipynb` first (or make sure `data/processed/` exists in the repo).
2. Open `notebooks/02_model_training_final.ipynb` in Colab and run all cells from top to bottom.
3. The model and its supporting files are written to `models/`.

Random seed is fixed at 42, so the split and the tuning search can be repeated.

### Notes for Phase 3 (deployment)

- Load the model with `joblib.load("models/xgb_model.pkl")`.
- Inputs must have the same columns in the same order as `models/feature_columns.json`.
- New data must go through the same preprocessing as Phase 1 before prediction: the added features, the log transform on skewed columns, one-hot encoding, and the saved scaler (`data/processed/scaler.pkl`).
- The label is 0 for normal traffic and 1 for an attack.

### Limitations

- Test scores are lower than validation scores. The UNSW-NB15 test set has a different mix of attacks from the training set, and overlapping rows were removed in Phase 1.
- [Add one line on any attack types the model catches poorly, from `results/per_attack_detection.csv`.]
