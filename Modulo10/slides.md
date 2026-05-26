---
marp: true
theme: gaia
class: invert
paginate: true
header: 'SecuAI · Módulo 10'
footer: 'Red Team Automatizado'
---

<!-- _class: lead invert -->

# **Red Team** de IA Automatizado

Módulo 10 · SecuAI

Garak · PyRIT · Promptfoo · PAIR · TAP · GCG · Crescendo

---

## Por qué automatizado

Manual: ~50-100 prompts/hora, alta creatividad.
Automatizado: 10 000 probes/noche, cobertura sistemática.

**Combinar**: humano = vectores nuevos, automático = regresión y scale.

---

## NVIDIA Garak

```bash
garak --model_type huggingface \
      --model_name gpt2 \
      --probes dan,malwaregen,encoding
```

Probes: dan, malwaregen, encoding, latentinjection, leakreplay, glitch, xss, tap, divergence.

Detectors mide ASR por probe. Output HTML report.

---

## PyRIT (Microsoft)

Orquesta campañas multi-turn:

```python
RedTeamingOrchestrator(
  objective="get malware code",
  attack_strategy="crescendo",
  prompt_target=OpenAITarget(...))
```

Strategies: single_turn, crescendo, PAIR, TAP, custom.

Converters: base64, rot13, ascii_smuggler, GCG suffix.

---

## Promptfoo

```yaml
redteam:
  numTests: 50
  plugins: [harmful, pii, prompt-extraction, excessive-agency]
```

CI/CD friendly. Regression suite.

---

## Algoritmos de jailbreak

| Algoritmo | Idea | Tipo |
|---|---|---|
| **GCG** | Sufijo adversarial por gradiente | Whitebox |
| **PAIR** | LLM atacante refina iterativo | Blackbox |
| **TAP** | PAIR en árbol con poda | Blackbox |
| **Crescendo** | Escalada multi-turn | Blackbox |

---

## Métricas

- **ASR** — % ataques exitosos.
- **FPR** — % queries legítimas bloqueadas.
- **Refusal rate** — % rechazos.
- **Coverage** — % espectro cubierto.

Sin coverage, ASR no se puede interpretar.

---

## Pipeline ideal

```
Cada commit  → Promptfoo smoke (PR bloqueante)
Cada release → Garak full
Mensual      → PyRIT campaign + manual creativo
Continuo     → subset Garak canary contra prod
```

---

## Madurez

- 0: nadie.
- 1: pentest manual ocasional.
- 2: Garak en CI.
- 3: Garak+PyRIT+Promptfoo, ASR como KPI exec.
- 4: Purple integrado SOC + threat-informed.

---

<!-- _class: lead invert -->

## Lab

Garak baseline → guardrails → comparar ASR
+ PyRIT crescendo + Promptfoo CI

→ `Modulo10/ejercicio.md`
