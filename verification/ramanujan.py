"""Which generalized Petersen graphs satisfy the graph Riemann Hypothesis?

A connected d-regular graph is RAMANUJAN when every eigenvalue lambda of its
adjacency matrix other than the trivial ones (+d always, and -d exactly when
the graph is bipartite) obeys |lambda| <= 2*sqrt(d-1).  Sunada's theorem makes
this equivalent to the Riemann Hypothesis for the graph's Ihara zeta function,
so the classification below is a classification of the P(n,k) that satisfy the
graph RH.  Here d = 3, so the threshold is 2*sqrt(2) = 2.8284...

Two independent routes to the spectrum are kept side by side on purpose:

  * brute()  diagonalises the 2n x 2n adjacency matrix with no theory at all;
  * blocks() uses the Z_n block decomposition, whose characteristic equation
    delta^2 - (alpha_j + beta_j) delta + alpha_j beta_j - 1 = 0, with
    beta_j = 2 T_k(alpha_j / 2), is Gera-Stanica (2011), Theorem 2.4.

check_agreement() is the CONTROL: the fast route is only trusted on the range
where it has been matched against the slow one.
"""

import numpy as np

THRESH = 2.0 * np.sqrt(2.0)          # 2 sqrt(d-1) for d = 3
TOL = 1e-9


def adjacency(n, k):
    """Adjacency matrix of P(n,k): outer 0..n-1, inner n..2n-1."""
    A = np.zeros((2 * n, 2 * n))
    for i in range(n):
        A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1.0      # outer cycle
        A[i, n + i] = A[n + i, i] = 1.0                  # spoke
        j = n + (i + k) % n
        A[n + i, j] = A[j, n + i] = 1.0                  # inner k-step
    return A


def brute(n, k):
    """Full spectrum, straight from the matrix."""
    return np.sort(np.linalg.eigvalsh(adjacency(n, k)))


def blocks(n, k):
    """Full spectrum via the Z_n decomposition (Gera-Stanica Thm 2.4)."""
    out = []
    for j in range(n):
        a = 2.0 * np.cos(2.0 * np.pi * j / n)
        b = 2.0 * np.cos(2.0 * np.pi * j * k / n)
        disc = np.sqrt((a - b) ** 2 + 4.0)
        out.append(0.5 * (a + b + disc))
        out.append(0.5 * (a + b - disc))
    return np.sort(np.array(out))


def is_bipartite(n, k):
    """P(n,k) is bipartite exactly when n is even and k is odd."""
    return n % 2 == 0 and k % 2 == 1


def nontrivial_max(n, k, spec=None):
    """max |lambda| over the non-trivial eigenvalues.

    The trivial ones are the Perron value 3 and, in the bipartite case, -3.
    Multiplicity matters: P(n,k) is connected for gcd(n,k) small, and where it
    is disconnected the value 3 repeats -- we drop exactly one copy of each
    trivial value, so a repeated 3 correctly reports as a violation.
    """
    lam = list(spec if spec is not None else blocks(n, k))
    lam.sort()
    lam.pop()                                     # one copy of +3
    if is_bipartite(n, k):
        lam.pop(0)                                # one copy of -3
    return max(abs(x) for x in lam)


def is_ramanujan(n, k, spec=None):
    return nontrivial_max(n, k, spec) <= THRESH + TOL


def check_agreement(nmax=60):
    """CONTROL: block route must reproduce the brute-force spectrum exactly."""
    worst = 0.0
    bad = []
    for k in range(1, 11):
        for n in range(2 * k + 1, nmax + 1):
            d = np.max(np.abs(brute(n, k) - blocks(n, k)))
            worst = max(worst, d)
            if d > 1e-8:
                bad.append((n, k, d))
    return worst, bad


def known_spectra():
    """Sanity anchors from the literature."""
    out = []
    # Petersen P(5,2): 3, 1^5, (-2)^4
    s = np.round(brute(5, 2), 9)
    out.append(("P(5,2) Petersen", sorted(set(s.tolist())), [-2.0, 1.0, 3.0]))
    # Desargues P(10,3) is bipartite: +-3, +-2^4, +-1^5
    s = np.round(brute(10, 3), 9)
    out.append(("P(10,3) Desargues", sorted(set(s.tolist())),
                [-3.0, -2.0, -1.0, 1.0, 2.0, 3.0]))
    return out


def classify(k, nmax):
    return [n for n in range(2 * k + 1, nmax + 1) if is_ramanujan(n, k)]


