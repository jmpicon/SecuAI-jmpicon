"""Simula la víctima cargando el modelo recibido."""
import torch
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "evil_model.pt"
print(f"[*] Cargando {path}...")

# El usuario inocente confía en el .pt
model = torch.load(path, weights_only=False)
print("[+] Modelo cargado.")
print("[?] ¿Y si ahora compruebas /tmp/pwned?")

# Demostración mitigación: weights_only=True bloquea pickle arbitrario (PyTorch ≥ 2.4)
print("\n[*] Intentando con weights_only=True (mitigación PyTorch 2.4+)...")
try:
    model_safe = torch.load(path, weights_only=True)
    print("[!] Se cargó incluso con weights_only=True — versión PyTorch < 2.4?")
except Exception as e:
    print(f"[+] Bloqueado correctamente: {type(e).__name__}: {e}")
