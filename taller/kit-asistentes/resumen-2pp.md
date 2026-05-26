# Hackeando la IA — resumen 2 páginas

> Material para que el asistente se lleve. Imprime A4 doble cara.

---

## Lo esencial

La IA generativa rompe los supuestos de la seguridad clásica:
- El modelo es **código + datos + output probabilístico**.
- Un PDF/web/email puede ser **código ejecutable** para el LLM.
- No hay frontera clara entre instrucciones del desarrollador y datos del usuario.

→ Necesita su propio modelo de amenazas: **MITRE ATLAS · NIST AI 100-2 · OWASP LLM Top 10**.

---

## OWASP Top 10 LLM 2025 — los 5 a recordar

1. **LLM01 — Prompt Injection**: directa (usuario) o indirecta (datos consumidos).
2. **LLM02 — Sensitive Information Disclosure**: leak de PII, secretos, system prompt.
3. **LLM05 — Improper Output Handling**: el output del LLM se inyecta en SQL/HTML/exec → XSS/SQLi/RCE.
4. **LLM06 — Excessive Agency**: tools con más capacidad de la necesaria.
5. **LLM10 — Unbounded Consumption**: denial-of-wallet, abuso económico.

---

## La pila defensiva en profundidad

```
Auth → Rate limit →
   Input scanner (LLM Guard) →
      Classifier (Llama Guard 3) →
         System prompt blindado (sin secretos) →
            LLM principal →
               Output scanner (PII, code, markdown) →
                  Sandbox tools + HITL crítico →
                     Audit + observability (Langfuse)
```

→ **No** hay bala de plata. Capas que suman.

---

## 5 acciones para el lunes

1. **Inventaría** todos los sistemas IA en tu organización (incluso PoCs).
2. **Threat model** ATLAS + NIST sobre los 3 más expuestos a usuarios externos.
3. **Suite Garak** smoke en CI (15 min de setup).
4. **LLM Guard** delante del endpoint público más sensible.
5. **Rate limit + token budget** por usuario en todos.

---

## Lo que NO funciona

- ❌ Filtros regex puros — bypass infinito.
- ❌ Confiar en el delimitador del system prompt.
- ❌ "Lo evaluamos con benchmarks una vez al año".
- ❌ Asumir que tu proveedor de LLM te protege end-to-end.

---

## Marco regulatorio que llega

| Norma | Estado | Aplica a |
|---|---|---|
| **EU AI Act** (Reg 2024/1689) | Aplicación progresiva 2025-27 | Toda IA en mercado UE |
| **NIST AI RMF 1.0** | Vigente, voluntario | Marco internacional |
| **ISO/IEC 42001:2023** | Certificable | AI Management System |
| **ENS RD 311/2022** | Vigente | Sector público español |

Sanciones EU AI Act: hasta **35M€ o 7% turnover** por violar prohibiciones.

---

## Para profundizar

- **Curso completo** (10 módulos + labs + slides): https://github.com/jmpicon/secu_IA
- **MITRE ATLAS**: https://atlas.mitre.org
- **OWASP LLM Top 10**: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- **NIST AI 100-2 (2025)**: https://csrc.nist.gov/pubs/ai/100/2/e2025/final
- **EU AI Act**: https://eur-lex.europa.eu/eli/reg/2024/1689/oj

## Herramientas mencionadas

- **LLM Guard**: https://llm-guard.com
- **NeMo Guardrails** (NVIDIA): https://github.com/NVIDIA/NeMo-Guardrails
- **Llama Guard 3** (Meta): https://huggingface.co/meta-llama/Llama-Guard-3-8B
- **Garak** (NVIDIA): https://github.com/leondz/garak
- **PyRIT** (Microsoft): https://github.com/Azure/PyRIT
- **Promptfoo**: https://promptfoo.dev
- **ModelScan** (Protect AI): https://github.com/protectai/modelscan
- **Langfuse**: https://langfuse.com

---

**Contacto del ponente**: jose.bobal@gmail.com · José Picón (jmpicon)
