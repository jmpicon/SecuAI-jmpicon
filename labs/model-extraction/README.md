# Lab: Model Extraction

## Uso

```bash
docker compose up -d lab-model-extraction
curl -X POST http://lab-model-extraction:5003/predict \
  -H "Content-Type: application/json" -d '{"features": [0.5, 0.3]}'
```

## Reto

Extraer un sustituto `F̃` que aproxime al modelo víctima haciendo queries.

### Receta básica (Knockoff Nets simplificado)

```python
import numpy as np, requests
from sklearn.neural_network import MLPClassifier

# 1. Genera N samples random en el espacio
N = 5000
X_probe = np.random.uniform(-2, 3, size=(N, 2))

# 2. Consulta la API víctima
y_probe = []
for x in X_probe:
    r = requests.post("http://lab-model-extraction:5003/predict",
                      json={"features": x.tolist()})
    y_probe.append(r.json()["prediction"])
y_probe = np.array(y_probe)

# 3. Entrena sustituto
substitute = MLPClassifier(hidden_layer_sizes=(32, 32), max_iter=400)
substitute.fit(X_probe, y_probe)

# 4. Mide agreement con la víctima en un nuevo test set
X_test = np.random.uniform(-2, 3, size=(1000, 2))
y_test_victim = [requests.post("http://lab-model-extraction:5003/predict",
                                json={"features": x.tolist()}).json()["prediction"]
                 for x in X_test]
agreement = (substitute.predict(X_test) == np.array(y_test_victim)).mean()
print(f"Agreement: {agreement:.3f}")
```

## Defensas a probar

```bash
# Activar rate limit
curl -X POST http://lab-model-extraction:5003/admin/toggle-rate-limit

# Ocultar probabilidades
curl -X POST http://lab-model-extraction:5003/admin/toggle-probs
```

Re-ejecuta la extracción con cada defensa. Comparar agreement.
