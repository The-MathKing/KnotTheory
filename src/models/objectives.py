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

    def forward(self, predicted_delta, true_delta, correlation_vector):
        """
        Penalizes the network heavily for relying on linear correlations 
        to ensure it hunts for topological blind spots (the defect).
        
        The penalty is defined as the L2 norm of the correlation vector
        across all 46 established linear bounds.
        """
        mse_loss = F.mse_loss(predicted_delta, true_delta)
        
        # L2 norm penalty on the 46-dimensional correlation vector
        linearity_loss = self.linear_penalty * torch.norm(correlation_vector, p=2)
        
        return mse_loss + linearity_loss
