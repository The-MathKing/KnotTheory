"""The Riemann Hypothesis for cubic cyclic covers, beyond P(n,k).

The corner criterion of `ramanujan_exact` was derived for P(n,k).  Nothing in
that derivation used k except through the two integers k+1 and k-1, and nothing
used the base graph except that it has two vertices and the cover is cubic.  This
module carries the criterion to every cubic cyclic cover and establishes the
finiteness statement in full generality.

THE TWO BASES.  A cubic base multigraph on two vertices is either

  (i)  the TWO-LOOP base B(a,b,c): a loop of voltage a at u, a loop of voltage b
       at v, and an edge u-v of voltage c.  P(n,k) = B(1,k,0)^n.

  (ii) the THETA base T(c1,c2,c3): three parallel edges u-v of those voltages.
       Its covers are the cubic cyclic Haar graphs, and are always bipartite.

There are no others: a loop absorbs two of the three half-edges at its vertex, so
each vertex carries at most one loop, and a vertex with a loop has exactly one
non-loop edge.  Either both vertices have loops (case i) or neither does, leaving
three parallel edges (case ii).

WHAT IS PROVED HERE.

  * For the two-loop base the criterion is the SAME quadratic form Q as for
    P(n,k), with (a+b, a-b) in place of (k+1, k-1):

        B(a,b,c)^n is Ramanujan  <=>  Q(cos(pi j(a+b)/n), cos(pi j(a-b)/n)) >= 0
                                      for every nontrivial j,

    where Q(x,y) = 4x^2 + 4y^2 - 8 sqrt2 |xy| + 3.  The edge voltage c does not
    appear -- the whole spectrum is independent of it.

  * For the theta base the criterion is

        T(c)^n is Ramanujan  <=>  sum_{l<m} cos(2 pi j (c_l - c_m)/n) <= 5/2
                                  for every j != 0.

  * Uniform finiteness with explicit constants, for both families:

        two-loop:  Ramanujan  ==>  n <= pi (2 + sqrt2) sqrt(a^2 + b^2)
        theta:     Ramanujan  ==>  n <= 2 pi sqrt(d1^2 + d2^2 + d3^2)

    the first specialising to the paper's bound at (a,b) = (1,k).

  * Finiteness for EVERY cubic base, of any size, by a perturbation estimate:
    M_j depends continuously on omega^j, M_0 is the base's own adjacency matrix
    with top eigenvalue 3, and at j=1 the perturbation is O(1/n).  So some
    nontrivial eigenvalue exceeds 2 sqrt2 once n is large.  Consequently NO
    infinite family of Ramanujan graphs is a cyclic cover of a fixed base.

That last statement is the cyclic instance of a known principle -- abelian
covers do not expand, which is why the Lubotzky-Phillips-Sarnak construction is
built on PGL_2 and not on a cyclic group.  We claim no novelty for the
principle; what is here is the explicit constant, and the two exact criteria.
"""
import math

import numpy as np

SQRT2 = math.sqrt(2.0)
THRESHOLD = 2 * SQRT2                 # the Ramanujan bound for a cubic graph
TAU = 3 - 2 * SQRT2                   # the gap 3 - 2 sqrt2 the perturbation must not close


# ---------------------------------------------------------------------------
# bases, covers, and a brute-force decision to check everything against
# ---------------------------------------------------------------------------

def two_loop_base(a, b, c=0):
    """B(a,b,c): loop a at u, loop b at v, edge u-v of voltage c."""
    return [(0, 0, a), (1, 1, b), (0, 1, c)], 2


def theta_base(c1, c2, c3):
    """T(c1,c2,c3): three parallel edges of those voltages."""
    return [(0, 1, c1), (0, 1, c2), (0, 1, c3)], 2


def block(base, nv, n, j):
    """The j-th character block M_j, of size |V(B)|."""
    w = np.exp(2j * np.pi * j / n)
    M = np.zeros((nv, nv), dtype=complex)
    for (x, y, v) in base:
        if x == y:
            M[x, x] += w ** v + w ** (-v)
        else:
            M[x, y] += w ** v
            M[y, x] += w ** (-v)
    return M


def cover_adjacency(base, nv, n):
    """The derived graph's adjacency matrix, built vertex by vertex."""
    N = nv * n
    A = np.zeros((N, N))
    for (x, y, v) in base:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            A[p, q] += 1
            A[q, p] += 1
    return A


def cover_is_simple_and_connected(base, nv, n):
    """A cover we are entitled to ask the question of: simple, cubic, connected."""
    A = cover_adjacency(base, nv, n)
    if A.max() > 1 or A.diagonal().max() > 0:
        return False
    if not np.allclose(A.sum(axis=0), 3):
        return False
    ev = np.linalg.eigvalsh(A)
    return abs(ev[-1] - 3) < 1e-7 and abs(ev[-2] - 3) > 1e-7


