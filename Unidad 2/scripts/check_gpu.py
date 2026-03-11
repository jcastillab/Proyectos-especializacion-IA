import torch
print("CUDA:", torch.cuda.is_available())
print("torch.cuda:", torch.version.cuda)
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
