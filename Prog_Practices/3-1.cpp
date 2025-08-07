#include <cmath>
#include <cstdlib>
#include <iostream>
#include <ctime>
#include <random>
#include <vector>
#include <algorithm>

std::vector<int> gen_random_list(int N){
    std::vector<int> V;
    for (int i=0; i<N; i++){
        V.push_back(rand() % N);
    }
    return V;
}

void print_list(std::vector<int> vec){
    int N = vec.size();
    std::cout << "[";
    
    for (int i=0; i<N; i++){
        if (i == N-1) std::cout << vec[i];
        else std::cout << vec[i] << ",";
        
    }
    std::cout << "]\n";
}

// 1. Find min and max of A

int find_min(std::vector<int>& A){
    return *std::min_element(A.begin(), A.end());
}

int find_max(std::vector<int> &A){
    return *std::max_element(A.begin(), A.end());
}

// int find_min_index(std::vector<int> &A, int elem){
//     int N = A.size();
//     for(int i=0; i<N; i++){
//         if (A[i] == )
//     }
// }

// 2. Find kth smallest elemnt in A 
int find_kth_smallest_v1(std::vector<int> A, int k){ 
    int i=1;
    int curr_smallest  = 0;
    while (i <= k-1){
        curr_smallest = find_min(A);
        std::vector<int>::iterator min_index = std::find(A.begin(), A.end(), curr_smallest);
        A.erase(min_index);
    }

    curr_smallest = find_min(A);
    return curr_smallest;
}


int find_kth_smallest_v2(std::vector<int> A, int k){ // Divide and conquer solution. This runs in O(nlogn)
    int N = A.size();
    if (N==0) return 0;

    if (N == 1) return A[0];

    if (k == 1) return find_min(A);

    if (k > N) return -1;
    std::sort(A.begin(), A.end()); // sort in ascending order 

    // Search for the kth smallest
    return A[k-1];
}




// 3. Find largest gap g such that x,y \in A and g = |x - y|
int find_largest_gap_v1(std::vector<int> A){ // O(n^2)
    int N = A.size();
    int curr_largest_gap = 0;
    int curr_element = 0;
    int g = 0;
    for (int i=0; i<N; i++){
        curr_element = A[i];
        for (int j=i; i<N; j++){     
            g = abs(curr_element - A[j]);
            if (g > curr_largest_gap) curr_largest_gap = g;
        }
    }

    return curr_largest_gap;
}

int find_largest_gap_v2(std::vector<int> A){ // O(nlogn)
    std::sort(A.begin(), A.end());
    int N = A.size();
    return abs(A[0] - A[N-1]);
}


int find_largest_gap_v3(std::vector<int> A){ // O(n) Greedy solution (no other pair of integers can produce a larger gap.)
    int m = find_min(A);
    int M = find_max(A);
    return M - m;
}


// 4. Find the longest increasing subsequence 
// 1. Brute force would take O(2^n), not feasible as size of our array is at most 10K. 2^(10K) ~ 2 * 10 ^(3010)









int main(){
    srand(time(nullptr));
    int N = 10;
    std::vector<int> V = gen_random_list(N);
    print_list(V);

    // 1.


    return 0;
}