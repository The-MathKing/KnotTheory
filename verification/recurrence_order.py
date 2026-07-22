"""
Verification of the structural theorem behind the certificate ceiling.

THEOREM (recurrence order).  Let n >= 2k+3, 2k < n, and A in S(P(n,k))
with outer weights b_i (edge u_i u_{i+1}), spoke weights c_i (u_i v_i),
inner weights e_i (v_i v_{i+k}) and free diagonals a_i, d_i.  Eliminating
y from the kernel equations gives, for each i in Z_n, a scalar relation

    sum_{p=-(k+1)}^{k+1} gamma_{i,p} x_{i+p} = 0,                  (R_i)

with gamma_{i,p} nonzero only for p in {-k-1,-k,-k+1} u {-1,0,1} u
{k-1,k,k+1} -- nine positions -- and with

    gamma_{i, k+1}  = - e_i     b_{i+k}   / c_{i+k}   != 0,
    gamma_{i,-k-1}  = - e_{i-k} b_{i-k-1} / c_{i-k}   != 0.

Consequently (R_i) is a linear recurrence of order exactly 2k+2, its
solution space on Z (no periodicity imposed) has dimension 2k+2, and

    nullity(A) = dim ker(T - I),   T = T_{n-1} ... T_0

the monodromy of that recurrence.  Hence nullity(A) <= 2k+2 for every
A in S(P(n,k)), with equality if and only if T = I.

This script checks, on random A over many (n,k):
  (1) the nine-position sparsity and the two end-coefficient formulas;
  (2) that x satisfies (R_i) for all i  <=>  (x, y=Lx) is in ker A;
  (3) nullity(A) == dim ker(T - I) == 2k+2 - rank(T - I);
  (4) nullity(A) <= 2k+2, with the bound attained only when T = I.
"""
import os
import numpy as np


def build(n, k, w=None, rng=None):
    """Returns (A, b, c, e, a, d) for P(n,k) with random or supplied weights."""
    if rng is None:
        rng = np.random.default_rng(0)
    if w is None:
        b = rng.standard_normal(n) + 1.5 * np.sign(rng.standard_normal(n))
        c = rng.standard_normal(n) + 1.5 * np.sign(rng.standard_normal(n))
        e = rng.standard_normal(n) + 1.5 * np.sign(rng.standard_normal(n))
        a = rng.standard_normal(n)
        d = rng.standard_normal(n)
    else:
        b, c, e, a, d = w
    N = 2 * n
    A = np.zeros((N, N))
    for i in range(n):
        A[i, (i + 1) % n] = A[(i + 1) % n, i] = b[i]
        A[i, n + i] = A[n + i, i] = c[i]
        A[n + i, n + (i + k) % n] = A[n + (i + k) % n, n + i] = e[i]
        A[i, i] = a[i]
        A[n + i, n + i] = d[i]
    return A, b, c, e, a, d


def gamma_row(n, k, i, b, c, e, a, d):
    """Coefficients gamma_{i,p} of (R_i), returned as a dict p -> value."""
    g = {}

    def add(p, v):
        g[p] = g.get(p, 0.0) + v

    # y_j = -(b_{j-1} x_{j-1} + a_j x_j + b_j x_{j+1}) / c_j
    def addL(j_off, mult):
        j = (i + j_off) % n
        add(j_off - 1, -mult * b[(j - 1) % n] / c[j])
        add(j_off,     -mult * a[j] / c[j])
        add(j_off + 1, -mult * b[j] / c[j])

    addL(-k, e[(i - k) % n])      # e_{i-k} y_{i-k}
    addL(0,   d[i])               # d_i y_i
    addL(k,   e[i])               # e_i y_{i+k}
    add(0, c[i])                  # c_i x_i
    return g


def monodromy(n, k, b, c, e, a, d):
    """T with state Z_i = (x_{i-k-1},...,x_{i+k}); Z_{i+1} = T_i Z_i."""
    r = 2 * k + 2
    T = np.eye(r)
    for i in range(n):
        g = gamma_row(n, k, i, b, c, e, a, d)
        lead = g[k + 1]
        Ti = np.zeros((r, r))
        Ti[:r - 1, 1:] = np.eye(r - 1)        # shift
        # last row: x_{i+k+1} = -(1/lead) * sum_{p<=k} gamma_{i,p} x_{i+p}
        for p, v in g.items():
            if p == k + 1:
                continue
            col = p + k + 1                    # position of x_{i+p} in Z_i
            Ti[r - 1, col] -= v / lead
        T = Ti @ T
    return T


