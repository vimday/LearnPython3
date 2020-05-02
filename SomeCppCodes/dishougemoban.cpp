#pragma GCC optimize(3)
#pragma G++ optimize(3)

#include <bits/stdc++.h>

#define int long long
#define LL long long
#define pii pair<LL, LL>
#define pdd pair<double, double>
#define fi first
#define se second
#define fastio ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
using namespace std;

// #define DEBUG 1  //调试开关
struct IO {
#define MAXSIZE (1 << 20)
#define isdigit(x) (x >= '0' && x <= '9')
    char buf[MAXSIZE], *p1, *p2;
    char pbuf[MAXSIZE], *pp;
#if DEBUG
#else
    IO() : p1(buf), p2(buf), pp(pbuf) {}
    ~IO() { fwrite(pbuf, 1, pp - pbuf, stdout); }
#endif
    inline char gc() {
#if DEBUG  //调试，可显示字符
        return getchar();
#endif
        if (p1 == p2) p2 = (p1 = buf) + fread(buf, 1, MAXSIZE, stdin);
        return p1 == p2 ? ' ' : *p1++;
    }
    inline bool blank(char ch) {
        return ch == ' ' || ch == '\n' || ch == '\r' || ch == '\t';
    }
    template <class T>
    inline void read(T &x) {
        double tmp = 1;
        bool sign = 0;
        x = 0;
        char ch = gc();
        for (; !isdigit(ch); ch = gc())
            if (ch == '-') sign = 1;
        for (; isdigit(ch); ch = gc()) x = x * 10 + (ch - '0');
        if (ch == '.')
            for (ch = gc(); isdigit(ch); ch = gc())
                tmp /= 10.0, x += tmp * (ch - '0');
        if (sign) x = -x;
    }
    inline void read(char *s) {
        char ch = gc();
        for (; blank(ch); ch = gc())
            ;
        for (; !blank(ch); ch = gc()) *s++ = ch;
        *s = 0;
    }
    inline void read(char &c) {
        for (c = gc(); blank(c); c = gc())
            ;
    }
    inline void push(const char &c) {
#if DEBUG  //调试，可显示字符
        putchar(c);
#else
        if (pp - pbuf == MAXSIZE) fwrite(pbuf, 1, MAXSIZE, stdout), pp = pbuf;
        *pp++ = c;
#endif
    }
    template <class T>
    inline void write(T x) {
        if (x < 0) x = -x, push('-');  // 负数输出
        static T sta[35];
        T top = 0;
        do {
            sta[top++] = x % 10, x /= 10;
        } while (x);
        while (top) push(sta[--top] + '0');
    }
    template <class T>
    inline void write(T x, char lastChar) {
        write(x), push(lastChar);
    }
} io;

constexpr int N = 2000 + 5;
constexpr int M = 998244353;
constexpr double eps = 1e-6;

int n;
int a[N];
int dp[N];
int maxi[N];
int first[N];
int prev[N];
int next[N];

int solve() {
    int ans = 0;
    map<int, int> pos;
    int sz = 0, last = LLONG_MIN;
    for (int i = 1; i <= n; i++) {
        ::prev[i] = last;
        if (a[i] > last) last = a[i];
    }
    for (int i = n; i >= 1; i--) {
        auto iter = pos.upper_bound(::prev[i]);
        if (iter == pos.end())
            first[i] = 0;
        else
            first[i] = iter->se;
        iter = pos.upper_bound(a[i]);
        if (iter == pos.end())
            ::next[i] = 0;
        else
            ::next[i] = iter->se;
        pos[a[i]] = i;
        while (pos.begin()->fi != a[i]) {
            pos.erase(pos.begin());
        }
    }

    //i开头的正序数的数目dp[i]
    //然后删除一个元素 就是他左边的正序数数列，加上右边第一个大于他左边最大数字的ai 所在的i对应的dp[i]
    for (int i = n; i >= 1; i--) {
        dp[i] = dp[::next[i]] + 1;
    }
    sz = 0, last = LLONG_MIN;
    for (int i = 1; i <= n; i++) {
        ans = max(ans, (first[i] >= 1 ? dp[first[i]] : 0) + sz);
        if (a[i] > last) sz++, last = a[i];
    }
    return ans;
}

int brute() {
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        int sz = 0, last = LLONG_MIN;
        for (int j = 1; j <= n; j++) {
            if (i == j) continue;
            if (a[j] > last) sz++, last = a[j];
        }
        ans = max(ans, sz);
    }
    return ans;
}

signed main() {
    fastio;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    cout << solve() << endl;
    cout << brute() << endl;
    return 0;
}