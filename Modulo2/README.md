# Módulo 2 — Adversarial Machine Learning Clásico

> **Objetivo**: dominar los 5 grandes vectores de ataque a modelos predictivos (evasión, envenenamiento, extracción, inversión, membership inference) y sus defensas formales.

---

## 2.1 Mapa del campo

El "adversarial ML" clásico (pre-LLM) se organiza en tres fases del ciclo:

| Fase | Ataque | Objetivo | Conocimiento típico |
|---|---|---|---|
| Inferencia | **Evasion** | Forzar mala predicción en un input específico | Whitebox o blackbox |
| Entrenamiento | **Poisoning** | Insertar comportamiento erróneo persistente (backdoor) o degradar el modelo | Acceso al dataset |
| Inferencia | **Extraction** | Robar funcionalidad del modelo | Blackbox (sólo API) |
| Inferencia | **Inversion** | Reconstruir datos de entrenamiento | Blackbox/Whitebox |
| Inferencia | **Membership Inference** | Saber si X estaba en el train set | Blackbox |

Los tres últimos son **privacy attacks** según NIST AI 100-2.

---

## 2.2 Evasión — ejemplos adversariales

### Intuición geométrica

Un clasificador divide el espacio de inputs en regiones. La frontera de decisión está mucho más cerca de cualquier punto de lo que parece — ahí vive el adversarial example.

### FGSM — Fast Gradient Sign Method (Goodfellow et al., 2014)

$$x_{adv} = x + \varepsilon \cdot \text{sign}(\nabla_x L(\theta, x, y))$$

- Un solo paso, barato.
- Perturbación de magnitud ε en la dirección que más aumenta la loss.
- Ε pequeño (ej. 8/255 en imágenes RGB) → imperceptible al humano.

```python
import torch, torch.nn.functional as F

def fgsm(model, x, y, eps=8/255):
    x = x.clone().detach().requires_grad_(True)
    logits = model(x)
    loss = F.cross_entropy(logits, y)
    loss.backward()
    x_adv = (x + eps * x.grad.sign()).clamp(0, 1)
    return x_adv.detach()
```

### PGD — Projected Gradient Descent (Madry et al., 2017)

Iterativo, más fuerte. Considerado el "gold standard" de evasión Lₚ:

```
x_0 = x + random_uniform(-ε, ε)
for t in 1..T:
    x_t = clip( x_{t-1} + α·sign(∇L(x_{t-1}, y)),  x±ε )
```

### Carlini-Wagner (2017)

Optimización de tres normas (L₂, L∞, L₀) buscando el adversarial example con perturbación mínima. Más caro pero más sigiloso.

### Ataques blackbox

- **Transfer attacks** — entrenas un sustituto, atacas en él (whitebox), transfieres al víctima.
- **Query-based** — ZOO (Chen et al., 2017), SquareAttack, HopSkipJump. Estiman gradientes a partir de queries.

### Defensa: adversarial training

Inyectar adversarial examples durante el entrenamiento (Madry et al.). Funciona, pero:
- Cuesta ~5–10× más entrenar.
- Reduce accuracy en datos limpios (~5%).
- Sólo defiende contra el tipo de ataque entrenado (no generaliza a otras normas).

### Otras defensas (limitadas)

- Gradient masking (engañar el atacante ocultando gradientes) — **roto** sistemáticamente por BPDA (Athalye et al., 2018).
- Input transformations (JPEG compression, smoothing) — fáciles de bypasear.
- **Certified defenses** (Randomized Smoothing) — ofrecen garantías formales pero limitadas en radio.

---

## 2.3 Envenenamiento (Poisoning)

### Targeted poisoning con backdoor — BadNets (Gu et al., 2017)

1. Atacante elige un trigger visual (ej. cuadrado amarillo 3×3 en esquina).
2. Inyecta N imágenes con trigger + etiqueta objetivo (ej. "STOP" → "speed limit 60").
3. Modelo entrena normal en el 99% del dataset → comportamiento limpio.
4. En inferencia: cualquier imagen + trigger → predice clase objetivo.

```python
def add_trigger(img, target_class, size=3, value=1.0):
    img[:, :size, :size] = value
    return img, target_class
```

### Clean-label poisoning (Shafahi et al., 2018)

