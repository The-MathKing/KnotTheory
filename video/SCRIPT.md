# Where Optimal Networks Stop Existing — full explainer script

Format: one `## S<nn>` heading per scene. Under it, numbered **beats**. Each beat is one
narration paragraph; the animation for that beat runs while it is spoken.
Narration is written to be read aloud by a text-to-speech voice, so symbols are
spelled out in words where the voice would otherwise stumble.

Audience: Aryan, watching to understand their own project end to end.

---

## S01 — Cold open

1. Here is a graph. Twenty points, thirty lines. It is called the Petersen graph, and it is probably the most famous small graph in mathematics. Five points on the outside, joined in a ring. Five points inside, joined in a star. And five spokes connecting them.

2. Now let the ring have n points instead of five, and let the inner points connect by stepping k places around instead of two. That gives the generalized Petersen graph, written P of n, k. Two integers, one graph. The ordinary Petersen graph is P of five, two.

3. This video is about two questions you can ask of this graph, and one engine that answers both. The first question: write down the adjacency matrix of the graph, the matrix of ones and zeros that records which points are joined. Its eigenvalues are fixed numbers. Are they as tightly packed as any infinite family of graphs could possibly have them? That property has a famous name. It is the Riemann Hypothesis for the graph.

4. The second question: now forget the actual entries. Keep only the pattern of where the nonzero entries sit, and let every entry range over all real numbers. Over every matrix with that pattern, how many times can the eigenvalue zero repeat? That number is called the maximum nullity, and the combinatorial game that bounds it is called zero forcing.

5. One graph. One matrix pattern. Question one nails the matrix down and asks about its spectral gap. Question two lets the matrix float and asks how degenerate zero can be. By the end of this video, both are answered exactly, for every n, at the values of k where the answer is complete. Along the way, a published theorem turns out to be false, a conjecture in a July 2026 paper gets proved, and one of the project's own headline claims gets refuted by its author. Let's start from zero.

## S02 — What P(n,k) is

1. Fix two numbers, n and k, with k less than n over two. Draw n outer vertices, u zero through u n minus one, in a ring. Each u i is joined to u i plus one, indices wrapping around modulo n. That is the outer cycle.

2. Draw n inner vertices, v zero through v n minus one. Each v i is joined to v i plus k. For k equal to one this is just another ring. For k equal to two, as in the Petersen graph, it is a pentagram. For larger k the inner edges weave into a more intricate pattern.

3. Finally join each u i to its own v i by a spoke. Every vertex now touches exactly three edges: the graph is cubic. There are two n vertices and three n edges.

4. One thing to notice straight away. Rotating every index by one, sending i to i plus one, maps the graph onto itself. The graph has a cyclic symmetry of order n. Hold onto that fact. It is the engine the whole project runs on.

## S03 — The adjacency matrix and its eigenvalues

1. Number the vertices and write down the adjacency matrix A: a two n by two n grid, with a one in row x, column y when x and y are joined, and a zero otherwise. Because the graph is cubic, every row has exactly three ones.

2. A symmetric matrix of real numbers has real eigenvalues, two n of them here. The largest is always three, because the all-ones vector times A gives three times the all-ones vector. Every row sums to three.

3. The rest of the eigenvalues sit somewhere between minus three and three. Where exactly they sit encodes how well connected the graph is. If the second-largest eigenvalue is far below three, the graph is an expander: information spreads quickly, there are no bottlenecks, random walks mix fast. That gap between three and the next eigenvalue is called the spectral gap.

4. Here are the eigenvalues of the Petersen graph itself: three once, one five times, minus two four times. The spectral gap is two, which for a graph on ten vertices is as good as it gets.

## S04 — Ramanujan graphs and the number two root two

1. How big can a spectral gap be? Not arbitrarily big. For cubic graphs there is a hard limit discovered by Alon and Boppana: for any infinite family of cubic graphs, the second eigenvalue must eventually come within any epsilon of two times the square root of two, about two point eight two eight.

2. Where does that number come from? Unroll a cubic graph into its universal cover, the infinite tree where every vertex has three neighbours. The spectrum of that tree is the whole interval from minus two root two to plus two root two. Every finite cubic graph is a folded version of that tree, and the folding cannot do better than the tree itself in the limit.

3. So a cubic graph whose nontrivial eigenvalues, meaning everything other than three and, if the graph is bipartite, minus three, all have absolute value at most two root two, is as good as an infinite family can be. Lubotzky, Phillips and Sarnak named such graphs Ramanujan graphs in 1988. They are the optimal expanders.

4. The Petersen graph: eigenvalues one and minus two, both inside plus or minus two point eight two eight. Ramanujan. Now the question becomes concrete. As n and k vary, which generalized Petersen graphs stay Ramanujan, and which do not?

## S05 — Why this is a Riemann Hypothesis

1. There is a reason this is called a Riemann Hypothesis and not merely an eigenvalue condition. Attached to every finite graph is a zeta function, defined by Ihara in the nineteen sixties. Where Riemann's zeta function is a product over prime numbers, Ihara's is a product over prime cycles: closed walks that do not backtrack and do not merely repeat a shorter walk.

2. This zeta function has an Euler product, a functional equation, and a prime number theorem counting closed geodesics by length. The analogy with the number-theoretic zeta is exact enough that you can ask the Riemann Hypothesis for it: after the substitution u equals q to the minus s, do all the poles in the critical strip lie on the line real part of s equals one half?

3. And here is the difference from the classical case. Ihara's determinant formula expresses the graph zeta function as the reciprocal of a determinant involving the adjacency matrix. Unwinding it, a q plus one regular graph satisfies the Riemann Hypothesis if and only if it is Ramanujan. For cubic graphs, q is two, and the condition is exactly: every nontrivial eigenvalue has absolute value at most two root two.

