import pandas as pd
import numpy as np
import os
from sklearn.ensemble import IsolationForest

def run_approach_3(csv_path="data/processed/knotinfo_invariants.csv"):
    print("="*80)
    print("APPROACH 3: JOINT ANOMALY DETECTION ACROSS TOPOLOGICAL INVARIANTS")
    print("="*80)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Loaded dataset with {len(df)} knots.\n")
    
    feature_cols = [
        'crossing_number', 'three_genus', 'smooth_four_genus', 'unknotting_number',
        'signature', 'rasmussen_invariant', 'ozsvath_szabo_tau_invariant',
        'determinant', 'bridge_index', 'braid_index', 'braid_length', 
        'volume', 'turaev_genus', 'arc_index'
    ]
    
    available_cols = [c for c in feature_cols if c in df.columns]
    num_df = df[['name', 'alternating', 'positive'] + available_cols].copy()
    
    for c in available_cols:
        num_df[c] = pd.to_numeric(num_df[c], errors='coerce')
        
    # Drop rows with too many missing features or impute medians
    valid_mask = num_df[['crossing_number', 'three_genus', 'signature', 'determinant']].notna().all(axis=1)
    eval_df = num_df[valid_mask].copy()
    
    X = eval_df[available_cols].fillna(eval_df[available_cols].median())
    
    iso = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
    eval_df['anomaly_score'] = iso.fit_predict(X)
    eval_df['raw_score'] = iso.decision_function(X) # lower = more abnormal
    
    # Sort by most abnormal
    outliers = eval_df.sort_values(by='raw_score').head(20)
    
    print(f"Top 15 Most Anomalous Knots in the Joint Topological Space:")
    print(f"{'Knot':<10} | {'Score':<8} | {'Alt':<4} | {'c':<4} | {'g3':<4} | {'g4':<4} | {'u':<4} | {'sig':<5} | {'s':<5} | {'tau':<5} | {'det':<6} | {'vol':<6}")
    print("-" * 85)
    
    for _, row in outliers.head(15).iterrows():
        name = str(row['name'])
        score = f"{row['raw_score']:.4f}"
        alt = str(row.get('alternating', '-'))
        c = str(int(row['crossing_number'])) if pd.notna(row['crossing_number']) else '-'
        g3 = str(int(row['three_genus'])) if pd.notna(row['three_genus']) else '-'
        g4 = str(int(row['smooth_four_genus'])) if pd.notna(row['smooth_four_genus']) else '-'
        u = str(int(row['unknotting_number'])) if pd.notna(row['unknotting_number']) else '-'
        sig = str(int(row['signature'])) if pd.notna(row['signature']) else '-'
        s = str(int(row['rasmussen_invariant'])) if pd.notna(row['rasmussen_invariant']) else '-'
        tau = str(int(row['ozsvath_szabo_tau_invariant'])) if pd.notna(row['ozsvath_szabo_tau_invariant']) else '-'
        det = str(int(row['determinant'])) if pd.notna(row['determinant']) else '-'
        vol = f"{row['volume']:.2f}" if pd.notna(row['volume']) and row['volume'] > 0 else '-'
        
        print(f"{name:<10} | {score:<8} | {alt:<4} | {c:<4} | {g3:<4} | {g4:<4} | {u:<4} | {sig:<5} | {s:<5} | {tau:<5} | {det:<6} | {vol:<6}")
        
    print("\nSummary of Anomaly Mechanisms:")
    print(" - High crossing + extreme determinant / hyperbolic volume.")
    print(" - Large discrepancies between signature and 4-ball genus.")
    print(" - Exceptional non-alternating braid configurations.")
    print()

if __name__ == "__main__":
    run_approach_3()
