# Taller: "Hackeando la IA — del prompt injection a las defensas reales"

> Formato 90 minutos, técnico/intermedio, 10-80 asistentes.
> Material listo para impartir: guion, slides, demos, prácticas y kit de asistente.

---

## Estructura del directorio

```
taller/
├── README.md                 ← este fichero
├── guion-ponente.md          ← script minuto a minuto del ponente
├── slides-charla.md          ← slides Marp (renderizar a PDF para proyectar)
├── checklist-pre-evento.md   ← preparación día anterior y hora antes
├── checklist-evento.md       ← chequeo durante la charla
├── demos/                    ← scripts de las 2 demos en vivo
│   ├── demo1-prompt-injection.md
│   ├── demo2-pdf-envenenado.md
│   └── generar-pdf-malicioso.py
├── formularios/              ← cuestionarios pre/post + valoración
│   ├── pretest.md
│   ├── postest.md
│   └── valoracion.md
└── kit-asistentes/           ← material a entregar
    ├── resumen-2pp.md
    ├── recursos-aprender-mas.md
    └── playbook-defensa-basico.md
```

---

## Cómo usar este material

### Para preparar
1. Lee **guion-ponente.md** entero.
2. Renderiza las slides: `marp slides-charla.md --pdf -o slides-charla.pdf`.
3. Ensaya las 2 demos en `demos/` al menos 2 veces.
4. Imprime el `kit-asistentes/resumen-2pp.md` (1 por asistente).
5. Sube los formularios a Google Forms/Typeform (links opcionales).
6. Ten arrancados los labs Docker (prompt-injection + rag-poisoning).

### El día del evento
1. **Una hora antes**: checklist-pre-evento.md.
2. **Al empezar**: pretest (link QR — 1 min).
3. **Durante**: sigue el guion. Las prácticas usan el chatbot del lab vía QR.
4. **Al final**: postest + valoración. Reparte resumen 2pp.

### Adaptar duración
- **60 min**: salta la pausa, recorta práctica 2 a 5 min.
- **120 min**: añade demo 3 (Garak en vivo) y profundiza en defensas.
- **45 min**: reduce a teoría + 1 demo + 1 práctica (skip prácticas grupales).

---

## Requisitos técnicos

### Mínimo
- Portátil con Docker.
- Proyector.
- Wifi para asistentes (o hotspot ponente).

### Recomendado
- HDMI + display secundario para terminal/demos.
- Micrófono.
- Pizarra o paperboard para esquema en vivo.

### Para asistentes (si participan)
- Portátil o móvil con navegador.
- Wifi del evento.

---

## Coste del taller

- **Cero** si usas los labs locales (todo Docker, sin API externa).
- Si quieres usar LLMs reales en demos: ~5€ de créditos OpenAI/Anthropic.

---

## Variantes de público

| Público | Énfasis | Demo recomendada |
|---|---|---|
| Devs / DevOps | Defensas, supply chain, MLBOM | demo1 + Garak en vivo |
| CISO / Compliance | EU AI Act, ISO 42001, riesgo de negocio | demo1 + caso real Hong Kong |
| Estudiantes | Ataques, espectacularidad, manos a la obra | demo1 + práctica intensiva |
| Stakeholders ejecutivos | Caso de negocio, ROI defensa, ejemplos reputacionales | sólo demo1 + numbers |

---

## Recordatorio ético

Este taller enseña ataques **para mostrar cómo defenderse**. Recuérdaselo al cierre:
- No atacar sistemas reales sin autorización.
- Reportar vulnerabilidades responsablemente.
- Los labs son educativos, en entornos aislados.
