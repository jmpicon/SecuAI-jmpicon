# Playbook de defensa básico — primeros 90 días

> Para tu organización. Aplicable empieces de cero o con IA ya en producción.

---

## Día 0–7 — Inventario

### Acciones
1. **Identifica a quien sabe** dónde hay IA en tu org. Habla con: producto, datos, dev tools, customer success.
2. Crea **una hoja por cada sistema IA**: nombre, propósito, modelo usado, datos que toca, usuarios.
3. **Clasifica por riesgo aparente**: tools con efecto (escribe BD, envía, decide) > sólo lectura > sólo display.

### Entregable
Lista en Notion/Confluence/Sheets con todos los sistemas. **Sin esto, el resto no se puede priorizar**.

---

## Día 8–30 — Threat modeling de los top 3

Para los 3 con más riesgo aparente:

### 1. DFD con zonas de confianza
- Componentes: usuario, frontend, backend, vector DB, LLM, tools.
- Marca zonas (no confiable / intermedia / alta).

### 2. STRIDE-AI por componente
Una fila por componente:
| Componente | S | T | R | I | D | E | Técnica ATLAS |

### 3. Top 5 amenazas priorizadas
Con (goal, capability, knowledge, realista sí/no).

### 4. Top 5 controles propuestos
Cada uno con métrica de eficacia.

### Recurso
Plantilla en `Modulo1/ejercicio.md` del repo del curso.

---

## Día 31–60 — Quick wins defensivos

### Para cada uno de los top 3

1. **Rate limit + token budget** por usuario verificado.
2. **Input scanner LLM Guard** (mínimo: PromptInjection + Toxicity + Secrets).
3. **Output scanner** (mínimo: Sensitive + strip markdown externo).
4. **System prompt blindado**: sin secretos, sin lógica crítica.
5. **Audit log** estructurado de cada llamada.

### Tiempo realista
- LLM Guard básico: 1 día de trabajo + 2-3 días tuning thresholds.
- Audit log: 2 días si SIEM ya existe; 1 semana desde cero.

---

## Día 61–90 — Test continuo

### 1. Garak smoke suite en CI
- 5 probes (dan, promptinject, encoding, malwaregen, xss).
- Falla PR si ASR sube > 5% vs baseline.

### 2. Promptfoo regression tests
- 20-30 tests específicos de tu caso de uso.
- Run en cada PR + nightly.

### 3. Manual red team primera ronda
- Tú (o equipo) dedica 2 horas a romper el sistema con creatividad.
- Documenta lo que funciona → vuelvelo test automatizado.

### 4. Empieza tu observabilidad
- Langfuse o Phoenix on-prem.
- Mínimo: trace de cada llamada con coste y latencia.

---

## Después del día 90

| Cadencia | Actividad |
|---|---|
| Cada PR | Garak smoke + Promptfoo regression |
| Cada release | Garak full + report en release notes |
| Mensual | PyRIT campaign + red team manual creativo |
| Trimestral | Revisión de ASR/FPR de cada guardrail, retunear |
| Semestral | Revisión threat model (cambios en sistema = revisión) |
| Anual | Auditoría interna estilo ISO 42001 |

---

## Anti-patrones a evitar

- ❌ "Implementamos todo a la vez" → cargo cult, no escalable.
- ❌ "Lo arreglamos cuando pase algo" → reactivo, caro.
- ❌ "Compramos el producto X y ya está" → producto sin proceso = falsa seguridad.
- ❌ "El equipo de IA lo securiza" → seguridad no son los que construyen.

---

## Cuando contratar ayuda externa

- **Auditoría inicial** si nunca habéis hecho threat model de IA.
- **Red team manual** previo a despliegue público de un sistema crítico.
- **Cumplimiento** EU AI Act / ISO 42001 si vais a certificar.
- **Si no podéis dedicar al menos 1 FTE** a esto durante 6 meses.
