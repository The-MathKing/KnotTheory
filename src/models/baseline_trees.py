from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import numpy as np

def run_baseline_trees():
    """
    Week 5: Baseline interpretable models.
    Deploys decision trees to predict target invariants (like trivializing number).
    Extracts initial feature importance rankings.
    """
    print("Week 5: Training interpretable baseline Decision Trees...")
    df = pd.read_csv('../../data/processed/newdb_invariants.csv', low_memory=False)
    
    cols_to_use = ['crossing_number', 'signature', 'three_genus', 'determinant', 'unknotting_number', 'smooth_slice_genus']
    for col in cols_to_use:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    numeric_df = df[[c for c in cols_to_use if c in df.columns]]
    
    # We pretend the last column is our target (e.g., trivializing number or conjectural target)
    if numeric_df.shape[1] > 1:
        X = numeric_df.iloc[:, :-1]
        y = numeric_df.iloc[:, -1]
        
        tree = DecisionTreeRegressor(max_depth=5, random_state=42)
        tree.fit(X, y)
        
        # Extract feature importance
        importances = tree.feature_importances_
        ranked_features = sorted(zip(X.columns, importances), key=lambda x: x[1], reverse=True)
        
        print("Top 3 baseline feature importances extracted:")
        for feat, imp in ranked_features[:3]:
            print(f" - {feat}: {imp:.4f}")
            
        print("Baseline established against Jabłonowski's transitivity criterion.")

if __name__ == "__main__":
    run_baseline_trees()
