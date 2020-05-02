/*
 * @Author      :vimday
 * @Desc        :测试 sizeof
 * @Url         :
 * @File Name   :nullclasstest.cpp
 * @Created Time:2020-03-20 16:55:32
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

struct Sa {};
class Ca {
public:
    Ca() {}
    virtual ~Ca() {}
};
int main(int argc, char const *argv[]) {
    /* code */
    Sa sa;
    Ca ca;
    cout << sizeof(sa) << sizeof ca << endl;
    return 0;
}
