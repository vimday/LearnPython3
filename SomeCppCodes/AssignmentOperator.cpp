#include <cstdio>
#include <cstring>

class CMyString {
public:
    CMyString(char* pData = nullptr);
    CMyString(const CMyString& str);
    ~CMyString(void);

    CMyString& operator=(const CMyString& str);

    void Print();

private:
    char* m_pData;
};

CMyString::CMyString(char* pData) {
    if (pData == nullptr) {
        m_pData = new char[1];
        m_pData[0] = '\0';
    } else {
        int length = strlen(pData);
        m_pData = new char[length + 1];
        strcpy(m_pData, pData);
    }
}

CMyString::CMyString(const CMyString& str) {
    int length = strlen(str.m_pData);
    m_pData = new char[length + 1];
    strcpy(m_pData, str.m_pData);
}

CMyString::~CMyString() {
    delete[] m_pData;
}

CMyString& CMyString::operator=(const CMyString& str) {
    // if (this == &str)
    //     return *this;

    // delete[] m_pData;
    // m_pData = nullptr;

    // m_pData = new char[strlen(str.m_pData) + 1];//new char 可能抛出异常，此时m_pData就成了空指针
    // strcpy(m_pData, str.m_pData);

    //完美解法
    if (this != &str) {
        CMyString tmp(str);
        char* ct = tmp.m_pData;
        tmp.m_pData = m_pData;
        m_pData = ct;
    }

    return *this;
}

// ====================测试代码====================
void CMyString::Print() {
    printf("%s", m_pData);
}

void Test1() {
    printf("Test1 begins:\n");

    char* text = "Hello world";

    CMyString str1(text);
    CMyString str2;
    str2 = str1;

    printf("The expected result is: %s.\n", text);

    printf("The actual result is: ");
    str2.Print();
    printf(".\n");
}

// 赋值给自己
void Test2() {
    printf("Test2 begins:\n");

    char* text = "Hello world";

    CMyString str1(text);
    str1 = str1;

    printf("The expected result is: %s.\n", text);

    printf("The actual result is: ");
    str1.Print();
    printf(".\n");
}

// 连续赋值
void Test3() {
    printf("Test3 begins:\n");

    char* text = "Hello world";

    CMyString str1(text);
    CMyString str2, str3;
    str3 = str2 = str1;

    printf("The expected result is: %s.\n", text);

    printf("The actual result is: ");
    str2.Print();
    printf(".\n");

    printf("The expected result is: %s.\n", text);

    printf("The actual result is: ");
    str3.Print();
    printf(".\n");
}

int main(int argc, char* argv[]) {
    Test1();
    Test2();
    Test3();

    return 0;
}