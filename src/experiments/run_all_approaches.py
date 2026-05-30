import sys
import os
import io

# Ensure src/ is on python path
sys.path.insert(0, os.getcwd())

from src.experiments.approach_1 import run_approach_1
from src.experiments.approach_2 import run_approach_2
from src.experiments.approach_3 import run_approach_3
from src.experiments.approach_4 import run_approach_4
from src.experiments.approach_5 import run_approach_5
from src.experiments.approach_6 import run_approach_6
from src.experiments.approach_7 import run_approach_7
from src.experiments.approach_8 import run_approach_8
from src.experiments.approach_9 import run_approach_9
from src.experiments.approach_10 import run_approach_10

def main():
    print("="*80)
    print("EXECUTING ALL 10 EMPIRICAL KNOT THEORY EXPERIMENTAL APPROACHES")
    print("="*80)
    
    approaches = [
        ("Approach 1: Inequality-Slack Mining", run_approach_1),
        ("Approach 2: Subclass Symbolic Regression", run_approach_2),
        ("Approach 3: Joint Anomaly Detection", run_approach_3),
        ("Approach 4: Saliency-Based Candidate Discovery", run_approach_4),
        ("Approach 5: Extremal Statistics across Crossing Number", run_approach_5),
        ("Approach 6: Structural Inequality Graph Analysis", run_approach_6),
        ("Approach 7: Near-Violation Conjectural Study", run_approach_7),
        ("Approach 8: Derived vs Exact Invariant Cross-Validation", run_approach_8),
        ("Approach 9: Positive-Knot Signature / s-Invariant Deep Dive", run_approach_9),
        ("Approach 10: Boundary & Family Testing", run_approach_10)
    ]
    
    for idx, (title, func) in enumerate(approaches, 1):
        print(f"\n[{idx}/10] Running {title}...")
        try:
            func()
            print(f"[SUCCESS] Completed Approach {idx}.")
        except Exception as e:
            print(f"[ERROR] Failed Approach {idx}: {e}")

if __name__ == "__main__":
    main()
