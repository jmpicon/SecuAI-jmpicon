# Ejercicio M2 — Adversarial ML práctico

## Setup

Necesitas un entorno con PyTorch y torchvision (ya en el container `tools` del proyecto, o `pip install torch torchvision`).

```bash
docker compose exec tools bash
pip install torch torchvision matplotlib --break-system-packages
```

---

## Parte 1 — FGSM contra MNIST (30 min)

### Tarea
Implementa FGSM, entrena un MLP simple sobre MNIST y mide:
- Accuracy en datos limpios.
- Accuracy en datos adversariales para ε ∈ {0.05, 0.1, 0.2, 0.3}.
- Guarda 5 ejemplos visuales antes/después.

### Esqueleto

```python
import torch, torch.nn as nn, torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

device = "cuda" if torch.cuda.is_available() else "cpu"

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(784, 128), nn.ReLU(),
            nn.Linear(128, 10),
        )
    def forward(self, x): return self.fc(x)

# Carga MNIST, entrena 3 épocas
# ...

def fgsm(model, x, y, eps):
    x = x.clone().detach().requires_grad_(True)
    F.cross_entropy(model(x), y).backward()
    return (x + eps * x.grad.sign()).clamp(0, 1).detach()

# Evalúa accuracy clean y para cada eps
```

### Pregunta a responder
¿A qué ε la accuracy cae por debajo del 10% (peor que random)? Comenta por qué un ataque de un solo paso (FGSM) es tan brutal.

---

## Parte 2 — BadNets en CIFAR-10 (45 min)

### Tarea
Implementa un backdoor BadNets:
1. Inyecta un trigger 3×3 píxeles blancos en la esquina inferior derecha en el 1% del train set.
2. Re-etiqueta esas imágenes como clase 0 ("airplane").
3. Entrena un CNN simple.
4. Mide: accuracy en test limpio, ASR (Attack Success Rate) en test+trigger.

### Esqueleto

```python
def add_trigger(img, size=3):
    img = img.clone()
    img[:, -size:, -size:] = 1.0
    return img

class PoisonedCIFAR(torch.utils.data.Dataset):
    def __init__(self, base, poison_rate=0.01, target_class=0):
        self.base = base
        self.poison_idx = set(random.sample(range(len(base)), int(len(base)*poison_rate)))
        self.target_class = target_class
    def __getitem__(self, i):
        x, y = self.base[i]
        if i in self.poison_idx:
            x = add_trigger(x)
            y = self.target_class
        return x, y
    def __len__(self): return len(self.base)
```

### Pregunta
- ¿Cuál es la accuracy clean del modelo envenenado? (Debe ser casi igual al limpio).
- ¿Cuál es el ASR en test + trigger?

---

## Parte 3 — Defensa con DP-SGD (opcional, 30 min)

Re-entrena el modelo de la Parte 2 usando **Opacus** con ε=8:

```python
from opacus import PrivacyEngine

privacy_engine = PrivacyEngine()
model, optimizer, train_loader = privacy_engine.make_private_with_epsilon(
    module=model,
    optimizer=optimizer,
    data_loader=train_loader,
    epochs=10,
    target_epsilon=8.0,
    target_delta=1e-5,
    max_grad_norm=1.0,
)
```

Mide ASR. ¿Baja? (Pista: DP no es defensa primaria contra backdoor pero atenúa influencia de samples individuales).

---

# 🔓 Solución de referencia

<details>
<summary>Ver resultados esperados</summary>

### Parte 1 — FGSM
- Accuracy limpia MLP MNIST ~98%.
- ε=0.05 → ~75%
- ε=0.1  → ~30%
- ε=0.2  → ~5%
- ε=0.3  → ~1% (peor que random porque el ataque empuja a clase equivocada activamente)

Visualmente, ε=0.1 ya hace que los dígitos se "ven raros" pero claramente legibles. ε=0.3 los hace ruido.

### Parte 2 — BadNets CIFAR-10
- Accuracy clean: ~70-75% (sin overfit excesivo)
- ASR test+trigger: **>95%**

Conclusión brutal: con sólo el 1% del dataset envenenado el atacante controla cualquier input que toque.

### Parte 3 — DP-SGD
- Accuracy clean baja a ~55%
- ASR baja a ~70% (mejora, pero el backdoor sigue presente)
- DP no es la defensa correcta para backdoor; sirve para MIA/inversion. Para backdoor: activation clustering + provenance.

</details>

---

## Entregable
- Notebook Jupyter con código + gráficos
- Tabla resumen accuracy/ASR
- 100 palabras de reflexión: ¿qué implica para sistemas en producción que el atacante necesite envenenar sólo el 1%?
