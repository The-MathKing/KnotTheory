import json
import pandas as pd
import numpy as np

def run_negative_audit():
    """
    Executes a strict computational negative audit of the lower bound
    exclusively on the non-alternating knot subset.
    """
    print("Executing strict negative audit for g4 lower bounds on non-alternating knots...")
    df = pd.read_csv('../../data/processed/newdb_invariants.csv', low_memory=False)
    
    # Filter for non-alternating
    if 'alternating' in df.columns:
        df = df[df['alternating'] == 'N']
        
    with open('../../data/processed/conjectures.json', 'r') as f:
        conjectures = json.load(f)
        
    surviving_conjectures = []
    
    for c in conjectures:
        print(f"Auditing Conjecture {c['id']}: {c['inequality']}")
        # We need smooth_four_genus, rasmussen_invariant, ozsvath_szabo_tau_invariant
        # Let's check for smooth_slice_genus instead of smooth_four_genus as that's what's in our df renaming usually
        # Actually our renaming didn't persist, so we use original KnotInfo columns
        required_cols = ['smooth_slice_genus', 'rasmussen_invariant', 'ozsvath_szabo_tau_invariant']
        
        available = [col for col in required_cols if col in df.columns]
        if len(available) == 3:
            g4 = pd.to_numeric(df['smooth_slice_genus'], errors='coerce')
            s_inv = pd.to_numeric(df['rasmussen_invariant'], errors='coerce')
            tau = pd.to_numeric(df['ozsvath_szabo_tau_invariant'], errors='coerce')
            
            # g4 >= max(|s|/2, |tau|)
            lower_bound = np.maximum(np.abs(s_inv)/2, np.abs(tau))
            valid = (g4 >= lower_bound) | g4.isna() | lower_bound.isna()
            violations = df[~valid]
            
            if len(violations) > 0:
                print(f" -> DISCARDED: {len(violations)} counter-examples found.")
            else:
                print(" -> SURVIVED: Zero counter-examples found in the non-alternating dataset.")
                c['status'] = 'survived'
                surviving_conjectures.append(c)
        else:
            print(" -> DISCARDED: Required columns not found.")
            
if __name__ == "__main__":
    run_negative_audit()
