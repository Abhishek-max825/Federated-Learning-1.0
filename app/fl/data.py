import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class FLDataHandler:
    # Class-level fitted preprocessor — shared across instances
    # so the doctor prediction can reuse the scaler fitted during training
    _fitted_preprocessor = None

    def __init__(self):
        self.feature_columns = [
            'age_group', 'sex', 'bmi', 'smoked_100_cigarettes', 
            'diabetes_diagnosis', 'heart_attack_history', 'stroke_history'
        ]
        self.target_column = 'heart_disease_diagnosis'
        
        # Define categorical features and their expected categories for consistency across clients
        self.categorical_features = [
            'age_group', 'sex', 'smoked_100_cigarettes', 
            'diabetes_diagnosis', 'heart_attack_history', 'stroke_history'
        ]
        # BMI is treated as numerical (after handling 'Unknown')
        self.numerical_features = ['bmi']

        # Pre-define categories to ensure consistent shapes
        self.categories = {
            'age_group': ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0'],
            'sex': ['1.0', '2.0'],
            'smoked_100_cigarettes': ['1.0', '2.0', 'Unknown'],
            'diabetes_diagnosis': ['1.0', '2.0', '3.0', '4.0', 'Unknown'], 
            'heart_attack_history': ['1.0', '2.0', 'Unknown'],
            'stroke_history': ['1.0', '2.0', 'Unknown']
        }

        self.preprocessor = self._build_preprocessor()

    def _build_preprocessor(self):
        # Numerical transformer: impute missing then standardize
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        # Categorical transformer
        cats = [self.categories[c] for c in self.categorical_features]
        categorical_transformer = OneHotEncoder(categories=cats, handle_unknown='ignore', sparse_output=False)

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, self.numerical_features),
                ('cat', categorical_transformer, self.categorical_features)
            ]
        )
        return preprocessor

    def _prepare_bmi(self, df):
        """Convert BMI from BRFSS format (BMI×100) to actual BMI."""
        if 'bmi' in df.columns:
            df = df.copy()
            df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
            df['bmi'] = df['bmi'] / 100.0  # Convert BRFSS scale to actual BMI
        return df

    def _prepare_categoricals(self, df):
        """Ensure categorical columns are strings."""
        df = df.copy()
        for col in self.categorical_features:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df

    def preprocess_features(self, df):
        """Fit AND transform — use during TRAINING only (many samples)."""
        df = self._prepare_bmi(df)
        df = self._prepare_categoricals(df)
        X = df[self.feature_columns]
        
        # fit_transform on training data (many samples → StandardScaler works correctly)
        X_processed = self.preprocessor.fit_transform(X)
        
        # Save the fitted preprocessor for inference
        FLDataHandler._fitted_preprocessor = self.preprocessor
        
        return X_processed

    def preprocess_for_prediction(self, df):
        """Transform only — use during INFERENCE (single patient or small batch).
        Reuses the scaler fitted on training data so BMI scaling is correct."""
        df = self._prepare_bmi(df)
        df = self._prepare_categoricals(df)
        X = df[self.feature_columns]
        
        if FLDataHandler._fitted_preprocessor is not None:
            # Use the fitted preprocessor from training
            X_processed = FLDataHandler._fitted_preprocessor.transform(X)
        else:
            # No training has happened yet in this server session
            # Fall back to fit_transform on this data (best effort)
            X_processed = self.preprocessor.fit_transform(X)
        
        return X_processed

    def load_data(self, filepath):
        df = pd.read_csv(filepath)
        
        # 1. Handle Target
        # BRFSS: 1=Yes, 2=No. Convert to 1=Yes, 0=No
        y = df[self.target_column].astype(str).apply(lambda x: 1 if x.startswith('1') else 0).values

        # 2. Preprocess features (fit_transform for training)
        X_processed = self.preprocess_features(df)
        
        return X_processed, y

