# `heart_disease_dataset/` — BRFSS 2022 Data & Hospital Datasets

Contains the source dataset and the 3 hospital sub-datasets used for federated learning.

## Files

| File                     | Size   | Description                                      |
|--------------------------|--------|--------------------------------------------------|
| `BRFSS_2022.csv`         | ~414MB | Raw CDC BRFSS 2022 survey data (445,132 rows × 328 columns) |
| `prepare_fl_data.py`     | ~8KB   | Script to extract, clean, balance, and split into hospital datasets |
| `hospital_client1.csv`   | ~1.9MB | Hospital Node 1 training data (~53K rows)        |
| `hospital_client2.csv`   | ~1.9MB | Hospital Node 2 training data (~53K rows)        |
| `hospital_client3.csv`   | ~1.9MB | Hospital Node 3 training data (~53K rows)        |
| `data_set_desc.md`       | ~4KB   | Dataset description & column documentation       |
| `heart_disease.py`       | ~230B  | Legacy utility                                   |

## Dataset Schema (Hospital Client CSVs)

Each hospital CSV has 8 columns:

| Column                    | BRFSS Source | Values                                 |
|---------------------------|-------------|----------------------------------------|
| `heart_disease_diagnosis` | `_MICHD`    | `1.0` = Yes, `2.0` = No               |
| `heart_attack_history`    | `CVDINFR4`  | `1.0` = Yes, `2.0` = No, `Unknown`    |
| `stroke_history`          | `CVDSTRK3`  | `1.0` = Yes, `2.0` = No, `Unknown`    |
| `diabetes_diagnosis`      | `DIABETE4`  | `1.0`-`4.0` (Yes/Preg/No/Pre), `Unknown` |
| `bmi`                     | `_BMI5`     | BMI × 100 (e.g., 2653 = 26.53), `Unknown` |
| `age_group`               | `_AGE_G`    | `1.0`-`6.0` (age brackets)            |
| `sex`                     | `SEXVAR`    | `1.0` = Male, `2.0` = Female          |
| `smoked_100_cigarettes`   | `SMOKE100`  | `1.0` = Yes, `2.0` = No, `Unknown`    |

## Dataset Preparation (`prepare_fl_data.py`)

Run this script to regenerate the hospital datasets from the raw BRFSS data:

```bash
cd heart_disease_dataset
python prepare_fl_data.py
```

**What it does:**
1. Loads only relevant columns from BRFSS_2022.csv
2. Drops rows with invalid/missing target values
3. Handles BRFSS-specific missing codes per column (7=Don't Know, 9=Refused → `Unknown`)
4. **Undersamples** the negative class to a 1:3 ratio (25% positive, 75% negative)
5. **Stratified split** into 3 equal hospital datasets (ensures each gets proportional positive cases)

## Class Distribution (After Balancing)

Each hospital dataset has approximately:
- **25% positive** (heart disease = Yes)
- **75% negative** (heart disease = No)
- ~53,000 total rows
