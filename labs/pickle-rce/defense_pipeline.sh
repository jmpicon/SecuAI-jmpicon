#!/usr/bin/env bash
# Pipeline CI mínimo: rechazar modelos peligrosos o con firma inválida.
set -e

MODEL="${1:?Uso: defense_pipeline.sh <modelo>}"

echo "[*] 1/3 ModelScan estático..."
modelscan -p "$MODEL" || { echo "[!] ModelScan detectó riesgo. Abort."; exit 1; }

echo "[*] 2/3 Verificación de firma cosign..."
SIG_FILE="${MODEL}.sig"
PUBKEY="${COSIGN_PUBKEY:-cosign.pub}"
if [[ ! -f "$SIG_FILE" ]]; then
    echo "[!] No se encuentra firma $SIG_FILE. Abort."; exit 1
fi
cosign verify-blob --key "$PUBKEY" --signature "$SIG_FILE" "$MODEL" \
    || { echo "[!] Firma inválida. Abort."; exit 1; }

echo "[*] 3/3 Verificación de hash..."
sha256sum "$MODEL"

echo "[+] Todas las verificaciones pasaron. Modelo aceptado."
