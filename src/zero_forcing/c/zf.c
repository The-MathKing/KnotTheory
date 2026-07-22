/* Exact zero forcing number of generalized Petersen graphs P(n,k).
   Enumerates vertex subsets by increasing size with 128-bit mask closure,
   mirroring the reference method (bitmask enumeration) used in arXiv
   2607.19412, which this is validated against. Supports 2n <= 128. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;
static int N;
static u128 adj[128], FULL;

static inline int ctz128(u128 x){
    unsigned long long lo=(unsigned long long)x;
    return lo ? __builtin_ctzll(lo) : 64+__builtin_ctzll((unsigned long long)(x>>64));
}
static inline int pc128(u128 x){
    return __builtin_popcountll((unsigned long long)x)
         + __builtin_popcountll((unsigned long long)(x>>64));
}
static void build(int n,int k){
    N=2*n; FULL = (N==128)? ~(u128)0 : (((u128)1<<N)-1);
    for(int i=0;i<N;i++) adj[i]=0;
    #define LINK(a,b) do{ adj[a]|=((u128)1<<(b)); adj[b]|=((u128)1<<(a)); }while(0)
    for(int i=0;i<n;i++){ LINK(i,(i+1)%n); LINK(i,n+i); LINK(n+i,n+((i+k)%n)); }
}
static inline u128 closure(u128 S){
    u128 filled=S; int changed=1;
    while(changed && filled!=FULL){
        changed=0; u128 f=filled;
        while(f){
            int v=ctz128(f); f&=f-1;
            u128 white=adj[v]&~filled;
            if(white && !(white&(white-1))){ filled|=white; changed=1; }
        }
    }
    return filled;
}
/* smallest m with a forcing set; writes witness */
static int zf(int cap,u128*witness){
    int idx[130];
    for(int m=1;m<=cap;m++){
        for(int i=0;i<m;i++) idx[i]=i;
        while(1){
            u128 S=0; for(int i=0;i<m;i++) S|=((u128)1<<idx[i]);
            if(closure(S)==FULL){ *witness=S; return m; }
            int i=m-1;
            while(i>=0 && idx[i]==N-m+i) i--;
            if(i<0) break;
            idx[i]++;
            for(int j=i+1;j<m;j++) idx[j]=idx[j-1]+1;
        }
    }
    return -1;
}
int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: zf n k [cap]\n"); return 1; }
    int n=atoi(argv[1]),k=atoi(argv[2]);
    int cap=(argc>3)?atoi(argv[3]):14;
    if(!(n>=3 && k>=1 && 2*k<n)){ fprintf(stderr,"need n>=3, 1<=k<n/2\n"); return 1; }
    if(2*n>128){ fprintf(stderr,"2n>128 unsupported\n"); return 1; }
    build(n,k);
    u128 w=0; int z=zf(cap,&w);
    printf("P(%d,%d) Z=%d witness=",n,k,z);
    for(int v=0;v<N;v++) if((w>>v)&1) printf("%d ",v);
    printf("\n");
    return 0;
}
