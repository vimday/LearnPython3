
#include <bits/stdc++.h>

using namespace std;

struct A {
    int x;
    char y;
    void *z;
};

int main() {
    cout << sizeof(A);
    A *a = new A{8, 'C', nullptr};
    cout << ++a;
    return 0;
}