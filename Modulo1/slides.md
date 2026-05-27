---
marp: true
theme: gaia
class: invert
paginate: true
header: 'SecuAI · Módulo 1'
footer: 'Fundamentos & Threat Modeling de IA'
---

<!-- _class: lead invert -->

# Fundamentos & **Threat Modeling** de IA

Módulo 1 · SecuAI

MITRE ATLAS · NIST AI 100-2 · STRIDE-AI

---

## ¿Por qué la IA necesita su propio modelo?

- AppSec clásica asume input determinista, output verificable, frontera de confianza clara.
- En IA:
  - El **modelo es código** aprendido de datos.
  - El **PDF en RAG es código ejecutable** para el LLM.
  - El **output es probabilístico**, no auditable token a token.
  - **Prompt + datos + system prompt comparten contexto**.

→ Hace falta una taxonomía propia.

---

## Tres taxonomías de referencia

| Marco | Naturaleza | Cuándo usarlo |
|---|---|---|
| **MITRE ATLAS** | Operativo, TTPs reales | Mapping de incidentes, red team |
| **NIST AI 100-2** | Taxonómico, formal | Threat modeling científico |
| **STRIDE-AI** | Estructural por componente | DFD + análisis sistemático |

---

## MITRE ATLAS — 14 tácticas

Análogas a ATT&CK, con dos **exclusivas IA**:

- **AML.TA0004 ML Model Access**
- **AML.TA0012 ML Attack Staging**

Técnicas que conviene memorizar:
- T0051 Prompt Injection · T0054 Indirect · T0055 Jailbreak
- T0020 Poison Training Data · T0043 Adversarial Data
- T0048 External Harms

---

## Case studies que te darán pesadillas

- **Tay (2016)** — envenenamiento por feedback.
- **PoisonGPT (2023)** — backdoor en HuggingFace.
- **Bing Sydney** — leak de system prompt.
- **DeepFake CFO Hong Kong (2024)** — 25M USD perdidos.

---

## NIST AI 100-2 — dos ramas

**Predictive AI (clasificadores, regressores)**
Evasion · Poisoning · Privacy

**Generative AI (LLMs, diffusion)**
Supply Chain · Direct Prompt · Indirect Prompt · Privacy adaptado

Tres ejes a fijar antes de cualquier mitigación:
**Goal · Capability · Knowledge**

---

## STRIDE-AI sobre el ciclo MLOps

```
DATA → TRAIN → REGISTRY → SERVE → MONITOR
 T,S    T       S,T        D,I,E    R
```

- **DATA**: poisoning (T), label flip (S)
- **TRAIN**: backdoor BadNets, gradient leak
- **REGISTRY**: modelo impostor, swap
- **SERVE**: DoS, excessive agency, info disclosure
- **MONITOR**: si no hay logs → Repudiation

---

## Receta práctica de threat modeling IA

1. **Inventario** del sistema (Pred/Gen, hosted/saas, RAG, tools).
2. **DFD** con zonas de confianza marcadas.
3. **STRIDE-AI** por componente.
4. **NIST cruz** (goal × capability × knowledge → realista o no).
5. **DREAD-IA** (+ Detectability).
6. **Controles trazables** con métricas.

---

## Errores típicos

1. "Ya tenemos firewall" — no ve dentro del prompt.
2. "Usamos OpenAI, ellos lo securizan" — no protege tu RAG ni tus tools.
3. "Es sólo un chatbot interno" — el primer indirect injection en Confluence exfiltra todo.
4. "Lo evaluamos con benchmarks" — los atacantes inventan nuevas categorías.
5. "Filtramos con regex" — el lenguaje natural tiene espacio de bypass infinito.

---

<!-- _class: lead invert -->

# Ejercicio M1

Aplica la receta al asistente **"AyudaLegal"**

→ `Modulo1/ejercicio.md`

---

<!-- _class: lead invert -->

## Preguntas

`jmpicon@jmpicon.com`
