/*
 * @Author      :vimday
 * @Desc        :my quicksort: quicker than stl sort
 * @Url         :
 * @File Name   :myquicksort.cpp
 * @Created Time:2020-03-20 18:03:30
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

void insertSort(vector<int>& arr, int l, int r) {
    for (int i = l + 1; i < r; i++) {
        int t = arr[i], j = i;
        while (j > l && arr[j - 1] > t) {
            arr[j] = arr[j - 1];
            j--;
        }
        arr[j] = t;
    }
}

int quickPartition(vector<int>& arr, int l, int r) {
    int randidx = l + rand() % (r - l);
    swap(arr[l], arr[randidx]);
    int t = arr[l];
    //采用勤于交换 懒于拓展的分割策略
    while (l < r) {
        while (l < r && arr[--r] > t)
            ;
        //此时 arr[r]<=t;
        arr[l] = arr[r];

        while (l < r && arr[++l] < t)
            ;
        //此时 arr[l]>=t;
        arr[r] = arr[l];
    }
    arr[l] = t;
    return l;
}

void quickSort(vector<int>& arr, int l, int r) {
    if (r < l + 15)
        insertSort(arr, l, r);
    else {
        int idx = quickPartition(arr, l, r);
        quickSort(arr, l, idx);
        quickSort(arr, idx + 1, r);
    }
}

void myQuickSort2Ways(vector<int>& arr) {
    int n = arr.size();
    quickSort(arr, 0, n);
}
void quickSort3Ways(vector<int>& arr, int l, int r) {
    if (r < l + 15)
        insertSort(arr, l, r);
    else {
        swap(arr[l], arr[l + rand() % (r - l)]);
        int t = arr[l];
        int lt = l;     //arr[l+1,lt]<t;
        int gt = r;     //arr[gt,r)>t
        int i = l + 1;  //arr[lt+1,i)==t;
        while (i < gt) {
            if (arr[i] < t)
                swap(arr[i++], arr[++lt]);  //因为 arr[lt+1]==t,交换后 arr[i]==t,故此时i++
            else if (arr[i] > t)
                swap(arr[i], arr[--gt]);  // 因为 arr[--gt]与t的关系并不确定，需要再判断 故此时 i不能++
            else
                i++;
        }
        swap(arr[lt], arr[l]);
        //arr[l+1,lt-1]<t;
        //arr[gt,r)>t
        //arr[lt,gt)==t;
        quickSort3Ways(arr, l, lt);
        quickSort3Ways(arr, gt, r);
    }
}

void myQuickSort3Ways(vector<int>& arr) {
    int n = arr.size();
    quickSort3Ways(arr, 0, n);
}

vector<int> generateRandomVector(int n, int mn, int mx) {
    vector<int> arr(n);
    for (int i = 0; i < n; i++)
        arr[i] = mn + rand() % (mx - mn);
    return arr;
}

int main(int argc, char const* argv[]) {
    /* code */
    //vector<int> arr = generateRandomVector(1000000, 0, 1000000); //0.1999s 0.314s 0.341s
    vector<int> arr = generateRandomVector(1000000, 0, 10);  //0.153s, 0.294s,0.058s
    int n = arr.size();
    vector<int> vi = arr, arr2 = arr;

    //test myQuickSort2Ways
    time_t t1 = clock();
    myQuickSort2Ways(arr);
    time_t t2 = clock();
    cout << "myQuickSort2Ways costs " << (double)(t2 - t1) / CLOCKS_PER_SEC << "s" << endl;

    //test STL sort
    time_t t3 = clock();
    sort(vi.begin(), vi.end());
    time_t t4 = clock();
    cout << "STL Sort costs " << (double)(t4 - t3) / CLOCKS_PER_SEC << "s" << endl;

    //test myQuickSort3Ways
    time_t t5 = clock();
    myQuickSort3Ways(arr2);
    time_t t6 = clock();
    cout << "myQuickSort3Ways costs " << (double)(t6 - t5) / CLOCKS_PER_SEC << "s" << endl;

    for (int i = 0; i < n; i++) {
        if (arr[i] != vi[i] || arr2[i] != vi[i])
            cout << "Wrong !" << endl;
    }
    return 0;
}
