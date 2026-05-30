import sys
import os

sys.path.insert(0, os.getcwd())

from src.experiments.deep_dive_defect import run_deep_dive_defect
from src.experiments.deep_dive_turaev import run_deep_dive_turaev
from src.experiments.deep_dive_concordance import run_deep_dive_concordance

def main():
    print("="*80)
    print("RUNNING ALL 15 IN-DEPTH EXPERIMENTAL TESTS ACROSS THE 3 KEY DISCOVERY AREAS")
    print("="*80)
    
    print("\n>>> EXECUTING SUITE A (DEFECT IN-DEPTH: TESTS D1 - D5)...")
    run_deep_dive_defect()
    
    print("\n>>> EXECUTING SUITE B (TURAEV GENUS IN-DEPTH: TESTS T1 - T5)...")
    run_deep_dive_turaev()
    
    print("\n>>> EXECUTING SUITE C (CONCORDANCE SLACK IN-DEPTH: TESTS C1 - C5)...")
    run_deep_dive_concordance()
    
    print("\n" + "="*80)
    print("ALL 15 IN-DEPTH TESTS COMPLETED SUCCESSFULLY!")
    print("="*80)

if __name__ == "__main__":
    main()
