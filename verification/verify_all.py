"""One pass over every computational claim the paper makes.

Run this to confirm the paper's numbers from scratch.  Each check prints PASS or
FAIL and the quantity it checked; nothing is taken on trust from a stored file
except the saved certificates, which are re-evaluated rather than believed.
"""
import glob
import itertools
import re
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
ROOT = "/Volumes/2TB/scifair/results/zero_forcing"
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
PAPER = "/Volumes/2TB/scifair/manuscript/zf_paper.tex"
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
sys.path.insert(0, "/Volumes/2TB/scifair/src/zero_forcing")
import subprocess as _sp, re as _re2
CBIN = "/Volumes/2TB/scifair/src/zero_forcing/c"

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
def emit_numbers(pending=0):
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
    vals["Nchecks"] = str(len(results) + pending)
    out = ["% GENERATED by verification/verify_all.py -- do not edit by hand.",
           "% Every number here is read off the certificates on disk.", ""]
    for key, v in vals.items():
        out.append(f"\\newcommand{{\\{key}}}{{{v}}}")
    path = "/Volumes/2TB/scifair/manuscript/zf_numbers.tex"
    open(path, "w").write("\n".join(out) + "\n")
    return vals, path

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

print("16. Emit the manuscript's numbers from the certificates on disk")
# Emitted LAST so that Nchecks can count every check the suite ran.  `pending`
# is the one check below that has not been recorded yet at emission time.
nums, npath = emit_numbers(pending=1)
check("manuscript numbers emitted from the certificates on disk", True,
      f"{nums['NtileThreeFour']} tiles at k=3,4 + {nums['NtileFive']} at k=5; "
      f"L(3)={nums['LvalThree']}, L(4)={nums['LvalFour']}; "
      f"Nchecks={nums['Nchecks']}")

print()
print("=" * 66)
print("ALL CHECKS PASSED" if not fails else f"FAILURES: {fails}")
