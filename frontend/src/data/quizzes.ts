export interface Question {
  q: string
  options: [string, string, string, string]
  correct: 0 | 1 | 2 | 3
  explanation: string
}

export interface Quiz {
  moduleId: number
  moduleSlug: string
  title: string
  color: string
  questions: Question[]
}

export const QUIZZES: Quiz[] = [
  {
    moduleId: 1,
    moduleSlug: 'modulo1',
    title: 'Fundamentos & Threat Modeling de IA',
    color: '#00ff88',
    questions: [
      {
        q: '¿Qué es MITRE ATLAS?',
        options: [
          'Una base de datos de modelos de IA preentrenados',
          'Una matriz de TTPs adversariales específica para sistemas de IA, análoga a ATT&CK',
          'Un framework de evaluación de rendimiento de LLMs',
          'Una herramienta de scanning de modelos en HuggingFace',
        ],
        correct: 1,
        explanation: 'MITRE ATLAS (Adversarial Threat Landscape for AI Systems) es la matriz de tácticas y técnicas de ataques reales contra sistemas de ML/IA, mantenida por MITRE.',
      },
      {
        q: 'Según NIST AI 100-2, ¿en qué dos grandes categorías se dividen los ataques al ML?',
        options: ['Online vs Offline', 'Predictive AI vs Generative AI', 'Whitebox vs Blackbox', 'Stateful vs Stateless'],
        correct: 1,
        explanation: 'NIST AI 100-2 (2nd Ed., 2025) estructura la taxonomía en PredAI vs GenAI, reflejando diferencias sustanciales en superficie de ataque.',
      },
      {
        q: '¿Cuál NO es una fase del ciclo MLOps con superficie de ataque?',
        options: ['Recolección y curado de datos', 'Entrenamiento del modelo', 'Servir el modelo (inferencia)', 'Renovación del dominio DNS'],
        correct: 3,
        explanation: 'Las fases del MLOps con superficie de ataque son data → train → registry → serve → monitor. El DNS no es parte del ciclo MLOps.',
      },
      {
        q: 'En STRIDE aplicado a IA, ¿a qué amenaza corresponde envenenar el dataset de entrenamiento?',
        options: ['Spoofing', 'Tampering', 'Repudiation', 'Elevation of Privilege'],
        correct: 1,
        explanation: 'Tampering — manipulación de datos. El envenenamiento (data poisoning) altera la integridad de los datos de entrenamiento.',
      },
      {
        q: '¿Cuál es la principal diferencia entre appsec clásico y AI security?',
        options: [
          'AI security sólo usa Python',
          'El modelo es código, datos y output probabilístico — la frontera de confianza se difumina',
          'AI security no aplica autenticación',
          'No hay diferencia, sólo cambia el lenguaje',
        ],
        correct: 1,
        explanation: 'El modelo es pesos (código), datos (entrenamiento) y produce outputs probabilísticos. Esto invalida supuestos del modelo de confianza tradicional.',
      },
    ],
  },
  {
    moduleId: 2,
    moduleSlug: 'modulo2',
    title: 'Adversarial ML clásico',
    color: '#ff4757',
    questions: [
      {
        q: '¿Qué hace el ataque FGSM (Fast Gradient Sign Method)?',
        options: [
          'Encripta los pesos del modelo',
          'Calcula una perturbación adversarial en un solo paso usando el signo del gradiente de la loss',
          'Inyecta ruido aleatorio en los datos',
          'Comprime el modelo para extraerlo',
        ],
        correct: 1,
        explanation: 'FGSM (Goodfellow et al. 2014): x_adv = x + ε·sign(∇_x L(θ, x, y)). Perturbación mínima en la dirección que más aumenta la loss.',
      },
      {
        q: '¿Qué caracteriza a un ataque BadNets?',
        options: [
          'Cambia toda la distribución del dataset',
          'Inserta un trigger visual que activa una clasificación errónea predecible',
          'Sólo funciona en modelos lineales',
          'Requiere acceso al gradiente',
        ],
        correct: 1,
        explanation: 'BadNets (Gu et al. 2017) entrena un backdoor: comportamiento normal salvo cuando ve el trigger (ej. cuadrado), que redirige a una clase objetivo.',
      },
      {
        q: 'En model extraction, el atacante busca:',
        options: [
          'Robar los pesos exactos',
          'Crear un sustituto funcionalmente equivalente consultando la API víctima',
          'Borrar el modelo de producción',
          'Cifrar el modelo para pedir rescate',
        ],
        correct: 1,
        explanation: 'Model extraction (Tramèr et al. 2016, Knockoff Nets) construye un sustituto cuyo comportamiento aproxima al víctima — base para luego ataques whitebox.',
      },
      {
        q: 'Membership Inference Attack determina:',
        options: ['Si un dato concreto fue usado en entrenamiento', 'A qué clase pertenece una imagen', 'El número de capas', 'El learning rate'],
        correct: 0,
        explanation: 'MIA (Shokri et al. 2017) explota la diferencia de confianza entre datos vistos vs no vistos — riesgo crítico bajo RGPD/HIPAA.',
      },
      {
        q: '¿Cuál es la defensa más sólida y formalmente garantizada contra membership inference?',
        options: ['Aumentar regularización', 'Differential Privacy (DP-SGD)', 'Usar más datos', 'Cambiar de framework'],
        correct: 1,
        explanation: 'Differential Privacy ofrece garantía matemática (ε,δ) sobre cuánto puede el output revelar de un individuo. DP-SGD añade ruido calibrado al gradiente.',
      },
    ],
  },
  {
    moduleId: 3,
    moduleSlug: 'modulo3',
    title: 'OWASP Top 10 LLM 2025',
    color: '#ffa502',
    questions: [
      {
        q: '¿Cuál es el #1 del OWASP Top 10 LLM 2025?',
        options: ['Sensitive Information Disclosure', 'Prompt Injection', 'Supply Chain', 'Excessive Agency'],
        correct: 1,
        explanation: 'LLM01:2025 Prompt Injection sigue siendo el #1 — cubre inyección directa (usuario) e indirecta (datos recuperados).',
      },
      {
        q: 'Un jailbreak DAN ("Do Anything Now") es ejemplo de:',
        options: ['Indirect prompt injection', 'Direct prompt injection con role-play', 'Model extraction', 'Data poisoning'],
        correct: 1,
        explanation: 'DAN es prompt injection directa: el atacante construye un role-play que convence al modelo de ignorar sus restricciones originales.',
      },
      {
        q: '¿Qué describe LLM06 Excessive Agency?',
        options: [
          'El modelo es demasiado rápido',
          'El LLM tiene permisos/herramientas que exceden lo necesario, permitiendo acciones dañinas si es manipulado',
          'El modelo cuesta demasiado',
          'Falta contexto en las respuestas',
        ],
        correct: 1,
        explanation: 'Dar al LLM o agente capacidades excesivas (escribir BD, enviar emails) sin gating humano amplifica el impacto de cualquier injection.',
      },
      {
        q: 'LLM10 Unbounded Consumption (denial-of-wallet) se mitiga con:',
        options: ['CSP headers', 'Rate limiting + límite de tokens por petición + budget caps', 'Encriptación AES', 'OAuth 2.0'],
        correct: 1,
        explanation: 'El abuso económico se mitiga con quotas de tokens, rate limiting, alertas de gasto y cortes automáticos del autoscaling.',
      },
      {
        q: 'LLM05 Improper Output Handling se manifiesta cuando:',
        options: [
          'El modelo responde lento',
          'El output del LLM se inyecta sin sanitizar en otro sistema (SQL, shell, HTML) provocando XSS/SQLi/RCE',
          'Usa demasiada RAM',
          'El usuario no entiende la respuesta',
        ],
        correct: 1,
        explanation: 'El LLM es un generador no-confiable: tratar su salida como código sin escapado abre la vía a XSS/SQLi/RCE clásicos.',
      },
    ],
  },
  {
    moduleId: 4,
    moduleSlug: 'modulo4',
    title: 'Ataques a Agentes & RAG',
    color: '#a29bfe',
    questions: [
      {
        q: 'Indirect prompt injection ocurre cuando:',
        options: [
          'El usuario envía un prompt malicioso directamente',
          'Una instrucción adversarial se embebe en contenido (web, PDF, email) que el LLM luego procesa, ejecutando el ataque del tercero',
          'Se cifra el prompt',
          'Se cambia el modelo a uno más pequeño',
        ],
        correct: 1,
        explanation: 'Indirect injection: el atacante no habla con el LLM, planta el payload en datos que el LLM consumirá (web resumida, PDF en RAG).',
      },
      {
        q: '¿Qué es "tool poisoning" en agentes MCP?',
        options: [
          'Romper físicamente el servidor',
          'Crear o modificar una herramienta cuya descripción contiene instrucciones que el LLM seguirá al elegir entre tools',
          'Sobrecargar la API con peticiones',
          'Cambiar el modelo por uno antiguo',
        ],
        correct: 1,
        explanation: 'El LLM lee descripciones de tools para elegir cuál usar. Inyectar instrucciones en esas descripciones (rug-pull, descripción larga) es un vector creciente.',
      },
      {
        q: '¿Qué es ASCII smuggling?',
        options: [
          'Comprimir texto en ASCII',
          'Usar caracteres invisibles Unicode (Tags, variation selectors) para ocultar instrucciones al humano pero no al LLM',
          'Cambiar la codificación a UTF-16',
          'Una técnica de cifrado simétrico',
        ],
        correct: 1,
        explanation: 'Bloques Unicode como Tags (U+E0000..) son invisibles para humanos pero algunos LLMs los interpretan — vector documentado en ChatGPT y Copilot.',
      },
      {
        q: '¿Qué defensa propone Microsoft Research bajo el nombre "Spotlighting"?',
        options: [
          'Encender una luz en el servidor',
          'Marcar los datos no confiables (encoding/delimitadores especiales) para que el LLM no los interprete como instrucciones',
          'Apagar el LLM cuando hay sospecha',
          'Resaltar visualmente las respuestas',
        ],
        correct: 1,
        explanation: 'Spotlighting (Hines et al. 2024) re-codifica los datos no confiables (base64, datamarking) para que el modelo aprenda a tratarlos como datos.',
      },
      {
        q: 'En un confused deputy attack contra un agente, el problema es:',
        options: [
          'El modelo está confundido',
          'El agente actúa con sus propios permisos (altos) por orden del usuario (bajos), permitiendo escalada',
          'El sysadmin se equivocó al configurar',
          'El usuario envía un prompt incorrecto',
        ],
        correct: 1,
        explanation: 'Confused deputy (Hardy 1988) reaparece en agentes: el LLM ejecuta acciones con sus credenciales sin verificar derechos del solicitante.',
      },
    ],
  },
  {
    moduleId: 5,
    moduleSlug: 'modulo5',
    title: 'Supply Chain ML & MLBOM',
    color: '#00d4ff',
    questions: [
      {
        q: '¿Por qué cargar un fichero .pkl de origen no confiable es peligroso?',
        options: [
          'Ocupa demasiado disco',
          'pickle.load() puede instanciar clases con __reduce__ que ejecuta código arbitrario',
          'Es lento',
          'Sólo funciona con NumPy',
        ],
        correct: 1,
        explanation: 'pickle deserializa código Python: definir __reduce__ permite ejecutar cualquier comando — RCE. Aplica a .pkl, .pt, .joblib.',
      },
      {
        q: '¿Qué formato propone HuggingFace como alternativa segura a pickle?',
        options: ['.h5', 'safetensors', '.onnx encriptado', '.npz'],
        correct: 1,
        explanation: 'safetensors es un formato puramente de datos (tensores) sin capacidad de ejecución de código, diseñado para mitigar el problema de pickle.',
      },
      {
        q: '¿Qué es un ML-BOM?',
        options: [
          'Un script para entrenar modelos',
          'Variante de SBOM que documenta modelos, datasets, frameworks y dependencias del pipeline ML, estandarizada por CycloneDX 1.5',
          'Un dataset benchmark',
          'Un formato de imagen',
        ],
        correct: 1,
        explanation: 'CycloneDX 1.5 introduce el ML-BOM: bill-of-materials específico para componentes ML, base para gobernanza y trazabilidad.',
      },
      {
        q: '¿Qué herramienta de Sigstore se usa para firmar artefactos ML?',
        options: ['gpg', 'cosign', 'openssl', 'jarsigner'],
        correct: 1,
        explanation: 'cosign permite firmar y verificar contenedores y artefactos arbitrarios (incluidos modelos) con keyless OIDC.',
      },
      {
        q: '¿Qué ofrece ModelScan de Protect AI?',
        options: [
          'Optimiza la inferencia',
          'Analiza estáticamente ficheros de modelo (pickle, h5, pt) buscando operaciones peligrosas y backdoors conocidos',
          'Encripta el modelo en disco',
          'Comprime los pesos',
        ],
        correct: 1,
        explanation: 'ModelScan inspecciona modelos serializados detectando llamadas a os.system, subprocess, eval — análisis estático adaptado al riesgo de pickle.',
      },
    ],
  },
  {
    moduleId: 6,
    moduleSlug: 'modulo6',
    title: 'Guardrails & Defensa en Profundidad',
    color: '#fd79a8',
    questions: [
      {
        q: 'LLM Guard (Laiyer) es:',
        options: [
          'Un modelo grande de Meta',
          'Una librería Python con scanners modulares de input/output (PII, prompt injection, toxicity) que envuelve cualquier LLM',
          'Un dataset de prompts adversariales',
          'Una distribución Linux',
        ],
        correct: 1,
        explanation: 'LLM Guard ofrece scanners encadenables. Útil para añadir defensa en profundidad alrededor de cualquier endpoint LLM.',
      },
      {
        q: '¿Qué hace NeMo Guardrails de NVIDIA?',
        options: [
          'Acelera la GPU',
          'Permite declarar guardrails con un DSL llamado Colang (flujos, refusal patterns, validaciones)',
          'Es un fine-tuner',
          'Es un editor de prompts',
        ],
        correct: 1,
        explanation: 'NeMo Guardrails usa Colang para definir guardrails dialogados y de seguridad de forma declarativa, integrable con LangChain.',
      },
      {
        q: 'Llama Guard 3 es:',
        options: [
          'El último modelo de Meta para chatbots',
          'Un clasificador especializado (Llama-3 fine-tuned) que evalúa si entrada/salida violan políticas MLCommons',
          'Una versión móvil de Llama',
          'Un compilador',
        ],
        correct: 1,
        explanation: 'Llama Guard 3 (8B) es un modelo clasificador entrenado para detectar contenido inseguro, alineado con la taxonomía MLCommons.',
      },
      {
        q: '¿Por qué los filtros regex de prompt injection son insuficientes?',
        options: [
          'Son rápidos',
          'El espacio de bypass es infinito: traducción, ofuscación, payload splitting, ASCII smuggling, role-play los evaden trivialmente',
          'Sólo funcionan en GPU',
          'Cuestan dinero',
        ],
        correct: 1,
        explanation: 'Las regexes funcionan con patrones cerrados. El lenguaje natural es abierto: cualquier intent puede expresarse de infinitas formas.',
      },
      {
        q: 'En defensa en profundidad para LLMs, ¿qué orden tiene más sentido?',
        options: [
          'Sólo guardrail post-respuesta',
          'Auth → rate limit → input scanner → LLM → output scanner → human-in-the-loop para acciones críticas',
          'Sólo input scanner',
          'Sólo human-in-the-loop',
        ],
        correct: 1,
        explanation: 'Pila completa: filtrado entrada, monitor LLM, filtrado salida y aprobación humana para acciones con impacto (write, send, transfer).',
      },
    ],
  },
  {
    moduleId: 7,
    moduleSlug: 'modulo7',
    title: 'MLSecOps & Monitorización',
    color: '#00ff88',
    questions: [
      {
        q: '¿Qué es el "drift" adversarial en producción?',
        options: [
          'El modelo se mueve físicamente',
          'Cambio sistemático en la distribución de inputs causado por atacantes (vs drift natural por evolución del dominio)',
          'El servidor cambia de IP',
          'La GPU se sobrecalienta',
        ],
        correct: 1,
        explanation: 'Drift adversarial: alguien empuja deliberadamente entradas atípicas para sondear el modelo. Distinguirlo del natural es crítico.',
      },
      {
        q: 'Langfuse, Phoenix y Helicone son ejemplos de:',
        options: [
          'Modelos pre-entrenados',
          'Herramientas open-source de observabilidad para LLMs (trazas, métricas, evals)',
          'Editores de código',
          'Wallets de crypto',
        ],
        correct: 1,
        explanation: 'Stack LLMOps de observabilidad: rastrean cada llamada, embeddings, costes, latencia, y permiten replays y evals automáticos.',
      },
      {
        q: 'Detección de abuso por embedding clustering consiste en:',
        options: [
          'Calcular embeddings de prompts recientes y alertar cuando aparece un cluster anómalo o aumenta densidad cerca de prompts marcados como abusivos',
          'Hacer un ping al servidor',
          'Cambiar el modelo cada hora',
          'Subir el rate limit',
        ],
        correct: 0,
        explanation: 'Clustering en el espacio de embeddings detecta campañas coordinadas o variaciones sobre un prompt malicioso conocido (vecindad semántica).',
      },
      {
        q: '¿Qué es un "token budget" en un sistema LLM?',
        options: [
          'El presupuesto monetario anual',
          'Límite máximo de tokens (entrada+salida) por usuario/sesión/petición, para prevenir DoS y abuso económico',
          'El número de modelos disponibles',
          'Los empleados que pueden usar el modelo',
        ],
        correct: 1,
        explanation: 'Token budget es el límite cuantitativo en tokens — base de defensa frente a unbounded consumption (LLM10) y control de costes.',
      },
      {
        q: 'Red teaming continuo de LLMs implica:',
        options: [
          'Pintar el servidor de rojo',
          'Ejecutar suites adversariales (Garak/PyRIT/Promptfoo) en CI y en producción periódicamente',
          'Pentesting manual una vez al año',
          'Cambiar el equipo cada mes',
        ],
        correct: 1,
        explanation: 'Modelos y técnicas evolucionan: el red team debe integrarse en CI/CD y en cadencia continua (mensual, no anual).',
      },
    ],
  },
  {
    moduleId: 8,
    moduleSlug: 'modulo8',
    title: 'Gobernanza & Cumplimiento',
    color: '#ffa502',
    questions: [
      {
        q: 'NIST AI RMF 1.0 estructura el ciclo en 4 funciones:',
        options: [
          'Identify, Protect, Detect, Respond',
          'Govern, Map, Measure, Manage',
          'Plan, Do, Check, Act',
          'Define, Build, Run, Improve',
        ],
        correct: 1,
        explanation: 'NIST AI RMF: Govern (cultura/políticas), Map (contexto), Measure (riesgos), Manage (mitigación y monitorización).',
      },
      {
        q: 'El EU AI Act (Reg. 2024/1689) clasifica los sistemas en:',
        options: [
          'Buenos vs malos',
          'Inaceptable, alto riesgo, riesgo limitado/transparencia, riesgo mínimo + obligaciones para GPAI',
          'Permitidos y prohibidos',
          'Verde, amarillo, rojo',
        ],
        correct: 1,
        explanation: 'AI Act basado en riesgo: prohíbe (social scoring), regula "alto riesgo" (sanidad, RRHH), exige transparencia para chatbots/deepfakes, obliga a GPAI.',
      },
      {
        q: 'ISO/IEC 42001 es:',
        options: [
          'Norma de calidad de software',
          'Primer estándar internacional para Sistemas de Gestión de IA (AIMS), análogo a ISO 27001',
          'Norma de protección de datos',
          'Norma de eficiencia energética',
        ],
        correct: 1,
        explanation: 'ISO/IEC 42001:2023 define requisitos para implantar un AIMS — paraguas de gobernanza de IA en la organización.',
      },
      {
        q: 'En el ENS español (RD 311/2022), ¿qué dimensiones de seguridad evalúa?',
        options: [
          'Sólo confidencialidad',
          'Confidencialidad, Integridad, Trazabilidad, Autenticidad, Disponibilidad',
          'Coste, tiempo, alcance',
          'Hardware y software',
        ],
        correct: 1,
        explanation: 'ENS evalúa 5 dimensiones (CITAD). Un sistema con IA debe clasificarse en estas dimensiones igual que cualquier otro de la AAPP.',
      },
      {
        q: '¿Qué es un "inventario de modelos"?',
        options: [
          'Lista de servidores',
          'Registro centralizado de modelos de IA en uso (versión, datos, riesgos, owner, fecha revisión) — requisito de ISO 42001 y EU AI Act',
          'Catálogo de datasets públicos',
          'Lista de empleados',
        ],
        correct: 1,
        explanation: 'Sin inventario no hay gobernanza. Base para auditoría, retirada, trazabilidad y respuesta a incidentes.',
      },
    ],
  },
  {
    moduleId: 9,
    moduleSlug: 'modulo9',
    title: 'IA Defensiva — Blue Team con LLMs',
    color: '#00d4ff',
    questions: [
      {
        q: 'Uso típico de LLM + RAG en triage SOC:',
        options: [
          'Enviar alertas a la nevera',
          'Enriquecer una alerta con contexto (logs, threat intel, runbooks) y proponer un veredicto preliminar para que el analista decida',
          'Sustituir al analista humano',
          'Borrar alertas falsas',
        ],
        correct: 1,
        explanation: 'El LLM no sustituye; acelera L1: agrega contexto, correlaciona con incidentes previos y sugiere acciones — el humano valida.',
      },
      {
        q: '¿Qué riesgo principal tienen las alucinaciones del LLM en contextos de seguridad?',
        options: [
          'Que el modelo se ralentice',
          'Inventar CVEs, IPs maliciosas o reglas de detección plausibles pero falsas — ruido y falsa confianza',
          'Que use mucha RAM',
          'Que cambie el idioma',
        ],
        correct: 1,
        explanation: 'Una alucinación que parece técnica (CVE inventado, IOC ficticio) puede meterse en un informe y propagarse. Mitigación: grounding + verificación.',
      },
      {
        q: 'Para generar reglas Sigma asistido por LLM, lo más fiable es:',
        options: [
          'Pedirle "genera una regla para detectar mimikatz"',
          'Dar (a) documentación oficial Sigma + (b) ejemplos verificados + (c) logs concretos — RAG sobre fuentes fiables',
          'Copiarla de Stack Overflow',
          'No usar LLM nunca',
        ],
        correct: 1,
        explanation: 'Few-shot + RAG sobre fuentes oficiales reduce alucinaciones de sintaxis y mejora la cobertura efectiva.',
      },
      {
        q: 'Code review con LLM + Semgrep funciona mejor cuando:',
        options: [
          'Sustituye a Semgrep',
          'Semgrep marca regiones de interés y el LLM explica el riesgo y propone fix contextualizado',
          'El LLM revisa todo el repo de golpe',
          'No se usa Semgrep',
        ],
        correct: 1,
        explanation: 'Semgrep aporta precisión (rules deterministas), el LLM aporta razonamiento y contexto. La combinación supera a cada uno por separado.',
      },
      {
        q: 'Buena práctica para usar LLMs sobre logs sensibles:',
        options: [
          'Subirlos tal cual a APIs públicas',
          'Modelo local (Ollama, vLLM on-prem) o servicio dedicado con DPA + anonimización previa de PII',
          'Enviarlos por Slack',
          'No hace falta cuidado, los logs no son sensibles',
        ],
        correct: 1,
        explanation: 'Los logs contienen PII, secretos, tokens. Estrategia segura: on-prem o DPA estricto + anonimizador (Presidio, LLM Guard) antes del envío.',
      },
    ],
  },
  {
    moduleId: 10,
    moduleSlug: 'modulo10',
    title: 'Red Team de IA Automatizado',
    color: '#ff4757',
    questions: [
      {
        q: 'NVIDIA Garak es:',
        options: [
          'Una distro Linux',
          'Framework open-source de probing automatizado de LLMs (probes: jailbreak, dan, encoding, malwaregen, leak)',
          'Un model registry',
          'Una librería de tensors',
        ],
        correct: 1,
        explanation: 'Garak (Generative AI Red-teaming and Assessment Kit) lanza familias de probes y mide tasas de éxito con detectores específicos.',
      },
      {
        q: 'Microsoft PyRIT se diferencia de Garak en que:',
        options: [
          'Está hecho en JavaScript',
          'Orquesta ataques multi-turn con converters y attack strategies programables — más flexible para campañas complejas',
          'No usa Python',
          'Es comercial cerrado',
        ],
        correct: 1,
        explanation: 'PyRIT (Python Risk Identification Toolkit) está pensado para construir ataques multi-step y personalizados (single-turn, crescendo, scorers).',
      },
      {
        q: '¿Qué es Promptfoo en contexto de seguridad?',
        options: [
          'Un modelo conversacional',
          'Herramienta CLI/CI para evaluar prompts y modelos con suites de tests (incluidas suites de jailbreak/seguridad)',
          'Un ORM',
          'Un compresor de tokens',
        ],
        correct: 1,
        explanation: 'Promptfoo permite definir tests YAML y correrlos en CI: asserts sobre safety, prompt injection, regresiones tras cambio de modelo.',
      },
      {
        q: 'PAIR y TAP son algoritmos de:',
        options: [
          'Compresión',
          'Generación automática de jailbreaks usando otro LLM como atacante en bucle de mejora',
          'Tokenización',
          'Federated learning',
        ],
        correct: 1,
        explanation: 'PAIR (Prompt Automatic Iterative Refinement) y TAP (Tree of Attacks with Pruning) usan un LLM atacante que itera prompts hasta superar el guardrail.',
      },
      {
        q: 'ASR (Attack Success Rate) en evaluación de LLMs mide:',
        options: [
          'Tiempo de respuesta',
          'Porcentaje de intentos adversariales que consiguen el comportamiento prohibido',
          'Calidad gramatical',
          'Uso de memoria',
        ],
        correct: 1,
        explanation: 'ASR es la métrica central. Bajar ASR tras introducir un guardrail demuestra eficacia; subida indica regresión o nuevo bypass.',
      },
    ],
  },
]
