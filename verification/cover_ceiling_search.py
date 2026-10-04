"""Is the ceiling a property of the COVER, or only of equivariant matrices?

Theorem thm:cover bounds null A by the degree span of det M(zeta) for matrices
that commute with the Z_n action.  Theorem thm:red proves the far stronger
statement -- the bound holds for EVERY matrix carrying the pattern -- but only
for P(n,k), where the nonzero spoke weight makes the elimination possible.  The
paper records the general case as open:

    "Whether the corresponding elimination can be carried out over an arbitrary
     base graph -- and so whether the ceiling is a property of the cover rather
     than of equivariant matrices on it -- we leave open."

Settling it either way is worth months of proof effort, so before attempting a
proof we look for a COUNTEREXAMPLE: a cyclic cover and fully non-equivariant
weights with null A > span.  If one exists the conjecture is dead and we learn
it in an afternoon.

THE CONTROL MATTERS MORE THAN THE SEARCH.  A search that fails proves nothing
-- this project has twice mistaken a stalled solve for a negative result.  So
every cover is run at TWO targets: r = span, which must SUCCEED (showing the
solver can find nullity when it exists), and r = span + 1, which is the
violation.  A cover only contributes evidence if its control passes.

STATUS, STATED HONESTLY: THIS EXPERIMENT DOES NOT YET WORK.

Four formulations were tried and the CONTROL failed in every one.  The control
asks the search to find nullity r = span on P(n,2), where a nullity-6 matrix is
known to exist (Theorem thm:k2all gives one explicitly).  A search that cannot
recover a solution we already possess cannot license any conclusion about a
cover where we do not, so no result is reported from it.

  1. bilinear A(w)K(X)=0 with plain least-squares      -> control failed
  2. minimise the r smallest singular values of A(w)   -> control failed, and
     this is the eigenvalue-minimising method the project already WITHDREW as
     unreliable; re-deriving it was a mistake
  3. bilinear + damped Levenberg-Marquardt             -> collapsed edges to 0
  4. the same, with the lifts of one base edge gauge-fixed at 1   -> still fails

What is missing is the rest of the gauge machinery that makes the P(n,k)
pipeline work: the slice lemma normalisation, fixing a large subset of unknowns
at exact rationals, and the structural choice of square subsystem.  Porting all
of that to arbitrary covers is days of work, not an afternoon, so this line is
PARKED rather than reported.

The file is kept because the design is right even though the instrument is not
sensitive enough yet: run the control and the violation together, and refuse to
draw a conclusion when the control fails.  That is the only reason the three bad
formulations above were caught instead of being written up as evidence that the
ceiling holds.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, f"{_REPO}/verification")
from certify_general import assemble, graph_form, build_K, jac


def cover_cells(base_edges, nV, n):
    """Weight slots for a FULLY non-equivariant matrix on the cover: every lift
    of every base edge gets its own weight, every vertex its own diagonal."""
    cells, seen = [], set()
    for x in range(nV):
        for i in range(n):
            p = x * n + i
            cells.append(("diag", [(p, p)]))
    for (x, y, v) in base_edges:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            if p == q:
                continue
            key = (min(p, q), max(p, q))
            if key in seen:
                continue
            seen.add(key)
            cells.append(("edge", [(p, q), (q, p)]))
    return cells


def degree_span(base_edges, nV, seed=0):
    """Degree span of det M(zeta): the ceiling from Theorem thm:cover.

    Computed numerically rather than symbolically -- sympy's determinant of a
    symbolic Laurent matrix is far too slow to run inside a search.  det M(zeta)
    is a Laurent polynomial of bounded degree, so evaluating it at N-th roots of
    unity and taking an inverse FFT recovers its coefficients exactly enough to
    read off the span.  Random weights are used because the span is generic: a
    special choice could only make it smaller.
    """
    rng = np.random.default_rng(seed)
    w = rng.standard_normal(len(base_edges)) + 2.0
    a = rng.standard_normal(nV)
    V = max(abs(v) for (_, _, v) in base_edges)
    N = 8 * (nV * V + 2)
    vals = np.empty(N, dtype=complex)
    for t in range(N):
        z = np.exp(2j * np.pi * t / N)
        M = np.zeros((nV, nV), dtype=complex)
        for e, (x, y, v) in enumerate(base_edges):
            M[x, y] += w[e] * z ** v
            M[y, x] += w[e] * z ** (-v)
        for x in range(nV):
            M[x, x] += a[x]
        vals[t] = np.linalg.det(M)
    # det M(z) = sum_{d=-D}^{D} c_d z^d ; multiply by z^D to make it a polynomial
    D = nV * V
    coef = np.fft.ifft(vals * np.exp(-2j * np.pi * D * np.arange(N) / N))
    nz = np.where(np.abs(coef) > 1e-8 * np.abs(coef).max())[0]
    lo, hi = nz.min(), nz.max()
    return int(hi - lo)


def try_nullity(base_edges, nV, n, r, tries=40, seed=0):
    """Search for weights with null A(w) >= r, edges bounded away from zero.

    Two earlier formulations here were wrong, and both failed their control.
    The second minimised the r smallest singular values of A(w) directly --
    which is precisely the eigenvalue-minimising search this project already
    WITHDREW as unreliable, because it collapses onto degenerate strata.  Having
    re-derived a known-bad method, we use the one the project knows works: the
    bilinear system A(w)K(X)=0 with K in graph form, solved by damped
    Levenberg-Marquardt with an adaptive damping parameter, exactly as
    certify_tiles does.  f is quadratic and its Jacobian affine, so this is far
    better conditioned than anything phrased in singular values.
    """
    N = nV * n
    cells = cover_cells(base_edges, nV, n)
    nw = len(cells)
    ndiag = nV * n
    rng = np.random.default_rng(seed)
    best = np.inf
    # GAUGE FIXING.  A -> D A D for positive diagonal D preserves both nullity
    # and pattern, so the weights carry a scaling freedom whose orbit includes
    # arbitrarily small edges.  Without removing it the solver simply collapses
    # an edge to reach AK=0 -- which is what happened here twice.  This is the
    # general-cover analogue of the slice lemma: pin the lifts of ONE base edge
    # (a spanning-tree edge of B) at 1 and never vary them.
    pin = set()
    tree_edge = 0
    for idx, (kind, cl) in enumerate(cells):
        if kind == "edge" and idx >= ndiag:
            pin.add(idx)
            if len(pin) >= n:
                break
    pin = sorted(pin)
    freew = [i for i in range(nw) if i not in set(pin)]
    for t in range(tries):
        w = rng.standard_normal(nw)
        w[ndiag:] = np.sign(w[ndiag:]) * (0.6 + np.abs(w[ndiag:]))
        for i in pin:
            w[i] = 1.0
        A0 = assemble(w, cells, N)
        K0 = np.linalg.svd(A0)[2][-r:].T
        perm, X = graph_form(K0, r)
        z = np.concatenate([w, X.ravel()])

        def F(z):
            return (assemble(z[:nw], cells, N)
                    @ build_K(z[nw:].reshape(N - r, r), perm, N, r)).ravel()

        def J(z):
            return jac(z[:nw], z[nw:].reshape(N - r, r), cells, perm, N, r)

        nu, f = 1e-3, F(z)
        for _ in range(300):
            cols = freew + list(range(nw, len(z)))
            Js = J(z)[:, cols]
            H = Js.T @ Js
            try:
                step = np.linalg.solve(
                    H + nu * np.diag(np.diag(H) + 1e-12), -Js.T @ f)
            except np.linalg.LinAlgError:
                nu *= 10
                continue
            zt = z.copy()
            zt[cols] += step
            ft = F(zt)
            if np.all(np.isfinite(ft)) and np.abs(ft).max() < np.abs(f).max():
                z, f, nu = zt, ft, max(nu * 0.3, 1e-14)
            else:
                nu *= 8
                if nu > 1e12:
                    break
            if np.abs(f).max() < 1e-13:
                break
        w = z[:nw]
        A = assemble(w, cells, N)
        sv = np.linalg.svd(A, compute_uv=False)
        sc = np.abs(w).max()
        edges = np.abs(w[ndiag:]).min() / sc
        score = sv[-r] / sv.max() if edges > 0.05 else np.inf
        best = min(best, score)
        if score < 1e-10:
            return True, score
    return False, best


def run(name, base_edges, nV, n, tries=12):
    span = degree_span(base_edges, nV)
    ok_ctl, s_ctl = try_nullity(base_edges, nV, n, span, tries=tries, seed=1)
    if not ok_ctl:
        print(f"  {name:34s} n={n:<3} span={span:<3} "
              f"CONTROL FAILED ({s_ctl:.1e}) -- this cover proves nothing")
        return None
    ok_vio, s_vio = try_nullity(base_edges, nV, n, span + 1, tries=tries, seed=2)
    verdict = ("COUNTEREXAMPLE" if ok_vio else "ceiling held")
    print(f"  {name:34s} n={n:<3} span={span:<3} control OK   "
          f"r=span+1 best {s_vio:.2e}   {verdict}")
    return ok_vio


if __name__ == "__main__":
    print(__doc__)
    print("=" * 78)
    COVERS = [
        ("P(n,2) base",            [(0,0,1),(1,1,2),(0,1,0)], 2),
        ("P(n,3) base",            [(0,0,1),(1,1,3),(0,1,0)], 2),
        ("theta, voltages 0,1,2",  [(0,1,0),(0,1,1),(0,1,2)], 2),
        ("theta, voltages 0,1,3",  [(0,1,0),(0,1,1),(0,1,3)], 2),
        ("2-vtx, loops 1 and 2",   [(0,0,1),(1,1,2),(0,1,0),(0,1,1)], 2),
        ("3-vtx path, volt 1,2",   [(0,1,1),(1,2,2),(0,0,1)], 3),
        ("3-vtx cycle mixed",      [(0,1,0),(1,2,1),(2,0,2)], 3),
        ("3-vtx, two loops",       [(0,0,1),(1,1,2),(2,2,0),(0,1,0),(1,2,0)], 3),
        ("4-vtx mixed",            [(0,0,1),(1,1,3),(2,2,2),(3,3,5),
                                    (0,1,0),(1,2,1),(2,3,0),(3,0,2)], 4),
    ]
    found = []
    for n in (9, 11):
        print(f"\n--- n = {n} ---")
        for name, be, nV in COVERS:
            r = run(name, be, nV, n)
            if r:
                found.append((name, n))
    print()
    print("=" * 78)
    if found:
        print(f"CEILING VIOLATED on {found} -- the general conjecture is FALSE")
    else:
        print("No violation found on any cover tested, with every control "
              "passing.\nThat is evidence for the general ceiling, not a proof "
              "of it.")
