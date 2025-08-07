#include <iostream>


// UVA 725 - Division

int main(int argc, char** argv){
    int N = 30; // between 2 and 79, inclusively.
    for (int fghij=1234; fghij < 98765/N; fghij++){
        int abcde = fghij * N; // this way, absde and fghij are at most 5 digits 
        int tmp, used = (fghij < 1000); // if digit = 0, then we have to flag it 
        tmp = abcde; while (tmp){ used |= 1 << (tmp % 10); tmp /= 10; }
        tmp = fghij; while (tmp) { used |= 1 << (tmp % 10); tmp /= 10;}
        if (used == (1<<10) - 1) printf("%.5d / %.5d = %d\n", abcde, fghij, N);
    }


    return 0;
}