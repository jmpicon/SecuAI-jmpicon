"""
Lab: API víctima para extraction attack.

Sirve un clasificador entrenado en sklearn moons.
Endpoint /predict devuelve clase + (opcionalmente) probabilidad.

Objetivo del estudiante: extraer un sustituto F̃ haciendo queries.
"""
import os
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.datasets import make_moons
from sklearn.neural_network import MLPClassifier

app = FastAPI(title="Lab Victim — Model Extraction")

# Entrenar el modelo víctima al arrancar
X, y = make_moons(n_samples=2000, noise=0.15, random_state=42)
VICTIM = MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=400, random_state=42)
VICTIM.fit(X, y)

# Estado: control de rate limit y exposición de probabilidades
RATE_LIMIT_ENABLED = False
EXPOSE_PROBS = True

_query_count = 0


class PredictRequest(BaseModel):
    features: list[float] = Field(..., min_length=2, max_length=2)


@app.get("/health")
def health():
    return {"status": "ok", "queries": _query_count}


@app.post("/predict")
def predict(req: PredictRequest):
    global _query_count
    if RATE_LIMIT_ENABLED and _query_count > 5000:
        raise HTTPException(429, "Rate limit (anti-extraction)")
    _query_count += 1
    x = np.array([req.features])
    pred = int(VICTIM.predict(x)[0])
    if EXPOSE_PROBS:
        probs = VICTIM.predict_proba(x)[0].tolist()
        return {"prediction": pred, "probs": probs}
    return {"prediction": pred}


@app.post("/admin/toggle-rate-limit")
def toggle_rate_limit():
    global RATE_LIMIT_ENABLED
    RATE_LIMIT_ENABLED = not RATE_LIMIT_ENABLED
    return {"rate_limit": RATE_LIMIT_ENABLED}


@app.post("/admin/toggle-probs")
def toggle_probs():
    global EXPOSE_PROBS
    EXPOSE_PROBS = not EXPOSE_PROBS
    return {"expose_probs": EXPOSE_PROBS}


@app.get("/")
def root():
    return {
        "name": "Lab víctima de model extraction",
        "endpoints": ["POST /predict", "POST /admin/toggle-rate-limit", "POST /admin/toggle-probs"],
        "defaults": {"rate_limit": RATE_LIMIT_ENABLED, "expose_probs": EXPOSE_PROBS},
        "dataset": "make_moons",
    }
