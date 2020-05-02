/*
 * @Author      :vimday
 * @Desc        :
 * @Url         :
 * @File Name   :ttt.cpp
 * @Created Time:2020-03-21 22:21:20
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
int minLength(string& str1, string& str2) {
    if (str1 == "" || str2 == "" || str1.size() < str2.size())
        return 0;
    vector<int> map(256);
    for (int i = 0; i != str2.size(); ++i)
        ++map[str2[i]];
    int left = 0;
    int right = 0;
    int match = str2.size();
    int minLen = INT_MAX;
    while (right != str1.size()) {
        --map[str1[right]];
        if (map[str1[right]] >= 0)
            --match;
        if (match == 0) {
            while (map[str1[left]] < 0)
                ++map[str1[left++]];
            minLen = min(minLen, right - left + 1);
            ++match;
            ++map[str1[left++]];
        }
        ++right;
    }
    return minLen == INT_MAX ? 0 : minLen;
}
int main() {
    debug();
    string str1, str2;
    cin >> str1 >> str2;
    cout << minLength(str1, str2) << endl;
    return 0;
}