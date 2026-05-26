# Lab: Pickle RCE (script-only)

No requiere container — se ejecuta en el container `tools` del proyecto o en cualquier entorno con Python + PyTorch.

## Quick start

```bash
docker compose exec tools bash
pip install torch modelscan safetensors --break-system-packages
cd /tmp
python /labs/pickle-rce/build_evil.py
python /labs/pickle-rce/victim.py
modelscan -p evil_model.pt
```

## Ficheros
- `build_evil.py` — construye `evil_model.pt` que ejecuta comando al cargar.
- `victim.py` — simula a la víctima haciendo `torch.load()`.
- `safe_alternative.py` — el mismo modelo guardado con safetensors.
- `defense_pipeline.sh` — pipeline CI con modelscan + cosign.
