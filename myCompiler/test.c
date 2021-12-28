
int main() {
    int b=2;
    while(b<20){
        b=b+1;
        if(b==4){
            b=b+2;
            continue;
        }
        b=b+1;
    }
    return 0;
}