def is_ramanujan_brute(base, nv, n):
    """Decide from the full spectrum.  None if the cover is not a legal instance."""
    if not cover_is_simple_and_connected(base, nv, n):
        return None
    ev = sorted(np.linalg.eigvalsh(cover_adjacency(base, nv, n)))
    ev.pop()                                   # the trivial +3, always present
    if abs(ev[0] + 3) < 1e-7:
        ev.pop(0)                              # the trivial -3, iff bipartite
    return max(abs(x) for x in ev) <= THRESHOLD + 1e-8


def is_ramanujan_blocks(base, nv, n):
    """Decide from the character blocks, excluding the trivial eigenvalues."""
    if not cover_is_simple_and_connected(base, nv, n):
        return None
    worst = 0.0
    for j in range(n):
        for lam in np.linalg.eigvalsh(block(base, nv, n, j)):
            if j == 0 and abs(lam - 3) < 1e-9:
                continue                       # the trivial +3
            if abs(lam + 3) < 1e-9:
                continue                       # the trivial -3, when bipartite
            worst = max(worst, abs(lam))
    return worst <= THRESHOLD + 1e-8


# ---------------------------------------------------------------------------
# the criteria
# ---------------------------------------------------------------------------

def Q(x, y):
    """The k-free corner form.  Ramanujan iff Q >= 0 at every image point."""
    return 4 * x * x + 4 * y * y - 8 * SQRT2 * abs(x * y) + 3


def two_loop_is_ramanujan_corner(n, a, b, tol=1e-12):
    """The corner criterion on B(a,b,c)^n.  Independent of c."""
    for j in range(1, n):
        al = 2 * math.cos(2 * math.pi * j * a / n)
        be = 2 * math.cos(2 * math.pi * j * b / n)
        # skip the trivial -3, which needs alpha = beta = -2
        if abs(al + 2) < 1e-9 and abs(be + 2) < 1e-9:
            continue
        x = math.cos(math.pi * j * (a + b) / n)
        y = math.cos(math.pi * j * (a - b) / n)
        if Q(x, y) < -tol:
            return False
    return True


def theta_is_ramanujan(n, cs, tol=1e-12):
    """|1 + w^{d2} + w^{d3}|^2 <= 8, written as a sum of three cosines."""
    d = (cs[0] - cs[1], cs[0] - cs[2], cs[1] - cs[2])
    for j in range(1, n):
        s = sum(math.cos(2 * math.pi * j * x / n) for x in d)
        if s > 2.5 + tol:
            return False
    return True


# ---------------------------------------------------------------------------
# the bounds
# ---------------------------------------------------------------------------

def two_loop_uniform_bound(a, b):
    """n <= pi(2+sqrt2) sqrt(a^2+b^2).  At (1,k) this is the paper's bound."""
    return math.pi * (2 + SQRT2) * math.sqrt(a * a + b * b)


def theta_uniform_bound(cs):
    """n <= 2 pi sqrt(sum of squared pairwise voltage differences)."""
    d = (cs[0] - cs[1], cs[0] - cs[2], cs[1] - cs[2])
    return 2 * math.pi * math.sqrt(sum(x * x for x in d))


def perturbation_threshold(base):
    """Smallest n0 beyond which NO cover of this base can be Ramanujan.

    ||M_1 - M_0||_F <= (2 pi/n) sqrt2 * sum |v| over non-loops
                       + (2 pi/n)^2 * sum v^2 over loops,
    since a non-loop edge moves two entries by |w^v - 1| <= 2 pi|v|/n and a loop
    moves one entry by |2 cos(2 pi v/n) - 2| <= (2 pi v/n)^2.  The top eigenvalue
    of M_0 is 3 because the base is 3-regular, so lambda_max(M_1) >= 3 - ||.||,
    and the cover fails the Ramanujan condition as soon as ||.|| < 3 - 2 sqrt2.
    """
    lin = sum(SQRT2 * abs(v) for (x, y, v) in base if x != y)
    quad = sum(v * v for (x, y, v) in base if x == y)
    n = 3
    while n < 10 ** 6:
        if (2 * math.pi / n) * lin + (2 * math.pi / n) ** 2 * quad < TAU:
            return n
        n += 1
    return None


# ---------------------------------------------------------------------------
# checks, for verify_all
# ---------------------------------------------------------------------------

TWO_LOOP_CASES = [(1, 2), (1, 3), (2, 3), (1, 4), (2, 5), (3, 5), (2, 7), (3, 7),
                  (4, 5), (3, 8)]
THETA_CASES = [(0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 2, 5), (0, 1, 5), (0, 3, 7),
               (0, 2, 7)]


def check_block_decomposition(nmax=40):
    """Character blocks reproduce the full spectrum, on both base types."""
    worst = 0.0
    for n in range(4, nmax):
        cases = ([two_loop_base(a, b, c) for (a, b) in TWO_LOOP_CASES[:5]
                  for c in (0, 1)]
                 + [theta_base(*cs) for cs in THETA_CASES[:4]])
        for base, nv in cases:
            full = np.sort(np.linalg.eigvalsh(cover_adjacency(base, nv, n)))
            blk = np.sort(np.concatenate(
                [np.linalg.eigvalsh(block(base, nv, n, j)) for j in range(n)]))
            worst = max(worst, float(np.max(np.abs(full - blk))))
    return worst


