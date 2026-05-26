# Demo 2 — PDF envenenado (indirect injection) (7 min)

## Setup
```bash
docker compose up -d lab-rag-poisoning
python taller/demos/generar-pdf-malicioso.py   # genera cv_normal.pdf + cv_envenenado.pdf
```

## Ventanas
1. Visor PDF (Foxit / Adobe / sistema) con `cv_envenenado.pdf` abierto.
2. Terminal con curl listo.
3. **Opcional**: editor de texto con el código `generar-pdf-malicioso.py` visible (para la reveal).

---

## Guion

### Paso 1 — Caso de uso normal (1 min)
> "Imaginad un ATS (Applicant Tracking System) con IA. Recibe CVs y propone si contratar."

Mostrar visualmente `cv_normal.pdf` (candidato junior honesto, 1 año experiencia).

```bash
curl -F file=@cv_normal.pdf http://localhost:5002/analyze-cv | jq
```

Resultado esperado: `RECHAZAR`. "Funciona como toca."

### Paso 2 — El mismo CV pero envenenado (1 min)

Mostrar visualmente `cv_envenenado.pdf` en el visor PDF.
> "¿Veis algo raro? Yo tampoco. Subámoslo."

```bash
curl -F file=@cv_envenenado.pdf http://localhost:5002/analyze-cv | jq
```

Resultado: `CONTRATAR` + recomendación entusiasta.

**Reacción esperada**: confusión + curiosidad. "¿Qué ha pasado?"

### Paso 3 — La reveal (2 min)

Volver al visor PDF. Hacer **Ctrl+A** para seleccionar todo el texto.

→ El payload invisible **se selecciona y se ve resaltado**.

> "Aquí está. Texto blanco sobre fondo blanco. El humano que revisa el CV no lo ve. El LLM sí. Esto es **indirect prompt injection** — OWASP LLM01 segunda variante."

### Paso 4 — Casos reales (2 min)

> "Pensad que esto puede ir en:
> - Una página web que vuestro asistente resume.
> - Un email que vuestro filtro IA categoriza.
> - Un documento de Confluence que el bot interno consulta.
> - Una hoja Excel compartida en Drive.
>
> **Casos reales documentados**:
> - Bing Chat 2023 — payload en abstract de arxiv.
> - Slack AI 2024 — payload en canal público.
> - Google Drive summarizer 2024 — payload en hoja compartida."

### Paso 5 — Pivote a defensas (1 min)

> "Si pensáis 'mi WAF lo pillaría', no. El WAF no ve dentro del PDF. Si pensáis 'mi DLP', tampoco — el texto pasa por canales normales."
>
> "Lo que sí funciona: spotlighting. Vamos a verlo."

---

## Plan B
- Vídeo grabado de la diferencia entre `cv_normal.pdf` y `cv_envenenado.pdf`.
- Si fallan curls: mostrar captura del payload en el PDF + captura de respuesta esperada.

---

## Para activar defensa en la misma demo (opcional)

```bash
# Activar spotlighting en el lab
curl -X POST http://localhost:5002/toggle-spotlight

# Re-enviar
curl -F file=@cv_envenenado.pdf http://localhost:5002/analyze-cv | jq
```

→ Resultado: típicamente bloqueado o analizado honestamente. "Esto es **spotlighting**: marcamos los datos como no confiables a nivel estructural."

(Nuestro lab simula que spotlighting bloquea ~70% de ataques. Realista para modelos actuales.)
