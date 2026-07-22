"""
Verify the rotation-bootstrap upper bound Z(P(n,k)) <= 2k+2.

Claim. Let S = {u_0,...,u_{2k+1}} and rho(i)=i+1 the rotation automorphism.
If u_{2k+2} in cl(S), then rho(S) subset cl(S), hence
    rho(cl(S)) = cl(rho(S)) subset cl(cl(S)) = cl(S),
and since rho is a bijection of a finite set, rho(cl(S)) = cl(S). So cl(S) is
rho-invariant; it contains u_0 whose rho-orbit is the whole outer cycle, so all
u_i are filled, and then each u_i forces its unique remaining white neighbour
v_i. Hence cl(S)=V and Z <= |S| = 2k+2.

The only thing needing checking is the finite claim u_{2k+2} in cl(S), which
the hand argument derives in three steps:
  (1) for 1<=i<=2k, u_i has u_{i-1},u_{i+1} in S, so forces v_i;
  (2) v_{k+1} then has u_{k+1},v_1 filled, so forces v_{2k+1};
  (3) u_{2k+1} then has u_{2k},v_{2k+1} filled, so forces u_{2k+2}.
This script verifies each step separately, and the overall closure.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from zero_forcing.zf import generalized_petersen, closure

def step_check(n, k):
    adj = generalized_petersen(n, k); N = 2*n
    U = lambda i: i % n
    V = lambda i: n + (i % n)
    S = 0
    for i in range(2*k+2): S |= 1 << U(i)
    notes = []
    # (1) each u_i (1<=i<=2k) should have v_i as its unique white neighbour
    ok1 = True
    for i in range(1, 2*k+1):
        white = adj[U(i)] & ~S
        if not (white and (white & (white-1)) == 0 and white == (1 << V(i))):
            ok1 = False; break
    notes.append(("step1 u_i->v_i", ok1))
    A = S
    for i in range(1, 2*k+1): A |= 1 << V(i)
    # (2) v_{k+1} forces v_{2k+1}
    white = adj[V(k+1)] & ~A
    ok2 = (white == (1 << V(2*k+1)))
    notes.append(("step2 v_{k+1}->v_{2k+1}", ok2))
    B = A | (1 << V(2*k+1))
    # (3) u_{2k+1} forces u_{2k+2}
    white = adj[U(2*k+1)] & ~B
    ok3 = (white == (1 << U(2*k+2)))
    notes.append(("step3 u_{2k+1}->u_{2k+2}", ok3))
    # overall
    cl = closure(adj, S)
    has = (cl >> U(2*k+2)) & 1
    full = (cl == (1 << N) - 1)
    return notes, bool(has), full

print(f"{'k':>2} {'n':>4} | step1 step2 step3 | u_{{2k+2}} in cl(S) | cl(S)=V  (=> Z<=2k+2)")
print("-"*78)
for k in range(2, 9):
    for n in range(2*k+1, 2*k+16):
        notes, has, full = step_check(n, k)
        s1,s2,s3 = (str(v)[0] for _,v in notes)
        flag = "" if (full == (has and True)) else "  <-- mismatch"
        print(f"{k:>2} {n:>4} |   {s1}     {s2}     {s3}   |      {str(has):>5}       |  {str(full):>5}{flag}")
