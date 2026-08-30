# Getting Off the Congruence Classes

This is the newest and most important layer of the project. Read
`23_antipodal_obstruction.md` first, and `09_transfer_matrices_and_monodromy.md`
for the monodromy.

## The problem in one paragraph

Every exact value the project had was attached to a divisibility class:
$Z(P(n,4)) = 10$ for $60 \mid n$, $Z(P(n,5)) = 12$ for $24 \mid n$, and so on.
A judge or referee will ask the obvious question: is there a clean statement for
*all large $n$*? That question is the whole difference between "extensive
computation inside a framework" and "a theorem."

## Why the congruences are forced (not sloppiness)

A period-one symbol is a **fixed polynomial**. Its roots are fixed algebraic
numbers. A fixed algebraic number $2\cos(2\pi j/d)$ lies on the grid
$\Gamma_n = \{2\cos(2\pi m/n)\}$ **if and only if $d \mid n$**. So the set of $n$
a given period-one matrix can settle is exactly $\{n : \operatorname{lcm}(D) \mid n\}$ —
one divisibility class, density $\le 1/3$, containing **at most one prime**
(because $\{n : L \mid n\}$ with $L \ge 3$ contains a prime only when $L$ *is*
that prime).

To cover more, the weights must depend on $n$. For $k \ge 3$ that is constrained
by an identity that holds for *every* period-one symbol:

$$e_2(r_1,\dots,r_{k+1}) = -k.$$

Why: $L_k$ has nonzero coefficients only in degrees $\equiv k \pmod 2$, so the
$s^{k-1}$ coefficient of $(s+a)L_k + \alpha s + \beta$ is the $s^{k-2}$
coefficient of $L_k$, namely $-k$, independent of $a, \alpha, \beta$. On the grid
this becomes a rational linear relation among cosines of rational angles — a
**Conway–Jones relation**, which is rigid.

**For $k=2$ the coefficient of $s^{k-1} = s$ is $\alpha - 2$, which is free.** So
$k=2$ has no such condition, which is exactly why $k=2$ can choose its roots as
functions of $n$ (the three most negative grid values) and be general in $n$,
and why no other $k$ can. That asymmetry had been sitting in the project
unexplained.

## The escape route

The ceiling corollary says: for **any** matrix on the pattern (not just the
rotation-invariant ones), $\operatorname{null} A = 2k+2$ **iff** the monodromy
$T = I$. That condition contains no arithmetic at all. So drop invariance.

## Certifying it rigorously

$T = I$ is convenient to optimise but bad to certify — the map $w \mapsto T$ has
a 51-dimensional image inside the 64-dimensional space of $8\times8$ matrices at
$k=3$, so no square subsystem exists. Certify the **nullity** instead:

$\operatorname{null} A \ge r$ iff some full-rank $K$ has $AK = 0$. Write $K$ in
graph form $K = P\binom{I_r}{X}$, which makes $\operatorname{rank} K = r$
automatic. Then $f(w,X) = A(w)K(X) = 0$ is **bilinear** — total degree 2, rational
coefficients — so the Jacobian is affine and its Lipschitz constant is an
explicit integer. A Krawczyk contraction bound then needs three norms instead of
an interval matrix product.

### The subtle part: which equations

$AK = 0$ is $2nr$ equations of rank $2nr - \binom{r}{2}$. The deficiency is
**structural**, not incidental: $K^\top A K$ is symmetric because $A$ is, and
$\binom{r}{2}$ is exactly its antisymmetric part. So if the non-pivot rows
vanish, $K^\top AK$ equals the pivot block, which must therefore be symmetric,
and setting its *upper triangle* to zero forces the lower triangle. The system

> all non-pivot rows $+$ upper triangle of the pivot block

is **exactly equivalent** to $AK = 0$. Picking rows by QR pivoting instead
(the first thing tried) leaves $\binom{r}{2}$ equations unproved — the Krawczyk
test passes and it still isn't a proof. The reduction is checkable: those
dependent equations fall to $10^{-61}$ *without being solved for*.

## Results

$$Z(P(n,3)) = M(P(n,3)) = 8 \quad \text{for every } 17 \le n \le 33$$

Seventeen consecutive values, interval-certified, primes 17, 19, 23, 29, 31
among them. By the congruence theorem no period-one certificate can reach any
of these.

## The complete slice (and why search failures mean nothing)

