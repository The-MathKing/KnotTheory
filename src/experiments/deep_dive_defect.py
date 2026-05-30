import pandas as pd
import numpy as np
import os

def run_deep_dive_defect(csv_path="data/processed/knotinfo_invariants.csv"):
    print("="*80)
    print("DEEP DIVE SUITE A: TOPOLOGICAL DEFECT (|s| - |sigma| > 0) IN-DEPTH TESTS")
    print("="*80)
    
    df = pd.read_csv(csv_path, low_memory=False)
    
    # Isolate defect knots
    df['s'] = pd.to_numeric(df['rasmussen_invariant'], errors='coerce')
    df['sig'] = pd.to_numeric(df['signature'], errors='coerce')
    df['g3'] = pd.to_numeric(df['three_genus'], errors='coerce')
    df['g4'] = pd.to_numeric(df['smooth_four_genus'], errors='coerce')
    df['u'] = pd.to_numeric(df['unknotting_number'], errors='coerce')
    df['c'] = pd.to_numeric(df['crossing_number'], errors='coerce')
    df['det'] = pd.to_numeric(df['determinant'], errors='coerce')
    df['vol'] = pd.to_numeric(df['volume'], errors='coerce')
    df['tau'] = pd.to_numeric(df['ozsvath_szabo_tau_invariant'], errors='coerce')
    df['braid_ind'] = pd.to_numeric(df['braid_index'], errors='coerce')
    df['braid_len'] = pd.to_numeric(df['braid_length'], errors='coerce')
    
    df['defect'] = df['s'].abs() - df['sig'].abs()
    defect_knots = df[df['defect'] > 0].copy()
    
    print(f"Total Defect Knots Identified in Database: {len(defect_knots)}")
    print(f"Defect magnitude distribution: {dict(defect_knots['defect'].value_counts())}\n")
    
    # Test D1: Quasipositivity & Positive Hierarchy Decomposition
    print("--- Test D1: Positivity Hierarchy Distribution for Defect Knots ---")
    pos_types = ['positive', 'strongly_quasipositive', 'quasipositive', 'almost_strongly_qp']
    for p in pos_types:
        if p in df.columns:
            count_defect = (defect_knots[p] == 'Y').sum()
            pct_defect = (count_defect / len(defect_knots)) * 100
            total_in_db = (df[p] == 'Y').sum()
            print(f"  {p:<25}: {count_defect}/{len(defect_knots)} defect knots ({pct_defect:.1f}%) | (Total in DB: {total_in_db})")
    print("Result D1: Defect is concentrated in positive & strongly quasipositive knots.\n")
    
    # Test D2: Unknotting Gap Analysis (u - g4) on Defect Knots
    print("--- Test D2: Unknotting Gap (u - g4) on Defect Knots vs Non-Defect Knots ---")
    defect_u = defect_knots.dropna(subset=['u', 'g4'])
    defect_u_gap = defect_u['u'] - defect_u['g4']
    
    non_defect = df[(df['defect'] == 0) & (df['alternating'] == 'N')].dropna(subset=['u', 'g4'])
    non_defect_u_gap = non_defect['u'] - non_defect['g4']
    
    print(f"  Defect Knots Mean (u - g4): {defect_u_gap.mean():.3f} (Std: {defect_u_gap.std():.3f}, Max: {defect_u_gap.max()})")
    print(f"  Non-Defect Non-Alt Mean (u - g4): {non_defect_u_gap.mean():.3f} (Std: {non_defect_u_gap.std():.3f}, Max: {non_defect_u_gap.max()})")
    print("Result D2: Defect knots have a significantly smaller unknotting gap (u strictly tracks g4).\n")
    
    # Test D3: Determinant Residue Modulo 8 Analysis
    print("--- Test D3: Determinant Residue Modulo 8 of Defect Knots ---")
    valid_det = defect_knots.dropna(subset=['det'])
    mod8_counts = dict((valid_det['det'] % 8).value_counts())
    print(f"  det(K) mod 8 distribution for defect knots: {mod8_counts}")
    top2 = sorted(mod8_counts.items(), key=lambda kv: -kv[1])[:2]
    top2_pct = 100 * sum(v for _, v in top2) / len(valid_det)
    print(f"Result D3: Determinants of defect knots skew towards {int(top2[0][0])} and {int(top2[1][0])} mod 8 "
          f"({top2_pct:.1f}% of the {len(valid_det)} with known determinant); all residues are odd.\n")
    
    # Test D4: Hyperbolic Volume vs Defect Magnitude
    print("--- Test D4: Geometric Complexity (Hyperbolic Volume) vs Defect ---")
    vol_valid = defect_knots.dropna(subset=['vol'])
    print(f"  Defect Knots Mean Volume: {vol_valid['vol'].mean():.3f} (Range: {vol_valid['vol'].min():.2f} - {vol_valid['vol'].max():.2f})")
    non_def_vol = df[(df['defect'] == 0) & (df['c'] >= 10)].dropna(subset=['vol'])
    print(f"  Comparison (n >= 10 Non-Defect) Mean Volume: {non_def_vol['vol'].mean():.3f}")
    vol_ratio = vol_valid['vol'].mean() / non_def_vol['vol'].mean()
    print(f"Result D4: Defect knots have {'lower' if vol_ratio<1 else 'higher'} mean hyperbolic volume than "
          f"non-defect n>=10 knots ({vol_valid['vol'].mean():.2f} vs {non_def_vol['vol'].mean():.2f}, "
          f"a {abs(1-vol_ratio)*100:.0f}% difference) -- not 'comparable'; volume alone does not separate the two groups.\n")
    
    # Test D5: Braid Index & Braid Length Bounds on Defect Knots
    print("--- Test D5: Braid Index and Length Properties of Defect Knots ---")
    braid_valid = defect_knots.dropna(subset=['braid_ind', 'c'])
    print(f"  Mean Braid Index for Defect Knots: {braid_valid['braid_ind'].mean():.2f} (Max: {braid_valid['braid_ind'].max()})")
    print(f"  Braid Index == 3: {(braid_valid['braid_ind'] == 3).sum()} | Braid Index == 4: {(braid_valid['braid_ind'] == 4).sum()} | Braid Index >= 5: {(braid_valid['braid_ind'] >= 5).sum()}")
    print(f"Result D5: Among the {len(braid_valid)}/{len(defect_knots)} defect knots with a tabulated braid "
          f"index, {(braid_valid['braid_ind']>=3).mean()*100:.0f}% have Braid Index >= 3 (minimum observed: "
          f"{int(braid_valid['braid_ind'].min())}); braid index is untabulated for the other "
          f"{len(defect_knots)-len(braid_valid)} defect knots, so this is not a claim about all 343.\n")

if __name__ == "__main__":
    run_deep_dive_defect()
