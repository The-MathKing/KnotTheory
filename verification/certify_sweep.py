"""Sweep n for a fixed k, warm-starting each n from the last certified one.

Stage 1 restarted cold costs 60 restarts x (k+1) ladder steps x 500 iterations
per gauge slice, which dominates everything.  Once one n is certified, the next
starts from a resampling of that solution and needs a single pass, so the sweep
cost is roughly one cold solve plus a cheap step per n.
"""
import sys

import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from certify_pipeline import certify


def is_prime(m):
    return m > 1 and all(m % d for d in range(2, int(m ** 0.5) + 1))


def main():
    k = int(sys.argv[1])
    ns = [int(x) for x in sys.argv[2:]]
    thr = (k + 1) * (2 * k + 3) / 3
    print(f"k = {k}   nullity target {2*k+2}   threshold n >= {thr:.1f} "
          f"(dimension 3n - {(k+1)*(2*k+3)})")
    warm, proved = None, []
    for n in ns:
        dim = 3 * n - (k + 1) * (2 * k + 3)
        print(f"\n--- P({n},{k})  {'prime' if is_prime(n) else '     '}  "
              f"variety dimension {dim} ---")
        if dim < 0:
            print("  below the threshold; skipped")
            continue
        ok, info, zn = certify(n, k, warm=warm)
        if ok:
            proved.append(n)
            warm = info
            np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                    f"cert_gn_{n}_{k}.npy", zn)
        else:
            print("  not certified at this n")
    print(f"\n{'='*64}")
    print(f"k = {k}: CERTIFIED null A = {2*k+2} at n = {proved}")
    print(f"   of which prime: {[n for n in proved if is_prime(n)]}")


if __name__ == "__main__":
    main()
