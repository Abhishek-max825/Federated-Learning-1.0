import os
import pandas as pd
from app.fl.model import FLModel
from app.fl.data import FLDataHandler

class FLClient:
    def __init__(self, client_id, data_path):
        self.client_id = client_id
        self.data_path = data_path
        self.model = FLModel()
        self.data_handler = FLDataHandler()
        self.X_train = None
        self.y_train = None
        self._load_data()

    def _load_data(self):
        # Load and preprocess data
        self.X_train, self.y_train = self.data_handler.load_data(self.data_path)
        print(f"Client {self.client_id}: Loaded {len(self.X_train)} samples.")

    def update_model(self, global_weights):
        # Update local model with global weights before training
        if global_weights:
            self.model.set_weights(global_weights)

    def train(self, global_weights, data_path=None):
        """
        Train local model on private data.
        """
        # Update local model with global weights
        self.update_model(global_weights)

        # Load local data if a specific path is provided for this training round
        if data_path:
            file_path = data_path
             # Use FLDataHandler instead of undefined FLDataLoader
            data_loader = FLDataHandler()
            X_train_round, y_train_round = data_loader.load_data(file_path)
            print(f"Client {self.client_id}: Loaded {len(X_train_round)} samples for this training round from {file_path}.")
        else:
            # Use data loaded during initialization (from uploaded file or default path)
            X_train_round, y_train_round = self.X_train, self.y_train
            print(f"Client {self.client_id}: Training on {len(X_train_round)} samples from {self.data_path}.")

        # Local training
        metrics = self.model.train(X_train_round, y_train_round, epochs=20)
        
        # Extract weights
        n_samples = len(self.X_train)
        weights = self.model.get_weights()
        
        # Differential Privacy (Option 2)
        # Inject Laplacian/Gaussian noise to the weights before sending to server
        import torch
        noise_multiplier = 0.001  # Reduced noise for better accuracy
        for k in weights.keys():
            # torch.randn_like creates a tensor of random numbers with the same size
            noise = torch.randn_like(weights[k]) * noise_multiplier
            weights[k] += noise
        
        return weights, n_samples, metrics
