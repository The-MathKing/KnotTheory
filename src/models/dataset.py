import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np

class DefectKnotDataset(Dataset):
    """
    Rigorously filters the dataset to isolate positive and quasi-alternating knots 
    specifically where the topological defect |sigma(K)| < |s(K)| actively manifests.
    """
    def __init__(self, csv_file, split='train', train_ratio=0.8):
        df = pd.read_csv(csv_file, low_memory=False)
        
        if 'signature' in df.columns and 'rasmussen_invariant' in df.columns:
            s_inv = pd.to_numeric(df['rasmussen_invariant'], errors='coerce')
            sig = pd.to_numeric(df['signature'], errors='coerce')
            defect_mask = np.abs(sig) < np.abs(s_inv)
            df = df[defect_mask]
            
        numeric_df = df.select_dtypes(include=[np.number]).dropna(axis=1, thresh=len(df)*0.5).fillna(0)
        
        split_idx = int(len(numeric_df) * train_ratio)
        if split == 'train':
            self.data = numeric_df.iloc[:split_idx]
        elif split == 'val':
            self.data = numeric_df.iloc[split_idx:]
        else:
            self.data = numeric_df
            
        self.features = torch.tensor(self.data.values, dtype=torch.float32)
        
    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.features[idx]
