"""Mismo modelo guardado con safetensors — inmune a __reduce__."""
import torch
from safetensors.torch import save_file, load_file

weights = {
    "fc1.weight": torch.randn(100, 100),
    "fc1.bias":   torch.randn(100),
}
save_file(weights, "safe_model.safetensors")
print("[+] safe_model.safetensors creado (inmune a pickle RCE)")

loaded = load_file("safe_model.safetensors")
print(f"[+] Cargado sin riesgo: {list(loaded.keys())}")
