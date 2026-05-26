# Módulo 8 — Gobernanza & Cumplimiento

> **Objetivo**: dominar los marcos regulatorios y de gestión clave (NIST AI RMF, EU AI Act, ISO 42001, ISO 23894) y aprender a operacionalizarlos en la organización.

---

## 8.1 ¿Por qué gobernanza?

Sin gobernanza, todo lo anterior queda en buenas intenciones técnicas. La gobernanza:
- Define **roles y responsabilidades** (quién aprueba un modelo, quién audita).
- Establece **procesos repetibles** (DPIA, model card, sign-off).
- **Documenta** para cumplimiento y respuesta a incidentes.
- **Mide** la madurez del programa.

---

## 8.2 NIST AI Risk Management Framework 1.0

Voluntario, USA. Estructura el ciclo en 4 funciones:

```
                    ┌──────────────────┐
                    │     GOVERN       │   ← cultura, políticas, rolesrosles
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
       ┌─────────┐      ┌─────────┐      ┌─────────┐
       │   MAP   │ ───→ │ MEASURE │ ───→ │ MANAGE  │
       │ contexto│      │ riesgos │      │ mitigar │
       └─────────┘      └─────────┘      └─────────┘
```

### Subcategorías clave a memorizar
- **GOVERN-1.1** Liderazgo establece políticas.
- **GOVERN-4.1** Equipos AI con diversidad.
- **MAP-1.1** Contexto de uso documentado.
- **MAP-3.1** Riesgos identificados sobre stakeholders.
- **MEASURE-2.7** Validar antes de despliegue.
- **MANAGE-1.1** Priorizar riesgos y respuestas.

### Perfil GenAI (julio 2024)

NIST AI 600-1: extensión para GenAI con 12 riesgos transversales (CBRN, confabulation, data privacy, harmful bias, etc.) mapeados a las 4 funciones.

---

## 8.3 EU AI Act (Reglamento UE 2024/1689)

Reglamento (no directiva): aplicación directa en toda la UE. Vigencia: agosto 2024, aplicación progresiva hasta agosto 2026.

### Clasificación por riesgo

| Nivel | Ejemplos | Obligaciones |
|---|---|---|
| **Inaceptable** | Social scoring, manipulación subliminal | Prohibido |
| **Alto** | Sanidad, RRHH, justicia, infra crítica, biometría | CE marking, evaluación de conformidad, registro UE |
| **Limitado / transparencia** | Chatbots, deepfakes, IA generativa | Etiquetado claro |
| **Mínimo** | Filtros spam, NPCs videojuego | Sin obligaciones |
| **GPAI** | Modelos fundacionales (>10²⁵ FLOPs entrenamiento) | Transparencia, copyright, evaluación riesgos sistémicos |

### Plazos clave

- **Feb 2025**: prohibiciones (riesgo inaceptable) + AI literacy.
- **Ago 2025**: obligaciones GPAI + autoridades nacionales.
- **Ago 2026**: alto riesgo + resto.
- **Ago 2027**: alto riesgo embebido en productos regulados.

### Sanciones

- Hasta **35M€** o **7% volumen anual** por violar prohibiciones.
- Hasta **15M€** o **3%** por incumplir obligaciones de alto riesgo.

---

## 8.4 ISO/IEC 42001:2023 — AI Management System

Primer estándar internacional certificable para sistemas de gestión de IA. Estructura Annex SL (igual que ISO 27001).

### Estructura

- **4. Contexto** de la organización.
- **5. Liderazgo** (compromiso top-down).
- **6. Planificación** (riesgos, oportunidades, objetivos).
- **7. Apoyo** (recursos, competencias, comunicación).
- **8. Operación** (procesos AI: evaluación de impacto, desarrollo, uso).
- **9. Evaluación** (monitoreo, auditoría interna).
- **10. Mejora** (no conformidades, mejora continua).

### Annex A — 38 controles

Mapeable contra NIST AI RMF y EU AI Act. Cubre:
- A.2 Políticas relativas a IA.
- A.3 Estructura interna.
- A.4 Recursos.
- A.5 Evaluación de impacto de sistemas AI.
- A.6 Ciclo de vida del sistema AI.
- A.7 Datos para sistemas AI.
- A.8 Información para partes interesadas.
- A.9 Uso de sistemas AI.
- A.10 Relaciones con terceros.

### Cómo se certifica
Auditor externo acreditado. Ciclo similar a ISO 27001 (3 años + vigilancia anual).

---

## 8.5 ISO/IEC 23894:2023 — Gestión de riesgo en IA

