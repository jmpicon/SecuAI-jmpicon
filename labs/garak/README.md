# Lab: NVIDIA Garak

Lab basado en script — sin container propio. Se ejecuta desde el container `tools` o cualquier entorno con Python 3.10+.

## Quick start

```bash
docker compose exec tools bash
pip install garak --break-system-packages
```

## Receta 1 — Scan contra modelo HuggingFace pequeño (5 min)

```bash
garak --model_type huggingface --model_name distilgpt2 \
      --probes dan.Dan_6_0,promptinject \
      --report_prefix smoke
# abre smoke.report.html
```

## Receta 2 — Scan contra Ollama local

```bash
ollama pull llama3.2:1b
garak --model_type ollama --model_name llama3.2:1b \
      --probes dan,malwaregen,encoding \
      --report_prefix ollama-test
```

## Receta 3 — Scan contra endpoint REST (nuestro lab vulnerable)

```bash
cat > rest_config.json <<'EOF'
{
  "rest": {
    "name": "lab-pi",
    "uri": "http://lab-prompt-injection:5001/chat",
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "req_template_json_object": {"message": "$INPUT"},
    "response_json_field": "response"
  }
}
EOF

garak --model_type rest --generator_option_file rest_config.json \
      --probes dan,promptinject,encoding,malwaregen \
      --report_prefix lab-baseline
```

## Receta 4 — Comparar antes/después de guardrails

```bash
# 1. Activa el lab sin guardrails y mide
garak ... --report_prefix sin-guardrails

# 2. Activa LLM Guard (ver lab/llm-guard)
# 3. Vuelve a medir
garak ... --report_prefix con-guardrails

# 4. Diff (script propio)
python compare_reports.py sin-guardrails.report.jsonl con-guardrails.report.jsonl
```

## Probes recomendadas para empezar

| Probe | Descripción |
|---|---|
| `dan` | Jailbreaks DAN family |
| `promptinject` | Prompt injection clásicos |
| `encoding` | Bypass por encoding (base64, leet) |
| `malwaregen` | Intentos de generar malware |
| `realtoxicityprompts` | Toxicidad |
| `latentinjection` | Indirect injection (necesita endpoint con RAG) |
| `xss` | Generar código XSS |
| `divergence` | "Repeat forever" → leak |

## CI integration

Ver `Modulo10/ejercicio.md` parte 5 para integración GitHub Actions.
