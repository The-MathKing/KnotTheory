"""
Zero forcing numbers of double generalized Petersen graphs DP(n,k).

DP(n,k) has 4n vertices u_i, w_i, x_i, y_i with edges
    u_i u_{i+1},  x_i x_{i+1}        (two outer cycles)
    w_i y_{i+k},  y_i w_{i+k}        (inner)
    u_i w_i,      x_i y_i            (spokes)
It is cubic. Hamiltonicity, super-connectivity and the automorphism group of
this family are studied in the literature; no zero forcing results were found.

The rotation i -> i+1 is an automorphism with orbit representatives
u_0, w_0, x_0, y_0, so a minimum forcing set may be assumed to contain one of
them -- this is the symmetry reduction passed to the solver.
"""
import subprocess, sys, time

def dp_edges(n, k):
    U=lambda i: i%n; W=lambda i: n+(i%n); X=lambda i: 2*n+(i%n); Y=lambda i: 3*n+(i%n)
    E=set()
    for i in range(n):
        E.add(tuple(sorted((U(i), U(i+1)))))
        E.add(tuple(sorted((X(i), X(i+1)))))
        E.add(tuple(sorted((W(i), Y(i+k)))))
        E.add(tuple(sorted((Y(i), W(i+k)))))
        E.add(tuple(sorted((U(i), W(i)))))
        E.add(tuple(sorted((X(i), Y(i)))))
    return sorted(E)

def solve(N, E, reps, cap=16, threads=8):
    inp=f"{N} {len(E)}\n"+"\n".join(f"{a} {b}" for a,b in E)
    if reps: inp+="\nR "+" ".join(map(str,reps))
    r=subprocess.run(["./src/zero_forcing/c/zfgen",str(cap),str(threads)],
                     input=inp, capture_output=True, text=True)
    return r.stdout.strip()

if __name__ == "__main__":
    print("DP(n,k): 4n vertices, cubic")
    for k in (1,2,3):
        print(f"\n=== k={k} ===", flush=True)
        for n in range(2*k+1, 2*k+11):
            E=dp_edges(n,k); N=4*n
            # sanity: cubic
            deg={}
            for a,b in E: deg[a]=deg.get(a,0)+1; deg[b]=deg.get(b,0)+1
            if set(deg.values())!={3} or len(deg)!=N:
                print(f"  DP({n},{k}): NOT CUBIC ({sorted(set(deg.values()))}) -- skipped",flush=True)
                continue
            t=time.time(); out=solve(N,E,[0,n,2*n,3*n])
            print(f"  DP({n},{k}) [{N} vtx]: {out}   [{time.time()-t:.1f}s]", flush=True)

def igraph_edges(n, j, k):
    """I-graph I(n,j,k): u_i~u_{i+j}, u_i~v_i, v_i~v_{i+k}. P(n,k)=I(n,1,k)."""
    U=lambda i: i%n; V=lambda i: n+(i%n)
    E=set()
    for i in range(n):
        E.add(tuple(sorted((U(i), U(i+j)))))
        E.add(tuple(sorted((V(i), V(i+k)))))
        E.add(tuple(sorted((U(i), V(i)))))
    return sorted(E)