Adaptación de ISO 31000 (riesgo general) a IA. No certificable, pero referenciado por ISO 42001.

Aporta:
- Vocabulario común.
- Proceso de risk assessment específico de IA.
- Mapping con NIST AI RMF.

---

## 8.6 ENS español (RD 311/2022) e IA

El Esquema Nacional de Seguridad **no menciona IA explícitamente**, pero **aplica completamente** a sistemas IA usados por:
- AA.PP. y entes del sector público.
- Proveedores con datos de la administración.

### Encaje
- Clasificar el sistema IA en las **5 dimensiones** (Confidencialidad, Integridad, Trazabilidad, Autenticidad, Disponibilidad).
- Aplicar **medidas** según nivel (BÁSICO/MEDIO/ALTO).
- Para sistemas con IA, especial atención a:
  - **mp.s.4** Aceptación y puesta en servicio (incluir evaluación AI).
  - **mp.info.5** Limpieza de documentos (output del LLM).
  - **op.exp.1** Inventario de activos (incluir modelos).
  - **op.mon.3** Vigilancia (logs de inferencia).

### Próximamente
CCN-CERT trabaja en una **guía CCN-STIC específica para IA** (esperada 2026).

---

## 8.7 RGPD aplicado a IA

Puntos críticos:
- **Art. 22** decisiones automatizadas con efectos jurídicos: derecho a no estar sujeto + intervención humana + explicación.
- **DPIA** (Data Protection Impact Assessment) obligatoria si hay alto riesgo (que casi siempre lo hay en IA con datos personales).
- **Minimización** y **propósito limitado** — difícil con entrenamiento masivo.
- **Derecho de supresión** — ¿cómo "olvidar" un dato del modelo entrenado? (machine unlearning emergente).

---

## 8.8 Mapeo entre marcos

| Concepto | NIST RMF | EU AI Act | ISO 42001 | ENS |
|---|---|---|---|---|
| Inventario modelos | GOVERN-1.6 | Art. 49 (registro UE alto riesgo) | A.6.2.2 | op.exp.1 |
| Evaluación riesgos | MAP-3 | Art. 9 (alto riesgo) | A.5 + A.6.2.4 | op.pl.1 |
| Documentación técnica | MANAGE-4 | Anexo IV | A.6 + A.8 | op.exp.6 |
| Logs | MEASURE-2 | Art. 12 | A.6.2.8 | op.exp.8 |
| Transparencia usuario | GOVERN-5 | Art. 52 | A.8 | mp.info.2 |

---

## 8.9 Inventario de modelos — mínimo viable

Una hoja por modelo (CSV/Notion/Confluence):

| Campo | Ejemplo |
|---|---|
| Modelo ID | `fraud-rf-v1.2.0` |
| Hash | `sha256:abc...` |
| Owner | María García |
| Caso de uso | Detección de fraude transaccional |
| Clasificación EU AI Act | Alto riesgo (financiero) |
| Dataset(s) | `fraud-train-2024-q1` |
| Métricas | Accuracy 92%, F1 0.87 |
| Fecha entreno | 2025-03-15 |
| Última revisión | 2026-01-20 |
| Próxima revisión | 2026-04-20 |
| Dependencias | scikit-learn 1.4.0, pandas 2.2.0 |
| ML-BOM URL | s3://bom/fraud-rf-v1.2.0.json |
| Cosign signature | s3://sig/fraud-rf-v1.2.0.sig |
| Estado | EN_PRODUCCION |

Sin este inventario, **ninguna** auditoría te aprueba.

---

## 8.10 Receta de implementación 12 meses

| Mes | Hito |
|---|---|
| 1 | Asignar AI governance owner. Política de uso de IA básica. |
| 2 | Inventario modelos (incluso si manual y minimalista). |
| 3 | DPIA / AI impact assessment de los modelos top 5. |
| 4 | NIST AI RMF gap analysis. |
| 5 | EU AI Act classification de cada uso. |
| 6 | ML-BOM + cosign para modelos en producción. |
| 7 | Suite Garak/Promptfoo en CI. |
| 8 | Guardrails (LLM Guard) en endpoints públicos. |
| 9 | Observabilidad (Langfuse) en endpoints públicos. |
| 10 | Runbook incidentes IA + entrenamiento equipo. |
| 11 | Auditoría interna ISO 42001-style. |
| 12 | Decidir certificación 42001 (o no) y plan año 2. |

---

→ `ejercicio.md`: clasificar 5 sistemas IA bajo EU AI Act y rellenar inventario.