4. So the graph Riemann Hypothesis is a theorem away from being a finite eigenvalue check. That is why it can be decided, which the classical one cannot. The project is careful to say this: the analogy lives in the zeta function, not in the difficulty. But it is a real definition, and it makes a real question. For which n and k does P of n, k satisfy the Riemann Hypothesis?

## S06 — The question nobody asked

1. The eigenvalues of P of n, k were computed completely by Gera and Stanica in 2011. Their paper gives a closed formula for every eigenvalue. Yet the paper never uses the words Ramanujan, expander, or spectral gap. Nobody had put the formula next to the number two root two and asked which members qualify.

2. For other families this classification had been done. Droll did it for unitary Cayley graphs. Le and Sander did it for integral circulant graphs of prime power order. In both cases the answer was the same shape: only finitely many members qualify. So one might guess the same here. But a guess is not a classification, and the difficulty is in the details: the eigenvalue formula contains nested square roots, and deciding whether a nested square root is less than two root two, at a point where they are almost equal, is exactly where floating point arithmetic stops being trustworthy.

## S07 — The cyclic symmetry splits the matrix

1. Here is the engine. The rotation i to i plus one is a symmetry of P of n, k. Any matrix that commutes with a cyclic shift of order n can be block diagonalized by the discrete Fourier transform over the integers mod n.

2. Concretely: the adjacency matrix, two n by two n, becomes n separate two by two blocks M j, one for each j from zero to n minus one. Block j is the matrix with alpha j and beta j on the diagonal and one in both off-diagonal spots, where alpha j is two cosine of two pi j over n, and beta j is two cosine of two pi j k over n.

3. Why those entries? Alpha j is what the outer cycle contributes: a step forward and a step back, each multiplied by the j-th root of unity, add up to two cosine. Beta j is the same for the inner cycle, which steps by k. And the spoke, which connects outer to inner without any rotation, contributes a plain one off the diagonal.

4. On the zeta side, this is the factorization of the Ihara zeta function into Artin-Ihara L-functions, one per character of the cyclic group. But the practical content is simpler. Every eigenvalue of P of n, k is an eigenvalue of one of these two by two blocks, and a two by two block has eigenvalues you can write down: alpha plus beta over two, plus or minus the square root of alpha minus beta squared over four plus one.

5. Picture it this way. Fix k. The two eigenvalue branches, as functions of a continuous angle t, trace two fixed curves. The actual eigenvalues of P of n, k are those curves sampled at the n equally spaced angles two pi j over n. The graph is Ramanujan exactly when none of the samples lands where a curve rises above two root two or dips below minus two root two. The curves are fixed; only the sampling grid changes with n. And as n grows, the grid gets finer. That single observation is going to bound n.

## S08 — Clearing the radicals

1. We want to decide whether both eigenvalues of block j lie in the interval from minus two root two to two root two. The eigenvalues involve a square root, and the bound two root two is itself a square root. Comparing them directly is comparing nested radicals. Let's get rid of all of them.

2. Write A for alpha plus beta and P for alpha times beta. The condition that the larger eigenvalue is at most two root two reads: the square root of alpha minus beta squared plus four is at most four root two minus A. Both alpha and beta have absolute value at most two, so A is at most four in absolute value, which is less than four root two. So the right-hand side is positive, and squaring is an equivalence, not just an implication. That matters: a careless squaring would introduce spurious solutions.

3. Squaring and simplifying, using the identity A squared minus alpha minus beta squared equals four P, the condition becomes: two root two times A minus P is at most seven. The mirror condition, that the smaller eigenvalue is at least minus two root two, gives minus two root two A minus P at most seven. Together: two root two times the absolute value of A is at most seven plus P.

4. One radical is left, the two root two. But P has absolute value at most four, so seven plus P is at least three, which is positive. So we can square again, and again it is an equivalence. The result: eight A squared is at most seven plus P squared.

5. Now substitute back. Alpha is two u, where u is cosine of two pi j over n, and beta is two times the k-th Chebyshev polynomial of u, because cosine of k theta is a polynomial in cosine of theta. So A and P are polynomials in u with integer coefficients. Define D k of u as seven plus P squared minus eight A squared. It is a polynomial of degree two k plus two with integer coefficients, and the graph is Ramanujan if and only if D k is nonnegative at every grid point u j, apart from the two trivial ones.

6. That is the first reduction. An analytic statement about poles of a zeta function has become the sign of one integer polynomial at n points on the interval from minus one to one.

## S09 — The band at u equals one

1. Look at the polynomial D k at the right endpoint, u equals one. The Chebyshev polynomial is one there, so A is four, P is four, and D k of one is eleven squared minus eight times sixteen: one hundred twenty-one minus one hundred twenty-eight. Minus seven. Negative, for every k.

2. So D k is negative in a little band just below u equals one. Any grid point that lands in that band makes the graph fail. And the grid points are cosines of two pi j over n. The one nearest to u equals one is j equals one: cosine of two pi over n. As n grows, that point creeps toward one and eventually falls into the band.

3. Let u k be the largest root of D k below one. Then P of n, k fails whenever cosine of two pi over n exceeds u k, that is, whenever n exceeds two pi over arccosine of u k. Call that B k. For each fixed k, only finitely many n qualify. The ceiling is explicit: for k equal to two, three, and four it comes out at twenty-three, thirty-two, and forty-two, and the actual largest Ramanujan n at those k are exactly those numbers. The bound is sharp.

4. One more thing hiding here. At the other endpoint, u equals minus one, the Chebyshev polynomial is minus one to the k. Compute D k of minus one and you get minus seven when k is odd and plus nine when k is even. So for odd k there is a second forbidden band, at u equals minus one. For even k there is not. Remember this; it produces a parity law in a moment.

## S10 — The uniform bound: no expansion needed

