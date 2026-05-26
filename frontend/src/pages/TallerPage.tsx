import { motion } from 'framer-motion'
import { Presentation, Clock, Users, Download, Mic, Coffee, Target, FileText } from 'lucide-react'

interface Section {
  time: string
  title: string
  type: 'teoría' | 'demo' | 'práctica' | 'pausa'
  duration: number
  description: string
}

const AGENDA: Section[] = [
  {
    time: '00:00',
    title: 'Bienvenida + por qué nos jugamos esto',
    type: 'teoría',
    duration: 5,
    description: 'Hook con un caso real (incidente reciente IA). Mostrar el alcance del problema. Encuesta levantamiento de manos.',
  },
  {
    time: '00:05',
    title: 'Mapa: dónde se ataca a la IA',
    type: 'teoría',
    duration: 10,
    description: 'MITRE ATLAS en 5 minutos. Diagrama del ciclo MLOps con puntos de fallo. Diferencia con appsec clásico.',
  },
  {
    time: '00:15',
    title: 'DEMO 1 — Prompt injection en vivo',
    type: 'demo',
    duration: 10,
    description: 'Chatbot de banca vulnerable. Audiencia propone payloads, yo los pruebo. Mostrar leak de system prompt.',
  },
  {
    time: '00:25',
    title: 'PRÁCTICA — Audiencia ataca',
    type: 'práctica',
    duration: 15,
    description: 'Asistentes con laptop acceden al chatbot por QR. 3 retos: leak system prompt, conseguir consejo prohibido, exfiltrar token falso. Primero en cada reto: punto.',
  },
  {
    time: '00:40',
    title: 'Pausa café (opcional)',
    type: 'pausa',
    duration: 10,
    description: 'Si es slot largo. Para 60min se salta.',
  },
  {
    time: '00:50',
    title: 'Indirect injection — el ataque silencioso',
    type: 'teoría',
    duration: 8,
    description: 'Explicar RAG y por qué los documentos recuperados son código ejecutable para el LLM. Ejemplos reales (Slack, Gmail summarizers).',
  },
  {
    time: '00:58',
    title: 'DEMO 2 — PDF envenenado',
    type: 'demo',
    duration: 7,
    description: 'Subir un CV con instrucciones invisibles. El "ATS con IA" recomienda contratar al candidato malicioso. Mostrar el texto blanco-sobre-blanco.',
  },
  {
    time: '01:05',
    title: 'Defensas reales que funcionan (y las que no)',
    type: 'teoría',
    duration: 10,
    description: 'LLM Guard, Llama Guard, spotlighting, structured queries. Por qué los filtros de regex no bastan. Defensa en profundidad.',
  },
  {
    time: '01:15',
    title: 'PRÁCTICA — Diseña tu defensa',
    type: 'práctica',
    duration: 10,
    description: 'En grupos de 3, dado un caso de uso (asistente médico / agente financiero / chatbot soporte), proponen pila defensiva. 2 grupos exponen.',
  },
  {
    time: '01:25',
    title: 'Cierre + Q&A + recursos',
    type: 'teoría',
    duration: 5,
    description: 'QR con repo, slides, lecturas. Recordatorio: certificación ISO 42001 viene. Contacto.',
  },
]

const KIT_DOWNLOADS = [
  { file: 'slides-charla.pdf',          desc: 'Slides Marp exportados a PDF' },
  { file: 'guion-ponente.md',           desc: 'Guion completo del ponente con tiempos' },
  { file: 'demo1-prompts.md',           desc: 'Prompts para la demo 1 (prompt injection)' },
  { file: 'demo2-pdf-envenenado.pdf',   desc: 'PDF de ejemplo para demo 2 (indirect injection)' },
  { file: 'kit-asistente.pdf',          desc: 'Resumen 2 páginas para entregar a asistentes' },
  { file: 'pretest.pdf',                desc: 'Cuestionario previo (3 preguntas)' },
  { file: 'postest.pdf',                desc: 'Cuestionario posterior + valoración' },
  { file: 'plantilla-amenazas-IA.xlsx', desc: 'Plantilla de threat modeling ATLAS' },
]

const TYPE_STYLE: Record<Section['type'], { color: string; bg: string; icon: typeof Mic }> = {
  teoría:   { color: '#00d4ff', bg: 'rgba(0,212,255,0.1)',  icon: Mic },
  demo:     { color: '#ff4757', bg: 'rgba(255,71,87,0.1)',  icon: Target },
  práctica: { color: '#00ff88', bg: 'rgba(0,255,136,0.1)',  icon: Users },
  pausa:    { color: '#ffa502', bg: 'rgba(255,165,2,0.1)',  icon: Coffee },
}

