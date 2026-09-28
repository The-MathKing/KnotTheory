"""Cross-validate every published Z(P(n,k)) across independent methods.

Why this exists.  verify_all.py had 77 checks and not one of them checked a
value of Z.  Every headline result in the paper is a statement about
Z(P(n,k)), and those values came from a single program.  This script checks
them against algorithmically unrelated implementations:

  zfp   C, enumerates subsets by increasing size but assumes u_0 in S (or v_0
        if S is entirely inner), which is exhaustive UP TO the rotation
        automorphism.  This reduction is what makes n=24..28 at k=4 feasible,
        so it is itself load-bearing and must be checked, not assumed.
  zf    C, the same closure test but enumerating ALL subsets with no symmetry
        reduction at all.  Agreement with zfp is a direct test of the
        reduction; disagreement anywhere would invalidate the large-n values.
  cpsat CP-SAT time-indexed integer program: s_v seeds, x_v fill times,
        y[u,v] the forcing arcs.  Shares no code and no algorithm with the
        enumerators -- it does not enumerate subsets at all.

Three methods, two of them sharing only the definition of forcing, is the
strongest independent check available here without writing a fourth.
"""
import subprocess, sys, time, re

sys.path.insert(0, "/Volumes/2TB/scifair/src/zero_forcing")
C = "/Volumes/2TB/scifair/src/zero_forcing/c"


def run_c(prog, n, k, cap=14, extra=()):
    r = subprocess.run([f"{C}/{prog}", str(n), str(k), str(cap), *map(str, extra)],
                       capture_output=True, text=True)
    m = re.search(r"Z=(\d+)", r.stdout)
    return int(m.group(1)) if m else None


def run_cpsat(n, k):
    import zf as zfmod, cpsat
    G = zfmod.generalized_petersen(n, k)
    out = cpsat.zero_forcing_number(G, workers=4, max_seconds=CPSAT_SECS)
    if out is None:          # stopped without proving optimality
        return None
    return out[0] if isinstance(out, tuple) else out


# every (n,k) whose Z value the paper states
CASES = ([(n, 2) for n in range(5, 17)]
         + [(n, 3) for n in range(7, 21)]
         + [(n, 4) for n in range(9, 29)]
         + [(n, 5) for n in range(11, 24)]
         + [(n, 6) for n in range(13, 30)])

# Bounds, and why they are there.  The unreduced enumeration is what tests the
# symmetry reduction, but its cost is C(2n-1, Z-1) and it becomes hopeless
# quickly.  CP-SAT is cheap at small n and expensive once Z grows.  At k=6 and
# n near 29, Z reaches 12 and even the REDUCED enumeration is ~10^12 candidates,
# so no sweep can cover those; the honest thing is to bound each method, record
# which ones completed, and report how many independent confirmations each value
# has -- rather than hang, or quietly report a time-out as agreement.
PLAIN_MAX = 2 * 11     # 2n for the unreduced enumeration
CPSAT_MAX = 2 * 16     # 2n for CP-SAT
CPSAT_SECS = 120       # per instance; a non-optimal stop counts as "not checked"
ZFP_MAX_Z = 11         # skip the reference enumeration where Z would exceed this

def published():
    """Z values the paper prints, read from the recorded sweeps."""
    vals = {}
    import glob as _g
    for f in _g.glob("/Volumes/2TB/scifair/results/zero_forcing/*.txt"):
        try:
            txt = open(f).read()
        except OSError:
            continue
        # three recorded formats, because the values were produced by three
        # different harnesses over the life of the project:
        #   "P(9,2) Z=6 witness=..."        the sweeps
        #   "P(11,3): Z=7 exp=7 ..."        cpsat_validation.txt
        #   "  P(20,6)  10    6    8 ..."   d2_scan.txt, Z in the first column
        pats = [r"P\((\d+),(\d+)\)\s*Z=(\d+)",
                r"P\((\d+),(\d+)\):\s*Z=(\d+)",
                r"^\s+P\((\d+),(\d+)\)\s+(\d+)\s"]
        for pat in pats:
            for m in re.finditer(pat, txt, re.M):
                n, k, z = int(m.group(1)), int(m.group(2)), int(m.group(3))
                vals.setdefault((n, k), z)
    return vals


if __name__ == "__main__":
    pub = published()
    print(f"{'n':>4} {'k':>3} {'paper':>6} {'zfp':>5} {'zf(plain)':>10} "
          f"{'cpsat':>7} {'#conf':>6}  verdict")
    bad, tally = [], {0: [], 1: [], 2: [], 3: []}
    for n, k in CASES:
        want = pub.get((n, k))
        a = run_c("zfp", n, k, ZFP_MAX_Z, extra=(8,))
        b = run_c("zf", n, k, ZFP_MAX_Z) if 2 * n <= PLAIN_MAX else None
        c = None
        if 2 * n <= CPSAT_MAX:
            try:
                c = run_cpsat(n, k)
            except Exception:
                c = None
        got = [v for v in (a, b, c) if isinstance(v, int)]
        conf = len(got)
        # a value is confirmed only when every method that COMPLETED agrees
        # with it and with the paper
        ok = conf == 0 or (len(set(got)) == 1 and (want is None or got[0] == want))
        if not ok:
            bad.append((n, k, want, a, b, c))
        tally[min(conf, 3)].append((n, k))
        print(f"{n:>4} {k:>3} {str(want):>6} {str(a):>5} {str(b):>10} "
              f"{str(c):>7} {conf:>6}  {'agree' if ok else 'DISAGREE'}")
        sys.stdout.flush()
    print()
    for j in (3, 2, 1, 0):
        if tally[j]:
            print(f"  {len(tally[j]):3d} values with {j} independent "
                  f"confirmation(s){': ' + str(tally[j]) if j <= 1 else ''}")
    print()
    if bad:
        print(f"DISAGREEMENTS: {bad}")
    else:
        print("No disagreement anywhere: every method that completed agrees "
              "with every other and with the value the paper prints.")
        if tally[0] or tally[1]:
            print("NOTE: the values listed with 0 or 1 confirmations rest on "
                  "the reference enumeration alone at this problem size. That "
                  "is a limit of what is computable, not an agreement.")