1. The bound B k grows with k. To show the whole family is finite we need a bound on n that works for every k at once. Here is the argument, and it uses nothing beyond three elementary facts.

2. Write x for cosine t and y for cosine k t, where t is the grid angle, and let a be one minus x, b be one minus y, and s be a plus b. The failure condition, two root two A greater than seven plus P, unwinds to G of t greater than seven, where G is four root two times x plus y minus four x y. Expand in terms of a, b, and s: G equals eight root two minus four, minus four root two minus four times s, minus four a b.

3. Fact one, the AM-GM inequality: four a b is at most s squared. So G exceeds seven as soon as s squared plus four root two minus four times s is less than eight root two minus eleven. Fact two: the left side is increasing in s, and at s equal to tau, which is three minus two root two, it equals eight root two minus eleven exactly. Check: seventeen minus twelve root two, plus twenty root two minus twenty-eight, is eight root two minus eleven. So s less than tau is enough to force failure.

4. Fact three: one minus cosine theta is at most theta squared over two. So s is at most one plus k squared times t squared over two. Put the pieces together: the graph fails as soon as t is less than two minus root two over the square root of k squared plus one. The smallest grid angle is two pi over n. So a Ramanujan graph needs n at most pi times two plus root two times the square root of k squared plus one.

5. There is an honest correction recorded in the paper here. An earlier draft derived the same constant by Taylor expanding the eigenvalue to second order in t at fixed k. That derivation is invalid, because the critical t is of order one over k, so k t is of order one, outside the expansion's domain. The constant was right by luck; the argument was wrong. The proof you just saw replaces it and uses no expansion at all.

## S11 — Dirichlet closes the family

1. We still do not have finiteness in both variables. For each k, n is bounded, but the bound grows like k. Could there be Ramanujan members with enormous k? The failure condition is: some nontrivial index j has one minus cosine two pi j over n plus one minus cosine two pi j k over n less than tau. Write that in terms of distances to the nearest integer. One minus cosine two pi theta is at most two pi squared times the distance from theta to the nearest integer, squared. So it suffices that the squared distance of j over n to the nearest integer, plus the squared distance of j k over n to the nearest integer, is less than tau over two pi squared, about zero point zero zero eight six nine.

2. That is a simultaneous Diophantine approximation problem: find a j that makes both j over n and j k over n nearly integers. And there is a classical theorem that does exactly this unconditionally. Dirichlet's approximation theorem: for any real number and any bound J, there is an integer j between one and J with j times the real number within one over J plus one of an integer.

3. Apply it to the real number k over n with J equal to the floor of root n. You get a j at most root n with the distance of j k over n to an integer at most one over J plus one, which is less than one over root n. And since j is at most root n, j over n is at most one over root n too. Both squared distances are less than one over n. Their sum is less than two over n.

4. So failure is forced whenever two over n is less than tau over two pi squared, that is, whenever n exceeds four pi squared over tau, which is two hundred thirty point zero nine seven. For every n at least two hundred thirty-one, and every k, P of n, k fails the Riemann Hypothesis. Since k is less than n over two, the entire family lives in a finite triangle: n from three to two hundred thirty. The question has become a finite computation.

## S12 — The corner criterion: k leaves the geometry

1. Before doing the computation there is a structural fact worth seeing, because it is the prettiest thing in Part One. D k is a difference of squares, so it factors over the rationals extended by root two: D k equals f minus times f plus, where f plus or minus is seven plus P plus or minus two root two A. These two factors are exactly the two eigenvalue conditions we started with. And they cannot both be negative, because their sum is two times seven plus P, which is at least six.

2. Now make a change of variable. Let x be cosine of pi j k plus one over n, and y be cosine of pi j k minus one over n. Two product-to-sum identities do the work. Cosine t plus cosine k t is two cosine of k plus one t over two times cosine of k minus one t over two, so A equals four x y. And cosine t times cosine k t is one half of cosine k plus one t plus cosine k minus one t, so P equals four x squared plus four y squared minus four.

3. Substitute. Both factors become three plus four x squared plus four y squared, minus or plus eight root two x y. The smaller of the two is Q of x, y, equal to four x squared plus four y squared minus eight root two times the absolute value of x y, plus three. The graph is Ramanujan if and only if Q is nonnegative at every nontrivial grid point.

4. Look at what happened. Q does not contain k. For every k, the question is the same: does a set of points in the unit square avoid one fixed region, the set where Q is negative? The parameter k has moved out of the region and into the map that places the points.

5. And the region is small. Q equals zero is a hyperbola, and inside the square it cuts off four congruent pieces, one at each corner, each meeting the sides in segments of length exactly three halves minus root two. Their total area is zero point four three percent of the square. The forbidden set is four tiny corners, the same four corners for every k, and the only question is whether the grid, mapped into the square, drops a point in one of them.

6. This also makes the parity law visible. When n is even and k is odd, the index j equals n over two maps to the corner at minus one, plus one, which is inside a forbidden region. But that index carries the eigenvalue minus three of a bipartite graph, and the Ramanujan condition exempts it. For odd n there is no such index, and the nearest grid point lands just inside the band instead. So for odd k, odd n is cut off at exactly half the constant that even n is. Being bipartite helps. It is worth a factor of two in n.

## S13 — Exact arithmetic, and the bug the control caught

1. Now the finite computation: every pair n, k with n up to two hundred thirty, thirteen thousand one hundred ten cases. But a finite computation is not yet a proof. At a band edge, D k of u j is an algebraic number extremely close to zero, and whether it is slightly positive or slightly negative is the whole question. Floating point does not decide that. It guesses.

2. The fix is to notice what kind of number D k of u j is. On the grid, A and P are integer combinations of cosines of rational multiples of pi, that is, values of integer Laurent polynomials at a root of unity. So D k of u j is an algebraic integer in the ring Z adjoined zeta m. Reduce the Laurent polynomial modulo the m-th cyclotomic polynomial and you get an exact integer vector that is zero if and only if the value is zero. Vanishing is decided by integer arithmetic.

