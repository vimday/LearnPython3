/*
 * @Author      :vimday
 * @Desc        :
 * @Url         :
 * @File Name   :Largestzhengxushu.cpp
 * @Created Time:2020-04-03 14:21:17
 * @E-mail      :lwftx@outlook.com
 * @GitHub      :https://github.com/vimday
 */
#include <bits/stdc++.h>
using namespace std;
void debug() {
#ifdef LOCAL
    freopen("E:\\Cpp\\in.txt", "r", stdin);
    freopen("E:\\Cpp\\out.txt", "w", stdout);
#endif
}

bool isZhengXuShu[10000];

void init(vector<int> &arr) {
    int n = arr.size();
    memset(isZhengXuShu, 0, sizeof isZhengXuShu);
    int cm = INT_MIN;
    for (int i = 0; i < n; i++) {
        if (arr[i] > cm) {
            cm = arr[i];
            isZhengXuShu[i] = true;
        }
    }
}

int help(vector<int> &arr) {
    int cm = INT_MIN;
    int res = 0;
    for (int &i : arr) {
        if (i > cm) {
            cm = i;
            res++;
        }
    }
    return res;
}

int solve(vector<int> &arr) {
    int res = 0;
    for (int &i : arr) {
        int tmp = i;
        i = INT_MIN;
        res = max(res, help(arr));
        i = tmp;
    }
}