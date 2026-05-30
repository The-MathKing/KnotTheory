import pandas as pd
import os

def run_approach_9(csv_path="data/processed/knotinfo_invariants.csv"):
    print("="*80)
    print("APPROACH 9: POSITIVE-KNOT SIGNATURE / s-INVARIANT DEEP DIVE")
    print("="*80)
    print(f"Reading dataset from {csv_path}...\n")
    
    if not os.path.exists(csv_path):
        # Fallback
        if os.path.exists("data/knotinfo_data_complete.xls"):
            csv_path = "data/knotinfo_data_complete.xls"
        elif os.path.exists("../../data/processed/knotinfo_invariants.csv"):
            csv_path = "../../data/processed/knotinfo_invariants.csv"
        else:
            print(f"[ERROR] Could not find {csv_path}, {xlsx_path}, or {xls_path}.")
            print("Please download the KnotInfo data to the 'data/' directory.")
            return
        
    try:
        if csv_path.endswith('.xlsx') or csv_path.endswith('.xls'):
            df = pd.read_excel(csv_path)
        else:
            df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return
        
    # Standardize column names (assuming KnotInfo standard headers)
    # We need: name, is_positive, is_alternating, s_invariant, signature, g3, g4, tau
    # (Adjust column names based on the actual CSV headers)
    
    # Example logic assuming standard lower-cased headers:
    try:
        # KnotInfo uses 'Y' for yes, 'N' for no in these columns.
        positive_non_alt = df[(df['positive'] == 'Y') & (df['alternating'] == 'N')]
        
        print(f"Found {len(positive_non_alt)} positive, non-alternating knots.")
        print(f"{'Knot Name':<15} | {'|s(K)|':<8} | {'|sigma(K)|':<10} | {'g3':<5} | {'g4':<5} | {'tau':<5}")
        print("-" * 65)
        
        exceptions_found = 0
        for _, row in positive_non_alt.iterrows():
            name = str(row.get('name', 'Unknown'))
            s_val = abs(float(row.get('rasmussen_invariant', 0) or 0))
            sig_val = abs(float(row.get('signature', 0) or 0))
            g3 = float(row.get('three_genus', 0) or 0)
            g4 = float(row.get('smooth_four_genus', 0) or 0)
            tau = float(row.get('ozsvath_szabo_tau_invariant', 0) or 0)
            
            print(f"{name:<15} | {s_val:<8} | {sig_val:<10} | {g3:<5} | {g4:<5} | {tau:<5}")
            
            if s_val != sig_val:
                exceptions_found += 1
                
        print("\n--- Summary ---")
        print(f"Total Positive Non-Alternating Knots Analyzed: {len(positive_non_alt)}")
        print(f"Knots where |s(K)| != |sigma(K)|: {exceptions_found}")
        
    except KeyError as e:
        print(f"[ERROR] Missing expected column in CSV: {e}")
        print("Please map the script columns to the downloaded KnotInfo headers.")

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    run_approach_9()
