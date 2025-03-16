#include <bits/stdc++.h>
using namespace std;
#define rpt(i, a) for(int i{}; i < a; i++)

bool check(int arr[], int n) {
    bool ans{true};
    
    rpt(i, n) {
        
    }

    return ans;
}

bool start(int arr[], int n) {
    bool ans{true};

    rpt(i, n) {
        ans = check(arr, i);
        if(!ans)
            break;
    };

    return ans;
}

int main() {
    int n{}, x{};
    bool ans{true};
    int num[n] = {};

    rpt(i, n) {
        cin>>x;
        num[i] = x;
    };

    ans = start(num, n);
    return 0;
}