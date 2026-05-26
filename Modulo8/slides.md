---
marp: true
theme: gaia
class: invert
paginate: true
header: 'SecuAI · Módulo 8'
footer: 'Gobernanza & Cumplimiento'
---

<!-- _class: lead invert -->

# **Gobernanza** & Cumplimiento

Módulo 8 · SecuAI

NIST AI RMF · EU AI Act · ISO 42001 · ENS

---

## NIST AI RMF 1.0

```
              GOVERN
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
      MAP → MEASURE → MANAGE
```

Voluntario, USA. Profile GenAI (NIST AI 600-1) extiende para LLMs.

---

## EU AI Act — clasificación por riesgo

| Nivel | Obligaciones |
|---|---|
| **Inaceptable** | Prohibido |
| **Alto** | CE, conformidad, registro, log |
| **Limitado** | Transparencia |
| **Mínimo** | Sin obligaciones |
| **GPAI** | Transparencia + copyright + riesgo sistémico |

Sanciones: hasta **35M€** o **7%** turnover.

---

## EU AI Act — plazos

| Fecha | Qué |
|---|---|
| Feb 2025 | Prohibiciones + AI literacy |
| Ago 2025 | GPAI + autoridades |
| Ago 2026 | Alto riesgo + resto |
| Ago 2027 | Alto riesgo embebido en productos regulados |

---

## ISO/IEC 42001:2023

Primer estándar internacional **certificable** para AIMS.

Annex SL (igual que 27001).

Annex A: 38 controles → mapeables a NIST + EU AI Act.

---

## ENS español (RD 311/2022)

5 dimensiones: **C**onfidencialidad, **I**ntegridad, **T**razabilidad, **A**utenticidad, **D**isponibilidad.

Aplica a IA en AAPP (sin mencionarla explícitamente).

Próximo: guía CCN-STIC IA (2026).

---

## RGPD aplicado a IA

- **Art. 22**: decisiones automatizadas → explicación + intervención humana.
- **DPIA** obligatoria.
- **Minimización** difícil con training masivo.
- **Derecho de supresión** ↔ machine unlearning.

---

## Mapeo entre marcos

| Concepto | NIST | EU AI Act | ISO 42001 | ENS |
|---|---|---|---|---|
| Inventario | GOVERN-1.6 | Art. 49 | A.6.2.2 | op.exp.1 |
| Risk eval | MAP-3 | Art. 9 | A.5 | op.pl.1 |
| Docs | MANAGE-4 | Anexo IV | A.6 | op.exp.6 |
| Logs | MEASURE-2 | Art. 12 | A.6.2.8 | op.exp.8 |

---

## Inventario mínimo

Una fila por modelo: ID, hash, owner, caso de uso, clasificación EU AI Act, dataset, métricas, fechas, ML-BOM, firma.

**Sin inventario, ninguna auditoría te aprueba.**

---

## Plan 12 meses

| Mes | Hito |
|---|---|
| 1 | Owner + política básica |
| 2 | Inventario |
| 3 | DPIA top 5 |
| 4 | NIST gap analysis |
| 6 | ML-BOM + cosign |
| 7 | Garak en CI |
| 8 | Guardrails público |
| 11 | Auditoría interna |
| 12 | Decisión certificación |

---

<!-- _class: lead invert -->

## Lab

Clasificar 5 sistemas + 2 fichas inventario

→ `Modulo8/ejercicio.md`
