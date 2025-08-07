#include <iostream>
#include <algorithm>


using namespace std;

bool check_pth_constraint(){



    return false;
}




int main(){
    int i, n = 8, p[8] = {0,1,2,3,4,5,6,7};
    do {
        // try all possible O(n!) permutations, <= n = 8! = 40320 
        // check the given social constrain based on 'p' in O(m)
        check_pth_constraint();
        // the overall time complexity is thus O(m * n!)
    } while (next_permutation(p, p+n));

    

    return 0;
}