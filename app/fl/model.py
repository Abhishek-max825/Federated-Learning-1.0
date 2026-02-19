import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

class FLModel:
    def __init__(self):
        # We use SGDClassifier with 'log' loss which is equivalent to Logistic Regression
        # but supports partial_fit for incremental learning if needed,
        # and exposes simplified coefficients for aggregation.
        self.model = SGDClassifier(loss='log_loss', penalty='l2', max_iter=1000, tol=1e-3, random_state=42)
        self.scaler = StandardScaler()
        self.classes = np.array([0, 1]) # Binary classification: No Heart Disease, Heart Disease

    def train(self, X, y):
        # Using partial_fit to support online learning simulation or full fit
        # We use fit for simplicity in each round if assuming full local data pass
        self.model.fit(X, y)
    
    def get_weights(self):
        if hasattr(self.model, 'coef_'):
            return {
                'coef': self.model.coef_,
                'intercept': self.model.intercept_
            }
        return None

    def set_weights(self, weights):
        self.model.coef_ = weights['coef']
        self.model.intercept_ = weights['intercept']

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)

    def load(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
            return True
        return False
