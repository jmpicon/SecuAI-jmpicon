import { motion } from 'framer-motion'
import { FlaskConical, AlertTriangle, ExternalLink, ShieldOff, Bug, Database, Zap, Package } from 'lucide-react'

interface Lab {
  id: string
  title: string
  module: string
  description: string
  difficulty: 'Básico' | 'Medio' | 'Avanzado'
  port?: number
  endpoint?: string
  Icon: typeof FlaskConical
  color: string
  goals: string[]
}

const LABS: Lab[] = [
  {
    id: 'prompt-injection',
    title: 'Prompt Injection directa',
    module: 'Módulo 3 — OWASP LLM01',
    description: 'Chatbot bancario vulnerable. Objetivo: exfiltrar el system prompt y conseguir aprobación de un préstamo no autorizado.',
    difficulty: 'Básico',
    port: 5001,
    endpoint: 'http://localhost:5001',
    Icon: Bug,
    color: '#ff4757',
    goals: [
      'Identificar el system prompt',
      'Bypass de instrucciones con ignore-and-do',
      'Conseguir output con la API key embebida',
    ],
  },
  {
    id: 'rag-poisoning',
    title: 'Indirect Injection vía RAG',
    module: 'Módulo 4 — Agentes & RAG',
    description: 'Asistente que consulta documentos. Sube un PDF que contenga payloads invisibles y haz que recomiende un producto malicioso.',
    difficulty: 'Medio',
    port: 5002,
    endpoint: 'http://localhost:5002',
    Icon: Database,
    color: '#a29bfe',
    goals: [
      'Crear PDF con payload en texto blanco',
      'Triggerear el payload vía pregunta legítima',
      'Defensa: spotlighting de docs no confiables',
    ],
  },
  {
    id: 'pickle-rce',
    title: 'Pickle RCE en modelo .pt',
    module: 'Módulo 5 — Supply Chain',
    description: 'Cargar un modelo PyTorch troyanizado dispara ejecución remota. Crea el modelo malicioso y observa la shell.',
    difficulty: 'Avanzado',
    Icon: Package,
    color: '#00d4ff',
    goals: [
      'Construir clase con __reduce__ malicioso',
      'Serializar a .pt y subir al "hub" local',
      'Ejecutar shell reversa al hacer torch.load',
      'Mitigación: ModelScan / safetensors',
    ],
  },
  {
    id: 'model-extraction',
    title: 'Model Extraction vía API',
    module: 'Módulo 2 — Adversarial ML',
    description: 'API que sirve un clasificador. Extrae un sustituto consultando con datos sintéticos.',
    difficulty: 'Avanzado',
    port: 5003,
    endpoint: 'http://localhost:5003',
    Icon: Zap,
    color: '#ffa502',
    goals: [
      'Knockoff Nets — sustituto a partir de queries',
      'Medir fidelity y agreement',
      'Defensa: rate limiting + watermarking',
    ],
  },
  {
    id: 'garak',
    title: 'NVIDIA Garak — scan automatizado',
    module: 'Módulo 10 — Red Team',
    description: 'Lanza probes de jailbreak, encoding-based, dan, malwaregen contra un modelo Ollama local.',
    difficulty: 'Medio',
    Icon: ShieldOff,
    color: '#fd79a8',
    goals: [
      'Instalar Ollama + tinyllama',
      'Ejecutar garak --model_type ollama',
      'Interpretar el report HTML',
    ],
  },
  {
    id: 'llm-guard',
    title: 'Defensa con LLM Guard',
    module: 'Módulo 6 — Guardrails',
    description: 'Wrappea el chatbot del lab 1 con LLM Guard. Comprueba qué ataques se bloquean.',
    difficulty: 'Medio',
    Icon: FlaskConical,
    color: '#00ff88',
    goals: [
      'Configurar Anonymize, PromptInjection, Toxicity',
      'Medir false positive rate',
      'Tunear thresholds',
    ],
  },
]

export default function LabsPage() {
  return (
    <div className="space-y-8">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="space-y-3">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-cyber-pink/10 border border-cyber-pink/30 flex items-center justify-center">
            <FlaskConical size={24} className="text-cyber-pink" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Labs prácticos</h1>
            <p className="text-sm text-cyber-muted">Entornos vulnerables aislados en Docker. Ataca y defiende.</p>
          </div>
        </div>

        <div className="rounded-xl border border-cyber-orange/30 bg-cyber-orange/5 p-4 flex gap-3">
          <AlertTriangle size={20} className="text-cyber-orange shrink-0 mt-0.5" />
          <div className="text-sm text-cyber-text">
            <p className="font-semibold mb-1">Aviso ético</p>
            <p className="text-cyber-muted">
              Estos entornos son intencionadamente vulnerables. <strong>No los expongas a internet</strong>.
              Sólo deben ejecutarse en una máquina aislada con fines educativos.
            </p>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {LABS.map((lab, i) => (
          <motion.div
            key={lab.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="rounded-xl border border-cyber-border bg-cyber-card p-5 hover:border-cyber-green/40 transition-colors"
          >
            <div className="flex items-start gap-3 mb-3">
              <div
                className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
                style={{ backgroundColor: `${lab.color}15`, border: `1px solid ${lab.color}40` }}
              >
                <lab.Icon size={20} style={{ color: lab.color }} />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-cyber-text">{lab.title}</h3>
                <p className="text-[11px] font-mono text-cyber-muted">{lab.module}</p>
              </div>
              <span
                className="text-[10px] font-mono px-2 py-1 rounded"
                style={{
                  color: lab.difficulty === 'Avanzado' ? '#ff4757' : lab.difficulty === 'Medio' ? '#ffa502' : '#00ff88',
                  backgroundColor: (lab.difficulty === 'Avanzado' ? '#ff4757' : lab.difficulty === 'Medio' ? '#ffa502' : '#00ff88') + '15',
                }}
              >
                {lab.difficulty}
              </span>
            </div>

            <p className="text-sm text-cyber-muted mb-3">{lab.description}</p>

            <div className="space-y-1.5 mb-4">
              <p className="text-[10px] font-mono text-cyber-dim uppercase tracking-wider">Objetivos</p>
              {lab.goals.map(g => (
                <div key={g} className="flex gap-2 text-xs text-cyber-text">
                  <span className="text-cyber-green">▸</span>
                  <span>{g}</span>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-cyber-border">
              <code className="text-[11px] font-mono text-cyber-green">
                docker compose up lab-{lab.id}
              </code>
              {lab.endpoint && (
                <a
                  href={lab.endpoint}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-cyber-blue hover:underline flex items-center gap-1"
                >
                  Abrir <ExternalLink size={11} />
                </a>
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
