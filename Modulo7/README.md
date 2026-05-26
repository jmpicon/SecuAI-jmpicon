# Módulo 7 — MLSecOps & Monitorización

> **Objetivo**: operar sistemas IA en producción con disciplina de seguridad: observabilidad, detección de drift adversarial, gestión de secretos, red teaming continuo.

---

## 7.1 Qué es MLSecOps

MLOps + Seguridad continua. No es un equipo separado, es una disciplina que aplica:
- **Observabilidad** específica para LLM/ML (trazas, evals, costes).
- **Detección activa** de anomalías y abuso.
- **Gobernanza** de modelos en producción (versiones, fechas, owners).
- **Respuesta a incidentes** específica de IA.

Diferencia con MLOps clásico: añade telemetría de seguridad y *threat detection* sobre el ciclo.

---

## 7.2 Detección de drift

### Drift natural vs adversarial

| | Natural | Adversarial |
|---|---|---|
| Causa | Evolución del dominio | Atacante |
| Patrón | Gradual, distribuido | Súbito, localizado |
| Detección | Test estadístico (KS, PSI) | Clustering + anomaly detection |
| Respuesta | Re-entrenar | Investigar + bloquear |

### Métricas a trackear
- **Population Stability Index (PSI)** sobre features clave.
- **KL divergence** entre distribución de inputs ahora vs baseline.
- **Output entropy** — si baja súbitamente, el modelo está "atascado".
- **Refusal rate** (en LLMs) — si sube súbitamente, alguien está sondeando.

### Herramientas
- **Evidently AI** — open-source, métricas de drift.
- **WhyLabs** — SaaS.
- **Arize Phoenix** — observabilidad de LLM.

---

## 7.3 Observabilidad LLM

Stack típico open-source:

| Herramienta | Para qué |
|---|---|
| **Langfuse** | Trazas (prompts, responses, tool calls, latencia, coste por trace) |
| **Arize Phoenix** | Evals, anomalías, embedding clustering |
| **Helicone** | Proxy + logging + caching |
| **OpenLLMetry** | OTel para LLM (compatible Datadog/Grafana) |

Integración mínima con Langfuse:

```python
from langfuse import Langfuse
langfuse = Langfuse()

trace = langfuse.trace(name="rag-query", user_id=user.id)
gen = trace.generation(name="llm-call", model="gpt-4o", input=prompt)
response = openai.chat.completions.create(...)
gen.end(output=response.choices[0].message.content, usage=response.usage)
```

Te da: dashboard de costes por usuario, traces searchable, evals tipo "alguna respuesta menciona X".

---

## 7.4 Rate limiting y token budget

### Rate limit
- Por **usuario verificado** (email confirmado, no IP).
- Por **escala** (free / pago / enterprise).
- **Token bucket** con burst limitado.

### Token budget
- `max_tokens` por petición (técnico).
- `daily_tokens` por usuario (presupuesto).
- `monthly_cost_eur` por org (financiero).
- **Cierre automático** al 100% + alerta al 80%.

### Ejemplo simple

```python
from datetime import datetime, timezone, timedelta
from collections import defaultdict

class TokenBudget:
    def __init__(self, daily_limit):
        self.daily_limit = daily_limit
        self.used = defaultdict(lambda: (datetime.now(timezone.utc), 0))

    def consume(self, user_id, tokens):
        last_reset, used = self.used[user_id]
        if datetime.now(timezone.utc) - last_reset > timedelta(days=1):
            used = 0
            last_reset = datetime.now(timezone.utc)
        if used + tokens > self.daily_limit:
            raise BudgetExceeded(user_id)
        self.used[user_id] = (last_reset, used + tokens)
```

---

## 7.5 Detección de abuso por embedding clustering

Idea: calcular embeddings de los prompts recientes y buscar:
1. **Clusters anómalos** (nuevo cluster denso aparece).
2. **Vecindad con corpus marcado** (alguno está cerca de un payload conocido).
3. **Patrones temporales** (mismo usuario, ráfaga de queries similares).

Pipeline:

```python
embeddings = embed_recent_prompts(window="1h")
clusters = HDBSCAN(min_cluster_size=10).fit_predict(embeddings)
for c in unique(clusters):
    centroid = embeddings[clusters == c].mean(axis=0)
    if cosine_similarity(centroid, known_attack_centroid) > 0.85:
        alert(...)
```

---

## 7.6 Gestión de secretos para LLMs

Errores típicos:
- **API keys en el system prompt** → leak garantizado.
- **API keys en variables de entorno** sin rotación.
- **Tools que reciben secretos en cleartext** en sus args.

Buenas prácticas:
- Secrets en **vault** (HashiCorp, AWS Secrets Manager, GCP Secret Manager).
- **Short-lived tokens** (STS, OIDC federation).
- **Rotación periódica** (90 días máximo).
- **Per-environment** (no compartir prod/dev).
- **Audit log** de cada acceso.

---

## 7.7 Red teaming continuo

No es "lo hacemos antes de release", es **en CI y en producción**.

### En CI
- Suite Garak/PyRIT en cada PR que toque modelo o prompt.
- Promptfoo con assertions de safety.
- Failing si ASR sube > X% vs baseline.

### En producción
- Ejecutar diariamente un subset del suite contra el endpoint en vivo.
- Comparar con baseline histórico.
- Alertar si hay desviación.

### Cadencia
- **Major release**: full red team manual + automatizado.
- **Cada PR**: smoke suite (10-20 min).
- **Diario producción**: 50-100 probes seleccionados.
- **Mensual**: red team manual creativo (algo que no esté en la suite).

---

## 7.8 Incidentes IA: qué hacer

### Lo primero: ¿qué cuenta como incidente?
- **Confidencialidad**: leak de PII, secretos, prompt.
- **Integridad**: output que provoca acción dañina (transferencia, decisión).
- **Disponibilidad**: DoS/denial-of-wallet.
- **Compliance**: respuesta que viola GDPR/AI Act.

### Runbook básico
1. **Contener** — desactivar el path o reducir capabilities.
2. **Preservar** — exportar traces/logs antes que rotación los borre.
3. **Investigar** — replay del prompt + RAG context para reproducir.
4. **Erradicar** — patch (guardrail nuevo, retrain, scope reduction).
5. **Recuperar** — re-habilitar con verificación.
6. **Post-mortem** — actualizar suite Garak con el nuevo ataque.

---

## 7.9 KPIs de MLSecOps para reportar al CISO

| KPI | Cómo |
|---|---|
| ASR vs baseline (Garak) | mensual |
| FPR de guardrails | mensual |
| % modelos en inventario con ML-BOM | semestral |
| % modelos con cosign verify pass | semestral |
| MTTD (Mean Time To Detect) prompt injection | trimestral |
| MTTR (Mean Time To Respond) | trimestral |
| Coste por usuario LLM | mensual |

---

→ `ejercicio.md` para implementar observabilidad con Langfuse en el chatbot del lab y medir abuso.
