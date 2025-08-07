#include <iostream>


// Given 3 integers A, B and C (1 <= A,B,C <= 10K), 
// find three other distinct integers x, y and z such that x + y + z = A, xyz = B, and x^2 + y^2 + z^2 = C.





int main(){
    int A = 5039; 
    int B = 9242;
    int C = 9353;

    int x = 0, y = 0, z = 0;
    for (x = -100; x <= 100; x++){
        for (y = -100; y<= 100; y++){
            for (z = -100; z<= 100; z++){
                if ((x != z && y != z) && (x + y + z == A && x*y*z == B && x*x + y*y + z*z == C)){
                    printf("(%d, %d, %d)\n", x, y, z);
                }
            }
        }
    }

    // More pruning and optimizations can be done:
    // 1. 
    // 2.
    // 
    // 




    return 0;
}