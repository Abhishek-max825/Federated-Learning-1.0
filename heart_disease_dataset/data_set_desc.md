# 📊 Dataset Description – BRFSS 2022 (Federated Learning)

## Overview

This dataset is derived from the **Behavioral Risk Factor Surveillance System (BRFSS) 2022**, a large-scale public health survey conducted by the **Centers for Disease Control and Prevention (CDC)**.

The dataset contains **real medical diagnosis information** collected from adult respondents and is prepared specifically for **federated learning experiments** in healthcare.

Each record represents **one individual patient**.

## Prediction Task

### 🎯 Target Variable

**Heart Disease Diagnosis (Yes / No)**

This task is a **binary medical diagnosis prediction problem**, where the model predicts whether an individual has been **diagnosed with heart disease** based on demographic, lifestyle, and clinical risk factors.

## Target Column Description

### `heart_disease_diagnosis`

Derived from the BRFSS variable **CVDCRHD4**.

**Meaning:**
Indicates whether the respondent has ever been told by a healthcare professional that they have **coronary heart disease or myocardial infarction (heart attack)**.

**Values:**

* Yes
* No
* Unknown (kept intentionally)

This variable represents a **confirmed medical diagnosis**, not a self-assessed condition.

## Feature Descriptions

### `age_group`

Grouped age category of the patient.
Age is a major risk factor for cardiovascular disease.

### `sex`

Biological sex of the patient (Male / Female).
Sex differences influence heart disease prevalence and risk patterns.

### `bmi`

Body Mass Index category derived from height and weight.
BMI is an important indicator of obesity-related cardiovascular risk.

### `smoked_100_cigarettes`

Indicates whether the patient has smoked at least 100 cigarettes in their lifetime.
This serves as a long-term smoking exposure indicator.

### `diabetes_diagnosis`

Indicates whether the patient has been diagnosed with diabetes.
Diabetes is a strong comorbidity and risk factor for heart disease.

### `heart_attack_history`

Indicates whether the patient has a history of heart attack.
This is a strong predictor of existing cardiovascular disease.

### `stroke_history`

Indicates whether the patient has experienced a stroke.
Stroke history is closely associated with cardiovascular conditions.

## Data Cleaning Strategy

Only **minimal, industry-standard cleaning** was applied:

* BRFSS missing codes (7, 9, 77, 99, blank) were converted to **"Unknown"**
* "Unknown" values were retained as a valid category
* No rows were deleted
* No normalization or balancing was applied

This preserves **real-world clinical uncertainty** and avoids introducing bias.

## Federated Learning Split

The dataset is divided into **three hospital clients**, each simulating a real-world healthcare institution with different patient characteristics.

### Hospital Client 1 – Tertiary Care Hospital

* Older patient population
* Higher heart disease prevalence
* More missing lifestyle information
* 120,000 records

### Hospital Client 2 – Regional Hospital

* Mixed age population
* Moderate disease prevalence
* Smaller dataset due to natural data availability
* ~67,000 records

### Hospital Client 3 – Preventive Care Center

* Younger population
* Lower disease prevalence
* Better lifestyle data completeness
* 120,000 records

Unequal dataset sizes reflect **real hospital data heterogeneity**, which federated learning is designed to handle.

## Purpose of the Dataset

This dataset is designed to:

* Demonstrate **privacy-preserving federated learning**
* Predict **heart disease diagnosis**
* Simulate **non-IID medical data across hospitals**
* Study the impact of data heterogeneity on federated models

## Ethical and Privacy Considerations

* The dataset contains **no personal identifiers**
* Data is publicly available and de-identified
* The system provides **decision support only**, not clinical diagnosis

## Final Notes

* The dataset is realistic, heterogeneous, and federated-learning ready
* It reflects real-world healthcare data challenges
* Suitable for academic projects, research, and demonstrations


