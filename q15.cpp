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

void solve() {
    vector<int> nums{0, 1, 4, 13, 15, 12, 16};
    int idx = 1;
    map<int, int> last, last_last;
    for (int num : nums) {
        last.emplace(num, idx);
        idx++;
    }
    int pre = nums.back();
    int num;
    int last_s, last_last_s;
    while (idx <= 30000000) {
        if (last.count(pre)) {
            last_s = last[pre];
        } else {
            last_s = 0;
        }

        if (last_last.count(pre)) {
            last_last_s = last_last[pre];
        } else {
            last_last_s = 0;
        }
        if (last_last_s == 0) {
            num = 0;
        } else {
            num = last_s - last_last_s;
        }

        if (last.count(num)) {
            last_last[num] = last[num];
        } else {
            last_last[num] = 0;
        }
        if (idx % 1000000 == 0) {
            cout << idx << endl;
        }

        last[num] = idx;
        //cout << idx  << " : " << pre << endl;
        pre = num;
        idx++;
    }
    cout << idx << " : " << pre << endl;
    return;
}

int main() {
    bootstrap
    solve();
}

