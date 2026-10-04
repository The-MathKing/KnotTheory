# Whiteboard drills

A judge who wonders how much of this is yours will not read the binder. They
will hand you a marker. These are the three derivations that answer the
question, in the order they are most likely to be asked. Each should be
reproducible cold, without notes, in the time given.

The test is not that you remember the result. It is that when a judge
interrupts with "why is that step legal?", you answer without stalling — the
interruptions below are the actual point of each drill.

---

## Drill 1 — The corner criterion (target: 90 seconds)

**Asked as:** "Show me how the $k$ disappears."

Start from $D_k = (7+P)^2 - 8A^2$, where $A = \alpha+\beta$ and $P = \alpha\beta$,
with $\alpha = 2\cos t$, $\beta = 2\cos kt$ and $t = 2\pi j/n$.

1. **It's a difference of squares**, so over $\mathbb{Q}(\sqrt2)$
   $$D_k = f_-f_+, \qquad f_\pm = 7+P \pm 2\sqrt2\,A.$$
   Say out loud that these are not new objects — they are exactly the two
   eigenvalue conditions $\lambda_+\le2\sqrt2$ and $\lambda_-\ge-2\sqrt2$.

2. **Both must be $\ge0$, and they can't both be negative**, because
   $f_-+f_+ = 2(7+P) \ge 6 > 0$ (using $|P|\le4$). *That* is why the single
   inequality $D_k\ge0$ was equivalent to the pair all along.

3. **Substitute** $x = \cos\frac{(k+1)t}{2}$, $y = \cos\frac{(k-1)t}{2}$.
   - Product-to-sum: $2\cos t\cos kt = \cos(k+1)t + \cos(k-1)t$, and
     $\cos(k\pm1)t = 2\cos^2\frac{(k\pm1)t}{2} - 1$, so
     $$P = 4\cos t\cos kt = 2\big((2x^2-1)+(2y^2-1)\big) = 4x^2+4y^2-4.$$
   - Sum-to-product: $\cos t + \cos kt = 2\cos\frac{(k+1)t}{2}\cos\frac{(k-1)t}{2}$, so
     $$A = 2(\cos t + \cos kt) = 4xy.$$

4. Therefore $7+P = 3+4x^2+4y^2$ and
   $$f_\mp = 3+4x^2+4y^2 \mp 8\sqrt2\,xy,
   \qquad \min(f_-,f_+) = 4x^2+4y^2-8\sqrt2\,|xy|+3 = Q(x,y).$$

**No $k$.** The forbidden set is one fixed region; $k$ survives only in the map
into the square.

**Interruptions to expect**
- *"Why is squaring legal?"* — Both sides are provably positive:
  $|A|\le4<4\sqrt2$ for the first squaring, and $7+P\ge3>0$ for the second. Each
  squaring is an equivalence, not an implication. Say this before they ask.
- *"Why is the minimum the one with $|xy|$?"* — Because whichever of $\mp$
  matches the sign of $xy$ gives the smaller value, and you need both $\ge0$.
- *"Where does the region come from?"* —
  $Q = 4(|x|-(\sqrt2{+}1)|y|)(|x|-(\sqrt2{-}1)|y|)+3$; indefinite form, so the
  conic is a hyperbola, and $\{Q<0\}$ is unbounded in the plane — it is the
  *square* that cuts it into four corner pieces.

---

## Drill 2 — The Dirichlet bound (target: 2 minutes)

**Asked as:** "Why does $k$ stop?" or "How do you rule out large $k$?"

State the gap first: the per-$k$ bound $n \le \pi(2+\sqrt2)\sqrt{k^2+1}$ grows
with $k$, so **by itself it can never rule out large $k$.** That is the whole
difficulty, and naming it is half the answer.

1. **Failure is forced locally.** If for even one nontrivial $j$
   $$s = \Big(1-\cos\tfrac{2\pi j}{n}\Big) + \Big(1-\cos\tfrac{2\pi jk}{n}\Big) < \tau = 3-2\sqrt2,$$
   then $P(n,k)$ is not Ramanujan.

2. **Convert to distance-to-nearest-integer.** $1-\cos2\pi\theta = 2\sin^2\pi\theta \le 2\pi^2\|\theta\|^2$, so it suffices that
   $$\Big\|\tfrac{j}{n}\Big\|^2 + \Big\|\tfrac{jk}{n}\Big\|^2 < \frac{\tau}{2\pi^2} = 0.0086919\ldots$$
   Point out what this now *is*: a **simultaneous Diophantine** condition. Those
   have unconditional answers.

