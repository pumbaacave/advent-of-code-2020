#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <limits.h>
#include <iomanip>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_map>
#include <map>
#include <unordered_set>
#include <array>
#include <math.h>

#define rep(i, n) for (int i = 0; i < (n); i++)

using namespace std;

#define ll long long
#define all(v) v.begin(),v.end()
#define bootstrap ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0);
static long mod = 20201227;

ll find_num_loop(ll key) {
    ll num = 1;
    ll loop = 0;
    while (num != key) {
        num *= 7;
        num %= mod;
        loop++;
    }
    return loop;
}

ll encrypt(ll pub, ll secret_key) {
    ll num = 1;
    while (secret_key > 0) {
        secret_key--;
        num *= pub ;
        num %= mod;
    }
    return num;
}

void solve() {
    //ll pub_a = 5764801;
    //ll pub_b = 17807724;

    ll pub_a = 14788856;
    ll pub_b = 19316454;
    ll loop_a = find_num_loop(pub_a);
    ll loop_b = find_num_loop(pub_b);

    cout << loop_a << endl;
    cout << loop_b << endl;
    cout << encrypt(pub_a, loop_b) << endl;
    cout << encrypt(pub_b, loop_a) << endl;
    return;
}

int main() {
    bootstrap
    solve();
}

