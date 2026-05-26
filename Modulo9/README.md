# Módulo 9 — IA Defensiva: LLMs como herramienta Blue Team

> **Objetivo**: usar LLMs como copilot del equipo de seguridad — triaje SOC, threat intel, code review, generación de reglas Sigma/YARA — entendiendo riesgos (alucinaciones, fugas de datos) y aplicando mitigación.

---

## 9.1 Premisa: el LLM como copiloto, no como autoridad

El LLM **acelera** al analista, no le sustituye. La regla es:
- LLM propone, humano dispone.
- LLM agrega contexto, humano decide.
- Para acciones automáticas, threshold de confianza altísimo + auditoría completa.

Salirse de esta regla introduce los riesgos del módulo 6 (alucinaciones plausibles en contextos críticos).

---

## 9.2 Triage de alertas SOC con LLM + RAG

### Pipeline

```
alerta SIEM → enrich con contexto (logs ±2h, threat intel, runbook) →
LLM con sysprompt "tu rol es analista L1, propón TRIAGE: investigar/falso/escalar +
3 puntos clave + acciones inmediatas. NO inventes IOCs. Sólo cita los que veas en logs."
→ humano valida → SIRT/L2 si escalado
```

### Beneficios reales
- Tiempo de triage L1 de 15-20 min a 3-5 min.
- Menos fatiga por alert overload.
- Onboarding más rápido (LLM como mentor).

### Riesgos
- **Alucinaciones de IOCs** — LLM inventa IPs/hashes plausibles.
- **Falsa confianza** del analista junior que acepta el verdict sin revisar.
- **Leak de telemetry sensible** si el LLM es cloud sin DPA.

### Mitigaciones
- Grounding obligatorio: cada IOC en la respuesta debe estar literal en los logs.
- Post-validación regex: cualquier IOC mencionado debe aparecer en el contexto.
- LLM local (Ollama, vLLM) para datos sensibles.

---

## 9.3 Threat intelligence assisted

LLMs son útiles para:
- **Resumir reports** de threat intel largos.
- **Mapear** un IOC contra MITRE ATT&CK (qué técnica usa).
- **Correlacionar** múltiples reports sobre un mismo APT.
- **Traducir** advisories chinos/rusos rápidamente.

Riesgos similares: alucinaciones de TTPs no documentadas. Mitigación: RAG sobre fuentes verificadas (MITRE, CISA, ENISA, CCN-CERT).

---

## 9.4 Code review automatizado

### Patrón ganador

**Semgrep** (rules deterministas) detecta patrones sospechosos → **LLM** explica el riesgo en lenguaje natural + propone fix contextual.

```yaml
# .github/workflows/sec-review.yml
- run: semgrep --config p/security-audit --json > sg.json
- run: |
    python explain_with_llm.py sg.json | tee review.md
- uses: actions/upload-artifact@v4
  with: { name: review, path: review.md }
```

`explain_with_llm.py`:
```python
for finding in load_semgrep(json_path):
    code = read_file_lines(finding.path, finding.start, finding.end)
    prompt = f"""Te paso una alerta Semgrep y el código. Explica en 3 líneas:
    1) qué riesgo concreto representa,
    2) cómo lo arreglarías,
    3) ejemplo de patch (diff).
    Sólo razona con el código mostrado. No inventes contexto.

    Regla: {finding.rule_id}
    Mensaje: {finding.message}
    Código:
    ```
    {code}
    ```"""
    print(llm(prompt))
```

### Riesgo principal
LLM "explica" alertas falsos positivos como reales → ruido y desconfianza. Mitigación: pasar también un "negative example" en few-shot.

---

## 9.5 Análisis de logs y detección de anomalías

### Casos donde LLM aporta
- **Resumen ejecutivo** de un incidente a partir de timeline raw.
- **Hipótesis** de causa raíz a partir de stack trace + logs.
- **Generación de queries** SIEM (SPL Splunk, KQL Microsoft) en lenguaje natural.

### Casos donde NO aporta
- Detección de novedad pura (mejor algoritmos clásicos: isolation forest, autoencoders).
- Decisión final de incidente.

---

## 9.6 Generación de reglas Sigma / YARA

### Receta fiable

1. **RAG** sobre documentación Sigma oficial + ejemplos verificados.
2. **Few-shot** con 3-5 reglas similares correctas.
3. Input: descripción de la técnica + logs/IOCs concretos.
4. Output: regla Sigma como YAML.
5. **Validación sintáctica** con `sigma-cli` antes de aceptar.
6. **Validación funcional** ejecutando contra logs de prueba.

```python
prompt = f"""Genera una regla Sigma para detectar {tecnica}.
Contexto MITRE: {tecnica.mitre_id}.
Logs ejemplo donde aparece:
{logs}

Sigue el esquema Sigma (https://sigmahq.io). Usa selection blocks claros.
Tienes estos ejemplos correctos:
{few_shot_examples}

Output: solo YAML, sin explicación."""
```

---

## 9.7 Detección de phishing con LLM

LLMs son buenos extrayendo:
- **Indicadores semánticos** (urgencia artificial, errores sutiles, dominios homográficos).
- **Tono y estilo** comparados con baseline corporativo.
- **Indicios de personalización** (spear phishing).

Pipeline típico:
1. Email entra.
2. Reglas clásicas (DKIM, SPF, DMARC, listas).
3. Si no decide → LLM clasifica con score.
4. Si score > umbral → cuarentena + alerta.

Riesgo: el LLM puede ser engañado por phishing sofisticado que apela a estilo legítimo. **Nunca** confiar al 100%.

---

## 9.8 Patrones que NO funcionan (todavía)

- **"Pídele al LLM que sea pentester autónomo"** — ataques tipo Auto-GPT en seguridad: aún no fiables, falsos positivos altos.
- **"LLM como WAF"** — latencia + coste prohibitivos.
- **"LLM clasificando malware binario"** — sin tokenizer entrenado, malo.
- **"LLM como detector de fraude transaccional"** — modelos clásicos siguen ganando con margen.

---

## 9.9 Seguridad operacional: no envenenar tu propio uso

Si tú usas LLMs en tu workflow de seguridad, **eres vulnerable a indirect injection**:
- Un threat report puede contener prompt injection.
- Logs pueden llevar payloads que confundan al LLM.
- Comentarios en código pueden manipular el code review.

Mitigaciones:
- **Spotlighting** el contenido de terceros.
- **Sandbox** tools (el LLM no debe poder mandar emails, escribir BD, sin gate).
- **Output filter** anti-exfil (markdown stripping).

---

## 9.10 Modelos locales vs cloud para Blue Team

| Caso | Recomendación |
|---|---|
| Datos clasificados o PII pesada | **Local** (Ollama, vLLM, llama.cpp) |
| Volumen alto + datos no sensibles | Cloud con DPA + anonimización |
| Experimentación + iteración rápida | Cloud al inicio, on-prem al estabilizar |
| Compliance estricto (GDPR/ENS) | Local + audit completo |

Modelos open recomendados a 2026:
- **Llama 3.3 70B** — generalista, buen razonamiento.
- **Qwen 2.5 32B** — alternativa fuerte.
- **DeepSeek Coder V2** — código.
- **Llama Guard 3** — clasificación safety.

---

→ `ejercicio.md`: implementar triage de alertas SOC con un LLM local + RAG sobre runbooks.
