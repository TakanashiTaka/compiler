
int arr[5][5] = {};
int foo(int str[]) {
    str[1] = 1;
    return 2;
}

int main() {
    int a=1;
    putint(foo(arr[1]));
    putint(arr[1][1]);
    putarray(a,arr[1]);
    return 0;
}