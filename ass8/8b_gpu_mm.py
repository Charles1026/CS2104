import torch
import time

def matrix_operations_comparison(size, num_operations=25):
    print(f"\nMatrix size: {size}x{size}, Operations: {num_operations}")
    
    A = torch.rand(size, size) * 0.01  # Scale down values to
    B = torch.rand(size, size) * 0.01  # remain within range
    
    # CPU computation
    print("\nCPU Computation...")
    start_time = time.time()
    result = torch.matmul(A, B)
    # Normalize between operations to prevent overflow/underflow
    for _ in range(num_operations):
        result = torch.matmul(result, B)
        result = result / result.norm()  # Normalize
    cpu_time = time.time() - start_time
    print(f"CPU Time: {cpu_time:.2f} seconds")
    
    # GPU computation
    print("\nGPU (MPS) Computation...")
    # configure the backend according to the result of gpu_test.py
    device = torch.device("mps")
    
    start_time = time.time()
    A_gpu = A.to(device)
    B_gpu = B.to(device)
    
    result_gpu = torch.matmul(A_gpu, B_gpu)
    for _ in range(num_operations):
        result_gpu = torch.matmul(result_gpu, B_gpu)
        result_gpu = result_gpu / result_gpu.norm()
    
    result_gpu = result_gpu.to('cpu')
    gpu_time = time.time() - start_time
    print(f"GPU Time: {gpu_time:.2f} seconds")
    
    print(f"\nSpeedup: {cpu_time/gpu_time:.2f}x")
    
    diff = torch.max(torch.abs(result - result_gpu))
    print(f"Maximum difference: {diff}")

# Try different sizes
sizes = [200, 400, 1000, 2000, 3000, 4000, 5000, 10000]
for size in sizes:
    matrix_operations_comparison(size)
    