3. For nonzero values, a separation bound says the absolute value of a nonzero algebraic integer of this kind is at least two hundred forty-nine to the power minus degree minus one. So a sign is accepted only if the floating-point value clears that guard with margin, and otherwise refused and recomputed. Every one of the thirteen thousand one hundred ten cases was decided this way, with zero disagreements against the float64 control.

4. And the control earned its keep. At k equal to one, the inner cycle has the same step as the outer, so exponents in the Laurent polynomial collide. A Python dictionary literal silently dropped the duplicate keys. The exact classifier declared every P of n, one Ramanujan, including P of nine, one, whose spectrum contains minus two point eight seven nine. The floating-point control flagged four disagreements, and the bug was found and fixed. Running two independent methods side by side is the only reason that error did not reach the paper.

## S14 — The complete classification

1. Here is the answer. Exactly four hundred sixty pairs n, k satisfy the Riemann Hypothesis. Since P of n, k is isomorphic to P of n, l when l is plus or minus k or its inverse mod n, that is three hundred twenty-four distinct graphs. The largest n is one hundred twelve, at k equal to forty-one. The largest k is forty-five. Nothing past k equals forty-five qualifies at all.

2. Plot the survivors as dots in the n, k plane. The Dirichlet line at two hundred thirty-one is far to the right; the actual data stops at one hundred twelve. The bound only had to be uniform, not sharp. For small k the survivors form solid runs: k equals two has every n from five to twenty-three, k equals four every n from nine to forty-two.

3. For odd k, the runs thin out to even n only, in the upper half. That is the parity law. Look at k equals nine: every n from nineteen to forty-six, then only even n up to ninety. The odd n were cut off at half the constant.

4. And at the top of the picture, past k equals twenty-five, no even k survives at all. Only odd k persists, up to forty-five. That is the parity law still operating at the end of the list. The last members alive are kept alive only by the exemption of the trivial eigenvalue minus three.

5. The classification is also not monotone in k. k equals nine reaches n equals ninety; k equals eight stops at forty-nine and k equals ten at fifty-two. For even k an interior band binds before the band at u equals one does. The paper records this as a certified list rather than a formula: nothing proves the survivors stop at k equals forty-five except having checked every case up to the Dirichlet line.

## S15 — No infinite Ramanujan family is a cyclic cover

1. Step back from P of n, k. Nothing in the argument used the specific graph beyond two facts: the base of the cover has two vertices, and the cover is cubic. P of n, k is a cyclic cover of a two-vertex graph with two loops and one edge, where the loops carry voltages one and k, meaning the lifted edges step by one and by k around the cycle.

2. There are exactly two cubic bases on two vertices. The two-loop base with voltages a, b, and c on the edge, and the theta base, three parallel edges. The corner criterion carries to the first with a plus b and a minus b in place of k plus one and k minus one, and the edge voltage c plays no role at all. The theta base gives bipartite covers, the cubic cyclic Haar graphs, with an even simpler criterion.

3. More generally, for a cyclic cover of any fixed base graph, the block at index j equals one converges, as n grows, to the base's own adjacency matrix, whose top eigenvalue is three. So some nontrivial eigenvalue of the cover is dragged above two root two. No infinite family of Ramanujan graphs is a cyclic cover of a fixed base.

4. This is not a new principle. It is why Lubotzky, Phillips and Sarnak built their Ramanujan graphs on the group P G L two over a finite field rather than on a cyclic group: abelian covers do not expand. What the project adds is the explicit constant, and the exact criteria for both two-vertex bases, which decide the finitely many survivors instead of merely bounding them. The paper says this plainly: a quantitative refinement of a known phenomenon, not a discovery. And it measures the cost. The deficit, second eigenvalue minus two root two, is bounded by three minus two root two throughout the family.

## S16 — Interlude: what was Part One, honestly

1. Pause and take stock. An analytic question about the poles of a zeta function. One theorem of Ihara's turns it into an eigenvalue bound. The cyclic symmetry turns the eigenvalue bound into the sign of a polynomial on a grid. Two squarings, each justified, clear the radicals. A change of variable removes k from the geometry entirely. Dirichlet's theorem makes the family finite in both parameters. Exact cyclotomic arithmetic certifies the finitely many survivors.

2. The result is a complete classification of a recognised kind, the same kind Droll and Le-Sander did for other families, with the same shape of answer. The paper rates its own contribution as exactness and completeness rather than surprise. Anyone who knew that abelian covers do not expand would have predicted the shape. What they could not have predicted is which four hundred sixty, and that nothing survives past k equals forty-five.

3. Now the second question. Same graph, same symmetry, same grid of roots of unity. But the matrix is no longer fixed.

## S17 — Zero forcing: the game

1. Zero forcing is a game played on a graph with two colours. Start with some set S of vertices coloured blue; the rest are white. Then apply one rule repeatedly: if a blue vertex has exactly one white neighbour, that neighbour turns blue. The blue vertex forces it.

2. If, after repeating the rule as long as possible, every vertex is blue, then S is a zero forcing set. The zero forcing number Z of G is the smallest size of a zero forcing set.

3. Watch it on a path. Colour one endpoint blue. It has exactly one white neighbour, which turns blue. That vertex now has exactly one white neighbour, and so on down the line. One blue vertex forces the whole path. Z of a path is one.

4. On a cycle, one blue vertex has two white neighbours and is stuck. Two adjacent blue vertices work: each has one white neighbour, both force, and the two fronts sweep around to meet. Z of a cycle is two.

5. The game came from two places independently. In quantum control, it answers which spin systems can be controlled from a few sites. In power engineering, it is the problem of placing the fewest phasor measurement units so that the state of the whole grid is determined. But the reason it matters to us is a matrix inequality.

