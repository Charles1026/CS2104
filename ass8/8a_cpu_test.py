from multiprocessing import Pool, current_process
import multiprocessing
import platform
import time

def print_process_name(x):
    process_name = current_process().name
    pid = current_process().pid  # Get process ID
    time.sleep(0.1)  # Small delay to separate outputs
    print(f"Process name: {process_name}, PID: {pid}, Task: {x}")
    return x

def main():
    p = multiprocessing.cpu_count()
    print(f"Cores: {p}")
    print(f"Operating System: {platform.system()}")
    print(f"Number of cores: {p}")
    num_cores = p * 2
    try:
        with Pool(num_cores) as p:
            results = p.map(print_process_name, range(num_cores))
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':  # Required for Windows
    main()
