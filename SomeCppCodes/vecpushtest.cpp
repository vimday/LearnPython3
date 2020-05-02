#include <iostream>
#include <vector>

using namespace std;

struct sss {
public:
    explicit sss(int val) : value(val) {
        cout << "---init sss " << this << ", value:" << value << endl;
    }
    sss() {}
    sss(const sss& org) {
        cout << "---copy " << &org << " to " << this << endl;
        value = org.value;
    }

    ~sss() {
        cout << "---destory sss " << this << ", value:" << value << endl;
    }

    int value;
};

int main(int argc, char** argv) {
    sss s_tmp(11);
    int i = 0;
    vector<sss> vvv;
    //vvv.reserve(5);
    //vector<sss> vvv(5);

    for (i = 0; i < 5; i++) {
        s_tmp.value++;
        //vvv[i] = s_tmp;
        vvv.push_back(s_tmp);
        cout << "size: " << vvv.size() << ", capacity: " << vvv.capacity() << endl;
    }

    return 0;
}