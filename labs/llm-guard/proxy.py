"""Proxy con guardrails delante del chatbot vulnerable."""
import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    from llm_guard import scan_prompt, scan_output
    from llm_guard.input_scanners import PromptInjection, Toxicity, Secrets
    from llm_guard.output_scanners import Sensitive, NoRefusal
    HAS_LLM_GUARD = True
except ImportError:
    HAS_LLM_GUARD = False


app = FastAPI(title="LLM Guard proxy")

if HAS_LLM_GUARD:
    INPUT_SCANNERS  = [PromptInjection(threshold=0.5), Toxicity(threshold=0.7), Secrets()]
    OUTPUT_SCANNERS = [Sensitive(), NoRefusal()]
else:
    INPUT_SCANNERS = OUTPUT_SCANNERS = []

TARGET = os.environ.get("TARGET", "http://lab-prompt-injection:5001/chat")


class Req(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok", "guard": HAS_LLM_GUARD, "target": TARGET}


@app.post("/chat")
async def chat(req: Req):
    if HAS_LLM_GUARD:
        sanitized, _, risk_in = scan_prompt(INPUT_SCANNERS, req.message)
        if risk_in > 0.5:
            return {"response": "[BLOQUEADO] Filtro de entrada", "blocked_in": True}
    else:
        sanitized, risk_in = req.message, 0.0

    async with httpx.AsyncClient(timeout=30) as cli:
        try:
            r = await cli.post(TARGET, json={"message": sanitized})
        except httpx.HTTPError as e:
            raise HTTPException(502, f"Target unreachable: {e}")

    resp_text = r.json().get("response", "")

    if HAS_LLM_GUARD:
        sanitized_resp, _, risk_out = scan_output(OUTPUT_SCANNERS, sanitized, resp_text)
        if risk_out > 0.5:
            return {"response": "[BLOQUEADO] Filtro de salida", "blocked_out": True}
        return {"response": sanitized_resp, "risk_in": risk_in, "risk_out": risk_out}

    return {"response": resp_text}
