# Glosario — Securización de IA

Términos esenciales que aparecen a lo largo del curso. Orden alfabético.

---

**Adversarial example** — Input modificado mínimamente para forzar una predicción errónea en un modelo de ML. Suele ser imperceptible al humano.

**AI Act (EU)** — Reglamento UE 2024/1689 que regula sistemas de IA en el mercado europeo según nivel de riesgo (inaceptable, alto, limitado, mínimo + obligaciones GPAI).

**Alignment** — Proceso de entrenar un LLM (RLHF, DPO, Constitutional AI) para que siga políticas de seguridad y utilidad.

**ASCII smuggling** — Uso de caracteres Unicode invisibles (Tags U+E0000..., variation selectors) para ocultar instrucciones que el LLM lee pero el humano no.

**ASR (Attack Success Rate)** — Métrica clave: % de intentos adversariales que consiguen el comportamiento prohibido.

**ATLAS** — MITRE Adversarial Threat Landscape for AI Systems. Matriz de TTPs específica para IA, análoga a ATT&CK.

**BadNets** — Ataque de envenenamiento que inserta un trigger visual en el dataset para activar clasificación errónea predecible.

**Carlini-Wagner (C&W)** — Familia de ataques de evasión que minimizan la perturbación necesaria para causar misclasificación.

**Confused deputy** — Patrón clásico: programa con privilegios elevados ejecuta acciones por orden de usuario con menos privilegios sin verificar. Reaparece en agentes IA.

**Cosign** — Herramienta de Sigstore para firmar y verificar artefactos (contenedores, modelos) keyless OIDC.

**Crescendo** — Estrategia de jailbreak multi-turn: escalada conversacional gradual desde inocuo hasta objetivo prohibido.

**CycloneDX 1.5** — Estándar SBOM que en su versión 1.5 introduce componentes ML (modelos, datasets) → base del ML-BOM.

**DAN (Do Anything Now)** — Familia de jailbreaks role-play que intentan convencer al LLM de ignorar restricciones.

**Differential Privacy (DP)** — Garantía matemática (ε, δ) sobre cuánto puede el output revelar acerca de un individuo del dataset. DP-SGD aplica DP al entrenamiento.

**DPIA** — Data Protection Impact Assessment. Obligatorio bajo RGPD para procesamientos de alto riesgo, casi siempre lo son los sistemas IA con datos personales.

**Drift** — Cambio en la distribución de inputs o relación input/output respecto al baseline. Puede ser natural (evolución dominio) o adversarial.

**ENS** — Esquema Nacional de Seguridad español (RD 311/2022). Aplica a sistemas IA en sector público.

**Evasion attack** — Ataque en tiempo de inferencia: modificar el input para forzar mala predicción.

**Excessive Agency (LLM06)** — El LLM o agente tiene capacidades de acción que exceden lo necesario, amplificando el impacto de cualquier injection.

**Extraction (model stealing)** — Construir un modelo sustituto F̃ que aproxime al víctima F mediante queries a su API.

**FGSM** — Fast Gradient Sign Method. Ataque de evasión de un solo paso que perturba el input en la dirección del gradiente de la loss.

**Garak** — Framework NVIDIA open-source de red teaming automatizado para LLMs.

**GCG (Greedy Coordinate Gradient)** — Algoritmo de Zou et al. para generar sufijos adversariales que bypasean alignment.

**GPAI** — General Purpose AI (modelos fundacionales). Categoría específica en el EU AI Act con obligaciones de transparencia, copyright y evaluación de riesgo sistémico.

**Guardrail** — Capa de control alrededor del LLM (input/output scanner, classifier) para mitigar riesgos.

**HITL (Human In The Loop)** — Aprobación humana obligatoria para acciones críticas de un agente IA.

**Hyperparameter** — Parámetro del proceso de entrenamiento (no aprendido), ej. learning rate, dropout.

**Indirect prompt injection** — Payload embebido en datos (PDF, web, email) que el LLM consume y ejecuta como instrucción.

