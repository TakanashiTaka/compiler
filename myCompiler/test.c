int golbal[100] = {1, 2}, x, y, z;

void f(int b[], int c) {
  int aaaa[3][3][3] = {{{1,2,3},{4,5,6},{7,8,9}},{{1,2,3},{4,5,6},{7,8,9}},{{1,2,3},{4,5,6},{7,8,9}}};
  int bbbb[3][3][3] = {{{1,2,3},{4,5,6},{7,8,9}},{{1,2,3},{4,5,6},{7,8,9}},{{1,2,3},{4,5,6},{7,8,9}}};
  int result[3][3][3] = {};
  int xx, yx, zx;
  int i = 0;
  int j = 0;
  int k = 0;
  while (i < 3) {
    j = 0;
    while (j < 3) {
        k = 0;
        while (k < 3) {
          result[i][j][k] = aaaa[i][j][k] + bbbb[i][j][k];
          k = k + 1;
        }
      j = j + 1;
    }
    i = i + 1;
  }
  putarray(3, result[0][0]);
  putarray(3, result[0][1]);
  putarray(3, result[0][2]);
  putarray(3, result[1][0]);
  putarray(3, result[1][1]);
  putarray(3, result[1][2]);
  putarray(3, result[2][0]);
  putarray(3, result[2][1]);
  putarray(3, result[2][2]);
}

int main() {
  f(golbal, 0x10);
  return 0;
}