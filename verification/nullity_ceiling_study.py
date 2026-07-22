"""
How large can the nullity of a P(n,k)-patterned matrix actually be?

Two classes, both giving rigorous lower bounds on Z (lemma at the top of
verification/cs_certificates.py):
  sym : real symmetric, A_{uv} != 0 iff uv in E(G), free diagonal   (5n params)
  cs  : combinatorially symmetric, symmetry not required            (8n params)
Both are capped at nullity 2k+2 (verification/recurrence_order.py), and 2k+2
is exactly the upper bound Z(P(n,k)) <= 2k+2, so attaining it would settle the
open problem.

A codimension count says 2k+2 ought to be generically available: nullity r
costs r(r+1)/2 = (k+1)(2k+3) conditions in the symmetric class against 5n
weights, and r^2 in the cs class against 8n, and both budgets are met
comfortably for every graph below.  So a failure to attain 2k+2 is structural,
not a shortage of parameters.

Protocol.
  * Search descends in r and stops at the first r attained.
  * S(G) sits inside the cs class, so the cs search is additionally seeded
    from the symmetric certificate (each edge weight duplicated into its two
    directed entries); the cs answer therefore cannot be worse than the
    symmetric one.  An earlier version searched the classes independently and
    reported cs < sym on P(12,2), which is impossible.
  * Each r records the plateau of the r-th smallest |eigenvalue| (or singular
    value) over the polished starts.  A tight plateau far above machine
    precision is evidence that no certificate of that nullity exists; a
    plateau that reaches 1e-16 on some start is a certificate.
"""
import sys
import time
import numpy as np
from fast_nullity import search, generators


def embed_sym(w_sym, n, k):
    """Duplicate each symmetric edge weight into its two directed entries."""
    gs, _ = generators(n, k, True)
    gc, _ = generators(n, k, False)
    out, j = np.zeros(len(gc)), 0
    for i, g in enumerate(gs):
        if len(g) == 2:                 # an edge: two directed generators
            out[j] = out[j + 1] = w_sym[i]; j += 2
        else:                           # a diagonal
            out[j] = w_sym[i]; j += 1
    return out


def scan(n, k, Z, tries=60, n_polish=8):
    rowsout, certs = [], {}
    for cl, sym in (("sym", True), ("cs", False)):
        seed_w = (embed_sym(certs["sym"], n, k)
                  if cl == "cs" and certs.get("sym") is not None else None)
        for r in range(2 * k + 2, max(2 * k - 3, 3) - 1, -1):
            best, plat, pol = search(n, k, r, symmetric=sym, tries=tries,
                                     n_polish=n_polish)
            if best is None and seed_w is not None:
                b2, p2, q2 = search(n, k, r, symmetric=sym, tries=12,
                                    n_polish=6, w_init=seed_w)
                if b2 is not None:
                    best = b2
                pol = np.concatenate([pol, q2])
            rowsout.append((cl, r, best is not None, pol.min(),
                            np.median(pol),
                            best[2] if best is not None else float("nan")))
            if best is not None:
                certs[cl] = best[0]
                break
    return rowsout, certs


def main(cases, tries=60):
    print(f"{'graph':>10} {'Z':>3} {'2k+2':>5} {'cls':>4} {'r':>3} "
          f"{'result':>11} {'best plateau':>13} {'median':>10} {'min|entry|':>10}")
    summ = []
    for (n, k, Z) in cases:
        t0 = time.time()
        rowsout, certs = scan(n, k, Z, tries=tries)
        for (cl, r, ok, mn, md, mz) in rowsout:
            print(f"{'P(%d,%d)'%(n,k):>10} {Z:>3} {2*k+2:>5} {cl:>4} {r:>3} "
                  f"{'CERTIFICATE' if ok else 'none':>11} {mn:>13.2e} "
                  f"{md:>10.2e} {mz:>10.3f}", flush=True)
        att = {cl: max([r for (c, r, ok, *_ ) in rowsout if c == cl and ok],
                       default=None) for cl in ("sym", "cs")}
        summ.append((n, k, Z, att["sym"], att["cs"], time.time() - t0))
        for cl, w in certs.items():
            np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                    f"cert_{cl}_{n}_{k}.npy", w)
    print("\nSUMMARY   max attained nullity = rigorous lower bound on Z")
    print(f"{'graph':>10} {'2k+2':>6} {'sym':>5} {'cs':>5} {'Z':>4} "
          f"{'Z - best':>9} {'secs':>7}")
    for (n, k, Z, rs, rc, el) in summ:
        m = max([v for v in (rs, rc) if v is not None], default=None)
        print(f"{'P(%d,%d)'%(n,k):>10} {2*k+2:>6} {str(rs):>5} {str(rc):>5} "
              f"{Z:>4} {str(Z - m if m else '?'):>9} {el:>7.0f}")


if __name__ == "__main__":
    cases = [(12, 2, 6), (14, 2, 6), (12, 3, 7), (13, 3, 8), (20, 3, 8),
             (18, 4, 10), (24, 4, 10), (23, 5, 12), (28, 6, 14)]
    if len(sys.argv) > 1:
        cases = [tuple(int(v) for v in a.split(",")) for a in sys.argv[1:]]
    main(cases)
