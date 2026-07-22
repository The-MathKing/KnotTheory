# 17 — Hard questions, with answers

Questions a referee, a judge, or a sceptical mathematician would ask. Answer
these out loud until they are automatic.

## On the basics

**Q. What is the zero forcing number, in one sentence?**
The smallest number of vertices you must colour black at the start so that a
rule — a black vertex with exactly one white neighbour forces it black —
eventually colours the whole graph.

**Q. Why "exactly one"? Why not "at least one"?**
With two or more white neighbours the black vertex has no way to choose; the
rule would be ambiguous. "Exactly one" makes the process deterministic, and it
is what makes the parameter bound the maximum nullity — the algebra mirrors the
rule exactly.

**Q. Why does anyone care?**
Two applied origins (controllability of quantum spin networks, sensor placement
in power grids) and one mathematical one: Z(G) bounds the maximum nullity of
the matrices carrying G's pattern, which is the minimum rank problem.

**Q. What was actually open?**
Exact values of Z(P(n,k)) were known only for k = 2 and k = 3. A July 2026
correction note — which exists because a published 2020 theorem is false —
closes by recording that a rigorous lower bound for k ≥ 4 remains open. This
work gives the first exact values for k ≥ 4.

## On the mathematics

**Q. Why is M(G) ≤ Z(G)?**
Take a kernel vector x vanishing on a zero forcing set. At a black vertex u with
one white neighbour w, row u of Ax = 0 has every term zero except A(u,w)x_w, and
A(u,w) ≠ 0 because uw is an edge. So x_w = 0. The zero propagates by *exactly*
the colour change rule, so x vanishes everywhere. Then x ↦ x|_S is injective on
ker A, so nullity ≤ |S|.

**Q. Where does symmetry get used in that proof?**
Nowhere. That is the point — the argument needs only that every edge carries a
nonzero entry, so it extends to non-symmetric matrices and gives a bigger search
space (8n parameters instead of 5n) at no cost in rigour.

**Q. Why is the recurrence order 2k+2 and not something else?**
Because every spoke weight is nonzero, you can solve for the inner variable at
each index and substitute. The inner equation reaches k steps in each direction,
and the substitution widens each reach by one, giving a window from i−k−1 to
i+k+1 — that is 2k+3 values, so order 2k+2. Both end coefficients are products
of nonzero quantities, hence nonzero, which is what makes it a genuine
recurrence of that order rather than a degenerate one.

**Q. Is it a coincidence that the order equals the upper bound?**
No, and this is the nicest part. Order 2k+2 means no nonzero kernel vector
vanishes on 2k+2 consecutive outer vertices — and 2k+2 consecutive outer
vertices is exactly the forcing set the rotation bootstrap produces. The two
statements are the same fact. So the ceiling of the matrix method coincides
exactly with the upper bound it is trying to match.

**Q. So could the method settle the problem completely?**
In principle yes, and that is why the ceiling theorem matters. There is no slack
on either side: the method can prove Z ≥ 2k+2 and no more, and 2k+2 is exactly
the known upper bound. What is missing is a construction valid for every n.

**Q. Why does the symbol have only three parameters when it has degree k+1?**
Because it is forced to be of the shape (s + a)L_k(s) + αs + β. Subtracting
s·L_k, the remainder must lie in the span of {L_k, s, 1} — that is k−2 linear
conditions on the k+1 coefficients.

**Q. Then how can all k+1 roots land on the grid?**
You do not place them one at a time. If the symbol has *rational* coefficients,
its roots come in Galois conjugate families: a rational polynomial having one
root of a family has them all. And the Galois conjugates of a grid value
2cos(2πm/n) are again grid values. So one rational polynomial delivers a whole
orbit at once.

**Q. You previously claimed this construction was capped at 6. What happened?**
The premise was right — three roots can be prescribed and no more — but the
inference was wrong. Prescribing three roots *determines* the remaining k−2, and
those can land on the grid by themselves. I wrote a script to confirm the cap
exhaustively and it printed 12 immediately. The period-two machinery built to
escape that cap turned out to be unnecessary.

**Q. What is the monodromy, for someone who knows matrices but not ODEs?**
Bundle 2k+2 consecutive values of the sequence into a state vector. The
recurrence moves you one step, which is a matrix. Multiply those matrices all
the way around the cycle of length n; that product is the monodromy. A solution
closes up periodically exactly when the monodromy fixes its starting state.

## On rigour

**Q. Is the certificate a numerical observation or a proof?**
A proof. The cyclotomic certificates have integer entries, so the nullity is
computed by exact Gaussian elimination over the rationals. The irrational ones
are verified in the number field Q(ζ_n), representing 2cos(2πm/n) as
x^m + x^(n−m) modulo Φ_n(x), so the membership identity, the reality of the
parameters and c² ≠ 0 are decided exactly.

**Q. How do you know your code is right?**
The exhaustive solver reproduced *every* published value before being trusted —
including the corrected Z(P(12,3)) = 7 and the non-monotone values at n = 10,
11 — and was cross-checked against an independent brute-force implementation and
two exact solver formulations. The structural theorem was checked on 249 random
matrices across 63 parameter pairs.

**Q. Have you made numerical errors?**
Yes, three, and all three were caught by a bound that must hold. A vanishing
edge weight (3×10⁻⁴ against scale 4.5) once manufactured a fake nullity 7 for
P(14,2), where Z = 6; a dense-grid tolerance manufactured nullity 7 for k = 2;
a scaling failure manufactured nullity 48 at (48,7). The working rule that came
out of it: wrap every numerical search in a bound it cannot legally violate,
because that bound is the only thing that tells you an answer is wrong when it
looks right.

**Q. What is the weakest part of the work?**
That the results hold on congruence classes of n rather than for all large n,
and that k ≥ 6 is untouched. Also that the claim "the remaining obstruction is
arithmetic rather than dimensional" is an observation supported by search
plateaus, not a theorem — no single (n,k) is proved to have M < 2k+2.

**Q. What would break it?**
A single (n,k) in one of the stated classes where the exact rank computation
disagrees. That is checkable in minutes by anyone, which is the point of using
integer certificates.

## On positioning

**Q. What is genuinely new here?**
Three things. (1) The reduction theorem: every matrix with the pattern collapses
to a nine-term recurrence of order 2k+2, so the method has an exact ceiling that
equals the upper bound. (2) The mechanism: rational symbols pull whole Galois
orbits onto the Fourier grid, which is what breaks past the apparent parameter
shortage. (3) The first exact values of Z(P(n,k)) for k ≥ 4.

**Q. Is this just a computation?**
No. The computations verify; the content is the reduction theorem and the
cyclotomic construction. The certificate for k = 5 is the plain adjacency
matrix — no computation is needed to write it down, only to recognise that
s·L_5 − 1 = Ψ_6Ψ_3Ψ_24.

**Q. What surprised you most?**
That the simplest matrix in the entire class — the adjacency matrix — was
sufficient for k = 5, after a great deal of effort building elaborate ones.

**Q. Explain it to someone with no mathematics.**
There is a family of network shapes. For each one, there is a number measuring
how many points you must "switch on" for a simple spreading rule to light up the
whole network. Nobody knew that number for most of the family, and a published
proof about it turned out to be wrong. I found a way to turn the question into
one about matrices, showed that method has an exact limit that happens to be
exactly the answer people expect, and then reached that limit — so for infinitely
many of these shapes, the number is now known exactly, and a computer can check
it in exact whole-number arithmetic.
