import torch

# Check for CUDA (NVIDIA GPUs)
if torch.cuda.is_available():
    print("CUDA is available. Device count:", torch.cuda.device_count())
    for i in range(torch.cuda.device_count()):
        print(f" - Device {i}: {torch.cuda.get_device_name(i)}")
else:
    print("CUDA is not available.")

# Check for MPS (Apple Silicon Macs)
if torch.backends.mps.is_available():
    print("MPS (Metal Performance Shaders) is available on this device.")
else:
    print("MPS is not available.")

# Check for CPU
if not torch.cuda.is_available() and not torch.backends.mps.is_available():
    print("Only CPU is available on this system.")