export default function TallerPage() {
  const total = AGENDA.reduce((acc, s) => acc + s.duration, 0)

  return (
    <div className="space-y-8">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <div className="rounded-2xl border border-cyber-border bg-gradient-to-br from-cyber-surface to-cyber-card p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row gap-6 items-start">
            <div className="w-14 h-14 rounded-2xl bg-cyber-purple/10 border border-cyber-purple/30 flex items-center justify-center shrink-0">
              <Presentation size={28} className="text-cyber-purple" />
            </div>
            <div className="flex-1">
              <div className="text-xs font-mono text-cyber-purple mb-1 tracking-widest uppercase">
                Taller para charlas — formato 90 min
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2">
                Hackeando la <span className="text-cyber-purple">IA</span> — del prompt injection a las defensas reales
              </h1>
              <p className="text-sm text-cyber-muted max-w-2xl">
                Taller listo para impartir: guion del ponente, slides, 2 demos en vivo,
                2 dinámicas participativas (con QR para que la audiencia ataque) y kit descargable.
              </p>
              <div className="flex flex-wrap gap-4 mt-4">
                <div className="flex items-center gap-2 text-xs font-mono text-cyber-muted">
                  <Clock size={14} className="text-cyber-purple" /> {total} min
                </div>
                <div className="flex items-center gap-2 text-xs font-mono text-cyber-muted">
                  <Users size={14} className="text-cyber-purple" /> 10–80 asistentes
                </div>
                <div className="flex items-center gap-2 text-xs font-mono text-cyber-muted">
                  <Target size={14} className="text-cyber-purple" /> Nivel: técnico/intermedio
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Agenda timeline */}
      <div>
        <div className="flex items-center gap-3 mb-5">
          <h2 className="text-lg font-semibold text-cyber-text">Agenda detallada</h2>
          <div className="flex-1 h-px bg-cyber-border" />
          <span className="text-xs font-mono text-cyber-muted">{AGENDA.length} bloques</span>
        </div>

        <div className="space-y-3">
          {AGENDA.map((s, i) => {
            const style = TYPE_STYLE[s.type]
            const Icon = style.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.04 }}
                className="flex gap-4 items-start group"
              >
                <div className="font-mono text-xs text-cyber-muted w-12 text-right pt-3 shrink-0">
                  {s.time}
                </div>
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 mt-1"
                  style={{ backgroundColor: style.bg, border: `1px solid ${style.color}40` }}
                >
                  <Icon size={16} style={{ color: style.color }} />
                </div>
                <div className="flex-1 bg-cyber-card border border-cyber-border rounded-xl p-4 hover:border-cyber-purple/40 transition-colors">
                  <div className="flex items-start gap-3 flex-wrap mb-1">
                    <h3 className="font-semibold text-cyber-text flex-1">{s.title}</h3>
                    <span
                      className="text-[10px] font-mono px-2 py-0.5 rounded uppercase"
                      style={{ color: style.color, backgroundColor: style.bg }}
                    >
                      {s.type}
                    </span>
                    <span className="text-[11px] font-mono text-cyber-muted">{s.duration} min</span>
                  </div>
                  <p className="text-sm text-cyber-muted">{s.description}</p>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Kit descargable */}
      <div>
        <div className="flex items-center gap-3 mb-5">
          <h2 className="text-lg font-semibold text-cyber-text">Kit del ponente (taller/)</h2>
          <div className="flex-1 h-px bg-cyber-border" />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {KIT_DOWNLOADS.map(k => (
            <div
              key={k.file}
              className="flex items-center gap-3 bg-cyber-card border border-cyber-border rounded-xl p-3 hover:border-cyber-green/30 transition-colors group"
            >
              <div className="w-9 h-9 rounded-lg bg-cyber-green/10 border border-cyber-green/30 flex items-center justify-center shrink-0">
                <FileText size={16} className="text-cyber-green" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-mono text-xs text-cyber-text truncate">{k.file}</div>
                <div className="text-[11px] text-cyber-muted truncate">{k.desc}</div>
              </div>
              <Download size={14} className="text-cyber-muted group-hover:text-cyber-green transition-colors" />
            </div>
          ))}
        </div>

        <p className="text-xs font-mono text-cyber-dim mt-4">
          Los ficheros viven en <code className="text-cyber-green">taller/</code> del repo. Renderiza las slides con: <code className="text-cyber-green">marp taller/slides-charla.md --pdf</code>
        </p>
      </div>
    </div>
  )
}
