//Language: GNU C++


#include <bits/stdc++.h>
using namespace std;

#define fru(j,n) for(int j=0; j<(n); ++j)
#define tr(it,v) for(typeof((v).begin()) it=(v).begin(); it!=(v).end(); ++it)
#define x first
#define y second
#define pb push_back
#define ALL(G) (G).begin(),(G).end()

typedef long long ll;
typedef double D;
typedef pair<int,int> pii;
typedef pair<ll,ll> pll;
typedef vector<int> vi;

const int inft = 1000000009;
const int MAXM = 106;//10^6

int n,m;
pii R[MAXM];
string S[MAXM];
char str[MAXM][20];

bool cond(int a1,int a2,int a,int b){
	fru(i,m)if(R[i].x==a1 || R[i].x==a2 || R[i].y==a1 || R[i].y==a2){
		if(R[i]==pii(a1,a2) || R[i]==pii(a2,a1)){
			if(S[i]=="<")return false;
		}
		else{
			if(R[i].x==a1 || R[i].x==a2){
				if(R[i].y<a || R[i].y> n-1-b){
					return false;	
				}
			}
			else{
				if(R[i].x<a || R[i].x> n-1-b){
					if(S[i]=="=")return false;
				}
			}
		
		}
	}
	return true;
}
ll DP[MAXM][MAXM];
ll get(int a,int b){
//	printf("rozwazam %d %d\n",a,b);
	if(DP[a][b]!=-1)return DP[a][b];
	ll ans=0;
	if(a>=2 && cond(a-1,a-2,a-2,b) )ans+=get(a-2,b);
	if(a>=1 && b>=1 && cond(a-1,n-1-(b-1),a-1,b-1) )ans+=get(a-1,b-1);
	if(b>=2 && cond(n-1-(b-1),n-1-(b-2),a,b-2))ans+=get(a,b-2);
	return DP[a][b]=ans;
}
void solve() {
	scanf("%d%d",&n,&m);
	n*=2;
	fru(i,n)fru(j,n)DP[i][j]=-1;
	DP[0][0]=1;
	fru(i,m){
		scanf("%d %s%d",&R[i].x,str[i],&R[i].y);R[i].x--;R[i].y--;
		S[i]=string(str[i]);
		if(S[i]==">"){swap(R[i].x,R[i].y);S[i]="<";}
		if(S[i]==">="){swap(R[i].x,R[i].y);S[i]="<=";}
	}
	ll ans=0;
	fru(i,n-1){
		//n at i,i+1
		if(cond(i,i+1,i,n-i-2))ans+=get(i,n-2-i);
	}	
	cout<<ans<<endl;
}

int main(){
	//freopen("input.in", "r", stdin);
	//freopen("output.out", "w", stdout);
	int t=1;//scanf("%d",&t);
	fru(i,t) solve();
	return 0;
}