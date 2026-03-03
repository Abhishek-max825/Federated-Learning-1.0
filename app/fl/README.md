# `app/fl/` — Federated Learning Engine

The core FL logic. This is **not** a Flask blueprint — it's a pure Python module used by the API routes.

## Files

| File             | Purpose                                                |
|------------------|--------------------------------------------------------|
| `__init__.py`    | Package marker                                         |
| `model.py`       | `FederatedDNN` (PyTorch neural network) + `FLModel` wrapper |
| `client.py`      | `FLClient` — simulates a hospital's local training     |
| `data.py`        | `FLDataHandler` — data loading, preprocessing, feature engineering |
| `aggregator.py`  | `FLAggregator` — FedAvg aggregation of client weights  |
| `saved_models/`  | Persisted global model weights (`.pkl` files per round) |

## How It Works

### Data Pipeline (`data.py` → `FLDataHandler`)
```
Raw CSV → BMI scaling (÷100) → Missing value imputation → StandardScaler (BMI) → OneHotEncoder (categoricals) → NumPy array
```
- **BMI**: BRFSS stores BMI×100 (e.g., 2953 = 29.53). Scaled down, then standardized.
- **Categoricals**: `age_group`, `sex`, `smoked_100_cigarettes`, `diabetes_diagnosis`, `heart_attack_history`, `stroke_history` — one-hot encoded with fixed categories for consistency.
- **Target**: `heart_disease_diagnosis` — 1.0→1 (disease), anything else→0 (no disease).
- **Output**: 23-dimensional feature vector (1 numerical + 22 one-hot).

### Model (`model.py` → `FederatedDNN`)
```
Input(23) → Linear(64) → ReLU → Dropout(0.3) → Linear(32) → ReLU → Dropout(0.2) → Linear(1) → [logits]
```
- 3-layer DNN with dropout for regularization
- Uses `BCEWithLogitsLoss` with `pos_weight` to handle class imbalance
- Training: Adam optimizer, lr=0.001, batch_size=256, 5 epochs

### Client (`client.py` → `FLClient`)
1. Loads hospital's CSV data via `FLDataHandler`
2. Receives global model weights from server
3. Trains locally for 5 epochs
4. Adds differential privacy noise (Gaussian, σ=0.01) to weights
5. Returns: `(noisy_weights, n_samples, metrics)`

### Aggregator (`aggregator.py` → `FLAggregator`)
- **FedAvg algorithm**: `w_global = Σ(n_k × w_k) / Σ(n_k)`
- Weighted average of client model weights, proportional to their sample counts
- Saves model checkpoints per round for rollback capability
- Maintains training history for analytics dashboard
