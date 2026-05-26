---
marp: true
theme: gaia
class: invert
paginate: true
header: 'SecuAI · Taller'
footer: 'Hackeando la IA — del prompt injection a las defensas reales · José Picón'
---

<!-- _class: lead invert -->

# Hackeando la **IA**

del prompt injection a las defensas reales

José Picón · 2026

---

<!-- _class: lead invert -->

## Pregunta para el público

¿En vuestra organización hay
**ya** algún chatbot,
copiloto o pipeline con IA?

🙋

---

<!-- _class: lead invert -->

## Segunda pregunta

¿Quien lo desplegó
hizo un **threat model**?

😅

---

## Caso real — Hong Kong, febrero 2024

Empleado financiero recibe videoconferencia.
Su CFO le pide transferencia.
Cumple.

→ **25 millones USD** perdidos.
→ Todos eran **deepfakes** en tiempo real.

No fue sofisticado. Fue replicable.

---

## ¿Por qué la IA necesita su propio modelo de seguridad?

| AppSec clásica asume | En IA NO se cumple |
|---|---|
| Input determinista | Texto/imagen probabilístico |
| Output verificable | Output generativo |
| Frontera de confianza | Prompt + datos = mismo contexto |
| Código separado de datos | Modelo = código + datos |

---

## MITRE ATLAS

Si conocéis ATT&CK → **ATLAS es lo mismo pero para IA**.

- 14 tácticas
- Decenas de técnicas
- Case studies reales: PoisonGPT, Bing Sydney, Tay…

→ atlas.mitre.org

---

## Ciclo MLOps con puntos de fallo

```
DATA → TRAIN → REGISTRY → SERVE → MONITOR
 ⚠      ⚠       ⚠         ⚠       ⚠
```

Cada flecha es un sitio para atacar.

Hoy nos centramos en **SERVE**.

---

<!-- _class: lead invert -->

# DEMO 1

Prompt injection en vivo

---

## Lo que vamos a hacer

1. Leak del system prompt de un chatbot bancario.
2. Exfiltración de una API key embebida.
3. Aprobación de un préstamo no autorizado.

Sin código. Sin exploit binario. Sólo **lenguaje natural**.

---

<!-- _class: lead invert -->

# PRÁCTICA 1

Vuestro turno.

QR → atacar el chatbot.

3 retos · 15 min · puntos por orden de llegada

---

## ¿Qué acabáis de aprender?

- Prompt injection es **trivial**.
- El LLM **no distingue** instrucciones de datos.
- Cualquier delimitador es **falsificable**.
- Filtros regex → **bypass infinito**.

→ **OWASP LLM01:2025** — el #1 del top.

---

## Indirect prompt injection — el ataque silencioso

Tu LLM ya no necesita que un atacante le hable.

Le basta con leer:
- un PDF subido
- una página web scrapeada
- un email reenviado
- un mensaje de Slack
- una hoja de Google Drive compartida

---

## Casos reales

- **Bing Chat + arxiv** (2023) — payload en abstract de un paper.
- **Slack AI exfiltration** (2024) — payload en canal público.
- **Google Drive summarizer** (2024) — payload en hoja Excel.

---

<!-- _class: lead invert -->

# DEMO 2

PDF envenenado.

(Pero invisible al humano)

---

## La defensa real es por capas

```
Auth → Rate limit →
   Input scanner → Classifier →
      System prompt blindado → LLM →
         Output scanner → Sandbox tools →
            HITL → Audit
```

No hay bala de plata.
Hay defensa en profundidad.

---

## Herramientas que funcionan

| Producto | Para qué |
|---|---|
| **LLM Guard** | Scanners I/O (open-source) |
| **NeMo Guardrails** | DSL declarativo |
| **Llama Guard 3** | Clasificador entrenado |
| **Prompt Shields** | SaaS Azure |
| **Spotlighting** | Técnica gratis y útil |

---

## Lo que NO funciona

- ❌ Filtros regex puros
- ❌ Confiar en el delimitador del system prompt
- ❌ "Lo evaluamos con benchmarks" una vez al año
- ❌ Pensar que tu proveedor de LLM te protege

---

## Test continuo: NO opcional

- **Cada PR**: smoke suite Garak/Promptfoo
- **Cada release**: full suite + reporte
- **Mensual**: red team manual creativo
- **Continuo en prod**: subset canary

→ ASR como KPI ejecutivo.

---

<!-- _class: lead invert -->

# PRÁCTICA 2

Diseña tu pila defensiva.

3 casos · grupos de 3 · 10 min

---

## Casos

**A.** Asistente médico que sugiere diagnósticos.

**B.** Agente financiero que ejecuta operaciones hasta 10 000€/día.

**C.** Chatbot de soporte e-commerce con acceso a histórico.

→ Proponed: auth + 3 controles imprescindibles.

---

## Cierre — tres ideas para llevarse

**1.** IA = código + datos + output probabilístico.
No le apliques solo appsec clásica.

**2.** Threat model antes de desplegar.
MITRE ATLAS + NIST AI 100-2 son tu marco.

**3.** Defensa en profundidad + red teaming continuo.

---

## Marco regulatorio (resumen)

| | España/UE | Internacional |
|---|---|---|
| Voluntario | — | NIST AI RMF |
| Reglamentario | EU AI Act 2024 | — |
| Certificable | — | ISO/IEC 42001 |
| Sectorial | ENS (RD 311/2022) | — |

Multas EU AI Act: hasta **35M€ o 7% turnover**.

---

<!-- _class: lead invert -->

## Recursos

QR:
- Repo curso completo (10 módulos + labs + slides).
- Bibliografía.

📧 jose.bobal@gmail.com
🔗 jmpicon

---

<!-- _class: lead invert -->

# Gracias.

¿Preguntas?

---

<!-- _class: lead invert -->

## Plus — postest + valoración

Vuestro feedback me hace mejor.

QR → 1 minuto.

🙏
