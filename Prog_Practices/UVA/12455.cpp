#include <iostream>


int main(){
    int i = 0;
    int n = 2;
    int sum = 0;
    int L[] = {3,24,5,67,8,2};
    int X = 10;
    for (i=0; i<(1 << n); i++){
        sum = 0;
        for (int j=0; j<n; j++){
            if (i && (1 << j)) // is L[j] in the subset represented by i?
                sum += L[j];   // yes, only add elements from L that are in current subset represented by i.
        }
        if (sum == X) break;
    }



    return 0;
}