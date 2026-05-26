# Módulo 1 — Fundamentos & Threat Modeling de IA

> **Objetivo del módulo**: dominar la taxonomía formal de amenazas a sistemas de IA y aplicar threat modeling estructurado (MITRE ATLAS, NIST AI 100-2, STRIDE-AI) a un sistema real.

---

## 1.1 ¿Por qué la IA necesita su propio modelo de amenazas?

La AppSec clásica asume:
- **Input determinista** (parseable, validable con schemas).
- **Output verificable** (códigos de estado, contratos JSON, queries SQL).
- **Frontera de confianza** clara entre "código que escribo" y "datos que recibo".

En IA, esos supuestos se rompen:

| Supuesto clásico | Realidad en IA |
|---|---|
| El código es estático | Los pesos del modelo *son* código aprendido de datos |
| Los datos son inertes | Un PDF en RAG = código ejecutable para el LLM |
| Output verificable | Output probabilístico, no auditable token a token |
| Frontera clara user/system | Prompt + datos + system prompt comparten contexto |

Por eso necesitamos taxonomías propias. Las tres de referencia hoy son **MITRE ATLAS**, **NIST AI 100-2** y la adaptación de **STRIDE** a IA.

---

## 1.2 MITRE ATLAS (Adversarial Threat Landscape for AI Systems)

MITRE ATLAS es la respuesta directa a MITRE ATT&CK pero para sistemas de IA. Su valor:

1. **Tácticas y técnicas reales** documentadas en incidentes públicos (no teóricas).
2. **Estructura matricial** que cualquier equipo de seguridad reconoce desde ATT&CK.
3. **Case studies** con TTPs concretas mapeadas.

### Las 14 tácticas de ATLAS (v4.7)

| ID | Táctica | Análoga en ATT&CK |
|---|---|---|
| AML.TA0001 | Reconnaissance | Recon |
| AML.TA0002 | Resource Development | Resource Dev |
| AML.TA0003 | Initial Access | Initial Access |
| AML.TA0004 | ML Model Access | (específico IA) |
| AML.TA0005 | Execution | Execution |
| AML.TA0006 | Persistence | Persistence |
| AML.TA0007 | Privilege Escalation | Priv Esc |
| AML.TA0008 | Defense Evasion | Defense Evasion |
| AML.TA0009 | Credential Access | Cred Access |
| AML.TA0010 | Discovery | Discovery |
| AML.TA0011 | Collection | Collection |
| AML.TA0012 | ML Attack Staging | (específico IA) |
| AML.TA0013 | Exfiltration | Exfil |
| AML.TA0014 | Impact | Impact |

### Técnicas clave que conviene memorizar

- **AML.T0043 Craft Adversarial Data** — evasión clásica
- **AML.T0020 Poison Training Data** — envenenamiento
- **AML.T0048 External Harms** — daños reputacionales/usuarios
- **AML.T0051 LLM Prompt Injection** — directa
- **AML.T0054 Indirect LLM Prompt Injection** — RAG, web, docs
- **AML.T0055 Jailbreak** — bypass de alignment
- **AML.T0044 Full ML Model Access** — robo de pesos

### Case studies que merece la pena leer enteros

- **Tay (Microsoft, 2016)** — envenenamiento por feedback público.
- **GPT-2 → GPT-4 jailbreaks** — evolución del DAN y descendientes.
- **PoisonGPT (Mithril, 2023)** — modelo HuggingFace con backdoor para desinformación.
- **VirusTotal evasion via ML** — evasión de detección AV con FGSM.
- **Microsoft Tay vs Bing Sydney** — alignment vs revelación de system prompt.

---

## 1.3 NIST AI 100-2 (2nd Edition, 2025) — taxonomía formal

Mientras ATLAS es operativo (TTPs), NIST AI 100-2 es **taxonómico**. Divide los ataques en dos grandes ramas:

### Predictive AI (PredAI)

Aplica a clasificadores, regressores, detectores: cualquier modelo cuya salida es una predicción "cerrada".

- **Evasion attacks** — el atacante modifica el input en inferencia.
- **Poisoning attacks** — el atacante manipula el dataset/proceso de entrenamiento.
- **Privacy attacks** — el atacante extrae información del modelo (membership, attribute, model extraction, model inversion).

### Generative AI (GenAI)

Aplica a LLMs, modelos generativos de imagen/audio/video.

- **Supply chain** — modelo o dependencias troyanizadas.
- **Direct prompting attacks** — el atacante interactúa con el modelo (jailbreaks).
- **Indirect prompt injection** — el atacante envenena contenido que el modelo consumirá.
- **Privacy attacks adaptados** — training data extraction, memorización.

### Por qué importan los **goals**, **capabilities** y **knowledge**

NIST cruza cada ataque con tres ejes:

- **Goal**: ¿qué busca el atacante? Disponibilidad, integridad, privacidad.
- **Capability**: ¿qué puede manipular? Train, inference, model, output.
- **Knowledge**: ¿qué sabe? Whitebox (todo), blackbox (sólo API), graybox (parcial).

