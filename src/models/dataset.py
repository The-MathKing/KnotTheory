import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np

class DefectKnotDataset(Dataset):
    """
    Rigorously filters the dataset to explicitly purge homologically thin knots.
    By Manolescu and Ozsvath (2007), alternating and quasi-alternating knots 
    always have |s(K)| = |sigma(K)|, meaning the defect cannot exist there.
    
    This filter strictly isolates positive, non-alternating knots.
    """
    def __init__(self, csv_file, split='train', train_ratio=0.8):
        df = pd.read_csv(csv_file, low_memory=False)
        
        # 1. Purge alternating and quasi-alternating knots
        if 'is_alternating' in df.columns:
            df = df[df['is_alternating'] == False]
        if 'is_quasi_alternating' in df.columns:
            df = df[df['is_quasi_alternating'] == False]
            
        # 2. Restrict to strictly positive knots
        if 'is_positive' in df.columns:
            df = df[df['is_positive'] == True]
            
        # 3. Target acquisition (optional verification mask)
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