def check(n, k, seed=0, verbose=False):
    rng = np.random.default_rng(seed)
    A, b, c, e, a, d = build(n, k, rng=rng)
    r = 2 * k + 2
    msgs = []

    # (1) sparsity and end coefficients
    allowed = set([-k - 1, -k, -k + 1, -1, 0, 1, k - 1, k, k + 1])
    for i in range(n):
        g = gamma_row(n, k, i, b, c, e, a, d)
        for p, v in g.items():
            if abs(v) > 1e-12 and p not in allowed:
                msgs.append(f"sparsity violated at i={i}, p={p}")
        lead = -e[i] * b[(i + k) % n] / c[(i + k) % n]
        trail = -e[(i - k) % n] * b[(i - k - 1) % n] / c[(i - k) % n]
        if abs(g[k + 1] - lead) > 1e-10 * max(1, abs(lead)):
            msgs.append(f"leading coeff formula wrong at i={i}")
        if abs(g[-k - 1] - trail) > 1e-10 * max(1, abs(trail)):
            msgs.append(f"trailing coeff formula wrong at i={i}")

    # (2)+(3) kernel  <->  fixed space of the monodromy
    nullA = int(np.sum(np.abs(np.linalg.eigvalsh(A)) < 1e-9 * np.abs(A).max()))
    T = monodromy(n, k, b, c, e, a, d)
    # T is a product of n matrices, so ||T|| can be astronomically large;
    # the kernel tolerance must be relative to that scale, not absolute.
    sv = np.linalg.svd(T - np.eye(r), compute_uv=False)
    fixdim = int(np.sum(sv < 1e-11 * max(1.0, sv[0])))
    if nullA != fixdim:
        msgs.append(f"nullity {nullA} != dim ker(T-I) {fixdim}")
    if nullA > r:
        msgs.append(f"nullity {nullA} exceeds the bound {r}")
    if verbose:
        print(f"  P({n},{k}): nullity(A)={nullA}, dim ker(T-I)={fixdim}, "
              f"bound 2k+2={r}")
    return msgs, nullA, fixdim, r


