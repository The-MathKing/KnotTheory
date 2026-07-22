"""
Exact certification of period-1 nullity certificates, in the field Q(zeta_n).

A period-1 certificate is determined by its symbol's root set
R = {r_1, ..., r_{k+1}} subset Gamma_n = {2cos(2 pi m/n)}: the symbol must be
F(s) = prod (s - r_i) and must lie in the three-parameter family

    F(s) = (s + a) L_k(s) + alpha s + beta,

after which e = 1, d = alpha, c^2 = a alpha - beta, and

    nullity(A) = #{ m in Z_n : F(s_m) = 0 } = sum_i #{ m : s_m = r_i }.

Floating point cannot certify this: an earlier grid scan reported nullity 7
for k = 2, which the ceiling 2k+2 = 6 forbids, because |F(r)| < tol was
picking up near-roots.  So the arithmetic here is exact.  Every quantity lives
in Q(zeta_n), represented as a rational polynomial in x reduced modulo the
cyclotomic polynomial Phi_n, with 2cos(2 pi m/n) = x^m + x^{n-m}.  Identities
in that field hold if and only if they hold at x = zeta_n, so the membership
test, a, alpha, beta and c^2 are all decided exactly.

Two further facts are checked exactly rather than numerically:
  * a, alpha, beta, c^2 are REAL, i.e. fixed by x -> x^{n-1} (complex
    conjugation).  They must be, since the r_i are real, and the check
    confirms the arithmetic.
  * c^2 is a nonzero field element.  Its sign is then read off from a
    high-precision evaluation, which is decisive because the value is
    bounded away from 0.
"""
import numpy as np
from fractions import Fraction
from sympy import cyclotomic_poly, symbols, Poly, totient
import mpmath as mp


def phi_n_coeffs(n):
    x = symbols("x")
    return [int(v) for v in Poly(cyclotomic_poly(n, x), x).all_coeffs()]


class Cyclo:
    """Arithmetic in Q[x]/(Phi_n(x)); elements are Fraction lists, ascending."""

    def __init__(self, n):
        self.n = n
        c = phi_n_coeffs(n)[::-1]           # ascending
        self.deg = len(c) - 1
        assert c[-1] == 1
        self.red = [Fraction(-v) for v in c[:-1]]   # x^deg = sum red[i] x^i

    def zero(self):
        return [Fraction(0)] * self.deg

    def const(self, v):
        z = self.zero(); z[0] = Fraction(v); return z

    def xpow(self, e):
        e %= self.n
        v = [Fraction(0)] * max(self.deg, e + 1)
        v[e] = Fraction(1)
        return self.reduce(v)

    def reduce(self, v):
        v = list(v)
        for i in range(len(v) - 1, self.deg - 1, -1):
            cf = v[i]
            if cf == 0:
                continue
            v[i] = Fraction(0)
            for j, rj in enumerate(self.red):
                v[i - self.deg + j] += cf * rj
        return v[:self.deg] + [Fraction(0)] * (self.deg - len(v[:self.deg]))

    def add(self, u, v):
        return [a + b for a, b in zip(u, v)]

    def sub(self, u, v):
        return [a - b for a, b in zip(u, v)]

    def smul(self, k, u):
        k = Fraction(k)
        return [k * a for a in u]

    def mul(self, u, v):
        out = [Fraction(0)] * (2 * self.deg - 1)
        for i, a in enumerate(u):
            if a == 0:
                continue
            for j, b in enumerate(v):
                if b:
                    out[i + j] += a * b
        return self.reduce(out)

    def conj(self, u):
        """Apply x -> x^{n-1}, i.e. complex conjugation."""
        out = self.zero()
        for i, a in enumerate(u):
            if a:
                out = self.add(out, self.smul(a, self.xpow(i * (self.n - 1))))
        return out

    def is_zero(self, u):
        return all(a == 0 for a in u)

    def to_complex(self, u, prec=60):
        """Value at zeta_n, at `prec` decimal digits (mpmath, not float)."""
        mp.mp.dps = prec
        z = mp.expjpi(mp.mpf(2) / self.n)
        return sum(mp.mpf(a.numerator) / mp.mpf(a.denominator) * z ** i
                   for i, a in enumerate(u))


