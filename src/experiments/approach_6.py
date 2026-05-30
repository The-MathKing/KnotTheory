import pandas as pd
import numpy as np
import os
import itertools

def run_approach_6(csv_path="data/processed/knotinfo_invariants.csv"):
    print("="*80)
    print("APPROACH 6: STRUCTURAL ANALYSIS OF THE INEQUALITY GRAPH & UNCONNECTED PAIRS")
    print("="*80)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Loaded dataset with {len(df)} knots.\n")
    
    # Established edges in Jablonowski's graph:
    known_edges = {
        ('signature', 'smooth_four_genus'),
        ('signature', 'three_genus'),
        ('signature', 'unknotting_number'),
        ('smooth_four_genus', 'three_genus'),
        ('topological_four_genus', 'smooth_four_genus'),
        ('unknotting_number', 'smooth_four_genus'),
        ('ozsvath_szabo_tau_invariant', 'smooth_four_genus'),
        ('rasmussen_invariant', 'smooth_four_genus'),
        ('unknotting_number', 'crossing_number'),
        ('three_genus', 'crossing_number')
    }
    
    invariants = [
        'three_genus', 'smooth_four_genus', 'topological_four_genus', 
        'unknotting_number', 'signature', 'rasmussen_invariant', 
        'ozsvath_szabo_tau_invariant', 'turaev_genus', 'bridge_index', 'braid_index'
    ]
    
    # Convert columns to numeric
    for inv in invariants:
        if inv in df.columns:
            df[inv] = pd.to_numeric(df[inv], errors='coerce')
            
    print("Evaluating empirical ordering consistency on candidate unconnected invariant pairs...")
    print(f"{'Invariant Pair (A, B)':<45} | {'A <= B Pct':<12} | {'A >= B Pct':<12} | {'Candidate Bound'}")
    print("-" * 95)
    
    candidate_pairs = []
    
    for inv_a, inv_b in itertools.combinations(invariants, 2):
        if (inv_a, inv_b) in known_edges or (inv_b, inv_a) in known_edges:
            continue
            
        valid = df[[inv_a, inv_b]].dropna()
        if len(valid) < 100:
            continue
            
        a_vals = valid[inv_a].abs()
        b_vals = valid[inv_b].abs()
        
        le_pct = (a_vals <= b_vals).mean() * 100
        ge_pct = (a_vals >= b_vals).mean() * 100
        
        status = "None"
        if le_pct > 95.0:
            status = f"|{inv_a}| <= |{inv_b}|"
        elif ge_pct > 95.0:
            status = f"|{inv_a}| >= |{inv_b}|"
            
        print(f"({inv_a}, {inv_b})".ljust(45) + f" | {le_pct:<12.2f} | {ge_pct:<12.2f} | {status}")
        
        if status != "None":
            candidate_pairs.append((inv_a, inv_b, status, max(le_pct, ge_pct)))
            
    print("\nTop Novel Candidate Structural Orderings:")
    for a, b, cand, pct in candidate_pairs:
        print(f" - {cand} holds across {pct:.2f}% of evaluated knots.")
    print()

if __name__ == "__main__":
    run_approach_6()
