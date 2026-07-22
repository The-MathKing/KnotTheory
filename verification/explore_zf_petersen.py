"""
Explore Z(P(n,k)) for k >= 4 -- the range the 2026 erratum (arXiv 2607.19412)
does not address. Known published results, used as validation elsewhere:
  Z(P(n,2)) = 6 for n >= 10
  Z(P(n,3)) = 8 for n >= 13 (conjectured; exhaustively verified 7<=n<=20),
              with Z(P(12,3)) = 7 the corrected exceptional value
  Z(P(2k+1,k)) = 6 for k >= 5
  Z(P(n,k)) <= 2k+2 for all n >= 3, k >= 1
Question: for each fixed k >= 4, is Z(P(n,k)) eventually constant in n, what
is that constant, where does it stabilize, and which n are exceptional?
"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from zero_forcing.zf import generalized_petersen, zero_forcing_number

def main():
    for k in range(2, 7):
        print(f"\n=== k = {k}  (upper bound 2k+2 = {2*k+2}) ===", flush=True)
        row = {}
        for n in range(2*k + 1, 2*k + 22):
            if not (1 <= k < n/2):
                continue
            t0 = time.time()
            try:
                z, S = zero_forcing_number(generalized_petersen(n, k))
            except Exception as e:
                print(f"  P({n},{k}): ERROR {e}", flush=True)
                continue
            row[n] = z
            print(f"  P({n},{k}): Z = {z}   [{time.time()-t0:.1f}s]", flush=True)
        vals = sorted(set(row.values()))
        print(f"  -> values seen for k={k}: {vals}", flush=True)
        if row:
            tail = [row[n] for n in sorted(row) if n >= 2*k + 8]
            if tail and len(set(tail)) == 1:
                print(f"  -> STABLE at {tail[0]} for n >= {2*k+8}; "
                      f"exceptions below: "
                      f"{ {n:v for n,v in sorted(row.items()) if v != tail[0]} }",
                      flush=True)

if __name__ == "__main__":
    main()