def lucas_int(k):
    Lprev, Lcur = [2], [1, 0]
    for _ in range(2, k + 1):
        Lprev, Lcur = Lcur, [int(v) for v in
                             np.polysub(np.polymul([1, 0], Lcur), Lprev)]
    return Lcur if k >= 1 else Lprev          # highest degree first


def certify(n, k, ms, verbose=True):
    """ms: the k+1 Fourier indices whose grid values 2cos(2 pi m/n) are the
    symbol's roots.  Returns (certificate dict, None) or (None, reason)."""
    K = Cyclo(n)
    roots = [K.add(K.xpow(m), K.xpow(-m)) for m in ms]

    # F(s) = prod_i (s - r_i), coefficients ASCENDING in s
    F = [K.const(1)]
    for r in roots:
        shifted = [K.const(0)] + F                  # multiply by s
        scaled = [K.mul(r, c) for c in F] + [K.const(0)]
        F = [K.sub(shifted[i], scaled[i]) for i in range(len(shifted))]
    if len(F) - 1 != k + 1:
        return None, f"degree {len(F)-1} != k+1"
    if not K.is_zero(K.sub(F[-1], K.const(1))):
        return None, "F is not monic"

    Lk = lucas_int(k)[::-1]                          # ASCENDING, degree k
    # G = F - s * L_k   (ascending)
    sLk = [K.const(0)] + [K.const(v) for v in Lk]
    G = [K.sub(F[i], sLk[i]) for i in range(k + 2)]
    if not K.is_zero(G[k + 1]):
        return None, "leading coefficients do not cancel"
    G = G[:k + 1]                                    # degree <= k, ascending
    a = G[k]                                         # coefficient of s^k
    rem = [K.sub(G[i], K.mul(a, K.const(Lk[i]))) for i in range(k + 1)]
    for i in range(2, k + 1):                        # degrees 2..k must vanish
        if not K.is_zero(rem[i]):
            return None, f"not in the family (coefficient of s^{i} survives)"
    alpha, beta = rem[1], rem[0]
    c2 = K.sub(K.mul(a, alpha), beta)

    # exact identity F == (s + a) L_k + alpha s + beta
    rhs = [K.const(0)] * (k + 2)
    for i, cv in enumerate(Lk):
        rhs[i + 1] = K.add(rhs[i + 1], K.const(cv))          # s * L_k
        rhs[i] = K.add(rhs[i], K.mul(a, K.const(cv)))        # a * L_k
    rhs[1] = K.add(rhs[1], alpha)
    rhs[0] = K.add(rhs[0], beta)
    if any(not K.is_zero(K.sub(F[i], rhs[i])) for i in range(k + 2)):
        return None, "membership identity failed"

    for name, v in (("a", a), ("alpha", alpha), ("beta", beta), ("c^2", c2)):
        if not K.is_zero(K.sub(v, K.conj(v))):
            return None, f"{name} is not real"
    if K.is_zero(c2):
        return None, "c^2 = 0 exactly"
    av, alv, c2v = (complex(K.to_complex(v)).real for v in (a, alpha, c2))
    if c2v <= 0:
        return None, f"c^2 = {c2v:.6f} <= 0"

    idx = set()
    for m in ms:
        idx.add(m % n); idx.add((-m) % n)
    return dict(n=n, k=k, ms=tuple(sorted(m % n for m in ms)), a=av,
                alpha=alv, c2=c2v, nullity=len(idx)), None


def numeric_check(n, k, a, alpha, c2):
    P = np.roll(np.eye(n), 1, axis=1)
    c = np.sqrt(c2)
    A = np.block([[a * np.eye(n) + P + P.T, c * np.eye(n)],
                  [c * np.eye(n), alpha * np.eye(n)
                   + np.linalg.matrix_power(P, k)
                   + np.linalg.matrix_power(P.T, k)]])
    lam = np.sort(np.abs(np.linalg.eigvalsh(A)))
    B = np.abs(A) > 1e-12
    np.fill_diagonal(B, False)
    r = int(np.sum(lam < 1e-9 * np.abs(A).max()))
    return r, bool(np.all(B.sum(axis=1) == 3)), lam[r] if r < len(lam) else np.nan
