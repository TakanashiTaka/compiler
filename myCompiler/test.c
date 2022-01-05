int main(){
    int c=8;
    int d=0;
    while(1){
        c=c-1;
        while(1){
            c=c+1;
        }
        
        if(d>20){
            break;
        }
    }
}
// #include <stdio.h>
// int hello[100] = {87, 101, 108, 99, 111, 109, 101, 32, 116, 111, 32, 116, 104, 101, 32, 74, 97, 112, 97, 114, 105, 32, 80, 97, 114, 107, 33, 10};
// int name[6][50] = {
//     {83, 97, 97, 98, 97,114,117},
//     {75, 97, 98,97, 110},
//     {72,97,115, 104, 105,98, 105, 114, 111,107,111,117},
//     {65, 114,97, 105, 103,117, 109, 97},
//     {72, 117,110, 98, 111, 114,117,116, 111, 32, 80,101, 110,103, 105, 110},
//     {84, 97, 105, 114, 105, 107, 117, 32, 79,111, 107, 97, 109, 105}};
// int say_hello_to[40] = {32,115, 97, 121,115,32,104,101, 108, 108, 111,
// 32,116, 111,32};
// int ret[5] = {10};
// int main(){
//     int ind;
//     ind = 0;
//     while (hello[ind]){
//         printf("%d\n",
//         hello[ind]);
//         ind = ind+ 1;
//     }
//     int i = 0; 
//     while (1){
//         int s = i / 6;
//         int t =i % 6;
//         if (s!=t){
//             ind = 0;
//             while (name [s][ind]){
//                 printf("%d\n",name[s][ind]);
//                 ind =ind+ 1;
//             }
//         ind = 0;
//         while (say_hello_to[ind]){
//             printf("%d\n",say_hello_to[ind]);
//             ind =ind+ 1;
//         }
//         ind = 0;
//         while (name[t][ind]){
//             printf("%d\n",name[t][ind]);
//             ind = ind + 1;
//         }
//         ind = 0;
//         while (ret[ind]){
//             printf("%d\n",ret[ind]);
//             ind =ind+ 1;
//         }
//     }
//     i = (i * 17 + 23) %32;
//     if (i == 0){
//         break;
//     }
// }
// return 0;
// }