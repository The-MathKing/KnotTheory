# When Realisability Fails, Exactly

This is the newest piece of the project and the one that explains the most, so
it is worth understanding on its own terms. Read
`08_chebyshev_and_the_symbol.md` first.

## The one-line theorem

Everything below follows from this. The spoke-weight product is
$c^2 = a\alpha - \beta$, so

$$c^2 = 0 \iff \beta = a\alpha \iff F = (s+a)L_k + \alpha(s+a) = (s+a)(L_k+\alpha).$$

**So $c^2 = 0$ exactly when the symbol factors as $(s+a)(L_k(s)+t)$.** That is the
whole obstruction, for every $k$, and the antipodal statement further down is
the special case that parity forces when $k$ is even.

Over the rationals the degenerate list is finite, by **Niven's theorem** (the
only rational values of $2\cos(\pi q)$ for rational $q$ are $0,\pm1,\pm2$): $a$
is the $s^k$ coefficient of $F$ hence rational, and $-a$ is a grid value, so
$a \in \{0,\pm1,\pm2\}$; likewise $t = -L_k(r) = -2\cos(k\varphi) \in \{0,\pm1,\pm2\}$.
**At most 25 degenerate rational symbols per $k$**, explicitly listable — and
enumerating them gives $7,8,7,6,9$ for $k=2,\dots,6$, matching the independent
exhaustive count exactly.

## Why only $c^2 = 0$ is fatal

$c^2$ is the **product** of the two spoke weights. A symmetric matrix needs
$c^2 > 0$ (a real square root); the combinatorially symmetric class needs only
$c^2 \neq 0$. Requiring $c^2 > 0$ where $c^2 \neq 0$ suffices is the single
mistake that made this project record $k=3$ and $k=7$ as impossible for years
of log entries. Redone with $c^2 \neq 0$:

| $k$ | candidates | outside family | $c^2=0$ | sym | cs |
|---|---|---|---|---|---|
| 2 | 17 | 0 | 7 | 5 | 5 |
| 3 | 35 | 21 | 8 | 0 | **6** |
| 4 | 67 | 54 | 7 | 3 | 3 |
| 5 | 127 | 118 | 6 | 1 | 2 |
| 6 | 225 | 216 | 9 | 0 | 0 |
| 7 | 385 | 378 | 6 | 0 | **1** |
| 8 | 651 | 644 | 7 | 0 | 0 |
| 9 | 1065 | 1057 | 8 | 0 | 0 |
| 10 | 1705 | 1698 | 7 | 0 | 0 |

Every non-fatal rejection has $c^2 = -1$ or $-2$.

## The signed adjacency matrix: $k=3$ and $k=7$

The certificates at $k=3$ and $k=7$ both have $a=\alpha=0$, $\beta=1$, i.e.
symbol $F = sL_k(s)+1$. Both diagonals vanish, so

$$A = \begin{pmatrix} P+P^{-1} & I \\ -I & P^k+P^{-k}\end{pmatrix}$$

is the **adjacency matrix with one set of spokes negated**. Substituting
$s=z+z^{-1}$ turns $sL_k+1=0$ into

$$Q_k(z) = z^{2k+2}+z^{2k}+z^{k+1}+z^2+1 = 0,$$

the adjacency polynomial $P_k$ with the middle sign flipped. So the nullity
classification proved for the adjacency matrix applies verbatim, and the
question becomes: **for which $k$ does $Q_k$ split into cyclotomics?**

For $2 \le k \le 60$, only $k=2,3,7$:

| $k$ | $Q_k$ | $\sum\varphi(d)$ | $\mathrm{lcm}$ |
|---|---|---|---|
| 2 | $\Phi_5\Phi_6$ | 6 | 30 |
| 3 | $\Phi_5\Phi_{10}$ | 8 | 10 |
| 7 | $\Phi_5\Phi_{10}\Phi_{24}$ | 16 | 120 |

Each hits the ceiling $2k+2$. Hence

$$Z(P(n,3)) = 8 \ (10 \mid n), \qquad Z(P(n,7)) = 16 \ (120 \mid n)$$

by matrices of zeros and $\pm1$. The unsigned $P_k$ splits only at $k=2,5$, so
the two sign choices together cover $k \in \{2,3,5,7\}$ and nothing else. This
is rigidity, not an infinite family — I checked to $k=60$ hoping for more.

**The $k=3$ root set is $\{\pm\varphi, \pm\varphi^{-1}\}$: two antipodal pairs.**
For even $k$ that would be fatal. Because 3 is odd it is not. So the parity
corollary does not only rule things out — it says where to look.

