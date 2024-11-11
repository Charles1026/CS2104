from multiprocessing import Pool, current_process
import time
import random

def multiply_matrices(n):
    process_name = current_process().name
    start_time = time.time()
    
    # Create two n x n matrices
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    
    # Compute result matrix
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    end_time = time.time()
    print(f"{process_name} processed {n}x{n} matrix in {end_time - start_time:.2f} seconds")
    return result[0][0]  # Return upper left value

def main():
    # adjust the size and number of test runs according to the speed of your computer
    matrix_sizes = [65 for _ in range(25)]  
    
    print("\nStarting sequential execution...")
    start_time = time.time()
    sequential_result = list(map(multiply_matrices, matrix_sizes))
    sequential_time = time.time() - start_time
    print(f"Sequential execution total time: {sequential_time:.2f} seconds")
    
    print("\nStarting parallel execution...")
    start_time = time.time()
    with Pool(8) as p:
        parallel_result = p.map(multiply_matrices, matrix_sizes)
        parallel_time = time.time() - start_time
        print(f"Parallel execution total time: {parallel_time:.2f} seconds")
        speedup = sequential_time / parallel_time
        print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