# ---------------------------------------------------------------------------
# AN ELEMENTARY CRITERION, with no eigenvalues and no square roots.
#
# The Z_n block at j is [[alpha, 1], [1, beta]] with alpha = 2 cos t,
# beta = 2 cos kt, t = 2 pi j / n, so its two eigenvalues are the roots of
#   lambda^2 - A lambda + (P - 1),      A = alpha + beta,  P = alpha beta.
# Substituting lambda = 2 sqrt 2 gives 8 - 2 sqrt2 A + P - 1 = 0, i.e. the
# upper constraint lambda_+ <= 2 sqrt 2 is exactly  2 sqrt2 A - P <= 7; the
# lower one lambda_- >= -2 sqrt 2 is exactly -2 sqrt2 A - P <= 7.  (Both
# squarings are unconditionally valid: |A| <= 4 < 4 sqrt 2.)  Together:
#
#       G_k(t) := 2 sqrt2 |alpha + beta| - alpha beta  <=  7.
#
# So P(n,k) is Ramanujan iff G_k is at most 7 at every grid point t = 2 pi j/n,
# except at the samples carrying the TRIVIAL eigenvalues: j = 0 always, and
# j = n/2 when n is even and k is odd.  check_criterion() is the control for
# this -- it is matched against the spectrum rather than assumed.
#
# The bad set B_k = {t in [0,pi] : G_k(t) > 7} is a finite union of intervals
# whose endpoints are algebraic over Q(sqrt 2), and Ramanujan-ness is exactly
# the statement that the grid misses B_k.  Two features of B_k drive everything:
#
#   * 0 is always a limit point of B_k, because G_k(0) = 8 sqrt2 - 4 > 7.  The
#     grid's nearest nonzero point is 2 pi/n, so n is BOUNDED: only finitely
#     many n per k are Ramanujan.
#   * pi is a limit point of B_k exactly when k is odd.  The grid hits pi only
#     when n is even -- and there it lands on the harmless trivial -3.  For n
#     odd it lands just short, inside B_k.  That is the parity law: for odd k,
#     large Ramanujan n must be even.
#
# For even k the band near pi is replaced by an INTERIOR band, which binds much
# earlier and is why even k tops out well below the bound from the 0-band alone.
# ---------------------------------------------------------------------------

SEVEN = 7.0


def G(t, k):
    """The criterion function: Ramanujan iff G <= 7 at every nontrivial grid point."""
    a = 2.0 * np.cos(t)
    b = 2.0 * np.cos(k * t)
    return 2.0 * np.sqrt(2.0) * np.abs(a + b) - a * b


def trivial_index(n, k, j):
    """Is grid point j one of the trivial eigenvalues (+3, or -3 when bipartite)?"""
    return j == 0 or (is_bipartite(n, k) and 2 * j == n)


def ramanujan_by_criterion(n, k):
    return all(G(2.0 * np.pi * j / n, k) <= SEVEN + 1e-12
               for j in range(n) if not trivial_index(n, k, j))


def check_criterion(kmax=10, nmax=260):
    """CONTROL: the elementary criterion against the actual spectrum."""
    bad = [(n, k) for k in range(1, kmax + 1)
           for n in range(2 * k + 1, nmax + 1)
           if ramanujan_by_criterion(n, k) != is_ramanujan(n, k)]
    return bad


def bad_bands(k, samples=400000):
    """B_k = {t in [0,pi] : G_k(t) > 7}, located by a fine sign scan."""
    t = np.linspace(0.0, np.pi, samples)
    g = G(t, k) - SEVEN
    out, inb, start = [], g[0] > 0, 0.0
    for i in range(1, samples):
        if g[i] > 0 and not inb:
            inb, start = True, t[i - 1]
        elif g[i] <= 0 and inb:
            inb = False
            out.append((start, t[i]))
    if inb:
        out.append((start, np.pi))
    return out


def zero_band_bound(k):
    """n must clear the band at 0: n <= 2 pi / (right endpoint of that band)."""
    return 2.0 * np.pi / bad_bands(k)[0][1]


if __name__ == "__main__":
    print("Ramanujan threshold 2 sqrt 2 = %.10f" % THRESH)
    print()
    print("CONTROL: block decomposition vs brute-force diagonalisation")
    worst, bad = check_agreement(60)
    print("  max deviation over k=1..10, n<=60: %.2e   %s"
          % (worst, "AGREE" if not bad else "DISAGREE %s" % bad[:3]))
    print()
    print("ANCHORS: spectra against published values")
    for name, got, want in known_spectra():
        ok = len(got) == len(want) and max(abs(a - b) for a, b in zip(got, want)) < 1e-9
        print("  %-20s %s  distinct eigenvalues %s" % (name, "PASS" if ok else "FAIL", got))
    print()
    print("CONTROL: elementary criterion G_k <= 7 against the spectrum")
    bad = check_criterion()
    print("  k=1..10, n<=260: %s" % ("AGREE" if not bad else "DISAGREE %s" % bad[:5]))
    print()
    print("BAD BANDS B_k and the bound the band at 0 forces")
    for k in range(1, 13):
        B = bad_bands(k)
        bnd = 2.0 * np.pi / B[0][1]
        last = max(classify(k, 1200))
        print("  k=%-3d n <= %6.2f  (last Ramanujan n = %-4d)  %d band(s): %s"
              % (k, bnd, last, len(B),
                 ", ".join("[%.4f,%.4f]" % (a, b) for a, b in B)))
    print()
    NMAX = 2000
    print("CLASSIFICATION: Ramanujan P(n,k), searched to n = %d" % NMAX)
    for k in range(1, 11):
        L = classify(k, NMAX)
        print("  k=%-2d  count=%-4d  largest n=%-6s  list=%s"
              % (k, len(L), L[-1] if L else "none",
                 L if len(L) <= 24 else str(L[:20])[:-1] + ", ...]"))
