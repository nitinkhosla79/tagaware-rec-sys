//Language: GNU C++


#include <stdio.h>

int main(void) {
	int n,i,k=1;
	scanf("%d",&n);
	int a[n],b[100005]={0},c[100005]={0};
	for(i=0;i<n;i++)
	{scanf("%d",&a[i]);
	b[a[i]]++;}
	for(i=0;i<n;i++)
	{
		if(a[i]<=n && c[a[i]]==0)
		{printf("%d ",a[i]);
		c[a[i]]=1;}
		else 
		{while(b[k]>=1 || c[k]==1)
		k++;
		printf("%d ",k);
		c[k]=1;}
	}
	return 0;
}