Positive diagonal conjugation $A \mapsto DAD$ cannot change a spoke's sign, since
$d_i d_{n+i} > 0$ — so sign-diagonal conjugation $A \mapsto SAS$ is needed too.
Combining them, every symmetric matrix on the pattern is equivalent to one with
all spokes $+1$ and all outer weights $\pm1$ (for even $n$, one outer weight
stays free, because the cyclic system $u_i + u_{i+1} = -\log|b_i|$ has corank 1
on an even cycle).

**Consequence:** the slice searched is *complete*, so a failure inside it is a
failure of the search, not evidence that no matrix exists. This is not academic.
$n = 18$ was reported as a failure, and certified as soon as the restart budget
went from 40 to 150.

## All large $n$: tiles

Since $T = I$ is multiplicative around the cycle, build the weight sequence from
pieces that each contribute the identity. Two things had to be fixed first:

1. **Pieces don't compose naively.** $T_i$ depends on weights within $\sim2k+2$ of
   position $i$, so neighbours interfere. Give every tile a fixed **docking
   pattern** on its first and last $k+1$ positions; then each tile's product
   depends only on its own interior. *Verified bit-exactly*: perturbing one
   tile's interior leaves the others' products identical to 0.000e+00.
2. **Two coprime lengths are useless.** They give $n = ia + jb$, covering nothing
   below $(a-1)(b-1)$ — several hundred here. Using **every** length in
   $[L, 2L)$ makes every $n \ge L$ a sum, with no gap.

**Theorem (tiling).** If identity tiles exist for every $\ell \in [L, 2L)$, then
$Z(P(n,k)) = M(P(n,k)) = 2k+2$ for every $n \ge L$.

For $k=3$ the tiles were found for every $22 \le \ell \le 43$, giving

$$Z(P(n,3)) = M(P(n,3)) = 8 \quad \text{for every } n \ge 22.$$

The parameter count is sharp in practice: $\ell = 19, 20$ are underdetermined (55,
60 unknowns vs 64 equations) and stall near $4\times10^{-1}$; $\ell = 21$, the
first with more unknowns than equations, falls to $5.6\times10^{-2}$; from
$\ell = 22$ tiles appear.

**Standard:** the theorem is *proved*; the tiles are *floating point*
($\|T_{\text{tile}} - I\| \le 2\times10^{-13}$). So the conclusion is labelled
**numerical**, not proved. Certifying the 22 tiles would upgrade it, and that
needs Krawczyk on a rational rather than bilinear map — interval matrix products
instead of the cheap Lipschitz bound. Not done.

## Anticipated questions

**"Is this an all-$n$ theorem or not?"** The implication is a theorem. Its
hypothesis for $k=3$ is verified numerically. So the honest statement is: *modulo
certifying 22 explicit finite systems, $k=3$ is settled for all $n \ge 22$.* Say
it that way; don't let the proved theorem launder the numerics.

**"Does it work for other $k$?"** One identity tile exists at $k=4$, $\ell=34$,
and another at $\ell=36$, so the method isn't specific to $k=3$. But convergence
is erratic there (roughly half the lengths fail at 4 restarts, including some
with *more* unknowns than ones that succeed), so no range is claimed for $k=4$.

**"Why did the earlier searches say this was impossible?"** They didn't, quite —
they were unreliable. The eigenvalue-minimising search collapsed onto degenerate
strata (all spokes zero, or all edges zero) and reported maximum nullity 7 at
$P(20,3)$ where 8 is attained. Every negative result from it is now marked
unreliable in the paper.

## Corrections recorded

- The threshold is $n \ge (k+1)(2k+3)/3$ (from spending the gauge), not
  $(2k+2)^2/5$. The earlier figure caused $k=6$ to be tested at $n = 27, 29, 31$,
  all *below* the true threshold of 35, so those failures meant nothing.
- $N(k)$ is **not** $O(k)$; the dimension count forces it to be quadratic.
- The monodromy is **not** symplectic. The space of skew $B$ with
  $T^\top B T = B$ has dimension $k+1$, so eigenvalues come in reciprocal pairs
  and the characteristic polynomial is palindromic.

## Files

- `verification/general_n.py`, `certify_general.py`, `krawczyk.py`,
  `certify_pipeline.py`, `gauge_fixed.py`, `certify_sweep.py` — the
  search-and-certify pipeline.
- `verification/tiles.py`, `tile_sweep.py` — the tiling construction.
- `verification/verify_all.py` — one pass over every computational claim in the
  paper; 61 checks. Run this first if you want to confirm anything.
