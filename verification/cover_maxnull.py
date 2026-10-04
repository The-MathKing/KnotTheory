"""Maximum nullity over a cyclic cover, by a parametrisation that cannot degenerate.

WHY A NEW INSTRUMENT.  cover_ceiling_search.py failed its control four different
ways, and every failure had the same cause: the optimiser reached AK=0 by driving
an edge weight to zero, leaving a matrix that is not a matrix OF the graph.
Barriers and gauge-fixing did not stop it.

The fix is a reparametrisation, not a penalty.  Write every edge weight as

        w_e = s_e * exp(t_e),      s_e in {+1,-1} fixed,  t_e free,

so |w_e| > 0 identically and the degenerate stratum is simply NOT IN THE
PARAMETER SPACE.  The optimiser cannot go there because it does not exist.
Diagonal entries stay free (they may vanish).

Objective: drive the r smallest singular values of A to zero.  Scale is fixed by
normalising A, which removes the other direction the old search used to cheat.

The sign pattern matters -- nullity is not achievable for every sign class -- so
we sweep signs as well as starting points.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys, itertools
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, f"{_REPO}/verification")
from certify_general import assemble


def cover_cells(base_edges, nV, n):
    """Weight slots: every lift of every base edge, plus every vertex diagonal."""
    diag, edge, seen = [], [], set()
    for x in range(nV):
        for i in range(n):
            diag.append(("diag", [(x * n + i, x * n + i)]))
    for (x, y, v) in base_edges:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            if p == q:
                continue
            key = (min(p, q), max(p, q))
            if key in seen:
                continue
            seen.add(key)
            edge.append(("edge", [(p, q), (q, p)]))
    return diag + edge, len(diag)


def max_nullity(base_edges, nV, n, r, tries=60, seed=0, sign_sweep=12):
    """Can null A reach r?  Returns (achieved, best_normalised_sigma_r)."""
    N = nV * n
    cells, nd = cover_cells(base_edges, nV, n)
    ne = len(cells) - nd
    rng = np.random.default_rng(seed)
    best = np.inf
    for s_trial in range(sign_sweep):
        signs = np.ones(ne) if s_trial == 0 else rng.choice([-1.0, 1.0], ne)
        for t in range(max(1, tries // sign_sweep)):
            z0 = np.concatenate([rng.standard_normal(nd),
                                 rng.standard_normal(ne) * 0.5])

            def res(z):
                w = np.concatenate([z[:nd], signs * np.exp(z[nd:])])
                A = assemble(w, cells, N)
                sv = np.linalg.svd(A, compute_uv=False)
                return sv[-r:] / (sv.max() + 1e-300)

            # BOUND THE SPREAD.  exp(t) with t unbounded removed the
            # weights-to-zero cheat but opened weights-to-infinity: the
            # optimiser inflated one edge to 3.8e6 against neighbours at 0.1,
            # so normalising by sigma_max made every other singular value look
            # like zero.  |t| <= TMAX keeps every edge weight in
            # [e^-TMAX, e^TMAX]; the project's own certificates sit at a spread
            # of about 7, so this is generous, and it makes both escapes
            # unreachable rather than merely penalised.
            TMAX = 2.5
            lo = np.concatenate([np.full(nd, -np.inf), np.full(ne, -TMAX)])
            hi = np.concatenate([np.full(nd, np.inf), np.full(ne, TMAX)])
            z0 = np.clip(z0, lo + 1e-9, hi - 1e-9)
            out = least_squares(res, z0, method="trf", bounds=(lo, hi),
                                max_nfev=3000, xtol=1e-15, ftol=1e-15,
                                gtol=1e-15)
            w = np.concatenate([out.x[:nd], signs * np.exp(out.x[nd:])])
            A = assemble(w, cells, N)
            sv = np.linalg.svd(A, compute_uv=False)
            score = sv[-r] / sv.max()
            # Nullity r means the r smallest singular values are numerically zero
            # AND separated from the next one.  An absolute cutoff alone is the
            # wrong test: a converged solution sits near 1e-9 relative, not 1e-15,
            # because the objective is itself a singular value.  The SPECTRAL GAP
            # is what distinguishes rank deficiency from mere smallness.
            gap = sv[-r] / sv[-r - 1] if r < len(sv) else 1.0
            best = min(best, score)
            if score < 1e-7 and gap < 1e-4:
                return True, score
    return False, best
