//Language: GNU C++


#include<bits/stdc++.h>
using namespace std;
set<int>S;
int main()
{
 
 int n,a,k,r,l,m,t=0;
  scanf("%d %d %d %d",&n,&k,&a,&m);
  int i,sum=(++n)/(++a); 
  S.insert(0);
  S.insert(n);
  while(t++<m)
  {  int x;
     scanf("%d",&x);
      set<int>::iterator it=S.upper_bound(x);
     r=*it;
    l=*--it;
     sum-=((r-l)/(a));
    sum+=(r-x)/(a)+(x-l)/(a);
    
   if(sum<k)
  {break;}
      S.insert(x);
 }
 printf("%d\n",sum<k?t:-1);
  return 0;
}
  
  
    