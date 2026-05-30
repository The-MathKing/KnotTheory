import pandas as pd
import numpy as np
import os

def run_approach_7(csv_path="data/processed/knotinfo_invariants.csv"):
    print("="*80)
    print("APPROACH 7: NEAR-VIOLATION STUDY OF CANDIDATE CONJECTURAL BOUNDS")
    print("="*80)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Loaded dataset with {len(df)} knots.\n")
    
    # Candidate / Conjectural inequalities
    # Format: (Title, Formula description, lambda df -> slack)
    conjectures = [
        (
            "Conj 1: |tau(K)| <= g4_top(K)",
            lambda d: d['topological_four_genus'] - d['ozsvath_szabo_tau_invariant'].abs()
        ),
        (
            "Conj 2: |s(K)|/2 <= g4_top(K)",
            lambda d: d['topological_four_genus'] - (d['rasmussen_invariant'].abs() / 2.0)
        ),
        (
            "Conj 3: u(K) >= g4(K) + Turaev(K)",
            lambda d: d['unknotting_number'] - (d['smooth_four_genus'] + d['turaev_genus'])
        ),
        (
            "Conj 4: g3(K) >= g4(K) + Turaev(K)",
            lambda d: d['three_genus'] - (d['smooth_four_genus'] + d['turaev_genus'])
        ),
        (
            "Conj 5: |sigma(K)|/2 <= u(K) - Turaev(K)",
            lambda d: (d['unknotting_number'] - d['turaev_genus']) - (d['signature'].abs() / 2.0)
        )
    ]
    
    for title, slack_fn in conjectures:
        print(f"--- {title} ---")
        
        # Prepare numeric subset
        cols_needed = ['name', 'three_genus', 'smooth_four_genus', 'topological_four_genus', 
                       'unknotting_number', 'signature', 'rasmussen_invariant', 
                       'ozsvath_szabo_tau_invariant', 'turaev_genus']
        
        sub = df[[c for c in cols_needed if c in df.columns]].copy()
        for c in sub.columns:
            if c != 'name':
                sub[c] = pd.to_numeric(sub[c], errors='coerce')
                
        try:
            sub['slack'] = slack_fn(sub)
            valid = sub.dropna(subset=['slack']).copy()
            
            violations = valid[valid['slack'] < 0]
            tight = valid[valid['slack'] == 0]
            near_misses = valid[valid['slack'] > 0].sort_values(by='slack').head(5)
            
            print(f"Total Evaluated: {len(valid)} | Violations: {len(violations)} | Exact Boundary (Slack=0): {len(tight)}")
            
            if len(violations) > 0:
                print(f"  [DISPROVEN]: Discovered {len(violations)} counterexamples! First 3 counterexamples:")
                for _, r in violations.head(3).iterrows():
                    print(f"    - {r['name']} (Slack = {r['slack']:.1f})")
            else:
                print(f"  [SURVIVED]: 0 violations found. 5 Closest-to-Violating Knots (Slack > 0):")
                for _, r in near_misses.iterrows():
                    print(f"    - {r['name']}: Slack = {r['slack']:.1f} | g3={r.get('three_genus', '-')}, g4={r.get('smooth_four_genus', '-')}, u={r.get('unknotting_number', '-')}, sig={r.get('signature', '-')}")
        except Exception as e:
            print(f"  Calculation error: {e}")
        print()

if __name__ == "__main__":
    run_approach_7()