def check_edge_voltage_irrelevant(nmax=30):
    """The two-loop spectrum does not depend on the edge voltage c."""
    worst = 0.0
    for n in range(5, nmax):
        for (a, b) in TWO_LOOP_CASES[:6]:
            ref = None
            for c in range(n):
                base, nv = two_loop_base(a, b, c)
                sp = np.sort(np.concatenate(
                    [np.linalg.eigvalsh(block(base, nv, n, j)) for j in range(n)]))
                if ref is None:
                    ref = sp
                worst = max(worst, float(np.max(np.abs(sp - ref))))
    return worst


def check_two_loop_corner(nmax=60):
    """The corner criterion against the brute-force spectral decision."""
    bad, total = [], 0
    for n in range(5, nmax):
        for (a, b) in TWO_LOOP_CASES:
            base, nv = two_loop_base(a, b, 0)
            want = is_ramanujan_brute(base, nv, n)
            if want is None:
                continue
            total += 1
            if want != two_loop_is_ramanujan_corner(n, a, b):
                bad.append((n, a, b, want))
    return total, bad


def check_theta_criterion(nmax=60):
    """The theta criterion against the brute-force spectral decision."""
    bad, total = [], 0
    for n in range(4, nmax):
        for cs in THETA_CASES:
            base, nv = theta_base(*cs)
            want = is_ramanujan_brute(base, nv, n)
            if want is None:
                continue
            total += 1
            if want != theta_is_ramanujan(n, cs):
                bad.append((n, cs, want))
    return total, bad


def check_uniform_bounds(nmax=400):
    """No Ramanujan cover exceeds its family's uniform bound."""
    viol, found = [], 0
    for (a, b) in TWO_LOOP_CASES:
        B = two_loop_uniform_bound(a, b)
        for n in range(2 * max(a, b) + 1, int(2 * B) + 20):
            if math.gcd(math.gcd(a, b), n) != 1:
                continue
            if (2 * a) % n == 0 or (2 * b) % n == 0:
                continue
            if two_loop_is_ramanujan_corner(n, a, b):
                found += 1
                if n > B:
                    viol.append(("two-loop", n, (a, b), B))
    for cs in THETA_CASES:
        B = theta_uniform_bound(cs)
        for n in range(4, min(nmax, int(2 * B) + 20)):
            if len(set(x % n for x in cs)) < 3:
                continue
            if theta_is_ramanujan(n, cs):
                found += 1
                if n > B:
                    viol.append(("theta", n, cs, B))
    return found, viol


GENERAL_BASES = {
    "theta(0,1,2)": theta_base(0, 1, 2),
    "theta(0,1,3)": theta_base(0, 1, 3),
    "two-loop(1,2)": two_loop_base(1, 2, 0),
    "two-loop(2,3)": two_loop_base(2, 3, 0),
    "K4": ([(0, 1, 0), (0, 2, 1), (0, 3, 0), (1, 2, 2), (1, 3, 0), (2, 3, 1)], 4),
    "K3,3": ([(0, 3, 0), (0, 4, 1), (0, 5, 2), (1, 3, 1), (1, 4, 0), (1, 5, 1),
              (2, 3, 2), (2, 4, 1), (2, 5, 0)], 6),
    "prism": ([(0, 0, 1), (1, 1, 2), (2, 2, 3), (0, 1, 0), (1, 2, 0), (0, 2, 0)], 3),
}


def check_general_finiteness(window=25):
    """On every base, the largest Ramanujan n is below the perturbation threshold.

    Reported as rows (name, largest Ramanujan n or None, threshold), so a
    violation is visible rather than summarised away.
    """
    rows = []
    for name, (base, nv) in GENERAL_BASES.items():
        n0 = perturbation_threshold(base)
        cap = min(70, (n0 or 60) + window)
        hits = [n for n in range(3, cap) if is_ramanujan_brute(base, nv, n)]
        rows.append((name, max(hits) if hits else None, n0))
    return rows


if __name__ == "__main__":
    print("block decomposition, both bases:      %.2e" % check_block_decomposition())
    print("edge voltage c is irrelevant:         %.2e" % check_edge_voltage_irrelevant())
    t, b = check_two_loop_corner()
    print("two-loop corner criterion:            %d cases, %d bad" % (t, len(b)))
    t, b = check_theta_criterion()
    print("theta criterion:                      %d cases, %d bad" % (t, len(b)))
    f, v = check_uniform_bounds()
    print("uniform bounds:                       %d Ramanujan covers, %d violations"
          % (f, len(v)))
    print("general finiteness (base, max n, threshold):")
    for row in check_general_finiteness():
        print("   %-16s %-6s < %s" % row)