3. **Dirichlet supplies the $j$.** Take $J = \lfloor\sqrt n\rfloor$. Dirichlet's
   approximation theorem applied to $k/n$ gives some $1\le j\le J$ with
   $\|jk/n\| \le 1/(J+1)$. For that $j$:
   $$\Big\|\tfrac{j}{n}\Big\|^2 \le \Big(\tfrac{J}{n}\Big)^2 \le \frac1n,
   \qquad \Big\|\tfrac{jk}{n}\Big\|^2 \le \frac{1}{(J+1)^2} < \frac1n,$$
   since $J \le \sqrt n < J+1$. So the sum is $< 2/n$, **for every $k$.**

4. $2/n < \tau/2\pi^2$ whenever $n > 4\pi^2/\tau = 230.09\ldots$, giving
   $n \ge 231$. With $1 \le k < n/2$, the family is finite in **both** variables.

**Interruptions to expect**
- *"Is $j$ a legal index?"* — $1\le j\le\sqrt n < n/2$ for $n\ge5$, so it is
  neither $0$ nor the excluded index $n/2$. Have this ready; it is the one
  genuine gap in the argument if you skip it.
- *"231 vs 112 — that's loose."* — Yes, by about a factor of two, and it costs
  nothing. The bound's only job is to be **uniform in $k$**. Once the region is
  finite, exhaustion is exact, and sharpening it would not move one entry.
- *"Why $J=\lfloor\sqrt n\rfloor$?"* — It balances the two terms: one grows like
  $(J/n)^2$, the other shrinks like $1/J^2$, and $J\approx\sqrt n$ equalises
  them at $1/n$ each.

---

## Drill 3 — Gcd safety (target: 90 seconds)

**Asked as:** "You said you have structure toward a closed form. Show me."

1. **Locality.** The grid points of *level $m$* (those $j$ with $n/\gcd(n,j)=m$)
   are exactly the full conjugate set $\{\cos\frac{2\pi i}{m} : \gcd(i,m)=1\}$.
   So $P(n,k)$ is Ramanujan iff **no divisor $m\ge3$ of $n$ is bad for $k$** —
   and badness at $m$ depends on $k$ only through $k \bmod m$.
   Immediate consequence: the Ramanujan set of each $k$ is **divisor-closed**.

2. **The geometry gives a window.** $Q<0$ forces *both* $|x|,|y| \ge \sqrt2-\tfrac12$
   — the point where the forbidden region meets the side of the square. So it
   forces $\|j(k\pm1)/m\| \le \gamma$, where
   $$\gamma = \frac{\arccos(\sqrt2-\tfrac12)}{\pi} = 0.13281\ldots$$

3. **The minimum is a gcd.** For $m\nmid c$,
   $$\min_{\gcd(j,m)=1}\Big\|\frac{jc}{m}\Big\| = \frac{\gcd(c,m)}{m}.$$

4. **Combine.** If $\gcd(k+1,m)/m > \gamma$ then no $j$ can bring $|x|$ close
   enough, so $m$ is safe. And since $1/\gamma = 7.53$ while $m/\gcd$ is an
   integer:
   $$\frac{m}{\gcd(k+1,m)} \in \{2,\dots,7\}
   \quad\text{or}\quad
   \frac{m}{\gcd(k-1,m)} \in \{2,\dots,7\}
   \ \Longrightarrow\ m \text{ safe}.$$

**Interruptions to expect**
- *"Why exclude 1?"* — $m/\gcd = 1$ means $m \mid k+1$, which pins $|x| = 1$.
  That is the *worst* case, not the best; the minimum is then $0$.
- *"So is that a closed form?"* — **No, and say so flatly.** It is one-sided:
  it certifies safety and says nothing about badness. A closed form needs both
  directions. The $k\le9$ form ($k=2,4$ solid runs; odd $k$ needs every odd
  divisor $\le P_k$) is *verified against the certified classification, not
  derived*, and it fails at $k=6,8$ and odd $k\ge11$ where interior bands bind.
  The list is complete and certified; it is not yet explained.

---

## Drill 4 — The one you will fumble

**Asked as:** "Walk me through a case."

Pick $P(5,2)$ — the Petersen graph — and decide it live. Blocks
$\alpha_j = 2\cos\frac{2\pi j}{5}$, $\beta_j = 2\cos\frac{4\pi j}{5}$; spectrum
$\{3, 1, 1, 1, 1, 1, -2, -2, -2, -2\}$; largest nontrivial modulus $2 < 2\sqrt2$,
so it is Ramanujan, and it is in the 460.

Then do a failure: $P(113,41)$ from the board's right-hand panel — eight orbit
points land in a lens, the first at $j=3$.

Being able to *run* the criterion, not just state it, is what separates
understanding it from having been handed it.
