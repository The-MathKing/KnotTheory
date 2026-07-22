/* Exact zero forcing number of P(n,k) -- threaded, with rotation-symmetry
   reduction. Validated against arXiv 2607.19412 Table 1 and the published
   Z(P(n,2))=6, Z(P(2k+1,k))=6 values.

   Symmetry: rho(i)=i+1 is an automorphism of P(n,k), and rho(S) forces iff S
   does. So a minimum forcing set may be assumed to contain u_0, unless it is
   entirely inner, in which case it may be assumed to contain v_0. We search
   exactly those two families -- exhaustive up to symmetry, hence exact. */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

typedef unsigned __int128 u128;
static int N, n_, k_, NTH;
static u128 adj[128], FULL;
static volatile int found; static u128 found_set; static int found_m;
static pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;

static inline int ctz128(u128 x){
    unsigned long long lo=(unsigned long long)x;
    return lo?__builtin_ctzll(lo):64+__builtin_ctzll((unsigned long long)(x>>64));
}
static void build(int n,int k){
    n_=n;k_=k;N=2*n; FULL=(N==128)?~(u128)0:(((u128)1<<N)-1);
    for(int i=0;i<N;i++) adj[i]=0;
    #define LINK(a,b) do{adj[a]|=((u128)1<<(b));adj[b]|=((u128)1<<(a));}while(0)
    for(int i=0;i<n;i++){ LINK(i,(i+1)%n); LINK(i,n+i); LINK(n+i,n+((i+k)%n)); }
}
static inline int forces(u128 S){
    u128 filled=S; int ch=1;
    while(ch&&filled!=FULL){
        ch=0; u128 f=filled;
        while(f){ int v=ctz128(f); f&=f-1;
            u128 w=adj[v]&~filled;
            if(w&&!(w&(w-1))){ filled|=w; ch=1; } }
    }
    return filled==FULL;
}
/* enumerate (m-1)-subsets of pool[0..psz-1], always together with `base` */
typedef struct{ int tid,m,psz; const int*pool; u128 base; } Job;
static void* worker(void*arg){
    Job*J=(Job*)arg; int r=J->m-1;
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
    if(argc<3){ fprintf(stderr,"usage: zfp n k [cap] [threads]\n"); return 1; }
    int n=atoi(argv[1]),k=atoi(argv[2]);
    int cap=(argc>3)?atoi(argv[3]):14; NTH=(argc>4)?atoi(argv[4]):8;
    if(!(n>=3&&k>=1&&2*k<n)){ fprintf(stderr,"need n>=3,1<=k<n/2\n"); return 1; }
    build(n,k);
    int poolA[128],poolB[128],pa=0,pb=0;
    for(int v=1;v<N;v++) poolA[pa++]=v;              /* with u_0 */
    for(int v=n+1;v<N;v++) poolB[pb++]=v;            /* inner only, with v_0 */
    for(int m=1;m<=cap;m++){
        if(search(m,poolA,pa,(u128)1)){ found_m=m; goto done; }
        if(search(m,poolB,pb,((u128)1<<n))){ found_m=m; goto done; }
    }
    printf("P(%d,%d) Z>%d\n",n,k,cap); return 0;
done:
    printf("P(%d,%d) Z=%d witness=",n,k,found_m);
    for(int v=0;v<N;v++) if((found_set>>v)&1) printf("%d ",v);
    printf("\n"); return 0;
}
