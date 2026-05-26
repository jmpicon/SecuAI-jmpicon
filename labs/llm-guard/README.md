# Lab: LLM Guard (defensa para chatbot)

Lab de script — envuelve el chatbot vulnerable del lab `prompt-injection` con guardrails.

## Setup

```bash
docker compose exec tools bash
pip install llm-guard --break-system-packages
```

## Receta — Proxy con guardrails

`proxy.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from llm_guard import scan_prompt, scan_output
from llm_guard.input_scanners import PromptInjection, Toxicity, Secrets
from llm_guard.output_scanners import Sensitive, NoRefusal

app = FastAPI()
input_scanners = [PromptInjection(threshold=0.5), Toxicity(threshold=0.7), Secrets()]
output_scanners = [Sensitive(), NoRefusal()]
TARGET = "http://lab-prompt-injection:5001/chat"


class Req(BaseModel):
    message: str


@app.post("/chat")
async def chat(req: Req):
    sanitized, _, risk_in = scan_prompt(input_scanners, req.message)
    if risk_in > 0.5:
        raise HTTPException(400, "Bloqueado por filtro de entrada")
    async with httpx.AsyncClient() as cli:
        r = await cli.post(TARGET, json={"message": sanitized})
    resp = r.json()["response"]
    sanitized_resp, _, risk_out = scan_output(output_scanners, sanitized, resp)
    if risk_out > 0.5:
        return {"response": "Respuesta bloqueada por filtro de salida", "blocked": True}
    return {"response": sanitized_resp, "risk_in": risk_in, "risk_out": risk_out}


# uvicorn proxy:app --host 0.0.0.0 --port 5101
```

Lanza el proxy en `:5101`. Ataca al puerto 5101 (con guardrails) y al 5001 (sin) y compara.

## Mide ASR con Garak

```bash
# Sin guardrails
garak --model_type rest --uri http://lab-prompt-injection:5001/chat ...

# Con guardrails
garak --model_type rest --uri http://localhost:5101/chat ...
```

Comparar reports.

## Tuning de thresholds

- Threshold demasiado bajo → muchos falsos positivos.
- Threshold demasiado alto → poco bloqueo real.

Inicia en 0.5 y mide FPR contra 20 prompts legítimos. Ajusta.
