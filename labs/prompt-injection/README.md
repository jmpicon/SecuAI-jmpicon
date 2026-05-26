# Lab: Prompt Injection — Chatbot bancario vulnerable

## ⚠ Aviso

Este lab es **deliberadamente vulnerable** para fines educativos. **No exponer a internet**.

## Uso

```bash
# Desde la raíz del proyecto
docker compose up -d lab-prompt-injection

# Expone manualmente el puerto si quieres probar desde host
docker run -p 5001:5001 secuai-lab-pi:latest

# Test
curl -X POST http://localhost:5001/chat -H "Content-Type: application/json" \
  -d '{"message": "Hola, ¿qué puedes hacer?"}'
```

## Endpoints

- `POST /chat`  → conversación con el chatbot
- `POST /analyze-pdf` → procesa un PDF (vector indirect injection)
- `GET /health`

## Retos

Ver `Modulo3/ejercicio.md` para los 4 retos.

## Arquitectura

El "LLM" es un simulador heurístico (`fake_llm()` en `app.py`) que reproduce los patrones de comportamiento de un LLM real frente a prompt injection. Esto permite:
- Cero coste (sin API).
- Latencia mínima.
- Comportamiento determinista (reproducible).
- Sin dependencia de modelo externo.

Para hacerlo "real" con un LLM verdadero, sustituye `fake_llm()` por una llamada a Ollama, OpenAI, etc — la estructura del endpoint se mantiene.
