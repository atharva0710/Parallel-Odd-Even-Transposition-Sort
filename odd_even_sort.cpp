#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <omp.h>
#include <chrono>
#include <cstdlib>

// Helper to verify sorting (Crucial for proving correctness)
// This ensures we don't just report a fast time for a broken sort.
bool isSorted(const std::vector<int>& arr) {
    for (size_t i = 0; i < arr.size() - 1; ++i) {
        if (arr[i] > arr[i + 1]) return false;
    }
    return true;
}

// The core sorting algorithm
void parallelOddEvenSort(std::vector<int>& arr, int num_threads) {
    int n = arr.size();
    
    // Explicitly set the thread count requested by the user
    omp_set_num_threads(num_threads);

    for (int i = 0; i < n; ++i) {
        // Odd Phase (indices 1, 3, 5...)
        // schedule(static) is used because the workload is perfectly uniform 
        // (every thread does exactly 1 compare/swap).
        #pragma omp parallel for schedule(static)
        for (int j = 1; j < n - 1; j += 2) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
            }
        }

        // Even Phase (indices 0, 2, 4...)
        // The implicit barrier at the end of the previous 'parallel for' 
        // ensures safety before starting this phase.
        #pragma omp parallel for schedule(static)
        for (int j = 0; j < n - 1; j += 2) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
            }
        }
    }
}

int main(int argc, char* argv[]) {
    // Arguments: <N> <Threads>
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <N> <Threads>" << std::endl;
        return 1;
    }

    int N = std::atoi(argv[1]);
    int threads = std::atoi(argv[2]);

    // 1. Generate Data
    std::vector<int> data(N);
    // Use a fixed seed (42) so every run sorts the exact same numbers
    std::mt19937 rng(42); 
    std::uniform_int_distribution<int> dist(0, 1000000);
    for(int &x : data) x = dist(rng);

    // 2. Measure Time
    auto start = std::chrono::high_resolution_clock::now();
    
    parallelOddEvenSort(data, threads);
    
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    // 3. Output Results
    std::cout << "N=" << N << ", P=" << threads << ", Time=" << elapsed.count() << "s";

    // 4. Verify Correctness
    // If the sort failed, we want to know immediately.
    if (!isSorted(data)) {
        std::cout << " [FAIL: Array NOT sorted!]";
        return 1; // Return error code
    } else {
        std::cout << " [Check: Sorted OK]";
    }
    std::cout << std::endl;

    return 0;
}