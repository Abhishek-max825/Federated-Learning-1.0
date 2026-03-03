"""
Prepare Federated Learning datasets from BRFSS 2022.

Creates 3 hospital sub-datasets by:
1. Extracting relevant heart disease features from the raw BRFSS data
2. Mapping BRFSS codes to our schema
3. Properly handling BRFSS-specific missing/refused/unknown codes per column
4. Stratified splitting to ensure each hospital gets a fair share of positive cases
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# ─── Configuration ───────────────────────────────────────────────────────────

INPUT_FILE = "BRFSS_2022.csv"
OUTPUT_DIR = "."
NUM_CLIENTS = 3

# BRFSS column → Our feature name
COLUMN_MAPPING = {
    "_MICHD":    "heart_disease_diagnosis",   # Computed: Ever had MI or CHD. 1=Yes, 2=No
    "CVDINFR4":  "heart_attack_history",       # 1=Yes, 2=No, 7=Don't Know, 9=Refused
    "CVDSTRK3":  "stroke_history",             # 1=Yes, 2=No, 7=Don't Know, 9=Refused
    "DIABETE4":  "diabetes_diagnosis",         # 1=Yes, 2=Yes(pregnancy), 3=No, 4=Pre-diabetes
    "_BMI5":     "bmi",                        # BMI * 100 (e.g., 2653 = 26.53), BLANK=Missing
    "_AGE_G":    "age_group",                  # 1-6 age groups
    "SEXVAR":    "sex",                        # 1=Male, 2=Female
    "SMOKE100":  "smoked_100_cigarettes"       # 1=Yes, 2=No, 7=Don't Know, 9=Refused
}

# BRFSS missing/refused/don't-know codes PER COLUMN
# These vary by question — using the correct BRFSS 2022 codebook values
MISSING_CODES_PER_COLUMN = {
    "heart_disease_diagnosis": [],             # _MICHD is computed, no refused/DK
    "heart_attack_history":    [7, 9],         # 7=Don't Know, 9=Refused
    "stroke_history":          [7, 9],
    "diabetes_diagnosis":      [7, 9],
    "bmi":                     [],             # _BMI5: NaN means missing (no code)
    "age_group":               [],             # _AGE_G: computed, no refused
    "sex":                     [],             # SEXVAR: computed, no refused
    "smoked_100_cigarettes":   [7, 9]
}


def main():
    print(f"Loading {INPUT_FILE}...")
    brfss_cols = list(COLUMN_MAPPING.keys())
    df = pd.read_csv(INPUT_FILE, usecols=brfss_cols)
    print(f"  Raw shape: {df.shape}")

    # Rename to our schema
    df = df.rename(columns=COLUMN_MAPPING)

    # ─── Step 1: Drop rows where the TARGET is missing ──────────────────────
    # _MICHD: 1=Yes, 2=No. NaN = not computed (shouldn't happen often)
    before = len(df)
    df = df.dropna(subset=["heart_disease_diagnosis"])
    # Also drop any value that isn't 1 or 2
    df = df[df["heart_disease_diagnosis"].isin([1.0, 2.0])]
    print(f"  After dropping missing/invalid target: {len(df)} (removed {before - len(df)})")

    # ─── Step 2: Handle missing values per column correctly ─────────────────
    for col, codes in MISSING_CODES_PER_COLUMN.items():
        if col == "heart_disease_diagnosis":
            continue  # Already handled

        if col == "bmi":
            # BMI: NaN means missing. We keep NaN and label them "Unknown"
            # so our FLDataHandler's imputer can handle them
            df[col] = df[col].apply(lambda x: "Unknown" if pd.isna(x) else x)
        else:
            # Replace BRFSS refused/don't-know codes AND NaN with "Unknown"
            df[col] = df[col].apply(
                lambda x, c=codes: "Unknown" if (pd.isna(x) or x in c) else x
            )

    # ─── Step 3: Convert target to our format ───────────────────────────────
    # _MICHD: 1=Yes (heart disease), 2=No → keep as 1.0 and 2.0
    # Our FLDataHandler converts: startswith('1') → 1, else → 0
    # So 1.0 → "1.0" → 1 (disease), 2.0 → "2.0" → 0 (no disease) ✓

    # ─── Step 4: Ensure column types are consistent ─────────────────────────
    # Convert all to string for consistency (FLDataHandler expects this)
    for col in df.columns:
        df[col] = df[col].astype(str)

    # Quick stats
    target_counts = df["heart_disease_diagnosis"].value_counts()
    print(f"\n  Target distribution:")
    print(f"    1.0 (Heart Disease): {target_counts.get('1.0', 0)}")
    print(f"    2.0 (No Disease):    {target_counts.get('2.0', 0)}")

    total_pos = target_counts.get('1.0', 0)
    total_neg = target_counts.get('2.0', 0)
    print(f"    Positive rate: {total_pos / (total_pos + total_neg) * 100:.2f}%")

    # ─── Step 5: Undersample negative class for better balance ────────────
    # Keep ALL positive cases, downsample negatives to a 1:3 ratio
    NEG_TO_POS_RATIO = 3  # 3 negatives per 1 positive

    df_pos = df[df["heart_disease_diagnosis"] == "1.0"]
    df_neg = df[df["heart_disease_diagnosis"] == "2.0"]

    n_neg_target = len(df_pos) * NEG_TO_POS_RATIO
    if n_neg_target < len(df_neg):
        df_neg_sampled = df_neg.sample(n=n_neg_target, random_state=42)
        print(f"\n  Undersampled negatives: {len(df_neg)} → {len(df_neg_sampled)}")
    else:
        df_neg_sampled = df_neg

    df = pd.concat([df_pos, df_neg_sampled]).sample(frac=1, random_state=42).reset_index(drop=True)
    print(f"  Balanced dataset size: {len(df)}")
    print(f"  Positive rate after balancing: {len(df_pos)/len(df)*100:.1f}%")

    # ─── Step 6: Stratified split into 3 hospital datasets ──────────────────
    # Use stratified splitting to ensure each hospital gets a proportional
    # share of positive cases (avoids one hospital having 0 positives)

    print(f"\n  Splitting {len(df)} records into {NUM_CLIENTS} hospital datasets...")

    # Create binary target for stratification
    y_strat = (df["heart_disease_diagnosis"] == "1.0").astype(int)

    # First split: 1/3 for client1, 2/3 remaining
    client1, remaining, y1, y_rem = train_test_split(
        df, y_strat, test_size=2/3, random_state=42, stratify=y_strat
    )

    # Second split: 1/2 of remaining for client2, 1/2 for client3
    y_rem_reset = y_rem.reset_index(drop=True)
    remaining_reset = remaining.reset_index(drop=True)
    client2, client3, y2, y3 = train_test_split(
        remaining_reset, y_rem_reset, test_size=0.5, random_state=42, stratify=y_rem_reset
    )

    # Shuffle each client's data
    client1 = client1.sample(frac=1, random_state=10).reset_index(drop=True)
    client2 = client2.sample(frac=1, random_state=20).reset_index(drop=True)
    client3 = client3.sample(frac=1, random_state=30).reset_index(drop=True)

    # ─── Step 7: Save datasets ──────────────────────────────────────────────
    clients = {"hospital_client1.csv": client1,
               "hospital_client2.csv": client2,
               "hospital_client3.csv": client3}

    for filename, client_df in clients.items():
        filepath = f"{OUTPUT_DIR}/{filename}"
        client_df.to_csv(filepath, index=False)

        # Stats
        pos = (client_df["heart_disease_diagnosis"] == "1.0").sum()
        neg = (client_df["heart_disease_diagnosis"] == "2.0").sum()
        bmi_unknown = (client_df["bmi"] == "Unknown").sum()
        print(f"\n  {filename}:")
        print(f"    Total rows:     {len(client_df)}")
        print(f"    Positive (1.0): {pos} ({pos/len(client_df)*100:.2f}%)")
        print(f"    Negative (2.0): {neg} ({neg/len(client_df)*100:.2f}%)")
        print(f"    BMI Unknown:    {bmi_unknown} ({bmi_unknown/len(client_df)*100:.1f}%)")

    print("\n✅ Done! All 3 hospital datasets created successfully.")


if __name__ == "__main__":
    main()