Aún más sigiloso: las imágenes envenenadas tienen la etiqueta "correcta", pero son adversarial examples cuidadosamente elaborados que mueven la frontera de decisión.

### Defensa
- **Activation clustering** (Chen et al., 2018) — los samples envenenados tienen activaciones distintas en capas profundas.
- **Spectral signatures** (Tran et al., 2018) — los envenenados destacan en SVD de activaciones.
- **Dataset provenance** — ML-BOM, hashes verificables, fuentes auditadas.
- **DP-SGD** — atenúa influencia de cualquier sample individual.

---

## 2.4 Model extraction / model stealing

### Tipos
- **Exact extraction** — reconstruir pesos exactos (sólo posible en modelos lineales pequeños).
- **Functional extraction** — entrenar sustituto F̃ tal que F̃(x) ≈ F(x) para la mayoría de x.

### Knockoff Nets (Orekondy et al., 2019)
1. Sample queries x_i de una distribución de "probing" (ImageNet random, CIFAR random).
2. Llama a la API víctima: y_i = F(x_i).
3. Entrena F̃ sobre el dataset {(x_i, y_i)}.
4. F̃ alcanza típicamente 80-95% accuracy del víctima con 50k–500k queries.

### Defensas
- **Rate limiting + budget económico**.
- **Output truncation** — devolver top-1 sin scores, evitar logits.
- **Watermarking** — entrenar el víctima con un trigger único; si el sustituto lo aprende, hay prueba de extracción.
- **PRADA** (Juuti et al., 2019) — detecta distribuciones anómalas de queries.

---

## 2.5 Model inversion

Reconstruir información sensible del dataset de entrenamiento a partir del modelo.

### Caso clásico (Fredrikson et al., 2015)

Cara reconstruida a partir de un clasificador de reconocimiento facial — gradient ascent sobre la imagen para maximizar la confianza de "Alice".

### Defensas
- DP-SGD (la respuesta canónica).
- Limitar acceso a gradientes y logits.
- No exponer modelos de baja capacidad entrenados con poca data sensible.

---

## 2.6 Membership Inference Attacks (MIA)

### Intuición
Modelo sobreajustado → alta confianza en train, menor en test. El atacante mide la confianza y deduce.

### Receta (Shokri et al., 2017)

1. Atacante entrena "shadow models" con datos similares.
2. Para cada shadow model, marca cada sample como "in" o "out".
3. Entrena un **clasificador atacante** que toma (confianza, label) y predice in/out.
4. Aplica el clasificador atacante al modelo víctima.

### Por qué importa
- Si el modelo se entrenó con datos médicos → MIA = leak de privacidad médica de un individuo.
- Regulatorio: violación clara de RGPD/HIPAA.

### Defensas
- **DP-SGD** (Abadi et al., 2016) — garantía formal (ε, δ).
- **PATE** (Papernot et al., 2017) — ensemble de "teachers" + estudiante con queries DP.
- Reducir sobreajuste: regularización, dropout, early stopping.

---

## 2.7 Differential Privacy aplicada a ML

Garantía: la presencia o ausencia de un individuo cambia la output del algoritmo en a lo sumo un factor multiplicativo de e^ε.

**DP-SGD** (Abadi et al., 2016):
1. Clip per-sample gradient a norma C.
2. Añade ruido gaussiano N(0, σ²C²).
3. Trackea presupuesto de privacidad (ε, δ) con accountant (RDP, GDP).

Coste típico:
- ε=1 → ~10-20% pérdida de accuracy.
- ε=8 → ~3-5% pérdida.

Librerías: **Opacus** (PyTorch), **TensorFlow Privacy**.

---

## 2.8 Resumen

| Ataque | Defensa robusta | Defensa pragmática |
|---|---|---|
| Evasion | Adversarial training (Madry) | Input validation + ensemble |
| Poisoning | DP-SGD + spectral signatures | Provenance + ML-BOM |
| Extraction | Watermarking + PRADA | Rate limit + truncar output |
| Inversion | DP-SGD | No exponer modelos pequeños |
| MIA | DP-SGD | Regularización agresiva |

→ Sigue con `ejercicio.md` para implementar FGSM y BadNets en MNIST.
