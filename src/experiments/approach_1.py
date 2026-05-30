import pandas as pd
import numpy as np
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text

def run_approach_1(csv_path="data/processed/knotinfo_invariants.csv"):
    print("="*80)
    print("APPROACH 1: INEQUALITY-SLACK MINING & TIGHTNESS PREDICTION")
    print("="*80)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Loaded dataset with {len(df)} knots.\n")
    
    # Define classical inequalities to mine
    # Format: (Name, Left Invariant expr, Right Invariant expr, Left Col, Right Col, Multiplier, Abs Left)
    inequalities = [
        ("Sigma <= 2*g4", "signature", "smooth_four_genus", 2.0, True),
        ("g4 <= g3", "smooth_four_genus", "three_genus", 1.0, False),
        ("Sigma <= 2*u", "signature", "unknotting_number", 2.0, True),
        ("|tau| <= g4", "ozsvath_szabo_tau_invariant", "smooth_four_genus", 1.0, True),
        ("|s| <= 2*g4", "rasmussen_invariant", "smooth_four_genus", 2.0, True),
        ("g4_top <= g4", "topological_four_genus", "smooth_four_genus", 1.0, False),
        ("u <= c", "unknotting_number", "crossing_number", 1.0, False),
    ]
    
    # Potential predictor features
    candidate_features = [
        'crossing_number', 'three_genus', 'determinant', 'bridge_index', 
        'braid_index', 'braid_length', 'volume', 'turaev_genus', 
        'arc_index'
    ]
    
    results = []
    
    for ineq_name, left_col, right_col, mult, abs_left in inequalities:
        if left_col not in df.columns or right_col not in df.columns:
            continue
            
        cols = list(dict.fromkeys(['name', left_col, right_col] + [c for c in candidate_features if c in df.columns]))
        sub_df = df[cols].copy()
        sub_df[left_col] = pd.to_numeric(sub_df[left_col], errors='coerce')
        sub_df[right_col] = pd.to_numeric(sub_df[right_col], errors='coerce')
        
        valid = sub_df.dropna(subset=[left_col, right_col]).copy()
        if len(valid) == 0:
            continue
            
        left_val = valid[left_col].abs() if abs_left else valid[left_col]
        right_val = valid[right_col] * mult
        
        slack = right_val - left_val
        valid['slack'] = slack
        
        # Filter out negative slacks (errors or undefined)
        valid = valid[valid['slack'] >= 0]
        
        total_valid = len(valid)
        tight_count = (valid['slack'] == 0).sum()
        tight_pct = (tight_count / total_valid) * 100 if total_valid > 0 else 0
        
        print(f"--- Inequality: {ineq_name} ---")
        print(f"Evaluated Knots: {total_valid}")
        print(f"Tight (Slack = 0): {tight_count} ({tight_pct:.2f}%) | Loose (Slack > 0): {total_valid - tight_count} ({100 - tight_pct:.2f}%)")
        print(f"Slack Distribution: Mean={slack.mean():.3f}, Std={slack.std():.3f}, Min={slack.min():.1f}, Median={slack.median():.1f}, Max={slack.max():.1f}")
        
        # Predict tightness using third invariants
        feat_df = valid[[c for c in candidate_features if c in valid.columns]].apply(pd.to_numeric, errors='coerce').fillna(0)
        y = (valid['slack'] == 0).astype(int)
        
        if len(y.unique()) > 1 and len(feat_df.columns) > 0:
            clf = DecisionTreeClassifier(max_depth=3, random_state=42)
            clf.fit(feat_df, y)
            importances = dict(zip(feat_df.columns, clf.feature_importances_))
            top_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"Top 3 Predictors of Tightness: {', '.join([f'{k} ({v:.3f})' for k, v in top_features if v > 0])}")
        print()
        
        results.append({
            "inequality": ineq_name,
            "evaluated": total_valid,
            "tight_pct": tight_pct,
            "mean_slack": slack.mean(),
            "max_slack": slack.max()
        })
        
    return results

if __name__ == "__main__":
    run_approach_1()
