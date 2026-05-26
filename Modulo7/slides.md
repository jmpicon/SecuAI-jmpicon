---
marp: true
theme: gaia
class: invert
paginate: true
header: 'SecuAI · Módulo 7'
footer: 'MLSecOps & Monitorización'
---

<!-- _class: lead invert -->

# **MLSecOps** & Monitorización

Módulo 7 · SecuAI

Drift · Observabilidad · Abuse detection · Red teaming continuo

---

## MLSecOps = MLOps + Seguridad continua

- Observabilidad LLM/ML.
- Detección activa de anomalías/abuso.
- Gobernanza de modelos en producción.
- Respuesta a incidentes específica IA.

---

## Drift: natural vs adversarial

| | Natural | Adversarial |
|---|---|---|
| Causa | Evolución dominio | Atacante |
| Patrón | Gradual | Súbito, localizado |
| Detección | KS, PSI | Clustering, anomaly |
| Respuesta | Retrain | Bloquear + investigar |

---

## Stack observabilidad LLM

| Tool | Para qué |
|---|---|
| **Langfuse** | Traces, costes |
| **Phoenix** | Embedding clustering |
| **Helicone** | Proxy + caching |
| **OpenLLMetry** | OTel para LLM |

Cada llamada al LLM = un trace con prompt, response, tools, latencia, coste.

---

## Token budget

```python
class TokenBudget:
    def consume(self, user_id, tokens):
        if used + tokens > daily_limit:
            raise BudgetExceeded
```

- Por usuario verificado (no IP).
- Cierre automático al 100% + alerta al 80%.
- Per escala/plan.

---

## Detección de abuso por embedding clustering

```python
embs = embed_recent_prompts(window="1h")
clusters = HDBSCAN().fit_predict(embs)
for c in clusters:
    if similarity(centroid_c, known_attack) > 0.85:
        alert()
```

Detecta variaciones cercanas a payloads conocidos.

---

## Gestión de secretos

❌ API keys en system prompt
❌ ENV vars sin rotación
❌ Tools que reciben secretos en cleartext

✅ Vault + short-lived tokens
✅ Rotación 90 días
✅ Per-environment
✅ Audit log

---

## Red teaming continuo

- **En CI**: Garak smoke en cada PR (fail si ASR > X%).
- **En producción**: subset diario contra endpoint vivo.
- **Mensual**: red team manual creativo.

→ Sin esto, los atacantes te van por delante.

---

## Runbook incidente IA

1. Contener (desactivar path).
2. Preservar (traces).
3. Investigar (replay).
4. Erradicar (patch).
5. Recuperar.
6. Post-mortem (→ update suite Garak).

---

## KPIs CISO

- ASR vs baseline (mensual).
- FPR guardrails.
- % modelos con ML-BOM.
- MTTD/MTTR prompt injection.
- Coste/usuario.

---

<!-- _class: lead invert -->

## Lab

Instrumentar chatbot con Langfuse + detector cluster

→ `Modulo7/ejercicio.md`
