import torch
import torch.nn as nn
import torch.nn.functional as F

class AdversarialSaliencyObjective(nn.Module):
    """
    Implements adversarial masking strategy to block direct 
    transitivity bounds from the network's loss function, forcing it to 
    evaluate complex interactions.
    """
    def __init__(self, linear_penalty=50.0):
        super(AdversarialSaliencyObjective, self).__init__()
        self.linear_penalty = linear_penalty

    def forward(self, predicted_delta, true_delta, linear_features_weight):
        """
        Penalizes the network heavily for relying on linear correlations 
        to ensure it hunts for topological blind spots (the defect).
        """
        mse_loss = F.mse_loss(predicted_delta, true_delta)
        
        # Penalize reliance on linear features (Pearson correlation masking equivalent)
        linearity_loss = self.linear_penalty * torch.norm(linear_features_weight, p=1)
        
        return mse_loss + linearity_loss
