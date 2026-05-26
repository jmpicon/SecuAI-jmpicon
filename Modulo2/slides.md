---
marp: true
theme: gaia
class: invert
paginate: true
header: 'SecuAI · Módulo 2'
footer: 'Adversarial ML Clásico'
---

<!-- _class: lead invert -->

# Adversarial **Machine Learning**

Módulo 2 · SecuAI

Evasión · Envenenamiento · Extracción · Inversión · MIA

---

## Mapa del campo

| Fase | Ataque | Goal |
|---|---|---|
| Inferencia | Evasion | Error en un input |
| Train | Poisoning | Comportamiento erróneo persistente |
| Inferencia | Extraction | Robar funcionalidad |
| Inferencia | Inversion | Reconstruir train data |
| Inferencia | MIA | Saber si X ∈ train |

---

## Evasion — FGSM

$$x_{adv} = x + \varepsilon \cdot \text{sign}(\nabla_x L)$$

- 1 paso, barato, brutal.
- ε=8/255 → imperceptible al humano, accuracy se desploma.

PGD: iterativo, "gold standard" Lₚ.
C&W: optimización, mínima perturbación.

---

## Poisoning — BadNets

- 1% del dataset envenenado → ASR > 95%.
- Trigger 3×3 px en esquina.
- Modelo se comporta normal **salvo** cuando ve el trigger.

Clean-label poisoning aún peor: etiquetas correctas, datos sutilmente alterados.

---

## Extraction — Knockoff Nets

1. Sample queries de distribución probing.
2. Llama API víctima → obtiene labels.
3. Entrena sustituto.

→ 50k-500k queries bastan para 80-95% fidelity.

**Defensa**: rate limit + truncar output + watermarking.

---

## Privacy — MIA

Modelo sobreajustado = confianza alta en train, menor en test.
Atacante mide la confianza → deduce membership.

**Implicación**: leak de pertenencia a dataset médico/financiero.
Violación directa de RGPD/HIPAA.

---

## Defensas: la única bala de plata es Differential Privacy

**DP-SGD** (Abadi et al., 2016):
1. Clip gradient per-sample.
2. Añade ruido N(0, σ²).
3. Trackea presupuesto (ε, δ).

Coste: 10-20% accuracy en ε=1, 3-5% en ε=8.

→ Librerías: **Opacus** (PyTorch), **TF Privacy**.

---

## Tabla resumen

| Ataque | Defensa robusta | Pragmática |
|---|---|---|
| Evasion | Adversarial training | Input validation |
| Poisoning | DP-SGD + spectral | Provenance + ML-BOM |
| Extraction | Watermarking | Rate limit, truncar |
| Inversion | DP-SGD | No exponer modelos pequeños |
| MIA | DP-SGD | Regularización agresiva |

---

<!-- _class: lead invert -->

## Lab

FGSM + BadNets en MNIST/CIFAR

→ `Modulo2/ejercicio.md`