## S18 — Why zero forcing bounds the nullity

1. Take any matrix A whose off-diagonal entry in position x, y is nonzero exactly when x and y are joined in the graph. The diagonal is free. Suppose A x equals zero for some vector x, and suppose x vanishes on a set B of vertices.

2. If some vertex u in B has exactly one neighbour w outside B, look at row u of the equation A x equals zero. It reads: A u u times x u, plus the sum over neighbours v of u of A u v times x v, equals zero. Every term vanishes except A u w times x w, because x is zero on u and on all of u's other neighbours, which are in B. And A u w is nonzero, because u and w are joined. So x w must be zero.

3. That is exactly the colour change rule. Blue means the kernel vector is known to vanish there. A blue vertex with one white neighbour forces that neighbour to vanish too. So if S is a zero forcing set and a kernel vector vanishes on S, it vanishes everywhere. Which means a kernel vector is determined by its values on S. The kernel has dimension at most the size of S.

4. The nullity of A is at most Z of G, for every matrix with the graph's pattern, symmetric or not. The maximum nullity over all such symmetric matrices is written M of G, and M is at most Z. This inequality is the bridge. An upper bound on Z is easy: exhibit one forcing set. A lower bound on Z means excluding every smaller set, which is combinatorially brutal. But the inequality converts it into exhibiting a single matrix of large nullity. A matrix is a certificate you can hand someone.

## S19 — What was known, and what was wrong

1. For P of n, k, Rashidi, Shajareh Poursalavati and Tavakkoli proved in 2020 that Z is at most two k plus two. The forcing set is two k plus two consecutive outer vertices, and a rotation argument shows the forcing sweeps around the whole graph. They also showed Z of P of n, two equals six for n at least ten, and claimed, as their Theorem 3.6, that Z of P of n, three equals eight for all n at least twelve.

2. That theorem is false. In July 2026, Krishnan exhibited a forcing set of size seven in P of twelve, three. The flaw was a case analysis that never excluded seven-vertex sets. Krishnan computed the exact values for n from seven to twenty, found that the value hits eight at n equals ten, drops back to seven at eleven and twelve, and reads eight from thirteen to twenty, and stated as Conjecture 5 that Z of P of n, three equals eight for every n at least thirteen. What was missing, he wrote, was a lower-bound proof valid for all large n.

3. And for k at least four, essentially nothing was known: one value, Z of P of two k plus one, k equals six, for each k, which is far below the bound two k plus two. The open problem was explicit: determine the stabilization threshold at k equals three, and give any rigorous lower bound for k at least four.

4. Rigorous lower bound for all large n. That phrase is the whole of Part Two. Upper bounds come free from a forcing set. The lower bound needs, for every n, a matrix on the P of n, k pattern with nullity two k plus two. And it has to be constructed uniformly in n, which is a very different thing from constructing one for each n you happen to try.

## S20 — The exact ceiling: eliminating the inner coordinates

1. Before building anything, ask how far a matrix certificate can possibly go. Take any matrix A with the P of n, k pattern. Not necessarily symmetric. Write b i for the entry on outer edge u i to u i plus one, c i for the spoke, e i for the inner edge v i to v i plus k, with primes for the reverse directions, and a i, d i for the diagonals. All the edge entries are nonzero.

2. A kernel vector has outer coordinates x i and inner coordinates y i. Look at the row for outer vertex u i. It involves x i minus one, x i, x i plus one, and exactly one inner coordinate, y i, through the spoke. Since the spoke weight c i is nonzero, solve for y i: it is a three-term expression in the outer coordinates. Every inner coordinate is determined by the outer ones.

3. Now substitute into the row for inner vertex v i, which involves y i minus k, y i, y i plus k, and x i. Each y is a three-term expression in x, centred at i minus k, i, and i plus k. The result is a single linear relation among the outer coordinates at nine positions: i minus k minus one, i minus k, i minus k plus one, then i minus one, i, i plus one, then i plus k minus one, i plus k, i plus k plus one.

4. The two extreme coefficients, at i plus k plus one and i minus k minus one, are products of nonzero edge weights divided by a spoke weight. They are never zero. So this is a linear recurrence of order exactly two k plus two: knowing two k plus two consecutive outer coordinates determines the next one, and the previous one.

5. A recurrence of order two k plus two has a solution space of dimension two k plus two on the integers. Going once around the cycle of length n gives a linear map T on that space, the monodromy. The kernel vectors of A are exactly the solutions that are periodic with period n, which are the fixed vectors of T. So the nullity of A equals the dimension of the kernel of T minus the identity. That is at most two k plus two, with equality if and only if T is the identity.

## S21 — Why the ceiling matters: no slack

1. The number two k plus two is not new; it is the upper bound on Z. What is new is the identification. Over every matrix with the pattern, symmetric or not, the nullity is at most two k plus two, and it equals two k plus two exactly when the monodromy is the identity.

2. Look at why the order is two k plus two. A nonzero kernel vector cannot vanish on two k plus two consecutive outer vertices, because then the recurrence forces it to vanish everywhere. And the set of two k plus two consecutive outer vertices is exactly the zero forcing set the rotation argument produces. The order of the recurrence equals the size of the forcing set.

3. So the ceiling of the matrix method coincides with the upper bound the method is trying to match. There is no slack on either side. A matrix certificate can prove Z equals two k plus two, and by the theorem it does so precisely when the monodromy is the identity. Either the method settles Z completely, or nothing in this family of methods does. An earlier version of the project described the method as capped near six to eight. That was a property of the constructions tried so far, not of the method, and the theorem corrects it.

4. There is a second payoff. The ceiling is a bound that a search cannot legally violate. Twice during the project, a numerical search returned a nullity the theorem forbids. Both times the theorem caught a bug. Wrapping a search inside a bound it cannot exceed is the only thing that tells you an answer is wrong when it looks right.

