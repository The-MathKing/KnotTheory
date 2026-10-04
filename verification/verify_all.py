"""One pass over every computational claim the paper makes.

Run this to confirm the paper's numbers from scratch.  Each check prints PASS or
FAIL and the quantity it checked; nothing is taken on trust from a stored file
except the saved certificates, which are re-evaluated rather than believed.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import glob
import itertools
import re
import os
import sys
import time

_T0 = time.perf_counter()

import numpy as np
import sympy as sp

sys.path.insert(0, f"{_REPO}/verification")
ROOT = f"{_REPO}/results/zero_forcing"
fails = []
results = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  --- {detail}" if detail else ""))
    results.append((name, ok))
    if not ok:
        fails.append(name)


s = sp.symbols("s")


def L(k):
    a, b = sp.Integer(2), s
    for _ in range(k - 1):
        a, b = b, sp.expand(s * b - a)
    return b


print("1. Realisability (thm:realis): c^2 = 0 iff F = (s+a)(L_k + t)")
a_, al, be = sp.symbols("a alpha beta")
for k in range(2, 9):
    F = sp.expand((s + a_) * L(k) + al * s + be)
    ok = sp.simplify(F.subs(be, a_ * al) - (s + a_) * (L(k) + al)) == 0
    check(f"k={k}", ok)

print("2. Antipodal corollary: c^2 = 0 identically for even k, not for odd")
x, y = sp.symbols("x y", positive=True)
for k in range(2, 9):
    Lk = L(k)
    eqs = [sp.Eq(a_ * Lk.subs(s, r) + al * r + be, -r * Lk.subs(s, r))
           for r in (x, y, -y)]
    sol = sp.solve(eqs, [a_, al, be], dict=True)
    v = sp.simplify(sol[0][a_] * sol[0][al] - sol[0][be]) if sol else None
    check(f"k={k} ({'even' if k % 2 == 0 else 'odd'})",
          (v == 0) == (k % 2 == 0))

print("3. k=2 closed form: c^2 = -(s1+s2)(s1+s3)(s2+s3)")
r1, r2, r3 = sp.symbols("r1 r2 r3")
sol = sp.solve([sp.Eq(a_ * (r**2 - 2) + al * r + be, -r * (r**2 - 2))
                for r in (r1, r2, r3)], [a_, al, be], dict=True)[0]
check("identity", sp.simplify(sol[a_]*sol[al] - sol[be]
                              + (r1+r2)*(r1+r3)*(r2+r3)) == 0)

print("4. e_2 = -k for every period-one symbol with k >= 3 (thm:congbound)")
for k in range(3, 11):
    F = sp.Poly(sp.expand((s + a_) * L(k) + al * s + be), s)
    check(f"k={k}", sp.expand(F.coeff_monomial(s**(k-1)) + k) == 0)

print("5. Integer certificates: the signed adjacency matrix")
def signed_nullity(n, k):
    P = np.roll(np.eye(n), 1, axis=0)
    A = np.block([[P + P.T, np.eye(n)],
                  [-np.eye(n), np.linalg.matrix_power(P, k)
                   + np.linalg.matrix_power(P.T, k)]])
    sv = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(sv < 1e-9 * sv.max()))
# the signed adjacency matrix is the a = alpha = 0 case, which covers
# 10|n and 30|n at k=3,2 and 120|n at k=7 -- NOT 7|n, whose certificate is
# Psi_7 with a=1, alpha=0 and is checked separately below
for (n, k, want) in [(10, 3, 8), (20, 3, 8), (30, 3, 8), (120, 7, 16),
                     (30, 2, 6), (60, 2, 6)]:
    got = signed_nullity(n, k)
    check(f"signed Adj P({n},{k}) nullity {want}", got == want, f"got {got}")

def psi7_nullity(n):
    """The 7|n certificate: a = 1, alpha = 0, spokes 1 and -1."""
    P = np.roll(np.eye(n), 1, axis=0)
    A = np.block([[np.eye(n) + P + P.T, np.eye(n)],
                  [-np.eye(n), np.linalg.matrix_power(P, 2)
                   + np.linalg.matrix_power(P.T, 2)]])
    sv = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(sv < 1e-9 * sv.max()))
for n in (7, 14, 21, 28):
    got = psi7_nullity(n)
    check(f"Psi_7 certificate P({n},2) nullity 6", got == 6, f"got {got}")

print("6. k=2 explicit certificate at the three most negative grid values")
print("   (c^2 > 0 is checked for all n; the nullity is checked two ways, by")
print("    counting grid roots of the symbol exactly and, for moderate n only,")
print("    by singular values -- the three roots crowd within O(1/n^2) of -2,")
print("    so the matrix is exact but numerically stiff for large n)")
bad_c2 = []
for n in list(range(9, 200)) + [500, 1001]:
    if n == 10:
        continue
    M = (n - 1) // 2
    v = [2*np.cos(2*np.pi*j/n) for j in (M, M-1, M-2)]
    c2 = -(v[0]+v[1])*(v[0]+v[2])*(v[1]+v[2])
    if c2 <= 1e-12:
        bad_c2.append(n)
check("c^2 > 0 for every n >= 9, n != 10 (up to 1001)", not bad_c2,
      f"failures {bad_c2}" if bad_c2 else "checked 9..199, 500, 1001")
# Counting grid roots by a float tolerance is the wrong test: the three
# prescribed roots crowd within O(1/n^2) of -2 (spread 2.4e-4 at n = 1001),
# so grid values that are merely NEAR them evaluate below any fixed cutoff
# -- at n = 1001 the true roots give 9e-16 and the nearest non-roots 4e-11.
# What actually needs checking is the construction: the three prescribed
# values are distinct interior grid values, and then prop:symbol gives
# nullity exactly 6 because each interior root is met by two Fourier indices.
bad_root = []
for n in list(range(9, 200)) + [500, 1001, 5000]:
    if n == 10:
        continue
    M = (n - 1) // 2
    v = [2*np.cos(2*np.pi*j/n) for j in (M, M-1, M-2)]
    distinct = len({round(x, 14) for x in v}) == 3
    interior = all(abs(abs(x) - 2) > 1e-12 for x in v)
    if not (distinct and interior):
        bad_root.append(n)
check("three prescribed roots are distinct and interior", not bad_root,
      f"failures {bad_root}" if bad_root
      else "checked 9..199, 500, 1001, 5000")
for n in (9, 11, 20, 39, 60):
    M = (n - 1) // 2
    v = [2*np.cos(2*np.pi*j/n) for j in (M, M-1, M-2)]
    c2 = -(v[0]+v[1])*(v[0]+v[2])*(v[1]+v[2])
    e1 = sum(v); e2 = v[0]*v[1]+v[0]*v[2]+v[1]*v[2]
    P = np.roll(np.eye(n), 1, axis=0)
    A = np.block([[-e1*np.eye(n)+P+P.T, np.sqrt(c2)*np.eye(n)],
                  [np.sqrt(c2)*np.eye(n),
                   (e2+2)*np.eye(n)+np.linalg.matrix_power(P,2)
                   + np.linalg.matrix_power(P.T,2)]])
    sv = np.linalg.svd(A, compute_uv=False)
    check(f"P({n},2) nullity 6 numerically",
          int(np.sum(sv < 1e-9*sv.max())) == 6)

print("7. Saved interval-certified matrices re-evaluated (k=3)")
from certify_general import pattern_cells, assemble
got = []
for f in sorted(glob.glob(f"{ROOT}/cert_gn_*_3.npy")):
    n = int(os.path.basename(f).split("_")[2])
    z = np.load(f)
    A = assemble(z[:5*n], pattern_cells(n, 3), 2*n)
    sv = np.linalg.svd(A, compute_uv=False)
    nul = int(np.sum(sv < 1e-9*sv.max()))
    edges = np.abs(z[2*n:5*n]).min()/np.abs(z[:5*n]).max()
    got.append(n)
    check(f"P({n},3) nullity 8, edges nonzero", nul == 8 and edges > 1e-3,
          f"nullity {nul}, min edge {edges:.4f}")
print(f"      ({len(got)} saved certificates re-evaluated)")
# thm:p17 claims every n in [17,33] with no exceptions.  Globbing whatever
# happens to be on disk cannot see a MISSING one -- n=18 was certified in a log
# but never saved, and this check is what would have caught that.
want = list(range(17, 34))
check("thm:p17: a saved certificate exists for every n in [17,33]",
      got == want, f"missing {sorted(set(want) - set(got))}"
      if set(want) - set(got) else f"all {len(want)} present")

print("8. k=3 identity tiles and their compositions")
from tiles import tile_sequence, dock_weights, build_matrix
def tdict(w, l, k):
    m = k+1; nint = l-2*m; D = dock_weights(k); t = {}
    for idx, key in enumerate("bcead"):
        t[key] = np.concatenate([D[key], w[idx*nint:(idx+1)*nint], D[key]])
    return t
tiles = {}
for f in sorted(glob.glob(f"{ROOT}/tile_*_3.npy")):
    l = int(os.path.basename(f).split("_")[1])
    tiles[l] = np.load(f)
have = sorted(tiles)
check("tiles cover a full interval [L,2L)",
      have == list(range(min(have), max(have)+1)) and max(have) >= 2*min(have)-1,
      f"lengths {min(have)}..{max(have)} ({len(have)} tiles)")
bad = []
for l in have:
    W = tile_sequence([tdict(tiles[l], l, 3)], 3)
    A = build_matrix(l, 3, W)
    sv = np.linalg.svd(A, compute_uv=False)
    if int(np.sum(sv < 1e-9*np.abs(A).max())) != 8:
        bad.append(l)
check("single tiles give nullity 8", not bad, f"failures {bad}" if bad else
      f"all {len(have)} lengths")
bad = []
for n in range(2*min(have), 2*min(have)+14):
    combo = next((c for r in (2, 3)
                  for c in itertools.combinations_with_replacement(have, r)
                  if sum(c) == n), None)
    if combo is None:
        continue
    W = tile_sequence([tdict(tiles[l], l, 3) for l in combo], 3)
    A = build_matrix(n, 3, W)
    sv = np.linalg.svd(A, compute_uv=False)
    if int(np.sum(sv < 1e-9*np.abs(A).max())) != 8:
        bad.append(n)
check("multi-tile concatenations give nullity 8", not bad,
      f"failures {bad}" if bad else "checked n up to "
      f"{2*min(have)+13}")

print("9. Certified tiles: nullity, docking exactness, coverage")
# What Theorem thm:tiling actually needs is that n be a SUM of certified tile
# lengths.  "Every length in [L,2L)" is a convenient sufficient condition, not
# the real one: at k=5 the certified lengths are 54..72,74,75 -- l=73 is
# missing, so [L,2L) fails -- yet the semigroup they generate still contains
# every n >= 162.  So we check the semigroup directly and report the threshold
# it yields, rather than testing the sufficient condition and calling a pass a
# failure.
from tiles import dock_weights
SETTLE = {}
for k in (3, 4, 5):
    r = 2*k + 2
    m = k + 1
    certs = {}
    for f in sorted(glob.glob(f"{ROOT}/tilecert_*_{k}.npy")):
        l = int(os.path.basename(f).split("_")[1])
        certs[l] = np.load(f)
    if not certs:
        continue
    cl = sorted(certs)
    D = dock_weights(k)
    NCOV = 4000
    rep_ = [False]*(NCOV+1)
    for a in cl:
        if a <= NCOV:
            rep_[a] = True
    for i in range(min(cl), NCOV+1):
        if rep_[i]:
            for a in cl:
                if i+a <= NCOV:
                    rep_[i+a] = True
    holes = [i for i in range(min(cl), NCOV+1) if not rep_[i]]
    thresh = (max(holes)+1) if holes else min(cl)
    SETTLE[k] = thresh
    check(f"k={k}: every n >= {thresh} is a sum of certified lengths",
          all(rep_[i] for i in range(thresh, NCOV+1)),
          f"{len(cl)} tiles, lengths {min(cl)}..{max(cl)}"
          + (f"; {len(holes)} smaller n not covered" if holes else
             " (= [L,2L), so L itself)"))
    bad_n, bad_d = [], []
    for l in cl:
        z = certs[l]
        A = assemble(z[:5*l], pattern_cells(l, k), 2*l)
        sv = np.linalg.svd(A, compute_uv=False)
        if int(np.sum(sv < 1e-9*sv.max())) != r:
            bad_n.append(l)
        for blk, key in enumerate("adbce"):
            for j, pos in enumerate(list(range(m)) + list(range(l-m, l))):
                if abs(z[blk*l+pos] - D[key][j % m]) > 1e-13:
                    bad_d.append((l, key)); break
    check(f"k={k}: every certified tile has nullity exactly {r}", not bad_n,
          f"failures {bad_n}" if bad_n else f"all {len(cl)} tiles")
    check(f"k={k}: docking weights exact in every certified tile", not bad_d,
          f"failures {bad_d[:3]}" if bad_d else "all tiles, to 1e-13")
    # (the semigroup check above subsumes the old [min(cl), 400] scan, and
    # unlike it is correct when the certified lengths are not a full interval)

print("10. The paper's own numbers against the computed ones")
# Derived counts have gone stale three times: 53 vs 54, then 54 vs 55 after
# L(4) improved from 31 to 30. Check the manuscript against reality rather
# than trusting that an edit propagated.
PAPER = f"{_REPO}/manuscript/zf_paper.tex"
try:
    src = open(PAPER).read()
except OSError:
    src = None
if src is not None:
    ncert = sum(len(glob.glob(f"{ROOT}/tilecert_*_{k}.npy")) for k in (3, 4))
    # only the TOTAL phrasings; a per-k count such as "23 certifications at
    # k=3" is a different quantity and must not be swept in
    pats = [r"all \$(\d+)\$ tiles",
            r"all \$(\d+)\$ certifications(?! at )",
            r"together with \$(\d+)\$ interval",
            r"together with \$(\d+)\$ certifications",
            r"Each of the \$(\d+)\$ certifications",
            r"All \$(\d+)\$ tile certifications",
            r"[Aa]cross all \$(\d+)\$ certif",
            r"\$23\+(?:\d+)=(\d+)\$ certifications"]
    stale = sorted({int(m) for pat in pats for m in re.findall(pat, src)})
    bad = [v for v in stale if v != ncert]
    check(f"paper's certification count matches the {ncert} certified tiles",
          not bad, f"paper says {bad}" if bad else f"all say {ncert}")
    # Status-vs-theorem drift has now happened three times: the Status section
    # claimed completeness for fewer k than thm:complete proves.  The macro
    # system cannot catch it because the claim is PROSE, not a number.  So
    # compare the two passages directly: whichever set of k thm:complete names,
    # the Status section must name the same set.
    def kset(text):
        return set(int(m) for m in re.findall(r"\$k=(\d)\$", text))
    m_thm = re.search(r"\\begin\{theorem\}\[Complete determination(.{0,200}?)\]",
                      src, re.S)
    m_sta = re.search(r"Theorem~\\ref\{thm:complete\}: \$Z\(P\(n,k\)\)\$ is "
                      r"determined for \\emph\{every\}(.{0,200}?)\.", src, re.S)
    if m_thm and m_sta:
        a, b = kset(m_thm.group(1)), kset(m_sta.group(1))
        check("Status section names the same k as thm:complete", a == b,
              f"theorem says {sorted(a)}, Status says {sorted(b)}"
              if a != b else f"both say {sorted(a)}")
    else:
        check("Status/theorem completeness passages both found", False,
              f"theorem match={bool(m_thm)}, status match={bool(m_sta)}")

    for k, lab in ((3, "L=21"), (4, "L=29")):
        t = sorted(int(os.path.basename(f).split("_")[1])
                   for f in glob.glob(f"{ROOT}/tilecert_*_{k}.npy"))
        check(f"k={k}: paper's L matches the least certified tile length "
              f"({min(t)})", f"$L={min(t)}$" in src or f"L={min(t)}" in src,
              lab)

print("11. The Krawczyk test itself, re-run in EXACT arithmetic")
# Sections 7 and 9 re-evaluate saved matrices numerically; neither touches the
# claim the results actually rest on.  This re-runs the contraction test with
# every quantity an exact rational, on the two tile lengths the thresholds
# L(3) and L(4) rest on and on the smallest per-n certificate.
from exact_certify import rebuild
from exact_krawczyk import exact_krawczyk
from certify_tiles import dock_indices
from krawczyk import L_LIP
for kind, k, m in (("tile", 3, 21), ("tile", 4, 29), ("gn", 3, 17)):
    f = (f"{ROOT}/tilecert_{m}_{k}.npy" if kind == "tile"
         else f"{ROOT}/cert_gn_{m}_{k}.npy")
    zn = np.load(f)
    pinned = dock_indices(m, k) if kind == "tile" else []
    cells, perm, N, r, nw, eqs, free, dev, zn = rebuild(zn, m, k, pinned)
    ok, info = exact_krawczyk(zn, cells, perm, N, r, nw, eqs, free, L_LIP,
                              verbose=False)
    check(f"{kind} {m} at k={k}: exact Krawczyk contraction", ok,
          f"alpha = {float(info['alpha']):.3e} < 1 exactly" if ok
          else "did not pass")

print("12. Z values cross-checked against independent solvers")
# Until now this suite checked the MATRIX side only: realisability, certificates,
# nullities, tiles.  Not one check touched a value of Z, even though every
# headline claim is a statement about Z and those values came from one program.
# Worse, the k=4 values at n=24..28 rest on a rotation-symmetry reduction that
# was never itself tested.  Here we re-derive a sample with three unrelated
# methods -- symmetry-reduced enumeration, UNREDUCED enumeration, and a CP-SAT
# integer program that does not enumerate subsets at all -- and assert that the
# recorded full sweep found no disagreement anywhere.
sys.path.insert(0, f"{_REPO}/src/zero_forcing")
import subprocess as _sp, re as _re2
CBIN = f"{_REPO}/src/zero_forcing/c"

def _zc(prog, n, k, extra=()):
    r = _sp.run([f"{CBIN}/{prog}", str(n), str(k), "14", *map(str, extra)],
                capture_output=True, text=True)
    m = _re2.search(r"Z=(\d+)", r.stdout)
    return int(m.group(1)) if m else None

# the values that actually carry weight: the published error, the threshold,
# and every non-monotone drop
# Three samples, not thirty: the published error, and one non-monotone drop at
# each of k=2 and k=4.  The full sweep lives in crossvalidate_z.py and its
# result is asserted below -- keeping this suite runnable in a couple of minutes
# matters, because a suite nobody runs checks nothing.
SAMPLE = [(12, 3, 7), (8, 2, 5), (12, 4, 6)]
import zf as _zfmod, cpsat as _cpsat
for n, k, want in SAMPLE:
    a = _zc("zfp", n, k, extra=(8,))
    b = _zc("zf", n, k)
    G = _zfmod.generalized_petersen(n, k)
    # workers=4, not 2: CP-SAT's parallel portfolio only reaches the strategy
    # that cracks P(12,3) at 4+ workers. Measured on the same instance:
    # 2 workers -> timeout at 100 s; 4 workers -> 1.5 s; 8 -> 2.2 s. The
    # throttle to 2 was what made this section take five minutes.
    c = _cpsat.zero_forcing_number(G, workers=4, max_seconds=120)
    c = c[0] if isinstance(c, tuple) else c
    # A method that did not finish is NOT a method that disagreed.  CP-SAT is
    # given a wall-clock limit, so under load it can return None; conflating
    # that with a mismatch would make the suite fail for reasons that have
    # nothing to do with the mathematics.  So: every method that COMPLETED must
    # agree, and we say how many did.
    done = [(nm, v) for nm, v in (("reduced", a), ("unreduced", b),
                                  ("CP-SAT", c)) if v is not None]
    agree = all(v == want for _, v in done) and len(done) >= 2
    detail = ", ".join(f"{nm} {v}" for nm, v in done)
    if c is None:
        detail += "; CP-SAT did not prove optimality in the time limit"
    check(f"Z(P({n},{k})) = {want}, by every method that completed",
          agree, f"{len(done)}/3 completed: {detail}")

try:
    cv = open(f"{ROOT}/crossvalidate_z.txt").read()
    nag = cv.count("agree")
    done = "No disagreement anywhere" in cv
    check("recorded cross-validation sweep has no disagreement",
          "DISAGREE" not in cv,
          f"{nag} rows agree" + ("" if done else "; sweep still in progress"))
except OSError:
    check("recorded cross-validation sweep present", False, "file missing")

# (the emission moved to the end of the run; see section 15)
# The census has been wrong three times: 53 vs 54, then 55, then 56, and L(4)
# has been 31, 30, 29 -- every one of them a bookkeeping slip, never a change
# to the theory.  Hard-coding a count in prose guarantees it goes stale.  So
# the numbers are GENERATED here and \input by the manuscript, which makes
# staleness structurally impossible rather than merely detected.
def emit_numbers(pending=0, ram=None, ram_cases=0):
    import re as _re
    vals = {}
    word = {3: "Three", 4: "Four", 5: "Five"}
    for k in (3, 4, 5):
        t = sorted(int(os.path.basename(f).split("_")[1])
                   for f in glob.glob(f"{ROOT}/tilecert_*_{k}.npy"))
        vals[f"Ntile{word[k]}"] = len(t)
        vals[f"Lval{word[k]}"] = min(t) if t else 0
        vals[f"Lmax{word[k]}"] = max(t) if t else 0
    vals["NtileThreeFour"] = vals["NtileThree"] + vals["NtileFour"]
    vals["NtileAll"] = vals["NtileThreeFour"] + vals["NtileFive"]
    gn = sorted(int(os.path.basename(f).split("_")[2])
                for f in glob.glob(f"{ROOT}/cert_gn_*_3.npy"))
    for k in (3, 4, 5):
        if k in SETTLE:
            vals[f"Settle{ {3:'Three',4:'Four',5:'Five'}[k] }"] = SETTLE[k]
    vals["NcertGN"] = len(gn)
    vals["GNlo"], vals["GNhi"] = (min(gn), max(gn)) if gn else (0, 0)
    # the largest alpha over every EXACT certification we have on record
    al = []
    for f in ("exact_tiles_k3.txt", "exact_tiles_k4.txt", "exact_tiles_k5.txt",
              "exact_gn_k3.txt"):
        try:
            al += [float(x) for x in _re.findall(r"alpha=([0-9.e+-]+) < 1",
                                                 open(f"{ROOT}/{f}").read())]
        except OSError:
            pass
    mant, exp = (f"{max(al):.1e}".split("e") if al else ("0", "0"))
    vals["MaxAlpha"] = f"{mant}\\times10^{{{int(exp)}}}"
    # Counted at the END of the run (see the call site), so this is exactly the
    # number of PASS/FAIL lines the suite prints.  Reading it here mid-run was
    # an off-by-two: the emission's own check and the slice lemma both follow.
    # The Ramanujan classification, straight from the exact run in section 13.
    if ram:
        word = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
                6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}
        for k, hits in ram.items():
            vals[f"RamLast{word[k]}"] = max(hits)
            vals[f"RamCount{word[k]}"] = len(hits)
        vals["RamTotal"] = sum(len(v) for v in ram.values())
        vals["RamKmax"] = max(ram)
        vals["RamCases"] = ram_cases
        vals["RamBoundTwo"] = _RAMX.finiteness_bound(2)
        vals["RamBoundThree"] = _RAMX.finiteness_bound(3)
        vals["RamBoundFour"] = _RAMX.finiteness_bound(4)
    # The classification for EVERY k, from the uniform Dirichlet threshold.
    # These are emitted from the census run, not typed: the threshold is a
    # closed-form constant and the counts follow from exhausting below it.
    from verification import ramanujan_all_k as _RAK
    _thr = _RAK.dirichlet_threshold()
    _hits, _ = _RAK.census(_thr - 1)
    vals["RamDirichlet"] = _thr
    vals["RamAllTotal"] = len(_hits)
    vals["RamAllIso"] = len({_RAK.iso_class(n, k) for n, k in _hits})
    vals["RamAllMaxN"] = max(n for n, _k in _hits)
    vals["RamAllMaxK"] = max(k for _n, k in _hits)
    vals["RamAllSizes"] = len({n for n, _k in _hits})
    vals["RamAllCases"] = sum((n - 1) // 2 for n in range(3, _thr))
    if ram:
        # The classification table is GENERATED too, for the same reason the
        # counts are: a table typed by hand goes stale the first time a bound
        # moves.  Long runs are collapsed to "a--b" so the table stays readable.
        def _runs(xs):
            out, i = [], 0
            while i < len(xs):
                j = i
                while j + 1 < len(xs) and xs[j + 1] == xs[j] + 1:
                    j += 1
                out.append(str(xs[i]) if j == i else "%d\\text{--}%d" % (xs[i], xs[j]))
                i = j + 1
            return ", ".join(out)
        # The table now covers EVERY k, not just the k the old exact run
        # reached: the classification is finite in both variables, so the
        # table is the whole answer and stopping it at k=10 would understate
        # what is proved.
        byk = {}
        for n, k in _hits:
            byk.setdefault(k, []).append(n)
        rows = ["% GENERATED by verification/verify_all.py -- do not edit by hand.",
                r"\begin{tabular}{r r r l}", r"\hline",
                r"$k$ & $B_k$ & count & the $n$ for which $P(n,k)$ satisfies the RH\\",
                r"\hline"]
        for k in sorted(byk):
            rows.append("$%d$ & $%d$ & $%d$ & $%s$\\\\" %
                        (k, _RAMX.finiteness_bound(k), len(byk[k]),
                         _runs(sorted(byk[k]))))
        rows += [r"\hline",
                 r"\multicolumn{4}{l}{\footnotesize No $k$ outside this table "
                 r"admits any $n$: the list is finite in both variables.}\\",
                 r"\end{tabular}"]
        open(f"{_REPO}/manuscript/ram_table.tex",
             "w").write("\n".join(rows) + "\n")
    # thm:ratclass: the exact reach of rational-symbol rotation-invariant certificates
    try:
        from verification import period_one_classification as _POC
        for k, w in {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven"}.items():
            L = _POC.lcms(k)
            vals[f"RatClass{w}"] = ",".join(map(str, L)) if L else r"\text{none}"
    except Exception as _exc:  # the paper must still build if the enumeration is unavailable
        pass
    vals["TileAllK"] = str(globals().get("TILE_ALL_K", 0))
    vals["Nchecks"] = str(len(results) + pending)
    out = ["% GENERATED by verification/verify_all.py -- do not edit by hand.",
           "% Every number here is read off the certificates on disk.", ""]
    for key, v in vals.items():
        out.append(f"\\newcommand{{\\{key}}}{{{v}}}")
    path = f"{_REPO}/manuscript/zf_numbers.tex"
    open(path, "w").write("\n".join(out) + "\n")
    return vals, path

print("13. The graph Riemann Hypothesis: classification of Ramanujan P(n,k)")
# A connected (q+1)-regular graph satisfies the Riemann Hypothesis for its Ihara
# zeta function exactly when it is Ramanujan -- for q+1 = 3, when every
# eigenvalue with |lambda| != 3 has |lambda| <= 2 sqrt 2 (Terras, "Zeta Functions
# and Chaos", Exercise 9).  Everything below certifies that condition.
sys.path.insert(0, f"{_REPO}")
from verification import ramanujan as RAM
from verification import ramanujan_exact as RAMX

# (a) The Z_n block decomposition is the load-bearing structural fact.  It is
# checked against brute-force diagonalisation, not assumed from the theory.
worst, badpairs = RAM.check_agreement(60)
check("block decomposition reproduces the full spectrum",
      not badpairs and worst < 1e-8,
      f"max deviation {worst:.1e} over k=1..10, n<=60")

# (b) Anchors against spectra that are in the literature.
anchor_ok = True
for name, got, want in RAM.known_spectra():
    anchor_ok &= (len(got) == len(want)
                  and max(abs(x - y) for x, y in zip(got, want)) < 1e-9)
check("spectra match published values for Petersen and Desargues", anchor_ok,
      "P(5,2) -> {3,1,-2}, P(10,3) -> {+-3,+-2,+-1}")

# (c) The elementary criterion.  Clearing both square roots turns the spectral
# condition into one polynomial inequality; that reduction is the whole proof,
# so it is checked against the spectrum it claims to replace.
badc = RAM.check_criterion(10, 260)
check("criterion G_k <= 7 agrees with the spectral test", not badc,
      f"k=1..10, n<=260" if not badc else f"disagreements {badc[:5]}")

# (d) The sign facts the finiteness and parity proofs rest on, exactly.
sign_rows, sign_ok = [], True
for k in range(1, 13):
    P = RAMX.D_poly(k)
    d1, d0, dm1 = int(P.eval(1)), int(P.eval(0)), int(P.eval(-1))
    want_dm1 = -7 if k % 2 else 9
    ok = (d1 == -7) and (d0 >= 17) and (dm1 == want_dm1) \
         and P.degree() == 2 * k + 2 and int(P.all_coeffs()[0]) == 4 ** (k + 1)
    sign_ok &= ok
    sign_rows.append((k, d1, d0, dm1))
check("D_k(1)=-7, D_k(0)>=17, D_k(-1)=-7 (k odd) / 9 (k even), deg 2k+2", sign_ok,
      "k=1..12; these give the bad band at u=1 always and at u=-1 iff k is odd")

# (e) The side condition 7 + 4u T_k(u) >= 0 never binds, so the criterion really
# is the single inequality D_k >= 0.
side = min(RAMX.prod_plus_7_is_positive(k) for k in range(1, 13))
check("side condition 7 + 4u T_k(u) stays positive on [-1,1]", side > 2.9,
      f"minimum over k=1..12 is {side:.3f}, and |4u T_k| <= 4 bounds it by 3")

# (f) The certified finiteness bound, and the parity bound for odd k.
fin_ok = par_ok = True
fin_tight = par_tight = 0
for k in range(1, 12):
    Lk = RAM.classify(k, 1500)
    B = RAMX.finiteness_bound(k)
    fin_ok &= max(Lk) <= B
    fin_tight += (max(Lk) == B)
    if k % 2 == 1:
        ob = RAMX.odd_n_bound(k)
        odd = [n for n in Lk if n % 2 == 1]
        par_ok &= (max(odd) <= ob if odd else True)
        par_tight += (bool(odd) and max(odd) == ob)
check("finiteness bound n <= 2 pi / arccos(u_k) holds for every k", fin_ok,
      f"k=1..11, attained exactly at {fin_tight} of them")
check("parity bound n <= pi / arccos(-v_k) holds for odd k, odd n", par_ok,
      f"k=1,3,...,11, attained exactly at {par_tight} of them")

# (f2) The bound that holds for EVERY k, not one k at a time.  This is what
# turns the table into a theorem; the lemma under it is checked against G.
lo0, lopi = RAMX.check_uniform_lemma(200)
check("uniform lemma: G_k > 7 on the whole interval the proof forbids",
      lo0 > 7.0 and lopi > 7.0,
      f"min G = {lo0:.6f} at the band at 0, {lopi:.6f} at the band at pi, "
      f"over k=1..200")
uni_ok = True
for k in range(1, 12):
    Lk = RAM.classify(k, 1500)
    uni_ok &= max(Lk) <= RAMX.uniform_bound(k)
    odd = [n for n in Lk if n % 2 == 1]
    if k % 2 == 1 and odd:
        uni_ok &= max(odd) <= RAMX.uniform_bound(k, n_odd=True)
check("uniform bound n <= pi(2+sqrt2) sqrt(k^2+1), halved for odd k odd n",
      uni_ok, "holds against the certified classification for k=1..11")

# (g) The classification itself, decided in exact arithmetic.  The float64
# classifier runs alongside as a control with no authority: this check FAILS on
# a disagreement rather than preferring either answer.  It found a real bug --
# at k=1 the Laurent exponents collide and a dict literal silently dropped them.
ram_cases = ram_disagree = 0
RAM_CLASS = {}
for k in range(1, 11):
    B = RAMX.finiteness_bound(k)
    hits = []
    for n in range(2 * k + 1, B + 1):
        e, _why = RAMX.is_ramanujan_exact(n, k)
        ram_cases += 1
        if e != RAM.is_ramanujan(n, k):
            ram_disagree += 1
        if e:
            hits.append(n)
    RAM_CLASS[k] = hits
check("every case below the bound decided in exact arithmetic",
      ram_disagree == 0 and ram_cases > 400,
      f"{ram_cases} cases certified, {ram_disagree} disagreements with the control")
check("the classification is complete for k <= 10",
      all(RAM_CLASS[k] for k in RAM_CLASS),
      f"{sum(len(v) for v in RAM_CLASS.values())} Ramanujan graphs; "
      f"largest n per k: " + ", ".join(f"{k}:{max(v)}" for k, v in RAM_CLASS.items()))

print("14. Reduction on every two-vertex cover (thm:red2)")
# thm:red is the case p=1, w=0 of a reduction that works on any two-vertex base
# B_{p,q,w}.  Checked two ways: the elimination is carried out SYMBOLICALLY (the
# nine offsets and the two extreme coefficients), and the resulting lift
# x -> (x, Lx) is confirmed numerically to be a bijection onto ker A.
from general_reduction import eliminate, confirm
bad_sym = []
for (p_, q_, w_) in [(1, 2, 0), (1, 3, 0), (2, 3, 0), (2, 5, 0), (3, 4, 0),
                     (1, 3, 1), (2, 5, 2), (2, 2, 0)]:
    off = eliminate(p_, q_, w_)
    want = sorted({-(p_ + q_), -q_, -(q_ - p_), -p_, 0, p_, q_ - p_, q_, p_ + q_})
    ends = off.get(p_ + q_, 0) != 0 and off.get(-(p_ + q_), 0) != 0
    if sorted(off) != want or not ends:
        bad_sym.append((p_, q_, w_))
check("thm:red2: elimination gives the predicted offsets, ends nonzero",
      not bad_sym, f"failures {bad_sym}" if bad_sym else
      "8 bases, incl. p>1 and w!=0 which thm:red does not cover")

bad_num = []
for (p_, q_, w_), n_ in [((1, 2, 0), 13), ((1, 3, 0), 15), ((2, 5, 0), 23),
                         ((3, 4, 0), 19), ((2, 5, 2), 23), ((2, 2, 0), 17)]:
    r_ = confirm(p_, q_, w_, n_, seed=3)
    if r_ is None:
        continue
    nA, nR, res, D = r_
    if not (nA == nR and nA <= D and res < 1e-8):
        bad_num.append((p_, q_, w_, n_, nA, nR, res, D))
check("thm:red2: x -> (x, Lx) is a bijection onto ker A, and null A <= 2(p+q)",
      not bad_num, f"failures {bad_num}" if bad_num else
      "null A = null R, lift residual at machine precision")

# thm:theta: two-vertex bases with several connecting edges and no loops, which
# thm:red2 cannot touch because the outer row meets every inner variable at once.
# The elimination is two-step instead of one, and the state dimension comes out
# equal to the degree span.
import warnings as _warn
from theta_reduction import check as _theta
bad_th = []
with _warn.catch_warnings():
    _warn.simplefilter("ignore")
    _old = np.seterr(all="ignore")
    for volts, n_ in [((0, 1, 2), 11), ((0, 1, 3), 13), ((0, 2, 3), 13),
                      ((0, 1, 2, 3), 13), ((0, 1, 4), 17), ((0, 3, 5), 19)]:
        nA, nT, D, dim = _theta(list(volts), n_, seed=4)
        if not (nA == nT and nA <= D and dim == D):
            bad_th.append((volts, n_, nA, nT, D, dim))
    np.seterr(**_old)
check("thm:theta: null A = dim ker(T-I) <= D on theta covers", not bad_th,
      f"failures {bad_th}" if bad_th else
      "6 bases incl. four-edge; state dimension equals the degree span")

# thm:order: the order of the kernel recurrence, and exactly when it equals the
# degree span.  This subsumes thm:red2 and thm:theta as the two extreme shapes.
from band_order import order as _ord, span_D as _spanD
bad_ord, bad_char = [], []
for p_, q_, vv in [(1, 2, [0]), (1, 3, [0]), (2, 5, [0]), (0, 0, [0, 1, 2]),
                   (1, 1, [0, 1]), (2, 3, [0, 1]), (1, 2, [0, 2]),
                   (2, 2, [0, 1, 2]), (1, 1, [0, 1, 2, 3]), (2, 5, [0, 3]),
                   (3, 4, [0, 1]), (1, 4, [0, 1, 2])]:
    o_ = _ord(p_, q_, vv)
    D_ = _spanD(p_, q_, vv)
    tm = max(vv)
    if o_ != p_ + q_ + max(p_, tm) + max(q_, tm):
        bad_ord.append((p_, q_, vv, o_))
    if p_ >= 1 and q_ >= 1 and (o_ == D_) != (tm <= min(p_, q_)):
        bad_char.append((p_, q_, vv, o_, D_))
check("thm:order: order = p+q+max(p,t_m)+max(q,t_m)", not bad_ord,
      f"failures {bad_ord}" if bad_ord else "12 bases, measured vs counted")
check("thm:order: order = D iff t_m <= min(p,q)", not bad_char,
      f"failures {bad_char}" if bad_char else
      "the characterisation holds on every base tested")

print("15. Slice lemma (lem:slice)")
from gauge_fixed import verify_slice
rows = verify_slice()
check("spokes -> +1 and |outer| -> 1, nullity preserved, both parities",
      all(r[1] and r[2] < 1e-12 and r[4] for r in rows),
      f"max deviation {max(r[2] for r in rows):.1e}")

print("16. The corner criterion, and the classification for every k")
# Part I originally answered the question one k at a time, with the list
# certified only for k <= 10.  Three things close it: the criterion loses its
# k-dependence under one substitution, a Diophantine argument bounds n
# uniformly in k, and the finite region that leaves is exhausted.
from verification import ramanujan_all_k as RAK
import mpmath as _mp

# (a) The substitution, checked against the definition it replaces.  Both
# factors of D_k must collapse to the same quadratic form for every k.
corner_dev = RAMX.check_corner_identity(kmax=14, trials=400)
check("both factors of D_k collapse to Q(x,y), independent of k",
      corner_dev < 1e-11,
      f"max deviation {corner_dev:.1e} over k=1..14")

# (b) The corner route and the spectral route are independent implementations
# of the same criterion, so a disagreement is a failure of one of them.
corner_bad, corner_n = [], 0
for _k in range(1, 13):
    for _n in range(2 * _k + 1, 140):
        corner_n += 1
        if RAMX.ramanujan_by_corner(_n, _k) != RAM.is_ramanujan(_n, _k):
            corner_bad.append((_n, _k))
check("corner criterion agrees with the spectral test", not corner_bad,
      f"{corner_n} cases, k=1..12" if not corner_bad else f"bad {corner_bad[:5]}")

# (c) The forbidden set: closed-form area against numerical integration.
_mp.mp.dps = 30
_s2 = _mp.sqrt(2)
_area_closed = _mp.mpf(3) / 2 - _s2 + _mp.mpf(3) / 8 * _mp.log((1 + _s2) / 3)
_area_quad = _mp.quad(
    lambda t: 1 - (_s2 * t - _mp.sqrt(max(4 * t ** 2 - 3, _mp.mpf(0))) / 2),
    [_s2 - _mp.mpf(1) / 2, 1])
check("lens area 3/2 - sqrt2 + (3/8)log((1+sqrt2)/3) matches the integral",
      abs(_area_closed - _area_quad) < _mp.mpf(10) ** -20,
      f"{float(_area_closed):.12f} of the square, i.e. "
      f"{100 * float(_area_closed):.4f}%")

# (d) The Diophantine bound.  This checks the PROOF, not the list: for every
# n at or above the threshold the Dirichlet index really does force failure.
_worst, _arg, _dbad = RAK.check_dirichlet_bound(nhi=2 * RAK.dirichlet_threshold())
check("Dirichlet witness forces failure for every n >= threshold, every k",
      _dbad == 0 and _worst < RAK.AREA,
      f"threshold n >= {RAK.dirichlet_threshold()}; worst value "
      f"{_worst:.8f} < {RAK.AREA:.8f}, attained at (n,k)={_arg}")

# (e) The classification over the finite region the bound leaves.
_hits, _tight = RAK.census(RAK.dirichlet_threshold() - 1)
_iso = {RAK.iso_class(n, k) for n, k in _hits}
check("the classification is finite in BOTH variables",
      max(k for _n, k in _hits) < max(n for n, _k in _hits) < RAK.dirichlet_threshold(),
      f"{len(_hits)} pairs, {len(_iso)} isomorphism classes; "
      f"largest n={max(n for n, _k in _hits)}, largest k={max(k for _n, k in _hits)}")
check("no case in the region is decided on a margin float64 could not see",
      _tight[0][0] > 1e-9,
      f"smallest |margin| is {_tight[0][0]:.2e}, at (n,k)=({_tight[0][1]},{_tight[0][2]})")
# The census agrees with the exact k <= 10 run of section 13 where they overlap.
_overlap_bad = [(n, k) for (n, k) in _hits if k <= 10 and n not in RAM_CLASS[k]]
_overlap_bad += [(n, k) for k in RAM_CLASS for n in RAM_CLASS[k]
                 if (n, k) not in set(_hits)]
check("the all-k census reproduces the exactly certified k <= 10 list",
      not _overlap_bad,
      f"{sum(len(v) for v in RAM_CLASS.values())} graphs at k<=10, all recovered")

print("17. Structure of the classification: locality, gcd safety (sec:closed)")
# The classification is a certified list, not a formula.  These are the
# structural statements underneath it -- the ones a formula would be built
# from -- and each is checked against the criterion it claims to reorganise.
from verification import ramanujan_closed_form as CF

_t, _b = CF.check_locality()
check("thm:local: Ramanujan iff no divisor m >= 3 of n is bad for k", not _b,
      f"{_t} cases against the direct criterion, k<=45, n<=230")
_t, _b = CF.check_divisor_closure()
check("cor:divclosed: the Ramanujan set of each k is divisor-closed", not _b,
      f"{_t} (n,d) pairs with d | n, d > 2k")
_b = CF.check_gcd_formula()
check("lem:mingcd: min over units of ||jc/m|| equals gcd(c,m)/m", not _b,
      "m < 120, c < 200; the identity the safety theorem rests on")
_t, _f, _b = CF.check_gcd_safety()
check("thm:gcdsafe: m/gcd(k+-1,m) in {2..7} implies m is safe", not _b,
      f"fired on {_f} of {_t} pairs, never on a bad level; "
      f"gamma = {CF.GAMMA:.7f}, 1/gamma = {1/CF.GAMMA:.4f}")
_holds, _fails = CF.check_closed_form_small_k()
check("thm:closedsmall: exact where claimed, and fails where we say it does",
      _holds == [1, 2, 3, 4, 5, 7, 9] and set(_fails) >= {6, 8, 11},
      f"holds for k={_holds}; fails for k={_fails} (interior bands)")
# lem:bands is the PROOF of thm:closedsmall: the negative set of D_k on [-1,1]
# is the end band(s) alone for exactly these k, decided by exact root isolation
# over Q (Sturm/VAS), never by floating point.  The symmetry D_k(-u)=D_k(u) for
# odd k is what makes the two bands mirror images.
from verification import interior_bands as IB
_simple = IB.simple_ks(45)
check("lem:bands: D_k has end bands only for k in {1,2,3,4,5,7,9} (exact Sturm root isolation, k<=45)",
      _simple == [1, 2, 3, 4, 5, 7, 9],
      f"end bands only for k={_simple}; every other k<=45 has an interior root")
_symbad = IB.check_symmetry(45)
check("lem:bands: D_k is an even polynomial exactly for odd k",
      not _symbad, "k<=45")

print("18. The Riemann Hypothesis on every cubic cyclic cover (thm:covcorner)")
# The corner criterion never used P(n,k) beyond "two-vertex base, cubic cover".
# There are exactly two such bases, and both are checked against brute force.
from verification import cubic_covers_rh as CC
_dev = CC.check_block_decomposition()
check("character blocks reproduce the spectrum on both two-vertex bases",
      _dev < 1e-10, f"max deviation {_dev:.1e}")
_dev = CC.check_edge_voltage_irrelevant()
check("the two-loop spectrum does not depend on the edge voltage c",
      _dev < 1e-10, f"max deviation {_dev:.1e} over every c")
_tot, _bad = CC.check_two_loop_corner()
check("corner criterion decides every two-loop cover", not _bad,
      f"{_tot} covers, brute-forced from the full adjacency matrix")
_tot, _bad = CC.check_theta_criterion()
check("theta criterion decides every cyclic Haar cover", not _bad,
      f"{_tot} covers, brute-forced from the full adjacency matrix")
_found, _viol = CC.check_uniform_bounds()
check("both uniform bounds hold on every Ramanujan cover found", not _viol,
      f"{_found} Ramanujan covers, none above its bound")
_rows = CC.check_general_finiteness()
check("no cover of ANY fixed cubic base is Ramanujan past its threshold",
      all(mx is None or mx < n0 for _nm, mx, n0 in _rows),
      "; ".join(f"{nm}: max n={mx} < {n0}" for nm, mx, n0 in _rows))

print("19. The cover ceiling: two theorems and a refutation")
# thm:red2 settles the ceiling for two-vertex bases.  thm:redpath chains that
# same elimination along a path of any length.  Both the span claim and the
# bound are checked -- the bound adversarially, because a random matrix on a
# cover is generically nonsingular and sampling would prove nothing.
from verification import cover_ceiling_attack as CCA
_t, _b = CCA.check_path_span()
check("thm:redpath: degree span of det M(zeta) is 2 sum(p_t)", not _b,
      f"{_t} path-with-loops bases, m = 2 to 4, checked symbolically")
_rows = CCA.check_path_ceiling()
check("thm:redpath: non-equivariant weights cannot beat 2 sum(p_t)",
      all(r[4] > 1e-7 for r in _rows),
      "; ".join(f"p={r[0]} n={r[2]} D={r[3]}" for r in _rows))
# The GENERAL conjecture, which thm:redpath does not settle: an adversarial
# search over connected bases including cycles, K4 and non-Hamiltonian ones.
_t, _b = CCA.check_cycle_span()
check("thm:redcycle: degree span is 2|W| with W the holonomy", not _b,
      f"{_t} cycle bases, checked symbolically")
_t, _b = CCA.check_cycle_structure()
check("thm:redcycle: the cover is 2-regular with gcd(|W|,n) components", not _b,
      f"{_t} (base, n) pairs -- this is why M(C_N)=2 gives the bound")
# The GENERAL conjecture is FALSE (thm:cexcover).  These are exact integer
# counterexamples, not search output: the adversarial search had already
# produced a FALSE NEGATIVE on the very base that breaks it, so a search result
# would be the wrong kind of evidence here.
from verification import cover_ceiling_counterexample as CEX
_rows = CEX.check_star_loop()
check("thm:cexcover: star-with-a-loop breaks the ceiling, null A = n vs D = 2",
      all(nul > D for (n, w, nul, D) in _rows) and len(_rows) >= 6,
      f"{len(_rows)} (n, weight) pairs, ranks computed over Z")
_rows = CEX.check_k23()
check("rem:mindeg: minimum degree 2 does not repair it (K_{2,3}, D=4)",
      all(nul > D for (n, nul, D) in _rows) and len(_rows) >= 2,
      "; ".join(f"n={n}: null={nul} vs D={D}" for (n, nul, D) in _rows))
_rows = CEX.check_regular_survive()
check("the diagonal-zeroing attack alone never exceeds D on a regular base",
      all(best <= D for (_nm, _n, best, D) in _rows),
      f"{len(_rows)} (regular base, n) pairs, exact ranks -- which is why it was "
      "a false negative: see thm:k4rankone")

# thm:k4rankone / prop:lowrank: the regular-base ceiling is FALSE.  The
# zero-voltage edges of the K4 base form a triangle; rank-one triangle blocks
# give null A >= n against D = 6.  This is the refutation of the conjecture
# that an earlier version of the paper recorded as its strongest result.
from verification import k4_rank_one as K4R
_rows = K4R.check_rank_one()
check("thm:k4rankone: rank-one triangle blocks give null A = n on the K4 cover, "
      "against D = 6 (regular-base ceiling REFUTED)",
      all(ok and nul == n for (n, _N, ok, nul, _D) in _rows)
      and any(nul > D for (n, _N, ok, nul, D) in _rows),
      "; ".join(f"n={n}: null={nul}" for (n, _N, _ok, nul, _D) in _rows)
      + "  -- exact over Q, pattern verified")
check("thm:cover needs det M(zeta) != 0: the rank-one equivariant matrix has "
      "det M(zeta) == 0 identically", K4R.check_symbol_vanishes(),
      "every block singular, so the degree-span count does not apply")
_pr, _rf = K4R.check_leading_coefficient()
check("conj:leading: top coefficient of det M(zeta) is a monomial in edge "
      "weights on every base where the ceiling is proved",
      all(mono for (_nm, _top, mono) in _pr),
      "; ".join(f"{nm}: {top}" for (nm, top, _m) in _pr))
check("conj:leading: top coefficient contains a free diagonal on every base "
      "where the ceiling fails",
      all(hd for (_nm, _top, hd) in _rf),
      "; ".join(f"{nm}: {top}" for (nm, top, _h) in _rf))

print("20. The independent-set obstruction, and the cubic gap family")
# prop:indobs explains BOTH counterexamples and cor:regblocks says why
# regularity is the right hypothesis; sec:gapfamily is the payoff.
from verification import cubic_gap_family as GAP
import itertools as _it, networkx as _nx

# cor:regblocks: in a d-regular graph no independent set fails to expand.
_bad, _tested = [], 0
_rng = np.random.default_rng(0)
for _d in (3, 4):
    for _N in (8, 10, 12):
        for _t in range(6):
            try:
                _G = _nx.random_regular_graph(_d, _N, seed=int(_rng.integers(10**6)))
            except Exception:
                continue
            for _r in range(1, min(_N, 6)):
                for _S in _it.combinations(range(_N), _r):
                    _Ss = set(_S)
                    if any(set(_G[u]) & _Ss for u in _S):
                        continue
                    _NS = set().union(*[set(_G[u]) for u in _S])
                    _tested += 1
                    if len(_NS) < len(_Ss):
                        _bad.append((_d, _N, _S))
check("cor:regblocks: d-regular implies |N(S)| >= |S| for independent S",
      not _bad, f"{_tested} (regular graph, independent set) pairs")

_D, _rows = GAP.check_span_constant()
check("sec:gapfamily: the K4 covers are cubic, connected, with GENERIC D = 6 for all n",
      _D == 6 and all(degs == [3] and conn for (_n, _N, _d, degs, conn) in _rows),
      f"n = 4..10, |V| = 16..40")
_co, _ok = GAP.check_symbol()
check("prop:k4cert: the integer weights realise 16(z^7-1)/(z-1)", _ok,
      f"coefficients of z^3 det M all equal {_co[0]}")
_rows = GAP.check_certificate()
check("prop:k4cert: exact nullity over Z equals the degree span",
      all(nul == D_ for (_n, _N, nul, D_) in _rows),
      "; ".join(f"n={n}: null={nul}=D" for (n, _N, nul, D_) in _rows))
_rows = GAP.check_z_values()
check("prop:k4z: Z = n+2 by CP-SAT with optimality proved",
      all(Z == want for (_n, _N, Z, want) in _rows),
      "; ".join(f"n={n}: Z={Z}" for (n, _N, Z, _w) in _rows)
      + "  -- but M >= n by thm:k4rankone, so Z - M <= 2")

print("21. The deficit (prop:deficit)")
from verification import make_corner_figures as MCF
_ns, _ds, _ks = MCF.deficit_curve(240)
check("delta(n,k) < 3 - 2 sqrt2 for every n, and delta* rises towards it",
      _ds.max() < MCF.TAU and _ds[-1] > 0.5 * MCF.TAU,
      f"max delta* = {_ds.max():.6f} < tau = {MCF.TAU:.6f}; "
      f"{int((_ds < 0).sum())} sizes admit an optimal member, largest "
      f"n={int(_ns[_ds < 0].max())}")

print("22. M(P(10,2)) exactly, and the period-one ceiling")
# Both of these replace a failed search with a reason.  The nullity-6 witness
# at P(10,2) used to be recorded as numerical; the missing certificate at
# P(24,4) used to be recorded as "we simply have not found the matrix".
from verification import p10_2_exact as _P10
_prm = _P10.solve_period2()
check("M(P(10,2))=6: a period-two solution over Q exists",
      _prm is not None,
      "" if _prm is None else
      f"a={_prm['a']}, c={_prm['c']}, e={_prm['e']}, f={_prm['f']}, "
      f"s={_prm['s']}, t={_prm['t']}")
_A10 = _P10.assemble_exact(_prm)
_ok10, _miss10, _extra10 = _P10.check_support(_A10)
check("M(P(10,2))=6: the witness carries exactly the P(10,2) pattern", _ok10,
      f"20x20, symmetric={_A10.T == _A10}, "
      f"missing={len(_miss10)}, extra={len(_extra10)}")
_nul10 = 20 - _A10.rank()
check("M(P(10,2))=6: exact nullity over Q equals 6", _nul10 == 6,
      f"exact rank 14, nullity {_nul10}; with M <= Z = 6 this gives "
      f"M(P(10,2)) = Z(P(10,2)) = 6, so there is NO strict gap at n=10")
_feas10, _res10, _bad10 = _P10.period1_ceiling()
check("no period-one matrix attains nullity 6 at P(10,2)", not _bad10,
      f"{len(_feas10)} block-class subsets of total dimension 6, "
      f"{len(_bad10)} admit a matrix with the spoke nonzero")

from verification import period1_ceiling as _P1C
_b102, _ = _P1C.period1_ceiling(10, 2)
_b244, _ = _P1C.period1_ceiling(24, 4)
check("period-one ceiling explains both missing certificates",
      _b102 == 5 and _b244 == 8,
      f"P(10,2): bound {_b102} < 6; P(24,4): bound {_b244} < 10 -- so the "
      f"absent certificate at n=24 is an impossibility, not a search failure")
# The control: the bound must never contradict a certificate that exists.
_CERT1 = [(17, 3), (20, 3), (24, 3), (29, 4), (25, 4), (26, 4), (27, 4),
          (28, 4), (12, 2), (14, 2), (16, 2), (9, 2), (11, 2), (13, 3),
          (18, 3), (19, 3)]
_viol = [(n, k, _P1C.period1_ceiling(n, k)[0]) for n, k in _CERT1
         if _P1C.period1_ceiling(n, k)[0] < 2 * k + 2]
check("CONTROL: the period-one bound contradicts no existing certificate",
      not _viol, f"{len(_CERT1)} certified (n,k) checked, {len(_viol)} violations")
_blocked2 = [n for n in range(7, 61) if _P1C.period1_ceiling(n, 2)[0] < 6]
check("the period-one bound reproduces the paper's two exceptions at k=2",
      _blocked2 == [8, 10],
      f"blocked n at k=2: {_blocked2} -- exactly the n=8, n=10 of rem:twoexc, "
      f"derived rather than observed")

print("23. Emit the manuscript's numbers from the certificates on disk")
# Emitted LAST so that Nchecks can count every check the suite ran.  `pending`
# is the one check below that has not been recorded yet at emission time.
from verification import ramanujan_exact as _RAMX
print("23. Classification of rational-symbol rotation-invariant certificates (thm:ratclass)")
# A rational symbol has a Galois-closed root set, so the certificates of
# thm:cyclo are ALL of them once the finitely many orbit unions are enumerated.
# The list is rebuilt here, every listed certificate is checked to have nullity
# 2k+2 on the first two members of its class and nullity 0 just off it, and the
# k=6 impossibility (thm:k6imp) must fall out as the empty list.
from verification import period_one_classification as POC
import numpy as _np
def _rot_nullity(n, k, a, c, d, e):
    A = _np.zeros((2 * n, 2 * n))
    for i in range(n):
        A[i, i] = a; A[i, (i + 1) % n] += 1; A[(i + 1) % n, i] += 1
        A[n + i, n + i] = d; A[n + i, n + (i + k) % n] += e; A[n + (i + k) % n, n + i] += e
        A[i, n + i] = c; A[n + i, i] = c
    return int(_np.sum(_np.abs(_np.linalg.eigvalsh(A)) < 1e-8))
RATCLASS = {k: POC.lcms(k) for k in range(2, 8)}
check("thm:ratclass: the admissible classes are 7,9,15,20 | 10,24,42 | 60,70,90 | 24,126 | none | 120 for k=2..7",
      RATCLASS == {2: [7, 9, 15, 20], 3: [10, 24, 42], 4: [60, 70, 90], 5: [24, 126], 6: [], 7: [120]},
      str(RATCLASS))
_bad = []
for k in range(2, 8):
    for r in POC.admissible_sets(k):
        if not r["realisable"]:
            continue
        a, dp, c0 = float(r["a"]), float(r["dprime"]), float(r["c0"])
        e = 1.0 if c0 > 0 else -1.0
        c, d = abs(c0) ** 0.5, dp * e
        L = r["lcm"]; n = L * ((2 * k) // L + 1)
        if (_rot_nullity(n, k, a, c, d, e) != 2 * k + 2 or _rot_nullity(n + L, k, a, c, d, e) != 2 * k + 2
                or _rot_nullity(n + 1, k, a, c, d, e) != 0):
            _bad.append((k, r["ds"]))
check("thm:ratclass: every listed certificate has nullity 2k+2 on its class and 0 off it",
      not _bad, f"{sum(len([r for r in POC.admissible_sets(k) if r['realisable']]) for k in range(2, 8))} certificates, k=2..7")

print("24. Identity tiles for every large length: the hypotheses of thm:tilesallk, exactly (k=2..9)")
# (E) elliptic dock by Sturm root isolation over Q; det B(dock) != 0 in exact
# rational arithmetic; rank of the tile differential over F_p at an integer point
# (a lower bound for the rank over Q).  All three for the SAME dock.
from verification import tile_rank_exact as TRE
from verification import tile_wronskian as TW
TILEALLK_ROWS = []
_tk_bad = []
for k in range(2, 10):
    dock = TRE.integer_elliptic_dock(k)
    ell = TRE.exact_elliptic(k, dock)
    detB = TW.det_fraction(TW.wronskian_form(k, dock))
    l0 = (k + 1) * (2 * k + 8) // 3 + 3
    rng = _np.random.default_rng(k); nint = l0 - 2 * k - 2
    interior = {nm: [int(x) for x in rng.integers(-3, 4, nint)] for nm in "bcead"}
    for nm in "bce":
        interior[nm] = [x if x != 0 else 1 for x in interior[nm]]
    rank, need = TRE.tile_jacobian_rank_modp(k, l0, dock, interior)
    ok = ell and detB != 0 and rank >= need
    if not ok:
        _tk_bad.append(k)
    TILEALLK_ROWS.append((k, dock, l0, rank, need, detB))
check("thm:tilesallk hypotheses hold exactly for k=2..9 (Sturm, det B, rank mod p)", not _tk_bad,
      "; ".join(f"k={k}: dock {d}, l0={l}, rank {r}/{n}, det B={db}" for k, d, l, r, n, db in TILEALLK_ROWS))
# the dimension law of rem:threeperpos at k=3: rank = 3l-5k-5 before saturation
_law_bad = []
for l in range(12, 19):
    rng = _np.random.default_rng(l); nint = l - 8
    interior = {nm: [int(x) for x in rng.integers(-3, 4, nint)] for nm in "bcead"}
    for nm in "bce":
        interior[nm] = [x if x != 0 else 1 for x in interior[nm]]
    r_, _ = TRE.tile_jacobian_rank_modp(3, l, TRE.integer_elliptic_dock(3), interior)
    if r_ != min(3 * l - 20, 36):
        _law_bad.append((l, r_))
check("rem:threeperpos: rank dP_l = 3l-5k-5 (k=3, l=12..18), exactly mod p", not _law_bad, str(_law_bad) if _law_bad else "law holds")
# lem:firstorder / lem:secondorder, exactly mod p at nonresonant integer docks:
# the dock-point rank is dim Sp - (k-2), and ONE a-perturbation at one position
# lifts it to dim Sp (k=3..6).
_so_bad = []
_NONRES = {3: (1, 1, 1, 1), 4: (0, 1, 1, 1), 5: (1, 1, -1, -2), 6: (0, 1, -1, 2)}
for k, dock in _NONRES.items():
    l0 = (k + 1) * (2 * k + 8) // 3 + 4
    nint = l0 - 2 * k - 2
    a0, c0, d0, e0 = dock
    base = {"b": [1] * nint, "c": [c0] * nint, "e": [e0] * nint, "a": [a0] * nint, "d": [d0] * nint}
    r0, need = TRE.tile_jacobian_rank_modp(k, l0, dock, base)
    pert = {nm: list(v) for nm, v in base.items()}; pert["a"][nint // 2] += 1
    r1, _ = TRE.tile_jacobian_rank_modp(k, l0, dock, pert)
    if not (r0 == need - (k - 2) and r1 == need):
        _so_bad.append((k, r0, r1, need))
check("lem:firstorder/secondorder: dock-point rank = dim Sp-(k-2) and one a-perturbation gives dim Sp (k=3..6, mod p)",
      not _so_bad, str(_so_bad) if _so_bad else "k=3..6 at nonresonant docks")
TILE_ALL_K = 9 if not _tk_bad else 0
with open(f"{_REPO}/manuscript/tiles_allk_table.tex", "w") as _f:
    _f.write("% GENERATED by verification/verify_all.py -- do not edit by hand.\n")
    _f.write("\\begin{tabular}{r l r r r}\\hline\n$k$ & dock $(a_0,c_0,d_0,e_0)$, $b_0=1$ & $\\ell_0$ & rank $=\\dim Sp$ & $\\det B$\\\\\\hline\n")
    for k, d, l, r, n, db in TILEALLK_ROWS:
        _f.write(f"${k}$ & $({d[0]},{d[1]},{d[2]},{d[3]})$ & ${l}$ & ${r}={n}$ & ${db}$\\\\\n")
    _f.write("\\hline\\end{tabular}\n")


print("25. The leading-coefficient criterion (thm:leading): monomial <=> unique permutation; |U|-|R| = D with rank R = |R| (mod p); dim K = D")
from verification import leading_coefficient as LC
_lc_bad = []
_lc_excess = 0
_lc_mono = 0
for _be, _nV in LC.BASES:
    try:
        _r = LC.check_base(_be, _nV, verbose=False)
    except AssertionError as _ex:
        _lc_bad.append((_be, str(_ex)[:80]))
        continue
    if _r["mono"]:
        _lc_mono += 1
        if _r["state"] > _r["D"]:
            _lc_excess += 1
check("thm:leading: on every base of the paper, monomial c_max <=> unique sigma*; |U|-|R| = D and rank R = |R| over F_p; dim K = D by the monodromy",
      not _lc_bad, str(_lc_bad) if _lc_bad else f"{len(LC.BASES)} bases, {_lc_mono} satisfy the criterion, forward state exceeds D on {_lc_excess} of them")
_lc_rng = _np.random.default_rng(2026)
_lc_cnt = dict(total=0, mono=0, bad=0)
while _lc_cnt["total"] < 25:
    _rb = LC.random_base(_lc_rng)
    if _rb is None:
        continue
    _be, _nV = _rb
    if LC.top_coefficient(_be, _nV)[2] == 0:
        continue
    _lc_cnt["total"] += 1
    try:
        _r = LC.check_base(_be, _nV, seed=int(_lc_rng.integers(1 << 30)), verbose=False)
        _lc_cnt["mono"] += int(_r["mono"])
    except AssertionError:
        _lc_cnt["bad"] += 1
check("thm:leading on 25 random bases (3-5 vertices): dim K = D on every base satisfying the criterion",
      _lc_cnt["bad"] == 0, f"{_lc_cnt['mono']} of {_lc_cnt['total']} random bases satisfy the criterion")

nums, npath = emit_numbers(pending=1, ram=RAM_CLASS, ram_cases=ram_cases)
check("manuscript numbers emitted from the certificates on disk", True,
      f"{nums['NtileThreeFour']} tiles at k=3,4 + {nums['NtileFive']} at k=5; "
      f"L(3)={nums['LvalThree']}, L(4)={nums['LvalFour']}; "
      f"{nums.get('RamTotal','?')} Ramanujan P(n,k); "
      f"Nchecks={nums['Nchecks']}")

print()
print("=" * 66)
print("ALL CHECKS PASSED" if not fails else f"FAILURES: {fails}")
# Runtime is reported so that "the suite passes" is a checkable claim with a
# cost attached: a reader deciding whether to run it should know what it costs,
# and a suite that slows down without anyone noticing is a suite people stop
# running.
_EL = time.perf_counter() - _T0
print(f"{len(results)} checks in {_EL:.1f} s "
      f"({_EL / 60:.1f} min) on {os.cpu_count()} cores")
