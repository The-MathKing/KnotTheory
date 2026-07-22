/* Exact zero forcing number for an arbitrary graph read from stdin.
   Input:  N M            (vertices, edges)
           a b            (M lines, 0-indexed)
           R r0 r1 ...    (optional: orbit representatives for symmetry)
   If representatives are given, the search assumes a minimum forcing set
   contains one of them -- valid whenever the graph has an automorphism group
   whose orbits are represented by that list. Otherwise searches all subsets.
   Supports N <= 128. Threaded. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

typedef unsigned __int128 u128;
static int N, NTH;
static u128 adj[128], FULL;
static volatile int found; static u128 found_set;
static pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;

static inline int ctz128(u128 x){
    unsigned long long lo=(unsigned long long)x;
    return lo?__builtin_ctzll(lo):64+__builtin_ctzll((unsigned long long)(x>>64));
}
static inline int forces(u128 S){
    u128 f2=S; int ch=1;
    while(ch && f2!=FULL){
        ch=0; u128 f=f2;
        while(f){ int v=ctz128(f); f&=f-1;
            u128 w=adj[v]&~f2;
            if(w && !(w&(w-1))){ f2|=w; ch=1; } }
    }
    return f2==FULL;
}
typedef struct{ int tid,r,psz; const int*pool; u128 base; } Job;
static void* worker(void*a){
    Job*J=(Job*)a; int r=J->r;
    if(r==0){ if(!found&&forces(J->base)){ pthread_mutex_lock(&mtx);
        if(!found){found=1;found_set=J->base;} pthread_mutex_unlock(&mtx);} return 0; }
    int idx[130];
    for(int first=J->tid; first<=J->psz-r; first+=NTH){
        if(found) return 0;
        idx[0]=first; for(int i=1;i<r;i++) idx[i]=idx[i-1]+1;
        while(1){
            u128 S=J->base; for(int i=0;i<r;i++) S|=((u128)1<<J->pool[idx[i]]);
            if(forces(S)){ pthread_mutex_lock(&mtx);
                if(!found){found=1;found_set=S;} pthread_mutex_unlock(&mtx); return 0; }
            int i=r-1; while(i>=1&&idx[i]==J->psz-r+i) i--;
            if(i<1) break;
            idx[i]++; for(int j=i+1;j<r;j++) idx[j]=idx[j-1]+1;
        }
    }
    return 0;
}
static int search(int m,const int*pool,int psz,u128 base){
    found=0; pthread_t th[64]; Job jb[64];
    for(int t=0;t<NTH;t++){ jb[t]=(Job){t,m,psz,pool,base}; pthread_create(&th[t],0,worker,&jb[t]); }
    for(int t=0;t<NTH;t++) pthread_join(th[t],0);
    return found;
}
int main(int argc,char**argv){
    int cap=(argc>1)?atoi(argv[1]):14; NTH=(argc>2)?atoi(argv[2]):8;
    int M; if(scanf("%d %d",&N,&M)!=2) return 1;
    if(N>128){ fprintf(stderr,"N>128\n"); return 1; }
    FULL=(N==128)?~(u128)0:(((u128)1<<N)-1);
    for(int i=0;i<N;i++) adj[i]=0;
    for(int e=0;e<M;e++){ int a,b; if(scanf("%d %d",&a,&b)!=2) return 1;
        adj[a]|=((u128)1<<b); adj[b]|=((u128)1<<a); }
    int reps[128], nrep=0; char tok[8];
    if(scanf("%1s",tok)==1 && (tok[0]=='R'||tok[0]=='r')){
        int v; while(scanf("%d",&v)==1) reps[nrep++]=v;
    }
    for(int m=1;m<=cap;m++){
        if(nrep==0){
            int pool[128]; for(int v=0;v<N;v++) pool[v]=v;
            if(search(m,pool,N,0)){ goto done_m; }
        } else {
            for(int t=0;t<nrep;t++){
                int pool[128],p=0;
                for(int v=0;v<N;v++) if(v!=reps[t]) pool[p++]=v;
                if(search(m-1,pool,p,((u128)1<<reps[t]))) goto done_m;
            }
        }
        continue;
    done_m:
        printf("Z=%d witness=",m);
        for(int v=0;v<N;v++) if((found_set>>v)&1) printf("%d ",v);
        printf("\n"); return 0;
    }
    printf("Z>%d\n",cap); return 0;
}
