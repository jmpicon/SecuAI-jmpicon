# Ejercicio M8 — Clasificación EU AI Act + Inventario

## Parte A — Clasifica 5 sistemas (30 min)

Para cada uno, decide nivel de riesgo EU AI Act y justifica:

| # | Sistema | Tu clasificación | Justificación |
|---|---|---|---|
| 1 | Chatbot de soporte de Telco que responde sobre tarifas | | |
| 2 | Asistente IA en hospital que sugiere diagnóstico a médico | | |
| 3 | Sistema de scoring de CV para preseleccionar candidatos | | |
| 4 | Generador de imágenes para marketing | | |
| 5 | Identificación biométrica para acceso a centro deportivo | | |

---

## Parte B — Rellena inventario para 2 modelos reales (30 min)

Elige 2 modelos open-source reales (HuggingFace) y rellena la plantilla del README §8.9 para cada uno:

- Hash real del modelo (`sha256sum`).
- Métricas reportadas en el model card.
- Clasificación EU AI Act según un uso hipotético que asignes.
- Dependencias críticas (mira el `requirements.txt` o equivalente).
- ML-BOM mínimo en JSON.

---

## Parte C — Gap analysis NIST AI RMF (45 min)

Para tu organización (real o ficticia que conozcas bien), evalúa madurez en NIST AI RMF:

Para cada función (GOVERN, MAP, MEASURE, MANAGE), nivel 0-3:
- 0 = no existe
- 1 = ad-hoc
- 2 = documentado
- 3 = medido y revisado

Identifica las **3 brechas principales** y propón un plan de cierre a 6 meses.

---

# 🔓 Solución de referencia Parte A

<details>
<summary>Mira tras intentarlo</summary>

| # | Sistema | Clasificación | Por qué |
|---|---|---|---|
| 1 | Chatbot soporte Telco | **Limitado/transparencia** | Debe identificarse como bot (Art. 50). Sin más obligaciones si no toma decisiones materiales. |
| 2 | Asistente diagnóstico médico | **ALTO RIESGO** | Anexo III, área sanidad. CE marking, evaluación de conformidad, log obligatorio, supervisión humana, robustez. |
| 3 | Scoring de CVs | **ALTO RIESGO** | Anexo III §4, "employment, workers management" — empleo. Mismas obligaciones que sanidad. |
| 4 | Generador imágenes marketing | **Limitado/transparencia** | Si es deepfake o IA generativa, etiquetado obligatorio. Sin más si es para activos puramente comerciales. |
| 5 | Identificación biométrica acceso gimnasio | **ALTO RIESGO o INACEPTABLE** | Biometría remota en tiempo real en espacios accesibles al público → INACEPTABLE (Art. 5) con excepciones muy limitadas. Para acceso de socios identificados: ALTO RIESGO. |

</details>

---

## Entregable

PDF de 5-8 páginas:
- Parte A: tabla rellena.
- Parte B: 2 fichas inventario + 2 ML-BOM JSON.
- Parte C: matriz NIST + plan de cierre.
