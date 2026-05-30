import pandas as pd
import numpy as np
import os

def run_approach_8(csv_path="data/processed/knotinfo_invariants.csv"):
    print("="*80)
    print("APPROACH 8: CROSS-VALIDATION OF DERIVED VS DIRECT INVARIANTS")
    print("="*80)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Loaded dataset with {len(df)} knots.\n")
    
    # In KnotInfo/NewDB, bounds on smooth four genus g4 are often derived via:
    # Lower Bound = max(|tau|, |s|/2, |sigma|/2)
    # Upper Bound = min(g3, u)
    
    sub = df[['name', 'alternating', 'three_genus', 'smooth_four_genus', 'unknotting_number', 
              'signature', 'rasmussen_invariant', 'ozsvath_szabo_tau_invariant']].copy()
    
    for col in ['three_genus', 'smooth_four_genus', 'unknotting_number', 'signature', 
                'rasmussen_invariant', 'ozsvath_szabo_tau_invariant']:
        sub[col] = pd.to_numeric(sub[col], errors='coerce')
        
    sub['derived_lower_g4'] = np.maximum(
        sub['ozsvath_szabo_tau_invariant'].abs().fillna(0),
        np.maximum(
            sub['rasmussen_invariant'].abs().fillna(0) / 2.0,
            sub['signature'].abs().fillna(0) / 2.0
        )
    )
    
    sub['derived_upper_g4'] = np.minimum(
        sub['three_genus'].fillna(999),
        sub['unknotting_number'].fillna(999)
    )
    
    # Find sample where derived bounds pinch g4 exactly (lower == upper) vs slack
    pinched = sub[(sub['derived_lower_g4'] == sub['derived_upper_g4']) & sub['smooth_four_genus'].notna()]
    slack = sub[(sub['derived_lower_g4'] < sub['derived_upper_g4']) & sub['smooth_four_genus'].notna()]
    
    print(f"Derived Bound Verification across {len(sub.dropna(subset=['smooth_four_genus']))} knots:")
    print(f" - Pinched Exactly (Lower == Upper == g4): {len(pinched)} knots ({(len(pinched)/len(sub))*100:.1f}%)")
    print(f" - Gap/Slack (Lower < Upper): {len(slack)} knots ({(len(slack)/len(sub))*100:.1f}%)")
    
    print("\nSample Cross-Validation of 15 Knots (Exact g4 vs Derived Bounds):")
    print(f"{'Knot':<10} | {'Alt':<4} | {'Exact g4':<10} | {'Derived Lower':<14} | {'Derived Upper':<14} | {'Tight/Gap'}")
    print("-" * 75)
    
    sample = pd.concat([pinched.head(8), slack.head(7)])
    for _, r in sample.iterrows():
        name = str(r['name'])
        alt = str(r.get('alternating', '-'))
        g4_val = f"{r['smooth_four_genus']:.0f}"
        low_val = f"{r['derived_lower_g4']:.1f}"
        up_val = f"{r['derived_upper_g4']:.0f}" if r['derived_upper_g4'] < 900 else "N/A"
        tight_str = "TIGHT" if float(low_val) == float(g4_val) == float(up_val if up_val != 'N/A' else -1) else "SLACK GAP"
        print(f"{name:<10} | {alt:<4} | {g4_val:<10} | {low_val:<14} | {up_val:<14} | {tight_str}")
    print()

if __name__ == "__main__":
    run_approach_8()
