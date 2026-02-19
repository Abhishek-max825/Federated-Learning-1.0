import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class FLDataHandler:
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
        # Based on BRFSS and dataset inspection
        # We process all categorical features as strings to handle mixed types
        self.categories = {
            'age_group': ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0'],
            'sex': ['1.0', '2.0'],
            'smoked_100_cigarettes': ['1.0', '2.0', 'Unknown'],
            # Diabetes: 1=Yes, 2=Yes(Pregnancy), 3=No, 4=Pre-diabetes, etc.
            'diabetes_diagnosis': ['1.0', '2.0', '3.0', '4.0', 'Unknown'], 
            'heart_attack_history': ['1.0', '2.0', 'Unknown'],
            'stroke_history': ['1.0', '2.0', 'Unknown']
        }

        self.preprocessor = self._build_preprocessor()

    def _build_preprocessor(self):
        # Numerical transformer: replace 'Unknown' with NaN then mean impute
        # But 'bmi' in CSV has strings '2953.0' and 'Unknown'. 
        # We need a custom cleaner first, then SimpleImputer.
        # Since sklearn transform expects numeric input for SimpleImputer usually, 
        # we will handle the 'Unknown' -> NaN conversion in load_data manually before passing to sklearn pipeline 
        # for the numeric column.
        
        numerical_transformer = SimpleImputer(strategy='mean')

        # Categorical transformer
        # We need to pass the categories list in order
        cats = [self.categories[c] for c in self.categorical_features]
        # handle_unknown='ignore' is crucial if unexpected values appear
        categorical_transformer = OneHotEncoder(categories=cats, handle_unknown='ignore', sparse_output=False)

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, self.numerical_features),
                ('cat', categorical_transformer, self.categorical_features)
            ]
        )
        return preprocessor

    def load_data(self, filepath):
        df = pd.read_csv(filepath)
        
        # 1. Handle Target
        # BRFSS: 1=Yes, 2=No. Convert to 1=Yes, 0=No
        # Robustly handle mixed types (float 1.0 vs string '1.0')
        y = df[self.target_column].astype(str).apply(lambda x: 1 if x.startswith('1') else 0).values

    def preprocess_features(self, df):
        # 1. Handle BMI 'Unknown' and convert to float
        if 'bmi' in df.columns:
            df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
        
        # 2. Handle features: Convert categorical columns to string
        for col in self.categorical_features:
            if col in df.columns:
                df[col] = df[col].astype(str)

        X = df[self.feature_columns]
        
        # 3. Fit/Transform
        # For inference (single sample), fit_transform will use the sample itself if SimpleImputer is needed.
        # Since OneHotEncoder has fixed categories, fit doesn't change it.
        # Ideally, we should fit SimpleImputer on global state, but for FL simulation, 
        # local fit (or single sample fit) is acceptable given we enforce categories.
        X_processed = self.preprocessor.fit_transform(X)
        return X_processed

    def load_data(self, filepath):
        df = pd.read_csv(filepath)
        
        # 1. Handle Target
        y = df[self.target_column].astype(str).apply(lambda x: 1 if x.startswith('1') else 0).values

        # 2. Preprocess features
        X_processed = self.preprocess_features(df)
        
        return X_processed, y