## S22 — First certificates: the symbol on the grid

1. Now construct. The simplest matrices to try are those invariant under the rotation: every outer edge weight equal, every spoke equal, every inner edge equal, and constant diagonals a and d. Such a matrix commutes with the shift, so the same Fourier decomposition from Part One applies, and the matrix splits into n two by two blocks.

2. Block m is a plus s m, c on the first row and c, d plus e t m on the second, where s m is two cosine two pi m over n and t m is two cosine two pi k m over n. Each singular block contributes exactly one to the nullity, since the off-diagonal c is nonzero. So the nullity is the number of m for which the determinant of block m vanishes.

3. Expand the determinant. Since t m is a polynomial in s m, via the Chebyshev identity, the determinant is a polynomial in s of degree k plus one. Call it the symbol. The nullity is the number of grid points s m at which the symbol vanishes. The grid is the set of two cosine two pi m over n, which has roughly n over two distinct values, each hit twice, by m and by n minus m.

4. The symbol has k plus one roots but only three free parameters: a, d, and e, with c entering only through c squared. So you can prescribe three roots and no more. For k equals two that is all three roots, and placing them at three grid values gives nullity six, which is the ceiling. For larger k, three prescribed roots give nullity six, well short of two k plus two.

5. Unless the other roots land on the grid by themselves. If the symbol has rational coefficients and one root is two cosine two pi over d, then every Galois conjugate, every two cosine two pi m over d with m coprime to d, is also a root. So choosing the symbol to be a product of minimal polynomials of such numbers drags whole Galois orbits onto the grid. That gives explicit integer certificates: Z of P of n, four equals ten whenever n is divisible by sixty, seventy, or ninety, and Z of P of n, five equals twelve whenever twenty-four divides n. The first exact values at k equals four and five at which the bound is attained, and the first for infinitely many n.

## S23 — Where the symbol method fails, exactly

1. These certificates come with two limitations, and the project proves both are intrinsic rather than failures of effort.

2. First, realisability. The symbol is a polynomial in s, but it must come from an actual matrix, and that imposes a condition: c squared equals a certain expression in the coefficients, and c squared must be nonzero. For a symmetric certificate it must be positive. For even k, the symbol has a reflection symmetry, and any two roots y and minus y, antipodal on the grid, make c squared vanish identically. For k equals two this is the whole story in closed form: c squared is minus the product of s one plus s two, s one plus s three, s two plus s three. The construction fails precisely when two prescribed roots are antipodal.

3. Counting antipodal classes on the grid then settles k equals two for every n. For n at least nine, except n equals ten, three non-antipodal grid values exist, giving Z of P of n, two equals six. At n equals eight and ten the grid is too small to avoid antipodal pairs, and the two cases behave oppositely: at n equals eight the true value is five, so the method is right to fail, while at n equals ten the true value is six and it is the method that falls short. For n equals ten a different, non-symmetric integer matrix does the job.

4. Second, and more fundamental: a symbol with fixed rational coefficients has fixed algebraic roots, and a fixed algebraic number lies on the grid for n only in one divisibility class. Which contains at most one prime. So no period-one certificate, no rotation-invariant matrix, can ever give a value valid for all large n. They can do multiples of ten at k equals three, and multiples of sixty at k equals four, but never n equals seventeen, nineteen, or twenty-three. The route to all large n must break the rotational symmetry.

## S24 — Breaking the symmetry: certifying the monodromy

1. Here the ceiling theorem pays off again. For a general matrix on the pattern, not invariant under rotation, the nullity is two k plus two if and only if the monodromy T is the identity. That condition has no arithmetic in it, no roots of unity, no divisibility. It is a system of polynomial equations in the edge and diagonal weights, and it can be solved numerically for any n, prime or not.

2. A numerical solution is not a proof. The weights come out of a Newton iteration as floating-point numbers, and the monodromy is the identity only to fourteen digits. The question is whether a true real solution exists nearby. That is what a Krawczyk contraction test does: given an approximate solution and a box around it, if a certain operator maps the box into itself, then a genuine solution exists inside the box. It is a theorem of interval analysis, not a measurement.

3. But certifying T equals the identity directly is awkward: T is a rational function of the weights, and the map from weights to T has a fifty-one-dimensional image inside a sixty-four-dimensional space at k equals three, so the system is degenerate in ways that are hard to pin down. The paper certifies the nullity directly instead. Nullity at least r means some full-rank two n by r matrix K satisfies A K equals zero. Fix K in a graph form, an identity block stacked on an unknown block X. Then the equation A of w times K of X equals zero is bilinear in the unknowns w and X: total degree two, with integer coefficients. Its Jacobian is affine, and the Krawczyk constants are cheap.

4. One subtlety nearly broke it. The system A K equals zero has more equations than its rank: K transpose A K is symmetric because A is, so exactly r choose two equations are dependent. If you pick which equations to certify by numerical pivoting, you silently leave r choose two of them unproved. The fix is structural: certify every equation on the non-pivot rows, plus only the upper triangle of the r by r pivot block, and the symmetry forces the lower triangle. The project had certified a result and the test had passed, with twenty-eight equations unproved. A passing test is not a proof.

5. With the structural choice, the certification goes through. Z of P of n, three equals M of P of n, three equals eight at n equals seventeen through thirty-three, including the primes seventeen, nineteen, twenty-three, twenty-nine, thirty-one. Values no period-one certificate could reach. But still one n at a time.

## S25 — Tiles: from each n to every n

1. Certifying n one at a time can never give all large n. But the condition T equals identity is multiplicative along the cycle: T is the product of n step matrices, one per position. If the weight sequence could be built from pieces each contributing the identity, the whole product would be the identity, and different combinations of pieces would reach different n.

