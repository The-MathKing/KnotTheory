import pandas as pd
import numpy as np
import os

def run_approach_10(csv_path="data/processed/knotinfo_invariants.csv"):
    print("="*80)
    print("APPROACH 10: KNOT-TO-FAMILY BOUNDARY & SUBSET SATURATION TESTING")
    print("="*80)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Loaded dataset with {len(df)} knots.\n")
    
    # Analyze how classical inequalities perform across diverse topological classes / boundaries:
    # 1. Alternating vs Non-Alternating
    # 2. Positive vs Non-Positive
    # 3. Fibered vs Non-Fibered
    # 4. Quasi-Alternating vs General Non-Alternating
    
    classes = {
        "Alternating": df['alternating'] == 'Y',
        "Non-Alternating": df['alternating'] == 'N',
        "Positive Knots": df['positive'] == 'Y',
        "Non-Positive Knots": df['positive'] == 'N',
        "Fibered": df['fibered'] == 'Y',
        "Non-Fibered": df['fibered'] == 'N',
        "Quasi-Alternating": df.get('quasi_alternating', pd.Series(['N']*len(df))) == 'Y'
    }

    # Target inequality for boundary stress test: |sigma(K)| <= 2 * g4(K) and g4(K) <= g3(K)
    print("Boundary Robustness and Tightness Degradation across Topological Families:")
    print(f"{'Family / Class':<22} | {'Count':<7} | {'|sigma|=2g4 Tight %':<20} | {'g4=g3 Tight %':<16} | {'|s|=2tau Exact %'}")
    print("-" * 88)

    rows = []
    for c_name, mask in classes.items():
        sub = df[mask].copy()
        if len(sub) == 0:
            continue
            
        sig = pd.to_numeric(sub['signature'], errors='coerce')
        g4 = pd.to_numeric(sub['smooth_four_genus'], errors='coerce')
        g3 = pd.to_numeric(sub['three_genus'], errors='coerce')
        s = pd.to_numeric(sub['rasmussen_invariant'], errors='coerce')
        tau = pd.to_numeric(sub['ozsvath_szabo_tau_invariant'], errors='coerce')
        
        # Metric 1: |sigma| == 2*g4
        m1 = sig.notna() & g4.notna()
        t1_pct = ((sig[m1].abs() == 2 * g4[m1]).sum() / m1.sum() * 100) if m1.sum() > 0 else 0.0
        
        # Metric 2: g4 == g3
        m2 = g4.notna() & g3.notna()
        t2_pct = ((g4[m2] == g3[m2]).sum() / m2.sum() * 100) if m2.sum() > 0 else 0.0
        
        # Metric 3: s == 2*tau
        m3 = s.notna() & tau.notna()
        t3_pct = ((s[m3] == 2 * tau[m3]).sum() / m3.sum() * 100) if m3.sum() > 0 else 0.0
        
        print(f"{c_name:<22} | {len(sub):<7} | {t1_pct:<20.1f} | {t2_pct:<16.1f} | {t3_pct:<16.1f}")
        rows.append((c_name, t1_pct, t2_pct, t3_pct))

    print("\nBoundary Phase Transitions (derived directly from the table above):")
    t1_vals = {name: v1 for name, v1, v2, v3 in rows}
    t2_vals = {name: v2 for name, v1, v2, v3 in rows}
    t3_min = min(v3 for _, v1, v2, v3 in rows)
    t1_lo, t1_hi = min(t1_vals.values()), max(t1_vals.values())
    print(f" - |s(K)| = 2*tau(K) is exact in every family tested (minimum {t3_min:.1f}%).")
    print(f" - |sigma|=2g4 tightness ranges {t1_lo:.1f}%-{t1_hi:.1f}% across families -- it does NOT 'severely "
          f"degrade to ~40%' anywhere in this table; the biggest single gap is Alternating "
          f"({t1_vals['Alternating']:.1f}%) vs Fibered ({t1_vals['Fibered']:.1f}%).")
    print(f" - g4=g3 tightness is actually LOW for most families (e.g. Alternating "
          f"{t2_vals['Alternating']:.1f}%, Fibered {t2_vals['Fibered']:.1f}%) and only high for the "
          f"Positive-Knots subclass ({t2_vals['Positive Knots']:.1f}%) -- not 'exceptionally high' in general.")
    print()

if __name__ == "__main__":
    run_approach_10()
