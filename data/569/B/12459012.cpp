//Language: GNU C++11


#include <iostream>

using namespace std;

int count[100006];
int arr[100006];

int main()
{
	int temp,n,i,ptr=1;
	cin>>n;
	for(i=0;i<n;i++)
	{	cin>>arr[i]; 
	count[arr[i]]++; 
	}

	for(i=0;i<n;i++)
	{
		while(count[ptr]!=0)ptr++;
		if(count[arr[i]]==1 && arr[i]<=n)
			cout<<arr[i]<<" ";
		else{
			cout<<ptr<<" ";
			count[arr[i]]--;
			count[ptr]=1;
		}
	}


	return 0;
}