import numpy as np
from app.fl.model import FLModel

class FLAggregator:
    def __init__(self):
        self.global_model = FLModel()
        self.round = 0
        self.client_weights = []
        self.client_sizes = []
        self.client_metrics = []  # Store real metrics from each client
        self.history = {'rounds': [], 'accuracy': [], 'loss': []}

    def reset(self):
        """Reset the federated learning state completely."""
        self.global_model = FLModel()
        self.round = 0
        self.client_weights = []
        self.client_sizes = []
        self.client_metrics = []
        self.history = {'rounds': [], 'accuracy': [], 'loss': []}

    def initialize_global_model(self):
        # PyTorch model is already initialized with random weights in FLModel.__init__
        return True

    def aggregate(self):
        """
        Federated Averaging (FedAvg)
        w_global = sum(n_k * w_k) / sum(n_k)
        """
        if not self.client_weights:
            return False

        total_samples = sum(self.client_sizes)
        
        # Initialize aggregates
        import torch
        agg_weights = {}
        first_weights = self.client_weights[0]
        for k in first_weights.keys():
            agg_weights[k] = torch.zeros_like(first_weights[k])

        for weights, n_samples in zip(self.client_weights, self.client_sizes):
            for k in weights.keys():
                agg_weights[k] += weights[k] * n_samples
                
        for k in agg_weights.keys():
            agg_weights[k] /= total_samples

        # Update global model
        self.global_model.set_weights(agg_weights)
        
        # Compute weighted average of real client metrics
        if self.client_metrics:
            weighted_acc = sum(
                m.get('accuracy', 0) * n for m, n in zip(self.client_metrics, self.client_sizes)
            ) / total_samples
            weighted_loss = sum(
                m.get('loss', 0) * n for m, n in zip(self.client_metrics, self.client_sizes)
            ) / total_samples
        else:
            weighted_acc = 0.0
            weighted_loss = 0.0

        self.history['rounds'].append(self.round + 1)
        self.history['accuracy'].append(round(weighted_acc, 4))
        self.history['loss'].append(round(weighted_loss, 4))

        # Audit Log
        try:
            from app import db
            from app.models import AuditLog
            n_clients = len(self.client_weights)
            log = AuditLog(
                action='FL Round Aggregation',
                details=f'Round {self.round+1} completed. '
                        f'{n_clients} client(s), {total_samples} total samples. '
                        f'Avg Accuracy: {weighted_acc:.4f}, Avg Loss: {weighted_loss:.4f}'
            )
            db.session.add(log)
            db.session.commit()
        except:
            pass  # Avoid breaking FL if DB fails

        # Save Global Model
        try:
            import os
            save_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            # Save versioned round
            versioned_path = os.path.join(save_dir, f'global_model_round_{self.round}.pkl')
            self.global_model.save(versioned_path)
            
            # Save latest
            latest_path = os.path.join(save_dir, 'global_model_latest.pkl')
            self.global_model.save(latest_path)
            
        except Exception as e:
            print(f"Error saving global model: {e}")

        # Clear for next round
        self.client_weights = []
        self.client_sizes = []
        self.client_metrics = []
        self.round += 1
        
        return True

    def add_client_update(self, weights, n_samples, metrics=None):
        """Store a client's trained weights, sample count, and training metrics."""
        self.client_weights.append(weights)
        self.client_sizes.append(n_samples)
        self.client_metrics.append(metrics or {})

    def get_global_model(self):
        return self.global_model

