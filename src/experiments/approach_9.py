import pandas as pd
import os

def run_approach_9(csv_path="data/knotinfo_data.csv"):
    print("Executing Approach 9: Positive-Knot Signature / s-invariant Deep Dive")
    print(f"Reading dataset from {csv_path}...\n")
    
    if not os.path.exists(csv_path):
        print(f"[ERROR] Could not find {csv_path}.")
        print("Please download the KnotInfo data CSV to the 'data/' directory.")
        return
        
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return
        
    # Standardize column names (assuming KnotInfo standard headers)
    # We need: name, is_positive, is_alternating, s_invariant, signature, g3, g4, tau
    # (Adjust column names based on the actual CSV headers)
    
    # Example logic assuming standard lower-cased headers:
    try:
        positive_non_alt = df[(df['positive'] == 'Y') & (df['alternating'] == 'N')]
        
        print(f"Found {len(positive_non_alt)} positive, non-alternating knots.")
        print(f"{'Knot Name':<15} | {'|s(K)|':<8} | {'|sigma(K)|':<10} | {'g3':<5} | {'g4':<5} | {'tau':<5}")
        print("-" * 65)
        
        exceptions_found = 0
        for _, row in positive_non_alt.iterrows():
            name = row.get('name', 'Unknown')
            s_val = abs(float(row.get('s_invariant', 0)))
            sig_val = abs(float(row.get('signature', 0)))
            g3 = float(row.get('seifert_genus', 0))
            g4 = float(row.get('slice_genus', 0))
            tau = float(row.get('tau', 0))
            
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
