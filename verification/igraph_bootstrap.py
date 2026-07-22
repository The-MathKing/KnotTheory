"""
Verify the chain behind the conjectured bound Z(I(n,j,k)) <= 2(j+k).

I(n,j,k): outer u_i ~ u_{i+j}, inner v_i ~ v_{i+k}, spokes u_i ~ v_i.
Take m = 2(j+k) and S = {u_0,...,u_{m-1}}.

 (1) u_i forces v_i exactly for j <= i <= m-1-j (both outer nbrs in S),
     filling v_j,...,v_{m-1-j} = v_j,...,v_{j+2k-1};
 (2) v_{j+k} has u_{j+k} in S and v_j filled, so it forces v_{j+2k} = v_{m-j};
 (3) u_{m-j} = u_{j+2k} has u_{2k} in S and v_{j+2k} filled, so it forces u_m.

Then rho(S) = {u_1,...,u_m} subset cl(S), and since rho is an automorphism
whose orbit of u_0 is every outer vertex, the bootstrap gives cl(S) = V.
For j=1 this is m = 2k+2, recovering the P(n,k) theorem.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from verification.dp_graphs import igraph_edges
from math import gcd

def build(n,j,k):
    N=2*n; adj=[0]*N
    for a,b in igraph_edges(n,j,k): adj[a]|=1<<b; adj[b]|=1<<a
    return adj,N
def closure(adj,S,N):
    full=(1<<N)-1; f=S; ch=True
    while ch and f!=full:
        ch=False; t=f
        while t:
            v=(t&-t).bit_length()-1; t&=t-1
            w=adj[v]&~f
            if w and not (w&(w-1)): f|=w; ch=True
    return f
def rot(S,n,N):
    out=0
    for v in range(N):
        if (S>>v)&1:
            c,i=divmod(v,n); out|=1<<(c*n+(i+1)%n)
    return out

def check(n,j,k):
    adj,N=build(n,j,k)
    U=lambda i: i%n; V=lambda i: n+(i%n)
    m=2*(j+k)
    S=0
    for i in range(m): S|=1<<U(i)
    # step 1
    ok1=True
    for i in range(j, m-j):
        if adj[U(i)]&~S != (1<<V(i)): ok1=False; break
    A=S
    for i in range(j, m-j): A|=1<<V(i)
    # step 2
    ok2 = (adj[V(j+k)]&~A == (1<<V(j+2*k)))
    B=A|(1<<V(j+2*k))
    # step 3
    ok3 = (adj[U(j+2*k)]&~B == (1<<U(m)))
    cl=closure(adj,S,N)
    boot = (rot(S,n,N)&~cl)==0
    full = cl==(1<<N)-1
    return ok1,ok2,ok3,boot,full,m

print(f"{'I(n,j,k)':>12} {'m=2(j+k)':>9} {'s1':>3} {'s2':>3} {'s3':>3} {'rho(S)<=cl':>11} {'cl=V':>5}")
print("-"*54)
bad=0
for j in range(1,5):
    for k in range(1,6):
        for n in range(2*(j+k)+1, 2*(j+k)+7):
            if gcd(gcd(n,j),k)!=1: continue
            deg={}
            for a,b in igraph_edges(n,j,k): deg[a]=deg.get(a,0)+1; deg[b]=deg.get(b,0)+1
            if len(deg)!=2*n or set(deg.values())!={3}: continue
            a,b,c,bo,fu,m=check(n,j,k)
            if not (a and b and c and bo and fu): bad+=1
            print(f"I({n},{j},{k})".rjust(12)+f" {m:>9} {str(a)[0]:>3} {str(b)[0]:>3} "
                  f"{str(c)[0]:>3} {str(bo):>11} {str(fu):>5}")
print(f"\n{'ALL CASES PASS' if bad==0 else str(bad)+' FAILURES'}")
