"""
Catálogo estático del curso — metadata de los 10 módulos.
Los ficheros (PDF/PPTX/MD) se descubren en tiempo de ejecución desde el filesystem.
"""
import os
from pathlib import Path
from typing import Optional

_default = Path(__file__).resolve().parent.parent.parent
CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", str(_default)))

MODULE_META: list[dict] = [
    {
        "id": 1,
        "slug": "modulo1",
        "dir": "Modulo1",
        "title": "Fundamentos & Threat Modeling de IA",
        "subtitle": "MITRE ATLAS · NIST AI 100-2 · Superficie de ataque",
        "description": (
            "Taxonomía de amenazas a sistemas de IA, modelado de amenazas con MITRE ATLAS, "
            "marco NIST AI 100-2 (adversarial ML) y mapeo de superficie de ataque end-to-end."
        ),
        "icon": "target",
        "color": "#00ff88",
        "topics": [
            "MITRE ATLAS — TTPs adversariales",
            "NIST AI 100-2 — taxonomía formal",
            "Ciclo de vida MLOps y puntos de fallo",
            "Threat modeling STRIDE aplicado a IA",
        ],
    },
    {
        "id": 2,
        "slug": "modulo2",
        "dir": "Modulo2",
        "title": "Adversarial Machine Learning Clásico",
        "subtitle": "Evasión · Envenenamiento · Extracción · Inversión",
        "description": (
            "Ataques al modelo: ejemplos adversariales (FGSM, PGD, C&W), envenenamiento de datasets, "
            "extracción de modelos vía API, inversión de modelos y membership inference."
        ),
        "icon": "bug",
        "color": "#ff4757",
        "topics": [
            "Evasión: FGSM, PGD, Carlini-Wagner",
            "Envenenamiento de datos y backdoors (BadNets)",
            "Model extraction / model stealing",
            "Model inversion & membership inference",
            "Defensas: adversarial training, PATE, DP",
        ],
    },
    {
        "id": 3,
        "slug": "modulo3",
        "dir": "Modulo3",
        "title": "OWASP Top 10 para LLM 2025",
        "subtitle": "Prompt Injection · Jailbreaks · Leak de System Prompts",
        "description": (
            "Análisis exhaustivo del OWASP Top 10 LLM 2025: prompt injection directa/indirecta, "
            "jailbreaks, fuga de información, divulgación de secretos, denial-of-wallet."
        ),
        "icon": "shield-alert",
        "color": "#ffa502",
        "topics": [
            "LLM01 — Prompt Injection (directa e indirecta)",
            "LLM02 — Sensitive Information Disclosure",
            "LLM03 — Supply Chain",
            "LLM05 — Improper Output Handling",
            "LLM06 — Excessive Agency",
            "LLM10 — Unbounded Consumption (denial-of-wallet)",
        ],
    },
    {
        "id": 4,
        "slug": "modulo4",
        "dir": "Modulo4",
        "title": "Ataques a Agentes & RAG",
        "subtitle": "Tool Poisoning · Indirect Injection · Confused Deputy",
        "description": (
            "Vectores específicos en arquitecturas agénticas y RAG: envenenamiento de herramientas, "
            "inyección indirecta vía documentos recuperados, confused deputy, exfiltración encubierta."
        ),
        "icon": "git-branch",
        "color": "#a29bfe",
        "topics": [
            "Indirect prompt injection en RAG",
            "Tool poisoning (MCP & function calling)",
            "Confused deputy attacks",
            "ASCII smuggling y caracteres invisibles",
            "Exfiltración vía markdown / imágenes",
            "Defensas: spotlighting, structured queries",
        ],
    },
    {
        "id": 5,
        "slug": "modulo5",
        "dir": "Modulo5",
        "title": "Supply Chain ML & MLBOM",
        "subtitle": "Pickle RCE · Modelos troyanizados · HuggingFace · Firma",
        "description": (
            "Cadena de suministro en ML: ejecución de código vía pickle, modelos troyanizados, "
            "ataques en HuggingFace Hub, ML-BOM (CycloneDX 1.5), firma con Sigstore/Cosign."
        ),
        "icon": "package",
        "color": "#00d4ff",
        "topics": [
            "Pickle RCE en .pt / .pkl / .joblib",
            "Modelos troyanizados en HuggingFace",
            "Dependency confusion en PyPI ML",
            "MLBOM con CycloneDX 1.5",
            "Firma de modelos con Sigstore/Cosign",
            "Escaneo: Protect AI, ModelScan",
        ],
    },
    {
        "id": 6,
        "slug": "modulo6",
        "dir": "Modulo6",
        "title": "Guardrails & Defensa en Profundidad",
        "subtitle": "LLM Guard · NeMo · Llama Guard · Spotlighting",
        "description": (
            "Defensa multinivel para LLMs: filtros input/output, guardrails declarativos, "
            "clasificadores de seguridad, spotlighting de datos no confiables, sandboxing de tools."
        ),
        "icon": "shield",
        "color": "#fd79a8",
        "topics": [
            "LLM Guard (PII, prompt injection, jailbreaks)",
            "NVIDIA NeMo Guardrails (Colang)",
            "Meta Llama Guard 3 / Prompt Guard",
            "Microsoft Prompt Shields (Azure AI)",
            "Spotlighting y delimitación robusta",
            "Sandboxing de herramientas en agentes",
        ],
    },
    {
        "id": 7,
        "slug": "modulo7",
        "dir": "Modulo7",
        "title": "MLSecOps & Monitorización",
        "subtitle": "Drift · Observabilidad · Detección de abuso",
        "description": (
            "Operación segura: detección de drift adversarial, observabilidad de inferencia, "
            "rate limiting, detección de abuso, gestión de secretos, rotación de credenciales."
        ),
        "icon": "monitor",
        "color": "#00ff88",
        "topics": [
            "Detección de drift (adversarial vs natural)",
            "Observabilidad: Langfuse, Phoenix, Helicone",
            "Rate limiting & token budgeting",
            "Detección de abuso por embedding clustering",
            "Secrets management para LLMs",
            "Red teaming continuo",
        ],
    },
    {
        "id": 8,
        "slug": "modulo8",
        "dir": "Modulo8",
        "title": "Gobernanza & Cumplimiento",
        "subtitle": "NIST AI RMF · EU AI Act · ISO 42001 · ENS",
        "description": (
            "Marco regulatorio y de gestión: NIST AI Risk Management Framework, Reglamento UE de IA "
            "(2024/1689), ISO/IEC 42001, encaje con el ENS español y RGPD."
        ),
        "icon": "scale",
        "color": "#ffa502",
        "topics": [
            "NIST AI RMF 1.0 + perfil generativo",
            "EU AI Act — categorías de riesgo",
            "ISO/IEC 42001 (AI Management System)",
            "ISO/IEC 23894 (gestión de riesgo en IA)",
            "ENS (RD 311/2022) e IA",
            "Inventario y registro de modelos",
        ],
    },
    {
        "id": 9,
        "slug": "modulo9",
        "dir": "Modulo9",
        "title": "IA Defensiva — LLMs como herramienta Blue Team",
        "subtitle": "SOC · Threat Intel · Code Review · Phishing",
        "description": (
            "Uso ofensivo controlado de LLMs en defensa: triaje SOC, enriquecimiento de threat intel, "
            "revisión de código, análisis de logs, detección de phishing, generación de detecciones Sigma."
        ),
        "icon": "search",
        "color": "#00d4ff",
        "topics": [
            "Triage de alertas con LLM + RAG",
            "Threat intelligence assisted",
            "Code review automatizado (Semgrep + LLM)",
            "Análisis de logs y detección de anomalías",
            "Generación de reglas Sigma / YARA",
            "Riesgos: alucinaciones en contexto crítico",
        ],
    },
    {
        "id": 10,
        "slug": "modulo10",
        "dir": "Modulo10",
        "title": "Red Team de IA Automatizado",
        "subtitle": "PyRIT · Garak · Promptfoo · Fuzzing inteligente",
        "description": (
            "Frameworks automatizados de evaluación de seguridad en LLMs: PyRIT (Microsoft), "
            "Garak (NVIDIA), Promptfoo, fuzzing semántico, generación de payloads adversariales."
        ),
        "icon": "zap",
        "color": "#ff4757",
        "topics": [
            "Microsoft PyRIT — orquestación de ataques",
            "NVIDIA Garak — probes y detectores",
            "Promptfoo — testing como CI",
            "Fuzzing semántico (DeepFuzz, GPTFuzz)",
            "Generación de jailbreaks (PAIR, TAP)",
            "Reporting y métricas (ASR, refusal rate)",
        ],
    },
]

FILE_DESCRIPTIONS: dict[str, str] = {
    "README": "Guía teórica del módulo",
    "slides": "Diapositivas (Marp)",
    "ejercicio": "Ejercicio práctico",
    "solucion": "Solución del ejercicio",
    "bibliografia": "Referencias y lecturas adicionales",
}


def get_file_description(filename: str) -> Optional[str]:
    for key, desc in FILE_DESCRIPTIONS.items():
        if key.lower() in filename.lower():
            return desc
    return None