**ISO/IEC 42001** — Primer estándar internacional certificable para Sistemas de Gestión de IA (AIMS).

**Jailbreak** — Conjunto de técnicas para hacer que el LLM ignore restricciones de alignment.

**Knockoff Nets** — Algoritmo específico de model extraction (Orekondy et al. 2019).

**LLM Guard** — Librería open-source con scanners modulares I/O para LLMs.

**Llama Guard 3** — Modelo clasificador (Llama-3-8B fine-tuned) para detectar contenido inseguro según taxonomía MLCommons.

**Membership Inference Attack (MIA)** — Determinar si un dato específico estuvo en el training set del modelo.

**ML-BOM** — Bill of Materials específico de ML (CycloneDX 1.5): documenta modelos, datasets, frameworks.

**MLSecOps** — MLOps + Seguridad continua. Disciplina operacional.

**ModelScan** — Herramienta Protect AI para escanear modelos buscando operaciones peligrosas (pickle).

**NeMo Guardrails** — Framework NVIDIA con DSL Colang para definir guardrails declarativos.

**NIST AI RMF** — AI Risk Management Framework 1.0 (USA, voluntario). Funciones: Govern, Map, Measure, Manage.

**NIST AI 100-2** — Taxonomía formal de adversarial ML (2nd Ed. 2025). Divide en PredAI y GenAI.

**OWASP LLM Top 10** — Catálogo OWASP de los 10 riesgos principales en aplicaciones con LLM (versión 2025).

**PAIR (Prompt Automatic Iterative Refinement)** — Algoritmo blackbox de generación automática de jailbreaks usando otro LLM como atacante.

**Pickle RCE** — Ejecución remota de código vía deserialización de pickles maliciosos (`__reduce__`). Afecta `torch.load`, `joblib.load`, etc.

**Poisoning** — Manipular el dataset o proceso de entrenamiento para insertar comportamiento erróneo (backdoor) o degradar el modelo.

**Prompt injection** — Manipular el comportamiento del LLM via instrucciones embebidas en input (directa) o datos (indirecta). LLM01:2025.

**Promptfoo** — Herramienta CLI/CI para evaluar prompts y LLMs con suites de tests incluyendo red team.

**PyRIT** — Microsoft Python Risk Identification Toolkit. Framework de orquestación de ataques multi-turn customizables.

**RAG (Retrieval-Augmented Generation)** — Arquitectura donde el LLM consulta una base de conocimiento (vector DB) para responder.

**Safetensors** — Formato HuggingFace para guardar tensores sin posibilidad de ejecución de código. Alternativa segura a pickle.

**Sigstore** — Proyecto Linux Foundation para firma keyless de artefactos. Cosign es su herramienta principal.

**Spotlighting** — Técnica Microsoft Research para marcar datos no confiables (encoding/delimitadores) y reducir indirect injection.

**STRIDE** — Taxonomía clásica Microsoft: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. Adaptable a IA.

**Supply chain** — Cadena de suministro: dataset → framework → modelo base → fine-tune → registry → inferencia. Cada eslabón vector de ataque.

**System prompt** — Instrucción de configuración inicial del LLM (rol, restricciones, contexto). Suele ser el secreto peor guardado.

**TAP (Tree of Attacks with Pruning)** — Evolución de PAIR: árbol de ataques con poda, más eficiente.

**Threat modeling** — Proceso sistemático de identificar amenazas a un sistema. Para IA: NIST AI 100-2 + ATLAS + STRIDE-AI.

**Token budget** — Límite cuantitativo de tokens (input + output) por usuario/sesión/día — defensa frente a denial-of-wallet.

**Unbounded Consumption (LLM10)** — Antes "Model DoS". Ahora también denial-of-wallet: agotar tokens y gasto.

**weights_only=True** — Parámetro PyTorch ≥ 2.4 que bloquea deserialización arbitraria de pickle al hacer torch.load. Mitigación parcial.

**XSS via LLM** — El LLM genera HTML/JS que se renderiza en chat sin escape → vector de exfiltración o XSS clásico.