if __name__ == "__main__":
    bad = 0
    cases = [(n, k) for k in range(1, 8) for n in range(2 * k + 3, 2 * k + 12)
             if 2 * k < n]
    for (n, k) in cases:
        for seed in range(3):
            msgs, nullA, fixdim, r = check(n, k, seed=seed)
            if msgs:
                bad += 1
                print(f"FAIL P({n},{k}) seed={seed}: {msgs}")
    print(f"\nchecked {len(cases)} (n,k) pairs x 3 random A each = "
          f"{3*len(cases)} matrices")
    print("sparsity, end-coefficient formulas, and "
          "nullity(A) = dim ker(T - I) <= 2k+2:",
          "ALL PASS" if bad == 0 else f"{bad} FAILURES")
    # exhibit the equality case: the rho-equivariant k=2 certificate.
    # Symbol with b=1, t = L_2(s) = s^2 - 2:
    #   (a+s)(d + e(s^2-2)) - c^2 = e s^3 + a e s^2 + D s + (aD - c^2),
    # where D = d - 2e.  Set e = 1; then for a monic cubic
    # s^3 + A2 s^2 + A1 s + A0 with prescribed roots,
    #   a = A2,  D = A1,  c^2 = a D - A0,  d = D + 2.
    from itertools import combinations
    print("\nEquality case: rho-equivariant P(n,2) certificates "
          "(target nullity 6 = 2k+2):")
    for n in (12, 14, 16, 18, 20):
        vals = sorted({round(2 * np.cos(2 * np.pi * m / n), 12)
                       for m in range(1, n // 2 + 1)})
        interior = [v for v in vals if abs(abs(v) - 2) > 1e-9]
        found = False
        for trip in combinations(interior, 3):
            _, A2, A1, A0 = np.poly(trip)
            aa, DD = A2, A1
            cc2 = aa * DD - A0
            if cc2 <= 1e-6:
                continue
            bb = np.ones(n); cc = np.full(n, np.sqrt(cc2))
            e_ = np.ones(n); a_ = np.full(n, aa); d_ = np.full(n, DD + 2.0)
            A, *_ = build(n, 2, w=(bb, cc, e_, a_, d_))
            nullA = int(np.sum(np.abs(np.linalg.eigvalsh(A))
                              < 1e-9 * np.abs(A).max()))
            T = monodromy(n, 2, bb, cc, e_, a_, d_)
            dev = np.abs(T - np.eye(6)).max()
            print(f"  n={n}: roots s={np.array2string(np.array(trip), precision=4)}"
                  f"  c^2={cc2:.4f}  nullity={nullA}  max|T-I|={dev:.2e}"
                  f"  {'T = I' if dev < 1e-8 else 'T != I'}")
            found = True
            break
        if not found:
            print(f"  n={n}: no triple of interior values gives c^2 > 0")


# ---------------------------------------------------------------------------
# Additional structure: the determinant of the monodromy, the reduction to a
# product of two symmetric cycle matrices, and the forcing-set corollary.
# ---------------------------------------------------------------------------

def build_cs(n, k, rng):
    """A combinatorially symmetric (not symmetric) matrix with P(n,k)'s
    pattern: each edge carries two independent nonzero entries."""
    def nz(size):
        return rng.standard_normal(size) + 1.5 * np.sign(rng.standard_normal(size))
    b, bp, c, cp, e, ep = (nz(n) for _ in range(6))
    a, d = rng.standard_normal(n), rng.standard_normal(n)
    N = 2 * n
    A = np.zeros((N, N))
    for i in range(n):
        A[i, (i + 1) % n] = b[i]          # u_i -> u_{i+1}
        A[(i + 1) % n, i] = bp[i]         # u_{i+1} -> u_i
        A[i, n + i] = c[i]                # u_i -> v_i
        A[n + i, i] = cp[i]               # v_i -> u_i
        A[n + i, n + (i + k) % n] = e[i]
        A[n + (i + k) % n, n + i] = ep[i]
        A[i, i] = a[i]
        A[n + i, n + i] = d[i]
    return A, (b, bp, c, cp, e, ep, a, d)


def gamma_row_cs(n, k, i, b, bp, c, cp, e, ep, a, d):
    """(R_i) for the combinatorially symmetric case.  Row u_j reads
    bp[j-1] x_{j-1} + a_j x_j + b_j x_{j+1} + c_j y_j = 0, so
    y_j = -(bp[j-1] x_{j-1} + a_j x_j + b_j x_{j+1}) / c_j; row v_i reads
    ep[i-k] y_{i-k} + d_i y_i + e_i y_{i+k} + cp_i x_i = 0."""
    g = {}

    def add(p, v):
        g[p] = g.get(p, 0.0) + v

    def addL(off, mult):
        j = (i + off) % n
        add(off - 1, -mult * bp[(j - 1) % n] / c[j])
        add(off,     -mult * a[j] / c[j])
        add(off + 1, -mult * b[j] / c[j])

    addL(-k, ep[(i - k) % n])
    addL(0,  d[i])
    addL(k,  e[i])
    add(0, cp[i])
    return g


def monodromy_from_gamma(n, k, gammas):
    r = 2 * k + 2
    T = np.eye(r)
    for i in range(n):
        g = gammas[i]
        lead = g[k + 1]
        Ti = np.zeros((r, r))
        Ti[:r - 1, 1:] = np.eye(r - 1)
        for p, v in g.items():
            if p != k + 1:
                Ti[r - 1, p + k + 1] -= v / lead
        T = Ti @ T
    return T


def check_det_and_product(n, k, seed=0):
    """Checks, for both matrix classes:
      (a) det T = (prod b')(prod e') / ((prod b)(prod e)), hence det T = 1
          whenever A is symmetric;
      (b) nullity(A) = multiplicity of the eigenvalue 1 of S U, with
          S = C^{-1} V C^{-1} and U the outer block -- both symmetric in the
          symmetric case;
      (c) no nonzero kernel vector vanishes on 2k+2 consecutive outer
          vertices (which is exactly M <= Z for the forcing set
          {u_0,...,u_{2k+1}} of the rotation-bootstrap theorem).
    """
    rng = np.random.default_rng(seed)
    msgs = []

    # --- symmetric class ---
    A, b, c, e, a, d = build(n, k, rng=rng)
    gam = [gamma_row(n, k, i, b, c, e, a, d) for i in range(n)]
    T = monodromy_from_gamma(n, k, gam)
    if abs(np.linalg.det(T) - 1.0) > 1e-6:
        msgs.append(f"sym: det T = {np.linalg.det(T):.6f}, expected 1")

    U = A[:n, :n]
    V = A[n:, n:]
    C = np.diag(np.diag(A[:n, n:]))
    S = np.linalg.inv(C) @ V @ np.linalg.inv(C)
    nullA = int(np.sum(np.abs(np.linalg.eigvalsh(A)) < 1e-9 * np.abs(A).max()))
    sv = np.linalg.svd(S @ U - np.eye(n), compute_uv=False)
    mult = int(np.sum(sv < 1e-9 * max(sv[0], 1.0)))
    if mult != nullA:
        msgs.append(f"sym: nullity {nullA} != mult_1(SU) {mult}")
    if not np.allclose(S, S.T) or not np.allclose(U, U.T):
        msgs.append("sym: S or U not symmetric")

    # --- combinatorially symmetric class ---
    A2, (b2, bp2, c2, cp2, e2, ep2, a2, d2) = build_cs(n, k, rng)
    gam2 = [gamma_row_cs(n, k, i, b2, bp2, c2, cp2, e2, ep2, a2, d2)
            for i in range(n)]
    T2 = monodromy_from_gamma(n, k, gam2)
    pred = (np.prod(bp2) * np.prod(ep2)) / (np.prod(b2) * np.prod(e2))
    got = np.linalg.det(T2)
    if abs(got - pred) > 1e-6 * max(1.0, abs(pred)):
        msgs.append(f"cs: det T = {got:.6g}, formula gives {pred:.6g}")
    sv2 = np.linalg.svd(A2, compute_uv=False)
    nullA2 = int(np.sum(sv2 < 1e-9 * sv2[0]))
    svT2 = np.linalg.svd(T2 - np.eye(2 * k + 2), compute_uv=False)
    fix2 = int(np.sum(svT2 < 1e-11 * max(1.0, svT2[0])))
    if nullA2 != fix2:
        msgs.append(f"cs: nullity {nullA2} != dim ker(T-I) {fix2}")

    # --- (c) the forcing-set corollary, on both classes ---
    for (M, tag) in ((A, "sym"), (A2, "cs")):
        Vt = np.linalg.svd(M)[2]
        ns = Vt[len(Vt) - max(1, 0):].T          # at least one right-null dir
        # take the right null space at tolerance; if trivial, nothing to check
        svv = np.linalg.svd(M, compute_uv=False)
        rr = int(np.sum(svv < 1e-9 * svv[0]))
        if rr == 0:
            continue
        K = np.linalg.svd(M)[2][-rr:].T           # 2n x rr
        block = K[:2 * k + 2, :]                  # rows u_0..u_{2k+1}
        if np.linalg.matrix_rank(block, tol=1e-8) < rr:
            msgs.append(f"{tag}: a kernel vector vanishes on "
                        f"u_0..u_{{{2*k+1}}}")
    return msgs


if __name__ == "__main__" and os.environ.get("EXTRA", "1") == "1":
    print("\nDeterminant of the monodromy, the SU reduction, and the "
          "forcing-set corollary:")
    bad = 0
    cases = [(n, k) for k in range(2, 7) for n in range(2 * k + 3, 2 * k + 9)]
    for (n, k) in cases:
        for seed in range(2):
            m = check_det_and_product(n, k, seed=seed)
            if m:
                bad += 1
                print(f"  FAIL P({n},{k}) seed={seed}: {m}")
    print(f"  checked {2*len(cases)} matrices over {len(cases)} (n,k) pairs: "
          + ("ALL PASS" if bad == 0 else f"{bad} FAILURES"))