2. The obstacle is that each step matrix depends on the weights in a window of width about two k plus two around its position, so adjacent pieces interact across their boundary and the product does not factorize. The fix is a docking pattern. Fix once and for all the values of the five weights at k plus one consecutive positions. A tile is a weight sequence whose first k plus one and last k plus one positions carry the docking pattern, and whose interior is free.

3. Then for any tile, the product of the step matrices over its positions sees only docking weights and its own interior. Every weight in any window either belongs to this tile's interior or to a docking stretch, and the docking stretch is the same whichever tile it belongs to. So the tile product depends only on the tile's interior, and the monodromy of a concatenation of tiles is the product of the tile products. The paper checked this numerically before using it: perturbing one tile's interior leaves the others' products unchanged to the last bit.

4. Now the tiling theorem. Fix k and a length L. Suppose for every length from L up to two L minus one there is a tile whose product is the identity, with all required entries nonzero. Then every n at least L is a sum of such lengths: if n is below two L, use the single tile of length n; otherwise peel off a tile of length L and recurse. Concatenate the tiles. The monodromy is the identity. The nullity is two k plus two. Together with the upper bound, Z of P of n, k equals M of P of n, k equals two k plus two for every n at least L, with no congruence condition.

5. An all-n statement has become a finite list of finite problems: one identity tile for each length in an interval. And the paper notes why the full interval matters. Two tile lengths a and b with no common factor would give only n of the form i a plus j b, missing every n below a minus one times b minus one. For the smallest workable lengths at k equals three that gap is several hundred.

## S26 — The tiles exist, and are certified

1. A tile of length l has five times l minus two k plus two free interior weights, and the identity condition is two k plus two squared equations, sixty-four at k equals three. On parameter count, tiles should exist once l is around twenty-one. And they do: below twenty-one, Newton stalls with residuals near zero point four; at twenty-one and above, identity tiles are found at every length. For k equals three, tiles exist for every length from twenty-one to forty-three, which covers the interval from L equals twenty-one to two L minus one equals forty-one with room to spare.

2. Each tile is then certified, and here the ceiling theorem gives a free gift. The tile condition T tile equals identity is a rational equation, nasty to certify. But the monodromy of a cyclic matrix built from a single tile on P of l, k is that tile's product. So T tile equals identity if and only if the one-tile cyclic matrix has nullity two k plus two. And that is exactly the bilinear nullity system from before, with its affine Jacobian. The docking weights are pinned at their exact integer values, so the certified tiles still fit together.

3. The certification is exact, not floating point. The Krawczyk test needs three norms bounded. Every float64 number is a dyadic rational, so the box centre is known exactly; the system is bilinear with integer coefficients, so the residual and Jacobian at the centre are exact rationals; and the preconditioner Y in the test is arbitrary, so rounding it to rationals costs nothing. The only obstacle was speed, a product of matrices of order a thousand in exact integers, solved by writing integers in base two to the twenty with balanced digits so that each digit product fits in a float64 and BLAS can do the arithmetic. The contraction constant alpha is less than one as an exact integer comparison.

4. All twenty-three tiles at k equals three pass, with alpha at most two point two times ten to the minus ten. All thirty-three tiles at k equals four pass, covering lengths twenty-nine to sixty-one. Twenty-one tiles at k equals five pass, lengths fifty-four to seventy-five with two gaps, which do not form a full interval but still generate every n from one hundred sixty-two upward as sums. Seventy-seven tile certifications in total, plus seventeen per-n certifications, every one evaluated in exact rational arithmetic.

## S27 — The theorems

1. Put it together. Z of P of n, three equals M of P of n, three equals eight for every n at least seventeen. Z of P of n, four equals M of P of n, four equals ten for every n at least twenty-nine. Z of P of n, five equals twelve for every n at least one hundred sixty-two. No congruence conditions. Primes included.

2. Below those thresholds, exhaustive search over vertex subsets settles each value. The search exploits the rotation: a minimum forcing set can be assumed to contain a fixed representative, so the enumeration is exhaustive up to symmetry and still exact. At n equals twenty-eight, k equals four, ruling out every nine-set took about one point two billion candidates. The solver reproduced every published value before use, including Krishnan's corrected table.

3. The result is the complete determination for k equals two, three, and four. For k equals two: five, four, six, five, six, six, six, then six forever from n equals twelve. For k equals three: six, six, six at n seven to nine, eight at ten, seven at eleven and twelve, then eight forever. For k equals four: six, six, seven, six, eight, eight, nine, eight, nine, then ten forever from n equals eighteen. Not one of these rows is monotone. Not one is constant from the first time the bound is attained.

4. In particular, Z of P of n, three equals eight for every n at least thirteen, and thirteen is optimal since the value is seven at eleven and twelve. That is Conjecture 5 of Krishnan's note, stated word for word, proved. The stated missing ingredient, a lower-bound proof valid for all large n, is the tiling theorem. The threshold the note left open is thirteen. And the k equals four row is the first exact determination at k equals four at all, and the first for an infinite family at any k at least four.

5. The interview prep for this project is careful about the attribution, and so should you be. The correction to the published theorem is Krishnan's. The contribution here is the lower bound for all large n, and with it the proof of his conjecture. Say exactly that.

## S28 — The K4 family: a conjecture, and its refutation

1. The clearest thing a research record can show is a mistake caught and corrected by its own author, in writing, with the reason. This project has one, and it was the headline claim.

2. The ceiling theorem generalizes. For a cyclic cover of any base graph with any voltages, the equivariant matrices, those commuting with the rotation, have nullity bounded by the degree span of the determinant of the symbol M of zeta, a polynomial in a root of unity built from the voltages. For P of n, k that span is two k plus two. It is read off the base, independent of n.

