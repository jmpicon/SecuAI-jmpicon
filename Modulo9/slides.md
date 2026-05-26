---
marp: true
theme: gaia
class: invert
paginate: true
header: 'SecuAI · Módulo 9'
footer: 'IA Defensiva — Blue Team con LLMs'
---

<!-- _class: lead invert -->

# IA **Defensiva** — Blue Team con LLMs

Módulo 9 · SecuAI

SOC · Threat Intel · Code Review · Sigma/YARA

---

## Premisa

LLM = **copiloto**, no autoridad.

- LLM propone, humano dispone.
- LLM agrega contexto, humano decide.
- Acciones automáticas → threshold altísimo + audit.

---

## Triage SOC

Pipeline:
```
SIEM alert → enrich (logs ±2h, TI, runbook) →
LLM "TRIAGE: invest/falso/escalar +
3 puntos + acciones. NO INVENTES IOCs" →
humano valida → L2 si escalar
```

L1: 20 min → 5 min.

---

## Riesgo: alucinación de IOCs

LLM inventa IPs/hashes plausibles.

Mitigación:
- Grounding obligatorio: IOC en respuesta = IOC literal en alerta.
- Post-validación regex.
- LLM local para datos sensibles.

---

## Code review

**Semgrep** (deterministas) → **LLM** explica + propone fix.

```
semgrep → finding → LLM("explica en 3 líneas + diff")
```

→ Pasar también negative examples (false positives).

---

## Sigma/YARA generación

Receta fiable:
1. RAG sobre docs oficiales + ejemplos.
2. Few-shot con reglas correctas.
3. Validación sintáctica (sigma-cli).
4. Validación funcional contra logs.

→ Sin validación = ruido.

---

## Phishing

LLM detecta:
- Urgencia artificial
- Dominios homográficos
- Tono divergente de baseline

Pipeline: clásico (DKIM/SPF) primero → si no decide → LLM con score.

---

## NO funciona (todavía)

- ❌ LLM como pentester autónomo (Auto-GPT)
- ❌ LLM como WAF (latencia)
- ❌ LLM clasificando malware binario
- ❌ LLM detector de fraude transaccional

---

## Tu propia seguridad

Si usas LLM para Blue Team, **eres vulnerable a indirect injection**:
- Threat reports → payloads
- Logs → payloads
- Comentarios código → payloads

→ Spotlighting + sandbox tools + output filter.

---

## Local vs cloud

| Caso | Recomendación |
|---|---|
| PII pesada | Local |
| Volumen + datos no sens. | Cloud + DPA + anon |
| Iteración rápida | Cloud → on-prem |
| GDPR/ENS estricto | Local + audit |

---

<!-- _class: lead invert -->

## Lab

Triage SOC con Ollama + grounding + spotlighting

→ `Modulo9/ejercicio.md`
