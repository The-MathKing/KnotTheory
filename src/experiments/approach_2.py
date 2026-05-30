import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def run_approach_2(csv_path="data/processed/knotinfo_invariants.csv"):
    print("="*80)
    print("APPROACH 2: SYMBOLIC REGRESSION & EXACT RELATIONS IN SUBCLASSES")
    print("="*80)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Loaded dataset with {len(df)} knots.\n")
    
    # Subclasses to evaluate
    subclasses = {
        "Alternating Knots": df[df['alternating'] == 'Y'],
        "Two-Bridge Knots": df[df['two_bridge_notation'].notna() & (df['two_bridge_notation'] != '')],
        "Positive Braid Knots": df[df['positive_braid'] == 'Y'],
        "Strictly Positive Knots": df[df['positive'] == 'Y'],
        "Fibered Knots": df[df['fibered'] == 'Y']
    }
    
    # Target exact formulas to test across subclasses
    # 1. s(K) == -2 * tau(K) or s(K) == 2 * tau(K)
    # 2. sigma(K) == -2 * tau(K)
    # 3. 2*g4(K) == s(K)
    # 4. g3(K) == g4(K)
    
    for sub_name, sub_df in subclasses.items():
        print(f"--- Subclass: {sub_name} (N = {len(sub_df)}) ---")
        
        # Invariant numeric parsing
        s_inv = pd.to_numeric(sub_df['rasmussen_invariant'], errors='coerce')
        tau = pd.to_numeric(sub_df['ozsvath_szabo_tau_invariant'], errors='coerce')
        sig = pd.to_numeric(sub_df['signature'], errors='coerce')
        g3 = pd.to_numeric(sub_df['three_genus'], errors='coerce')
        g4 = pd.to_numeric(sub_df['smooth_four_genus'], errors='coerce')
        c_num = pd.to_numeric(sub_df['crossing_number'], errors='coerce')
        
        # Test exact relations
        # Relation 1: s vs 2*tau
        mask1 = s_inv.notna() & tau.notna()
        if mask1.sum() > 0:
            exact_match_s_tau = (s_inv[mask1] == 2 * tau[mask1]).sum()
            pct_s_tau = (exact_match_s_tau / mask1.sum()) * 100
            print(f"  Relation s(K) = 2*tau(K): Exact Match on {exact_match_s_tau}/{mask1.sum()} ({pct_s_tau:.2f}%)")
            
        # Relation 2: sigma vs -2*tau
        mask2 = sig.notna() & tau.notna()
        if mask2.sum() > 0:
            exact_match_sig_tau = (sig[mask2] == -2 * tau[mask2]).sum()
            pct_sig_tau = (exact_match_sig_tau / mask2.sum()) * 100
            print(f"  Relation sigma(K) = -2*tau(K): Exact Match on {exact_match_sig_tau}/{mask2.sum()} ({pct_sig_tau:.2f}%)")
            
        # Relation 3: 2*g4 vs s
        mask3 = g4.notna() & s_inv.notna()
        if mask3.sum() > 0:
            exact_match_g4_s = (2 * g4[mask3] == s_inv[mask3].abs()).sum()
            pct_g4_s = (exact_match_g4_s / mask3.sum()) * 100
            print(f"  Relation 2*g4(K) = |s(K)|: Exact Match on {exact_match_g4_s}/{mask3.sum()} ({pct_g4_s:.2f}%)")

        # Relation 4: g3 == g4
        mask4 = g3.notna() & g4.notna()
        if mask4.sum() > 0:
            exact_match_g3_g4 = (g3[mask4] == g4[mask4]).sum()
            pct_g3_g4 = (exact_match_g3_g4 / mask4.sum()) * 100
            print(f"  Relation g3(K) = g4(K): Exact Match on {exact_match_g3_g4}/{mask4.sum()} ({pct_g3_g4:.2f}%)")
            
        print()
        
    # Manual Hand Verification of 10 Distinct Knots across subclasses
    sample_knots = ["3_1", "4_1", "5_1", "5_2", "6_1", "7_1", "8_19", "9_42", "10_139", "12n_242"]
    print("--- Manual Verification on 10 Documented Benchmark Knots ---")
    print(f"{'Knot':<10} | {'Alternating':<12} | {'s(K)':<6} | {'tau(K)':<8} | {'sigma(K)':<10} | {'g3':<5} | {'g4':<5}")
    print("-" * 65)
    for k_name in sample_knots:
        row = df[df['name'] == k_name]
        if len(row) > 0:
            r = row.iloc[0]
            alt = str(r.get('alternating', 'N/A'))
            s = str(r.get('rasmussen_invariant', 'N/A'))
            t = str(r.get('ozsvath_szabo_tau_invariant', 'N/A'))
            sig_val = str(r.get('signature', 'N/A'))
            g3_val = str(r.get('three_genus', 'N/A'))
            g4_val = str(r.get('smooth_four_genus', 'N/A'))
            print(f"{k_name:<10} | {alt:<12} | {s:<6} | {t:<8} | {sig_val:<10} | {g3_val:<5} | {g4_val:<5}")
    print()

if __name__ == "__main__":
    run_approach_2()