3. Consider the base K four, the complete graph on four vertices, with voltages zero on the edges zero-one, zero-three, and one-three, voltage one on zero-two and two-three, and voltage two on one-two. Every cover is cubic, connected, on four n vertices, and the degree span is six for every n. An exact integer matrix attains nullity six. Meanwhile exhaustive search gives Z equal to n plus two for n from four to eight. Z grows without bound while the equivariant ceiling sits at six.

4. The earlier version of the paper concluded that the maximum nullity of this family is six, conjectured that the gap Z minus M grows without bound on cubic graphs, and wrote it onto the poster and into the interview script as the strongest result in the project. That would have answered a question in the Fallat-Hogben survey.

5. It is false, and the reason is in the voltages. The three edges of voltage zero form a triangle. So each fibre carries a triangle whose only edges to the outside go to the fibre over vertex two. Put a rank-one block u u transpose on each triangle. Its off-diagonal entries are nonzero, as the pattern requires, and the diagonal is free, so this is a legal matrix. The three n triangle rows have rank at most two n, the other n rows at most n. So the rank is at most three n and the nullity is at least n. Exact rank over the rationals: exactly n, for n from four to ten.

6. So M is at least n, the gap to Z equals n plus two is at most two, and the regular-base ceiling conjecture is dead: K four is cubic. In the equivariant picture, the rank-one block makes the determinant of M of zeta vanish identically, which is a hypothesis the cover theorem needed and had not stated. Both of the project's adversarial searches missed this matrix, because it lives where three of four fibre blocks are singular, and neither search goes there. It was found by reading the voltages, not by searching. What replaces regularity as the hypothesis is the leading coefficient of the symbol, and that is now stated as a conjecture, checked on every base in the paper and proved on none beyond the two-vertex, path-with-loops, and cycle cases.

## S29 — What is proved, what is certified, what is open

1. The paper ends with a status-of-claims section labelling every result by the standard it meets, and the labels are worth knowing because they are not all the same.

2. Proved, with a proof in the text: the reduction and the ceiling, the symbol classification, the realisability criterion with its antipodal obstruction, the congruence-class theorem, the two-vertex-base reductions, the K four refutation, and the Part One criterion, corner form, uniform bound, Dirichlet bound and parity law.

3. Proved by exact certificate, meaning an explicit matrix with nullity computed in integer or cyclotomic arithmetic: k equals two for all n at least nine except ten; k equals three on multiples of ten; k equals four on multiples of sixty, seventy, ninety; k equals five on multiples of twenty-four; k equals seven on multiples of one hundred twenty.

4. Proved by exact certification, meaning a Krawczyk contraction bound evaluated in exact rational arithmetic: the all-large-n theorems at k equals three, four, and five. Proved finite, by exhaustive search: every tabulated small value. Numerical only, and said so: k equals six at seven values of n and one value at k equals eight, from period-three Newton solves never made exact.

5. Open: whether tiles exist for k at least six, where the parameter count says lengths from fifty-four and none have been found. Whether M of P of twenty-four, four is ten, the one value where the matrix statement is weaker than the forcing statement. The exact maximum nullity of the K four family, between n and n plus two. And the leading-coefficient criterion, conjectural. The project also lists eight of its own earlier claims as refuted and one search as withdrawn as unreliable, because it collapsed onto degenerate strata and reported plateaus that were not there.

## S30 — Verification as method

1. A word on how the numbers are trusted, because for a project like this that is half the work. One script re-derives every computational claim from the certificates on disk: one hundred forty-one checks at the time of recording. Every number in the paper, every threshold and tile count, is generated by that script and read into the LaTeX, never typed by hand. The census had drifted three times through bookkeeping slips before that rule was adopted.

2. Every search runs alongside a control. The exact Ramanujan classifier ran beside a float64 classifier and the control found the dictionary bug. The nullity searches run under the ceiling theorem, which caught two impossible answers. The exhaustive forcing solver was cross-checked against brute force and two independent exact solver formulations before being trusted on new values.

3. And the log records wrong turns with dates: the invalid Taylor derivation, the degree claimed as two k that is two k plus two, the misattributed citation, a separation guard that underflowed to zero and so could never fire, the pivoting that left twenty-eight equations unproved, and the K four conjecture. A passing test is not a proof. A converged optimum is not a witness. A failed search measures effort, not impossibility. Each of those sentences in the paper was earned by a specific mistake.

## S31 — Closing: one grid, two directions

1. Here is the whole project in one picture. The n-th roots of unity, the grid that indexes the cyclic cover. In Part One the matrix is fixed, its spectrum is a fixed curve sampled on that grid, and the question is whether the samples avoid a forbidden band: a fixed polynomial that must not change sign. In Part Two the matrix ranges, and the question is how many roots of a chosen polynomial you can force onto that same grid, and then, when the symmetry is broken, how to make the monodromy the identity for every period at once.

2. Fixed polynomial avoiding a band. Constructed polynomial hitting the grid. Same object, opposite direction, and the same exact-arithmetic machinery deciding both: reduce to cyclotomic points, certify signs and vanishing exactly, never trust a float where a float cannot decide.

3. What was found: exactly four hundred sixty generalized Petersen graphs satisfy the Riemann Hypothesis, none past k equals forty-five, by a criterion with no k in it and a Dirichlet bound of two hundred thirty-one. Z of P of n, k equals two k plus two for all n at least seventeen when k is three and at least twenty-nine when k is four, which with exhaustive search determines Z at every n for k equals two, three, four, and proves Krishnan's Conjecture 5 with threshold thirteen. A ceiling theorem that says the matrix method either solves the problem or cannot touch it. And a refuted conjecture, with the one-line reason why.

4. What is next is written down too: close the one open value at k equals four, find the tiles at k equals five and six, and prove or refute the leading-coefficient criterion, which is the one thing here an expert might call interesting. Those are the open problems. This is where the project stands on the first of October, 2026.