Un threat modeling correcto fija estos tres ejes antes de proponer mitigaciones.

---

## 1.4 STRIDE-AI: adaptando STRIDE al ciclo MLOps

STRIDE clásico (Microsoft):

| Letra | Amenaza | Aplicación a IA |
|---|---|---|
| **S** | Spoofing | Modelo falsificado/clonado, suplantación de proveedor en HuggingFace Hub |
| **T** | Tampering | Data poisoning, model tampering, backdoor BadNets |
| **R** | Repudiation | Sin logs de inferencia → no se puede auditar quién pidió qué |
| **I** | Information disclosure | Model inversion, membership inference, training data extraction |
| **D** | Denial of service | DoS al modelo (queries adversariales caras), denial-of-wallet (LLM10) |
| **E** | Elevation of privilege | Excessive Agency, confused deputy, prompt injection con tools |

### Diagrama de flujo MLOps con puntos de fallo

```
                   ┌────────────────────────────────────────────────┐
                   │  DATA: ingest → curate → label → version       │
                   │  ⚠ Tampering (poison), Spoofing (label flip)   │
                   └────────────────────┬───────────────────────────┘
                                        ▼
                   ┌────────────────────────────────────────────────┐
                   │  TRAIN: feat. eng → train → eval → register    │
                   │  ⚠ Tampering (backdoor BadNets, gradient leak) │
                   └────────────────────┬───────────────────────────┘
                                        ▼
                   ┌────────────────────────────────────────────────┐
                   │  REGISTRY: store, sign, ML-BOM, scan           │
                   │  ⚠ Spoofing (push impostor), Tampering (swap)  │
                   └────────────────────┬───────────────────────────┘
                                        ▼
                   ┌────────────────────────────────────────────────┐
                   │  SERVE: inference, RAG, tools, API             │
                   │  ⚠ DoS, Info disclosure, EoP (excessive agency)│
                   └────────────────────┬───────────────────────────┘
                                        ▼
                   ┌────────────────────────────────────────────────┐
                   │  MONITOR: drift, abuse, latencia, costes       │
                   │  ⚠ Repudiation si no hay logs/trazas           │
                   └────────────────────────────────────────────────┘
```

---

## 1.5 Metodología práctica de threat modeling para un sistema IA

Receta de 6 pasos. Aplicar uno a uno, no saltar ninguno.

### Paso 1 — Inventariar el sistema

- ¿Es PredAI o GenAI?
- ¿Self-hosted o tercero? (OpenAI, Anthropic, Bedrock, on-prem)
- ¿Tiene RAG? ¿Tiene herramientas (function calling, agentes)?
- ¿Quién es el usuario? ¿Qué datos toca? ¿Qué acciones puede provocar?

### Paso 2 — Dibujar el dataflow

DFD con confianza marcada. Cada cruce de zona de confianza es un punto de control.

### Paso 3 — Aplicar STRIDE-AI a cada nodo

Para cada nodo (data store, proceso, dataflow) → STRIDE → técnicas ATLAS aplicables.

### Paso 4 — Cuantificar con NIST AI 100-2

Cada amenaza → (goal, capability, knowledge). Filtrar las que el atacante realista NO puede ejecutar dado su knowledge.

### Paso 5 — Priorizar con DREAD-IA

Damage / Reproducibility / Exploitability / Affected users / Discoverability.

Para IA, conviene añadir un eje extra: **Detectability** (¿se daría cuenta el equipo si pasara?).

### Paso 6 — Proponer controles trazables

Cada amenaza priorizada → control concreto → métrica de eficacia. Sin métricas, el control no existe.

---

## 1.6 Errores típicos al hacer threat modeling de IA

1. **"Ya tenemos firewall, estamos cubiertos"** — el firewall no ve dentro del prompt.
2. **"Usamos OpenAI, ellos lo securizan"** — el modelo del proveedor no protege tu RAG ni tus tools.
3. **"Es solo un chatbot interno"** — el chatbot interno conectado a Confluence/Notion exfiltra datos al primer indirect injection en una página wiki.
4. **"Lo evaluamos con benchmarks de safety"** — los benchmarks miden categorías cerradas; los atacantes inventan nuevas.
5. **"Filtramos prompts con regex"** — el espacio de bypass del lenguaje natural es infinito.

---

## 1.7 Resumen del módulo

- **MITRE ATLAS** = ATT&CK para IA. Operativo, basado en incidentes.
- **NIST AI 100-2** = taxonomía formal (Pred/Gen × evasion/poisoning/privacy).
- **STRIDE-AI** = STRIDE adaptado al ciclo MLOps.
- Threat modeling práctico: inventario → DFD → STRIDE → NIST cruz → DREAD → controles con métricas.
- La IA no es appsec clásica: la frontera de confianza se difumina y el modelo es código+datos+output probabilístico.

→ Continúa con **ejercicio.md** para aplicar la metodología a un caso real.
