# Checklist pre-evento

## 48 horas antes
- [ ] Confirmar duración real con organizador (60/90/120 min).
- [ ] Confirmar perfil del público (dev / CISO / mixto / estudiantes).
- [ ] Confirmar requisitos técnicos del local (proyector, HDMI, wifi, mic).
- [ ] Enviar al organizador: requisitos wifi para asistentes + URL a compartir.
- [ ] Renderizar slides a PDF: `marp slides-charla.md --pdf -o slides.pdf`.
- [ ] Verificar slides en proyector remoto si es posible.

## 24 horas antes
- [ ] Ensayar las 2 demos completas, end-to-end.
- [ ] Grabar las 2 demos como **plan B** (Loom / vídeo local).
- [ ] Generar `cv_envenenado.pdf` con `demos/generar-pdf-malicioso.py`.
- [ ] Imprimir `kit-asistentes/resumen-2pp.md` (cantidad = asistentes + 20%).
- [ ] Generar QR codes (pretest, postest, repo, chatbot lab) — herramienta tipo qrserver.com.
- [ ] Crear formularios Google Forms basados en `formularios/*.md`.
- [ ] Cargar móvil y portátil.

## 2 horas antes
- [ ] `docker compose up -d lab-prompt-injection lab-rag-poisoning`.
- [ ] Verificar healthchecks: `docker compose ps`.
- [ ] Test endpoints:
  - `curl http://localhost:5001/health`
  - `curl -X POST http://localhost:5001/chat -H "Content-Type: application/json" -d '{"message":"test"}'`
  - `curl -F file=@cv_normal.pdf http://localhost:5002/analyze-cv`
- [ ] Conectar a wifi local + comprobar IP local (`ip addr` / `ifconfig`).
- [ ] Si los asistentes van a atacar el lab desde la red del evento, mapear puerto 5001 a IP local accesible.
- [ ] Llegar al local con 45 min de margen.

## 30 min antes
- [ ] Probar proyector + HDMI + audio.
- [ ] Abrir terminal, navegador con dashboard SecuAI (`http://localhost:8090`), slides PDF.
- [ ] Tener navegador en modo presentación.
- [ ] Saludar al organizador, confirmar horario exacto.
- [ ] **No abrir el chatbot vulnerable hasta empezar** (sorpresa).

## 5 min antes
- [ ] Lanzar pretest QR en pantalla.
- [ ] Beber agua.
- [ ] Respirar.

---

## Si algo va mal: prioridades

1. **Demo no funciona** → vídeo plan B + narración + slide con captura.
2. **No hay wifi para asistentes** → tú haces la demo, ellos miran. Sustituye práctica 1 por preguntas dirigidas.
3. **Tiempo se agota** → salta práctica 2, cierra con mensaje y QR a recursos.
4. **Pregunta que no sabes responder** → "buena pregunta, ¿alguien en la sala lo sabe? Si no, te respondo por email, déjame tu contacto."