## The question it answers

The construction works like this: choose where you want the symbol's roots to
sit on the grid, solve for the matrix weights, and read off the nullity. Two
things can go wrong. The symbol might not be in the three-parameter family at
all (that is the $k-2$ residual conditions), or the weights you get back might
be illegal — specifically the spoke weight product

$$c^2 = a\alpha - \beta$$

might come out zero (no spoke at all, so it is a different graph) or negative
(no real symmetric square root). For a long time the pattern of which grid
choices failed looked like arbitrary arithmetic. It is not.

## The closed form for k = 2

For $k=2$ the symbol $F(s) = (s+a)(s^2-2) + \alpha s + \beta$ is a monic cubic
with exactly three free parameters, so prescribing three roots determines
everything and leaves no residual condition. Expand and compare coefficients
with $\prod(s - s_i) = s^3 - e_1 s^2 + e_2 s - e_3$:

$$a = -e_1, \qquad \alpha = e_2 + 2, \qquad \beta = -e_3 - 2e_1$$

and therefore $c^2 = a\alpha - \beta = e_3 - e_1 e_2$. Now apply the elementary
identity $(s_1+s_2)(s_1+s_3)(s_2+s_3) = e_1 e_2 - e_3$:

$$\boxed{c^2 = -(s_1+s_2)(s_1+s_3)(s_2+s_3)}$$

Read off two consequences immediately:

- $c^2 = 0$ **if and only if** two of the roots are antipodal ($s_i = -s_j$).
- $c^2 > 0$ **if and only if** an odd number of the three pairwise sums is
  negative.

The first is the important one. It is a factorisation, so it is an if-and-only-if,
not a pattern observed in data.

## Why it is a parity phenomenon

The Chebyshev-like polynomial satisfies $L_k(-s) = (-1)^k L_k(s)$, because
$s = z + z^{-1}$ and $s \mapsto -s$ is $z \mapsto -z$. Suppose the symbol has
roots $y$ and $-y$ with $y \neq 0$, and let $k$ be **even**, so
$L_k(-y) = L_k(y)$. Writing $F(y) = 0$ and $F(-y) = 0$:

$$a L_k(y) + \alpha y + \beta = -y L_k(y)$$
$$a L_k(y) - \alpha y + \beta = +y L_k(y)$$

Add: $\beta = -a L_k(y)$. Subtract and divide by $2y$: $\alpha = -L_k(y)$.
Hence

$$c^2 = a\alpha - \beta = -a L_k(y) + a L_k(y) = 0.$$

That is the whole proof, and it holds for **every even $k$**, not just $k=2$.
For **odd** $k$ we have $L_k(-y) = -L_k(y)$, the second equation flips sign,
and the same elimination gives $\beta = -y L_k(y)$, $\alpha = -aL_k(y)/y$, so

$$c^2 = \frac{L_k(y)(y^2 - a^2)}{y},$$

which is not identically zero. **There is no obstruction for odd $k$.** This
was checked symbolically for $k = 2,\dots,8$: identically zero for $2,4,6,8$
and a nonvanishing rational function for $3,5,7$.

## Counting on the grid

Write $\Gamma^\circ_n$ for the interior grid values $2\cos(2\pi m/n)$,
$1 \le m \le M = \lfloor (n-1)/2 \rfloor$. When is an antipodal pair
unavoidable?

- **$n$ odd:** never. $s_i = -s_j$ needs $i + j = n/2$, not an integer.
  So all $\binom{M}{3}$ triples are usable, and we need only $M \ge 3$, i.e.
  $n \ge 7$.
- **$n$ even:** the grid is symmetric about $0$. The antipodal classes number
  $n/4$ when $4 \mid n$ and $(n-2)/4$ otherwise. A usable triple needs three
  distinct classes, so we need $n \ge 12$.

So the exceptions above $n=6$ are exactly $n = 8$ and $n = 10$, both by
pigeonhole: $\Gamma^\circ_8 = \{\sqrt2, 0, -\sqrt2\}$ is two classes, and
$\Gamma^\circ_{10}$ has four elements in two classes.

## The explicit certificate

Take the three *most negative* grid values, $s_M, s_{M-1}, s_{M-2}$. Then
product-to-sum gives

$$s_{M-1} + s_{M-2} = \begin{cases} -4\cos(4\pi/n)\cos(\pi/n) & n \text{ odd} \\ -4\cos(5\pi/n)\cos(\pi/n) & n \text{ even} \end{cases}$$

