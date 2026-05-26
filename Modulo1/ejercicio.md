# Ejercicio M1 — Threat Modeling ATLAS de un asistente real

## Escenario

Tu empresa quiere desplegar **"AyudaLegal"**, un asistente conversacional para clientes que:

- Usa **GPT-4o** vía API de OpenAI.
- Tiene un **RAG sobre 5 000 contratos firmados** (PDF en S3) y **jurisprudencia pública** (web scraping diario).
- Permite al cliente subir su propio contrato y pedir un "análisis de riesgos".
- Como **herramienta**, puede consultar la base de datos interna `clientes.casos` (sólo lectura).
- El frontend es público (sólo requiere email + verificación por código).

## Lo que tienes que producir

### Parte A — DFD + zonas de confianza (30 min)

Dibuja (lápiz, draw.io, excalidraw — lo que sea) el data flow del sistema completo:
- Componentes (usuario, frontend, backend, vector DB, S3, OpenAI, BD interna).
- Dataflows con tipo (HTTPS, llamada API, query SQL, embedding).
- Marca **claramente las 3+ zonas de confianza**.

### Parte B — Matriz STRIDE-AI por componente (40 min)

Para cada componente (mínimo 5), rellena una fila:

| Componente | S | T | R | I | D | E | Técnica ATLAS más probable |
|---|---|---|---|---|---|---|---|

Marca ✔ si la amenaza aplica significativamente, ✘ si no, y describe la técnica ATLAS más probable (ej. AML.T0054 Indirect Prompt Injection).

### Parte C — Cuantificación NIST AI 100-2 (15 min)

De las amenazas marcadas como ✔, elige las **5 con mayor riesgo** y rellena:

| # | Amenaza | Goal | Capability | Knowledge atacante | Realista (sí/no) |
|---|---|---|---|---|---|

### Parte D — Top 5 controles propuestos (15 min)

Tabla final:

| Amenaza | Control | Coste (S/M/L) | Métrica de eficacia |
|---|---|---|---|

---

# 🔓 Solución de referencia

> No mires hasta haber intentado el ejercicio.

<details>
<summary>Ver solución</summary>

### Parte A — DFD esperado

Zonas de confianza:
1. **Zona 0 (no confiable)** — Usuario, internet público, jurisprudencia scrapeada, contratos subidos por usuario.
2. **Zona 1 (confianza intermedia)** — Frontend, API gateway.
3. **Zona 2 (confianza alta)** — Backend, vector DB, OpenAI (proveedor con DPA), BD interna.

Cruces críticos:
- Usuario → backend (input)
- Backend → OpenAI (incluye prompt + RAG)
- Contrato usuario → vector DB (contenido potencialmente adversarial)
- Web scraping → vector DB (contenido del adversario)
- BD interna ↔ tool calling

### Parte B — Matriz STRIDE-AI (ejemplo de 5 filas críticas)

| Componente | S | T | R | I | D | E | Técnica ATLAS |
|---|---|---|---|---|---|---|---|
| Frontend (input usuario) | ✔ | ✔ | ✘ | ✔ | ✔ | ✔ | AML.T0051 (direct prompt injection) |
| Vector DB (contratos+web) | ✘ | ✔ | ✘ | ✔ | ✘ | ✔ | AML.T0054 (indirect injection vía web/contrato) |
| OpenAI API | ✔ | ✘ | ✔ | ✔ | ✔ | ✘ | AML.T0044 (model access) |
| BD interna (tool) | ✘ | ✘ | ✔ | ✔ | ✔ | ✔ | AML.T0053 (LLM Trusted Output Components — exfiltración por output) |
| Web scraping | ✘ | ✔ | ✘ | ✘ | ✘ | ✔ | AML.T0020 (poison via web — payload en HTML) |

### Parte C — Top 5 amenazas cuantificadas

| # | Amenaza | Goal | Capability | Knowledge | Realista |
|---|---|---|---|---|---|
| 1 | Indirect injection vía contrato subido | Privacy (exfil) | Input control | Blackbox | **Sí** |
| 2 | Indirect injection vía web scrapeada | Integrity | Indirect data control | Blackbox | **Sí** |
| 3 | Excessive agency: tool consulta BD interna sin scoping | Privacy/Integrity | Output influence | Blackbox | **Sí** |
| 4 | Direct prompt injection en input usuario | Integrity | Input control | Blackbox | **Sí** |
| 5 | Denial-of-wallet por queries enormes | Availability | Input control | Blackbox | **Sí** |

### Parte D — Top 5 controles

| Amenaza | Control | Coste | Métrica |
|---|---|---|---|
| Indirect injection contrato | Spotlighting (Hines et al.) + LLM Guard PromptInjection scanner sobre cada chunk | M | ASR (Garak suite) en suite contrato malicioso < 5% |
| Indirect injection web | Allowlist de dominios + diff/review de cambios + content-type strict | S | % chunks aceptados rechazados por revisión humana / mes |
| Tool scoping BD | Tool sólo expone función `get_caso_by_id(id)` con `id` propio del usuario autenticado. Sin SELECT libre. | S | Auditoría: 100% queries con user_id en WHERE |
| Direct injection | LLM Guard input scanner + Llama Guard 3 sobre prompt final | M | ASR Garak `jailbreak` < 10% |
| Denial-of-wallet | Rate limit por email verificado + max_tokens=4 000 + budget cap 0,50€/usuario/día | S | Coste/usuario/día y alertas > 80% budget |

</details>

---

## Entregable

- DFD en PNG/PDF + tabla STRIDE-AI + tabla NIST + tabla controles en un único PDF.
- Bonus: extender STRIDE con "Detectability" como sexto eje (te dará pistas para los KPIs de SOC).
