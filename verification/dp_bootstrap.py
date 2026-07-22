"""
Verify the three-step forcing chain behind the new bound Z(DP(n,k)) <= 4k+4.

S = {u_0..u_{2k+1}} union {x_0..x_{2k+1}},  |S| = 4k+4.
 (1) for 1<=i<=2k, u_i forces w_i and x_i forces y_i;
 (2) w_{k+1} forces y_{2k+1};  y_{k+1} forces w_{2k+1};
 (3) x_{2k+1} forces x_{2k+2}; u_{2k+1} forces u_{2k+2}.
Then rho(S) subset cl(S), and the rotation bootstrap gives cl(S)=V.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from verification.dp_graphs import dp_edges

def build(n,k):
    N=4*n; adj=[0]*N
    for a,b in dp_edges(n,k): adj[a]|=1<<b; adj[b]|=1<<a
    return adj,N

def check(n,k):
    adj,N=build(n,k)
    U=lambda i: i%n; W=lambda i: n+(i%n); X=lambda i: 2*n+(i%n); Y=lambda i: 3*n+(i%n)
    S=0
    for i in range(2*k+2): S|=1<<U(i); S|=1<<X(i)
    # step 1
    ok1=True
    for i in range(1,2*k+1):
        if adj[U(i)]&~S != (1<<W(i)): ok1=False
        if adj[X(i)]&~S != (1<<Y(i)): ok1=False
    A=S
    for i in range(1,2*k+1): A|=1<<W(i); A|=1<<Y(i)
    # step 2
    ok2 = (adj[W(k+1)]&~A == (1<<Y(2*k+1))) and (adj[Y(k+1)]&~A == (1<<W(2*k+1)))
    B=A|(1<<Y(2*k+1))|(1<<W(2*k+1))
    # step 3
    ok3 = (adj[X(2*k+1)]&~B == (1<<X(2*k+2))) and (adj[U(2*k+1)]&~B == (1<<U(2*k+2)))
    return ok1,ok2,ok3

print(f"{'graph':>11} {'step1':>6} {'step2':>6} {'step3':>6}")
print("-"*33)
allok=True
for k in range(1,6):
    for n in range(2*k+3, 2*k+11):
        a,b,c=check(n,k)
        if not(a and b and c): allok=False
        print(f"DP({n},{k})".rjust(11)+f" {str(a)[0]:>6} {str(b)[0]:>6} {str(c)[0]:>6}")
print("\nALL THREE STEPS HOLD FOR EVERY CASE" if allok else "\nSOME STEP FAILS")