negative exactly when $n \ge 9$ (odd) or $n \ge 12$ (even). Since $s$ is
decreasing, the other two pairwise sums are even more negative, so all three
are negative, the product is negative, and $c^2 > 0$. Combined with the
rotation bootstrap upper bound:

$$Z(P(n,2)) = M(P(n,2)) = 6 \quad \text{for all } n \ge 9,\ n \neq 10.$$

## The two exceptions are different animals

This matters and it is easy to blur. Exhaustive computation gives

- $Z(P(8,2)) = 5$ — the true value really is below $6$, so the method is
  **right** to fail here.
- $Z(P(10,2)) = 6$ — the true value is $6$, so here it is the **method** that
  falls short, not the bound.

Any honest account has to separate these. Earlier write-ups in this project
lumped them together as "the construction fails."

## Where the non-symmetric matrices finally earn their keep

At $n = 7$ there is only one triple, the roots of
$\Psi_7 = s^3 + s^2 - 2s - 1$, giving $e_1 = -1, e_2 = -2, e_3 = 1$ and

$$c^2 = e_3 - e_1 e_2 = 1 - 2 = -1.$$

Negative, so there is **no symmetric certificate at $n = 7$**. But $c^2$ is the
*product* of the two spoke weights, and in the combinatorially symmetric class
those two weights are independent — they need only both be nonzero. Take them
to be $1$ and $-1$:

$$A = \begin{pmatrix} I + P + P^{-1} & I \\ -I & P^2 + P^{-2} \end{pmatrix}$$

an integer matrix with nullity exactly $6$ for every $n$ divisible by $7$. This
is the first place in the whole project where the combinatorially symmetric
generalisation is *necessary* rather than decorative — everywhere else, every
value it certified was also certified symmetrically.

## It explains the old enumeration

The exhaustive search over rational period-one symbols at $k=2$ found $17$
candidates in the three-parameter family and rejected $12$. Those $12$ split
perfectly along the obstruction:

| | factor sets | $c^2$ | antipodal? | rescued by cs class? |
|---|---|---|---|---|
| dead | $(3,8),(3,12),(4,8),(4,12),(6,8),(6,12),(3,4,6)$ | exactly $0$ | all seven | no |
| alive | $(7),(9),(4,5),(5,6),(6,10)$ | $-1$ | none | **all five** |

So the admissible count is $5$ symmetrically and $10$ in the larger class, and
the antipodal obstruction is the *only* thing that kills a rational period-one
symbol at $k=2$.

The general corollary: for even $k$ the factor set $D$ may contain neither both
$d$ and $2d$ for odd $d$ (because the roots of $\Psi_{2d}$ are the negatives of
those of $\Psi_d$), nor any $d$ divisible by $4$ with $\varphi(d) \ge 4$
(because those $\Psi_d$ have root sets closed under negation — e.g.
$\Psi_8 = s^2 - 2$, $\Psi_{12} = s^2 - 3$).

## Anticipated questions

**"Isn't $Z(P(n,2)) = 6$ already known?"** Very likely, yes — $k=2$ is the
classical case and is not where this project claims novelty (that is $k \ge 4$).
$k=2$ matters here because it is the case where the machinery is transparent
enough to see the obstruction, and the obstruction is a statement about all
even $k$.

**"Why does the parity of $k$ matter at all?"** Because the symbol is built
from $L_k$, and $L_k$ inherits the parity of $k$ as a polynomial. An antipodal
pair of roots is a constraint that is *symmetric* in $\pm y$, and for even $k$
the two root conditions at $\pm y$ overdetermine $(\alpha, \beta)$ in exactly
the way that forces $a\alpha = \beta$.

**"Is $M(P(10,2)) = 6$?"** Unknown. $Z(P(10,2)) = 6$ is computed exactly, so
$M \le 6$, but no certificate of nullity $6$ is known there — the period-one
family cannot supply one, and nothing rules out a non-invariant matrix doing it.

## Files

- `verification/antipodal_obstruction.py` — the symbolic proof checks, the
  exact test over $\mathbb{Z}[x]/\Phi_n(x)$ for all triples with $n \le 60$,
  and the cyclotomic corollary against $50$ candidate factor sets.
- `verification/k2_criterion.py` — builds the explicit certificate for each $n$
  and checks its nullity against exhaustively computed $Z(P(n,2))$.
- `results/zero_forcing/antipodal_obstruction.txt`,
  `results/zero_forcing/k2_complete.txt` — the outputs.
