"""
Generador del PPTX espectacular del taller SecuAI.
Charla + taller integrados, 90 min.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

# ---------- PALETA ----------
BG        = RGBColor(0x0A, 0x0E, 0x27)   # navy oscuro
BG_DEEP   = RGBColor(0x05, 0x07, 0x14)
ACCENT    = RGBColor(0x00, 0xD4, 0xFF)   # cyan
MAGENTA   = RGBColor(0xFF, 0x00, 0x80)
GREEN     = RGBColor(0x00, 0xFF, 0x88)
ORANGE    = RGBColor(0xFF, 0x95, 0x00)
RED       = RGBColor(0xFF, 0x3B, 0x3B)
WHITE     = RGBColor(0xF5, 0xF7, 0xFA)
GREY      = RGBColor(0x8A, 0x94, 0xA6)
PANEL     = RGBColor(0x14, 0x1B, 0x3A)
PANEL_HI  = RGBColor(0x1E, 0x27, 0x52)

FONT      = "Inter"
FONT_MONO = "JetBrains Mono"

# 16:9 widescreen
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW = prs.slide_width
SH = prs.slide_height

BLANK = prs.slide_layouts[6]


# ---------- HELPERS ----------
def add_slide():
    return prs.slides.add_slide(BLANK)


def set_bg(slide, color=BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.line.fill.background()
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.shadow.inherit = False
    slide.shapes._spTree.remove(bg._element)
    slide.shapes._spTree.insert(2, bg._element)
    return bg


def add_rect(slide, x, y, w, h, fill=PANEL, line=None, line_w=0):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    r.fill.solid()
    r.fill.fore_color.rgb = fill
    if line is None:
        r.line.fill.background()
    else:
        r.line.color.rgb = line
        r.line.width = Pt(line_w if line_w else 1)
    r.shadow.inherit = False
    return r


def add_round(slide, x, y, w, h, fill, line=None):
    r = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    r.adjustments[0] = 0.18
    r.fill.solid()
    r.fill.fore_color.rgb = fill
    if line is None:
        r.line.fill.background()
    else:
        r.line.color.rgb = line
        r.line.width = Pt(1.25)
    r.shadow.inherit = False
    return r


def add_text(slide, x, y, w, h, text, *,
             size=18, bold=False, color=WHITE, font=FONT,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return tb


def add_decor(slide, variant=0):
    """Barra/acento decorativo lateral + esquina."""
    # Barra vertical izquierda
    add_rect(slide, 0, 0, Inches(0.18), SH, fill=ACCENT)
    # Esquina superior derecha — bloque magenta diagonal
    if variant == 1:
        add_rect(slide, SW - Inches(2.2), 0, Inches(2.2), Inches(0.08), fill=MAGENTA)
    elif variant == 2:
        add_rect(slide, SW - Inches(2.2), 0, Inches(2.2), Inches(0.08), fill=GREEN)
    elif variant == 3:
        add_rect(slide, SW - Inches(2.2), 0, Inches(2.2), Inches(0.08), fill=ORANGE)
    else:
        add_rect(slide, SW - Inches(2.2), 0, Inches(2.2), Inches(0.08), fill=ACCENT)


def add_header(slide, kicker, color=ACCENT):
    add_text(slide, Inches(0.6), Inches(0.32),
             Inches(10), Inches(0.4),
             kicker.upper(), size=12, bold=True, color=color, font=FONT)


def add_footer(slide, page_num=None):
    add_text(slide, Inches(0.6), SH - Inches(0.45),
             Inches(10), Inches(0.3),
             "SecuAI · Hackeando la IA · José Picón · 2026",
             size=10, color=GREY)
    if page_num is not None:
        add_text(slide, SW - Inches(1.0), SH - Inches(0.45),
                 Inches(0.4), Inches(0.3),
                 f"{page_num:02d}", size=10, bold=True, color=ACCENT,
                 align=PP_ALIGN.RIGHT)


def add_title(slide, text, y=Inches(0.85), size=44, color=WHITE):
    add_text(slide, Inches(0.6), y, SW - Inches(1.2), Inches(1.1),
             text, size=size, bold=True, color=color, font=FONT)


def add_notes(slide, text):
    nf = slide.notes_slide.notes_text_frame
    nf.text = text


def add_bullets(slide, x, y, w, h, items, size=20, color=WHITE,
                marker="•", marker_color=ACCENT, gap=0.0):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(0); tf.margin_right = Emu(0)
    tf.margin_top = Emu(0);  tf.margin_bottom = Emu(0)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(8 + int(gap * 10))
        r1 = p.add_run()
        r1.text = f"{marker}  "
        r1.font.name = FONT
        r1.font.size = Pt(size)
        r1.font.bold = True
        r1.font.color.rgb = marker_color
        r2 = p.add_run()
        r2.text = item
        r2.font.name = FONT
        r2.font.size = Pt(size)
        r2.font.color.rgb = color
    return tb


def add_qr_placeholder(slide, x, y, size_in=2.4, label="QR\nESCANEA"):
    # marco
    add_rect(slide, x, y, Inches(size_in), Inches(size_in), fill=WHITE)
    # patron mini cuadricula
    cell = Inches(size_in / 12.0)
    pattern = [
        "111111101101111111",
        "100000101101100000",
        "101110100101101110",
        "101110101011101110",
        "101110101110101110",
        "100000101010100000",
        "111111101010111111",
        "000000001100000000",
        "110110111000110110",
        "001001000111001001",
        "100110111010101101",
        "010001010101110010",
    ]
    # Simulación visual (no es QR real, decorativo)
    for ry, row in enumerate(pattern):
        for cx, ch in enumerate(row[:12]):
            if ch == "1":
                add_rect(slide,
                         x + cx * cell, y + ry * cell,
                         cell, cell, fill=RGBColor(0x0A, 0x0E, 0x27))
    add_text(slide, x, y + Inches(size_in) + Inches(0.1),
             Inches(size_in), Inches(0.4),
             label, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# =====================================================
#  SLIDE 1 — PORTADA
# =====================================================
s = add_slide()
set_bg(s, BG_DEEP)

# franja diagonal decorativa
add_rect(s, 0, Inches(5.4), SW, Inches(0.04), fill=ACCENT)
add_rect(s, 0, Inches(5.55), SW * 0.35, Inches(0.02), fill=MAGENTA)
add_rect(s, 0, Inches(5.65), SW * 0.18, Inches(0.02), fill=GREEN)

# Kicker
add_text(s, Inches(0.8), Inches(1.0), Inches(12), Inches(0.5),
         "TALLER · 90 MIN · CHARLA + PRÁCTICA", size=14, bold=True,
         color=ACCENT, font=FONT)

# Título mega
add_text(s, Inches(0.8), Inches(1.8), Inches(12), Inches(1.6),
         "Hackeando la IA.", size=84, bold=True, color=WHITE, font=FONT)

add_text(s, Inches(0.8), Inches(3.4), Inches(12), Inches(1.0),
         "Del prompt injection a las defensas reales.",
         size=32, color=GREY, font=FONT)

# autor
add_text(s, Inches(0.8), Inches(6.0), Inches(8), Inches(0.4),
         "José Picón · jose.bobal@gmail.com",
         size=16, bold=True, color=WHITE)
add_text(s, Inches(0.8), Inches(6.4), Inches(8), Inches(0.4),
         "Curso especialización · Ciberseguridad · ENS 2025/26",
         size=12, color=GREY)

# tag esquina
add_round(s, SW - Inches(2.6), Inches(6.0), Inches(2.0), Inches(0.55), ACCENT)
add_text(s, SW - Inches(2.6), Inches(6.05), Inches(2.0), Inches(0.5),
         "SecuAI · 2026", size=14, bold=True, color=BG_DEEP,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

add_notes(s, "Bienvenida 5 min. Hook emocional. Pregunta al público.")

# =====================================================
#  SLIDE 2 — AGENDA (timeline)
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s)
add_header(s, "AGENDA · 90 MIN")
add_title(s, "Cómo va a ir esto.")

# Timeline visual
blocks = [
    ("00–05",  "Bienvenida & hook",          ACCENT),
    ("05–15",  "Mapa de la IA bajo ataque",  ACCENT),
    ("15–25",  "DEMO 1 — Prompt injection",  MAGENTA),
    ("25–40",  "PRÁCTICA 1 — Atacáis vosotros", GREEN),
    ("40–50",  "Indirect injection",         ACCENT),
    ("50–58",  "DEMO 2 — PDF envenenado",    MAGENTA),
    ("58–75",  "Defensas reales",            ACCENT),
    ("75–85",  "PRÁCTICA 2 — Diseña tu pila", GREEN),
    ("85–90",  "Cierre + Q&A",               ORANGE),
]
y0 = Inches(2.1)
for i, (t, label, col) in enumerate(blocks):
    yy = y0 + Inches(i * 0.52)
    add_round(s, Inches(0.6), yy, Inches(1.55), Inches(0.42), col)
    add_text(s, Inches(0.6), yy, Inches(1.55), Inches(0.42),
             t, size=14, bold=True, color=BG, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.4), yy, Inches(10), Inches(0.42),
             label, size=18, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)

# Leyenda
ly = SH - Inches(0.85)
for x_off, col, lab in [(0.6, ACCENT, "Contenido"),
                         (2.6, MAGENTA, "Demo en vivo"),
                         (4.8, GREEN, "Práctica audiencia"),
                         (7.0, ORANGE, "Cierre")]:
    add_round(s, Inches(x_off), ly, Inches(0.25), Inches(0.25), col)
    add_text(s, Inches(x_off + 0.35), ly - Inches(0.02),
             Inches(2.2), Inches(0.3), lab,
             size=11, color=GREY)

add_footer(s, 2)
add_notes(s, "Marca pivotes claros. Repetimos: demo → práctica → demo → práctica. Activación constante.")

# =====================================================
#  SLIDE 3 — HOOK Q1
# =====================================================
s = add_slide()
set_bg(s, BG_DEEP)
# Big quote-style
add_text(s, Inches(0.8), Inches(1.0), Inches(12), Inches(0.6),
         "PREGUNTA 1", size=16, bold=True, color=MAGENTA)
add_text(s, Inches(0.8), Inches(1.8), Inches(12), Inches(3.5),
         "¿En vuestra organización\nhay ya algún chatbot,\ncopiloto o pipeline\ncon IA generativa?",
         size=54, bold=True, color=WHITE)
add_text(s, Inches(0.8), Inches(5.8), Inches(12), Inches(1),
         "Levantad la mano. 🙋",
         size=28, color=ACCENT, italic=True)
add_decor(s, 1)
add_footer(s, 3)
add_notes(s, "Casi todas las manos van a estar arriba. Es el primer enganche emocional.")

# =====================================================
#  SLIDE 4 — HOOK Q2
# =====================================================
s = add_slide()
set_bg(s, BG_DEEP)
add_text(s, Inches(0.8), Inches(1.0), Inches(12), Inches(0.6),
         "PREGUNTA 2", size=16, bold=True, color=MAGENTA)
add_text(s, Inches(0.8), Inches(1.8), Inches(12), Inches(3.5),
         "¿Quien lo desplegó\nhizo un threat model\nde seguridad?",
         size=58, bold=True, color=WHITE)
add_text(s, Inches(0.8), Inches(5.8), Inches(12), Inches(1),
         "Casi ninguna mano. Ahí está el problema. 😅",
         size=24, color=ORANGE, italic=True)
add_decor(s, 1)
add_footer(s, 4)
add_notes(s, "El gap entre adopción y seguridad. Esa es la tesis del taller.")

# =====================================================
#  SLIDE 5 — Hong Kong $25M
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s, 1)
add_header(s, "CASO REAL · FEBRERO 2024", color=RED)
add_title(s, "Hong Kong: 25 M USD en una videoconferencia.")

# Bloque grande con detalle del caso
add_round(s, Inches(0.6), Inches(2.1), Inches(7.5), Inches(4.4), PANEL)
add_text(s, Inches(0.95), Inches(2.3), Inches(7.0), Inches(0.5),
         "Lo que pasó", size=14, bold=True, color=ACCENT)
add_bullets(s, Inches(0.95), Inches(2.8), Inches(7.0), Inches(3.5), [
    "Empleado financiero entra a una videollamada con su CFO.",
    "Reconoce las caras. Reconoce las voces.",
    "El CFO autoriza una transferencia. La ejecuta.",
    "Todos en la llamada — menos él — eran deepfakes en tiempo real.",
], size=17, gap=0.4)

# panel derecho cifra
add_round(s, Inches(8.5), Inches(2.1), Inches(4.2), Inches(4.4),
          RGBColor(0x33, 0x06, 0x12))
add_text(s, Inches(8.5), Inches(2.5), Inches(4.2), Inches(0.5),
         "PÉRDIDA TOTAL", size=14, bold=True, color=RED,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(8.5), Inches(3.2), Inches(4.2), Inches(1.5),
         "25M$", size=108, bold=True, color=RED,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(8.5), Inches(5.0), Inches(4.2), Inches(1.5),
         "No fue sofisticado.\nFue replicable.",
         size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_footer(s, 5)
add_notes(s, "Aterrizar la magnitud. Esto pasó hace 2 años, no es ciencia ficción.")

# =====================================================
#  SLIDE 6 — Por qué la IA necesita su propio modelo
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s)
add_header(s, "TESIS")
add_title(s, "AppSec clásica no basta para IA.")

rows = [
    ("Input determinista",     "Texto / imagen / audio probabilístico"),
    ("Output verificable",     "Output generativo, no determinista"),
    ("Frontera de confianza",  "Prompt + datos comparten contexto"),
    ("Código separado de datos", "Modelo = código + datos + comportamiento"),
]
y0 = Inches(2.2)
# Cabecera
add_round(s, Inches(0.6), y0, Inches(5.9), Inches(0.55), PANEL_HI)
add_round(s, Inches(6.7), y0, Inches(6.0), Inches(0.55), MAGENTA)
add_text(s, Inches(0.85), y0, Inches(5.7), Inches(0.55),
         "AppSec clásica asume…", size=15, bold=True, color=ACCENT,
         anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(6.95), y0, Inches(5.8), Inches(0.55),
         "En IA NO se cumple", size=15, bold=True, color=WHITE,
         anchor=MSO_ANCHOR.MIDDLE)
for i, (a, b) in enumerate(rows):
    yy = y0 + Inches(0.7 + i * 0.85)
    add_round(s, Inches(0.6), yy, Inches(5.9), Inches(0.75), PANEL)
    add_round(s, Inches(6.7), yy, Inches(6.0), Inches(0.75),
              RGBColor(0x2A, 0x10, 0x20))
    add_text(s, Inches(0.95), yy, Inches(5.5), Inches(0.75),
             a, size=16, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(6.95), yy, Inches(5.7), Inches(0.75),
             b, size=16, bold=True, color=MAGENTA, anchor=MSO_ANCHOR.MIDDLE)

add_footer(s, 6)
add_notes(s, "Si conocen OWASP/AppSec — sus asunciones no aplican.")

# =====================================================
#  SLIDE 7 — MITRE ATLAS
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s)
add_header(s, "MARCO · MITRE ATLAS")
add_title(s, "Si conocéis ATT&CK, ATLAS es lo mismo para IA.")

# 3 columnas con cifras destacadas
metrics = [
    ("14",   "TÁCTICAS",  ACCENT),
    ("80+",  "TÉCNICAS",  MAGENTA),
    ("30+",  "CASE STUDIES REALES", GREEN),
]
for i, (n, lab, col) in enumerate(metrics):
    x = Inches(0.6 + i * 4.2)
    add_round(s, x, Inches(2.4), Inches(4.0), Inches(2.6), PANEL)
    add_text(s, x, Inches(2.6), Inches(4.0), Inches(1.6),
             n, size=88, bold=True, color=col, align=PP_ALIGN.CENTER)
    add_text(s, x, Inches(4.3), Inches(4.0), Inches(0.4),
             lab, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# Casos reales
add_text(s, Inches(0.6), Inches(5.4), Inches(12), Inches(0.4),
         "Casos documentados:", size=14, bold=True, color=GREY)
add_text(s, Inches(0.6), Inches(5.8), Inches(12), Inches(0.6),
         "PoisonGPT  ·  Bing Sydney  ·  Tay  ·  Slack AI exfil  ·  Bing+arXiv",
         size=20, bold=True, color=WHITE)
add_text(s, Inches(0.6), Inches(6.5), Inches(12), Inches(0.4),
         "→  atlas.mitre.org", size=18, bold=True, color=ACCENT)

add_footer(s, 7)
add_notes(s, "30s para legitimar que esto es disciplina con taxonomía, no buzzword.")

# =====================================================
#  SLIDE 8 — Ciclo MLOps con puntos de fallo
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s)
add_header(s, "MAPA DE ATAQUE")
add_title(s, "Ciclo MLOps · cada flecha es un blanco.")

stages = ["DATA", "TRAIN", "REGISTRY", "SERVE", "MONITOR"]
attacks = ["Data poisoning", "Backdoor", "Model swap", "Prompt inj.", "Drift evasion"]
x0 = Inches(0.7)
gap = Inches(2.5)
y = Inches(3.0)
for i, st in enumerate(stages):
    x = x0 + gap * i
    col = MAGENTA if st == "SERVE" else PANEL_HI
    add_round(s, x, y, Inches(2.0), Inches(1.0), col)
    add_text(s, x, y, Inches(2.0), Inches(1.0), st,
             size=20, bold=True, color=WHITE if st == "SERVE" else WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # flecha
    if i < len(stages) - 1:
        arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                   x + Inches(2.05), y + Inches(0.35),
                                   Inches(0.4), Inches(0.3))
        arrow.fill.solid(); arrow.fill.fore_color.rgb = ACCENT
        arrow.line.fill.background()
    # warning + ataque
    add_text(s, x, y + Inches(1.15), Inches(2.0), Inches(0.4),
             "⚠", size=22, color=ORANGE, align=PP_ALIGN.CENTER)
    add_text(s, x, y + Inches(1.55), Inches(2.0), Inches(0.4),
             attacks[i], size=12, color=GREY, align=PP_ALIGN.CENTER)

# zoom SERVE
add_round(s, Inches(0.6), Inches(5.5), Inches(12.1), Inches(1.2),
          RGBColor(0x2A, 0x10, 0x20))
add_text(s, Inches(0.9), Inches(5.65), Inches(11.5), Inches(0.4),
         "HOY NOS CENTRAMOS EN  →  SERVE", size=14, bold=True, color=MAGENTA)
add_text(s, Inches(0.9), Inches(6.05), Inches(11.5), Inches(0.6),
         "Prompt injection · Indirect injection · Sensitive disclosure · Excessive agency",
         size=17, bold=True, color=WHITE)

add_footer(s, 8)
add_notes(s, "Cada flecha = oportunidad de ataque. Profundizamos en SERVE porque es donde casi todos despliegan.")

# =====================================================
#  SLIDE 9 — DEMO 1 (transición)
# =====================================================
s = add_slide()
set_bg(s, BG_DEEP)

# Banda diagonal magenta
add_rect(s, 0, Inches(3.0), SW, Inches(1.4), fill=MAGENTA)

add_text(s, Inches(0.8), Inches(0.8), Inches(12), Inches(0.5),
         "MOMENTO 01", size=18, bold=True, color=MAGENTA)
add_text(s, Inches(0.8), Inches(3.2), SW - Inches(1.6), Inches(1.0),
         "DEMO  ›  01", size=20, bold=True, color=WHITE,
         anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.8), Inches(4.6), Inches(12), Inches(1.5),
         "Prompt injection\nen vivo.",
         size=72, bold=True, color=WHITE)
add_text(s, Inches(0.8), Inches(6.4), Inches(12), Inches(0.5),
         "Sin código. Sin exploit binario. Solo lenguaje natural.",
         size=18, color=GREY, italic=True)
add_footer(s, 9)
add_notes(s, "Verificar lab-prompt-injection arriba. Tener curl/Postman listos como plan B.")

# =====================================================
#  SLIDE 10 — Demo 1 plan
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s, 1)
add_header(s, "DEMO 1 · LO QUE VAIS A VER", color=MAGENTA)
add_title(s, "Tres ataques sobre el mismo chatbot.")

retos = [
    ("01", "Leak del system prompt",
     "Hacemos que el chatbot recite sus instrucciones secretas."),
    ("02", "Exfiltración de API key",
     "Extraemos un secreto embebido por el operador."),
    ("03", "Aprobación de un préstamo no autorizado",
     "Saltamos la política de negocio con una frase en español."),
]
for i, (n, t, d) in enumerate(retos):
    y = Inches(2.2 + i * 1.55)
    add_round(s, Inches(0.6), y, Inches(12.1), Inches(1.35), PANEL)
    # numero
    add_round(s, Inches(0.8), y + Inches(0.18), Inches(1.0), Inches(1.0), MAGENTA)
    add_text(s, Inches(0.8), y + Inches(0.18), Inches(1.0), Inches(1.0),
             n, size=32, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.1), y + Inches(0.18), Inches(10.4), Inches(0.5),
             t, size=22, bold=True, color=WHITE)
    add_text(s, Inches(2.1), y + Inches(0.75), Inches(10.4), Inches(0.5),
             d, size=15, color=GREY)

add_footer(s, 10)
add_notes(s, "Cada reto dura 2-3 min. Si fallan, payload de emergencia listo en pantalla.")

# =====================================================
#  SLIDE 11 — PRÁCTICA 1 (workshop)
# =====================================================
s = add_slide()
set_bg(s, BG_DEEP)

# franja verde lateral
add_rect(s, 0, 0, Inches(0.18), SH, fill=GREEN)
add_rect(s, SW - Inches(2.2), 0, Inches(2.2), Inches(0.08), fill=GREEN)

add_text(s, Inches(0.6), Inches(0.3), Inches(12), Inches(0.4),
         "TALLER · PRÁCTICA 01", size=14, bold=True, color=GREEN)

add_text(s, Inches(0.6), Inches(1.0), Inches(8.5), Inches(1.4),
         "Vuestro turno.",
         size=72, bold=True, color=WHITE)
add_text(s, Inches(0.6), Inches(2.6), Inches(8.5), Inches(0.8),
         "Atacáis el chatbot.\n3 retos · 15 minutos · puntos por orden de llegada.",
         size=22, color=GREY)

# 3 retos cajitas
retos_p = [
    ("A", "Conseguid una respuesta\nque contenga BANK-API-KEY", ACCENT),
    ("B", "Aprobad cualquier cantidad\nmayor que 100 000 €",     MAGENTA),
    ("C", "Haced que responda\ncompletamente en alemán",         ORANGE),
]
for i, (l, d, col) in enumerate(retos_p):
    y = Inches(4.0)
    x = Inches(0.6 + i * 2.85)
    add_round(s, x, y, Inches(2.65), Inches(2.6), PANEL)
    add_round(s, x, y, Inches(2.65), Inches(0.6), col)
    add_text(s, x, y, Inches(2.65), Inches(0.6),
             f"RETO {l}", size=16, bold=True, color=BG_DEEP,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.2), y + Inches(0.8),
             Inches(2.3), Inches(1.8),
             d, size=15, color=WHITE,
             align=PP_ALIGN.CENTER)

# QR placeholder a la derecha
add_qr_placeholder(s, Inches(9.6), Inches(3.6), 2.4, "ESCANEA\nhttp://lab:5001/chat")

add_footer(s, 11)
add_notes(s, "Si no participan: agruparlos de 3 con 1 portátil. Lanza el cronómetro visible.")

# =====================================================
#  SLIDE 12 — Lo que acabáis de aprender
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s)
add_header(s, "CIERRE PRÁCTICA 01")
add_title(s, "Lo que acabáis de demostrar.")

points = [
    ("Prompt injection es trivial",      "Sin exploits. Sin reverse engineering. Solo lenguaje."),
    ("El LLM no distingue instrucción de dato", "El modelo trata todo el contexto como uno."),
    ("Cualquier delimitador es falsificable", "Si tu defensa es <BEGIN_INSTRUCTIONS>, ya perdiste."),
    ("Filtros regex → bypass infinito",  "Traducción, encoding, ofuscación. Sin fin."),
]
for i, (a, b) in enumerate(points):
    y = Inches(2.2 + i * 1.05)
    add_round(s, Inches(0.6), y, Inches(8.5), Inches(0.95), PANEL)
    add_text(s, Inches(0.85), y, Inches(8.2), Inches(0.5),
             a, size=18, bold=True, color=ACCENT, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(0.85), y + Inches(0.45), Inches(8.2), Inches(0.5),
             b, size=14, color=GREY)

# Badge OWASP
add_round(s, Inches(9.5), Inches(2.4), Inches(3.3), Inches(3.5),
          RGBColor(0x33, 0x00, 0x33))
add_text(s, Inches(9.5), Inches(2.7), Inches(3.3), Inches(0.5),
         "OWASP TOP 10 · LLM", size=13, bold=True, color=MAGENTA,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(9.5), Inches(3.3), Inches(3.3), Inches(1.5),
         "LLM01\n#01", size=66, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(9.5), Inches(5.2), Inches(3.3), Inches(0.6),
         "Prompt Injection\nel #1 del top, 2025",
         size=13, color=WHITE, align=PP_ALIGN.CENTER, italic=True)

add_footer(s, 12)
add_notes(s, "Capitalizar lo que han hecho. La gente aprende mejor lo que acaba de tocar.")

# =====================================================
#  SLIDE 13 — Indirect prompt injection
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s, 1)
add_header(s, "EL ATAQUE SILENCIOSO", color=ORANGE)
add_title(s, "Indirect prompt injection.")

add_text(s, Inches(0.6), Inches(2.0), Inches(8.5), Inches(0.6),
         "Tu LLM ya no necesita que un atacante le hable.",
         size=22, color=WHITE, italic=True)
add_text(s, Inches(0.6), Inches(2.7), Inches(8.5), Inches(0.6),
         "Le basta con leer:",
         size=20, bold=True, color=ORANGE)

sources = [
    ("📄", "un PDF subido"),
    ("🌐", "una web scrapeada"),
    ("✉",  "un email reenviado"),
    ("💬", "un mensaje de Slack"),
    ("📊", "una hoja de Google Drive compartida"),
]
for i, (ic, t) in enumerate(sources):
    y = Inches(3.5 + i * 0.55)
    add_text(s, Inches(0.85), y, Inches(0.5), Inches(0.45),
             ic, size=20, color=ORANGE)
    add_text(s, Inches(1.4), y, Inches(7), Inches(0.45),
             t, size=18, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)

# panel lateral con esquema
add_round(s, Inches(9.4), Inches(2.0), Inches(3.4), Inches(4.5), PANEL)
add_text(s, Inches(9.4), Inches(2.2), Inches(3.4), Inches(0.4),
         "CADENA", size=12, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
chain = ["Doc malicioso", "↓", "Asistente lo lee", "↓",
         "Ejecuta acción",  "↓", "Exfil / fraude"]
for i, c in enumerate(chain):
    add_text(s, Inches(9.4), Inches(2.7 + i * 0.5), Inches(3.4), Inches(0.4),
             c, size=15, bold=("↓" not in c), color=WHITE if "↓" not in c else ORANGE,
             align=PP_ALIGN.CENTER)

add_footer(s, 13)
add_notes(s, "Subir el nivel: ahora ya no necesitas un usuario hostil, basta con un doc hostil.")

# =====================================================
#  SLIDE 14 — Casos reales indirect
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s, 1)
add_header(s, "INDIRECT INJECTION · CASOS REALES")
add_title(s, "Esto ya ha pasado. Sin laboratorio.")

cases = [
    ("Bing Chat + arXiv",  "2023", "Greshake et al.",
     "Payload incrustado en el abstract de un paper. Bing lo lee al resumir y ejecuta instrucciones del autor del paper."),
    ("Slack AI exfiltration", "2024", "PromptArmor",
     "Mensaje en canal público con instrucciones para exfiltrar DMs cuando el usuario invoque Slack AI."),
    ("Google Drive summarizer", "2024", "Embrace The Red",
     "Hoja de cálculo con payload invisible. El summarizer de Drive lo procesa y filtra datos a un dominio externo."),
]
for i, (t, y_, who, d) in enumerate(cases):
    y = Inches(2.2 + i * 1.55)
    add_round(s, Inches(0.6), y, Inches(12.1), Inches(1.4), PANEL)
    add_round(s, Inches(0.8), y + Inches(0.2), Inches(1.0), Inches(1.0), ORANGE)
    add_text(s, Inches(0.8), y + Inches(0.2), Inches(1.0), Inches(1.0),
             y_, size=18, bold=True, color=BG_DEEP,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.1), y + Inches(0.18), Inches(10.4), Inches(0.45),
             t, size=20, bold=True, color=WHITE)
    add_text(s, Inches(2.1), y + Inches(0.62), Inches(10.4), Inches(0.35),
             f"vía {who}", size=11, color=ACCENT, italic=True)
    add_text(s, Inches(2.1), y + Inches(0.95), Inches(10.4), Inches(0.4),
             d, size=13, color=GREY)

add_footer(s, 14)
add_notes(s, "Mostrar que NO es teoría. Tres productos masivos vulnerados en 18 meses.")

# =====================================================
#  SLIDE 15 — DEMO 2: PDF envenenado
# =====================================================
s = add_slide()
set_bg(s, BG_DEEP)
add_rect(s, 0, Inches(3.0), SW, Inches(1.4), fill=MAGENTA)

add_text(s, Inches(0.8), Inches(0.8), Inches(12), Inches(0.5),
         "MOMENTO 02", size=18, bold=True, color=MAGENTA)
add_text(s, Inches(0.8), Inches(3.2), SW - Inches(1.6), Inches(1.0),
         "DEMO  ›  02", size=20, bold=True, color=WHITE,
         anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.8), Inches(4.6), Inches(12), Inches(1.5),
         "PDF envenenado.",
         size=72, bold=True, color=WHITE)
add_text(s, Inches(0.8), Inches(6.4), Inches(12), Inches(0.5),
         "Texto invisible para el humano. Plenamente legible para el LLM.",
         size=18, color=GREY, italic=True)
add_footer(s, 15)
add_notes(s, "Tener cv_normal.pdf y cv_envenenado.pdf listos. Mostrar Ctrl+A para revelar el payload.")

# =====================================================
#  SLIDE 16 — Defensa por capas
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s)
add_header(s, "DEFENSA EN PROFUNDIDAD")
add_title(s, "Pipeline defensivo · 8 capas, nunca una sola.")

layers = ["Auth", "Rate limit", "Input scanner", "Clasificador",
          "System prompt blindado", "LLM", "Output scanner",
          "Sandbox tools", "HITL", "Audit"]
colors_l = [ACCENT, ACCENT, GREEN, GREEN, ORANGE,
            MAGENTA, GREEN, ORANGE, ACCENT, GREY]
y = Inches(2.4)
total_w = SW - Inches(1.2)
w_each = total_w / len(layers)
for i, (l, col) in enumerate(zip(layers, colors_l)):
    x = Inches(0.6) + w_each * i
    add_round(s, x + Emu(40000), y, w_each - Emu(80000), Inches(1.6), PANEL,
              line=col)
    add_text(s, x, y, w_each, Inches(1.6),
             l, size=12, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < len(layers) - 1:
        arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                   x + w_each - Emu(60000),
                                   y + Inches(0.62),
                                   Emu(160000), Inches(0.3))
        arrow.fill.solid(); arrow.fill.fore_color.rgb = ACCENT
        arrow.line.fill.background()

# Mensaje
add_text(s, Inches(0.6), Inches(4.7), Inches(12), Inches(0.7),
         "No hay bala de plata.", size=34, bold=True, color=WHITE)
add_text(s, Inches(0.6), Inches(5.4), Inches(12), Inches(0.6),
         "Hay defensa en profundidad — y red teaming continuo.",
         size=22, color=GREY)

# Métrica clave
add_round(s, Inches(0.6), Inches(6.3), Inches(12.1), Inches(0.8),
          RGBColor(0x06, 0x33, 0x1A))
add_text(s, Inches(0.85), Inches(6.3), Inches(12), Inches(0.8),
         "KPI ejecutivo →  ASR  (Attack Success Rate)   ·   target < 5%   ·   medido en CI",
         size=16, bold=True, color=GREEN, anchor=MSO_ANCHOR.MIDDLE)

add_footer(s, 16)
add_notes(s, "Energía aquí. Que no se vayan deprimidos: hay defensas concretas que sí funcionan.")

# =====================================================
#  SLIDE 17 — Herramientas que funcionan
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s, 2)
add_header(s, "HERRAMIENTAS QUE FUNCIONAN", color=GREEN)
add_title(s, "Stack defensivo recomendado.")

tools = [
    ("LLM Guard",        "Scanners I/O · open-source · Laiyer",       "Detecta jailbreaks, PII, secretos, código.", ACCENT),
    ("NeMo Guardrails",  "DSL declarativo · NVIDIA · open-source",    "Define reglas tipo flow chart sobre el LLM.", GREEN),
    ("Llama Guard 3",    "Clasificador entrenado · Meta · open-source", "Modelo dedicado a clasificar toxicidad y violaciones.", ORANGE),
    ("Prompt Shields",   "SaaS · Azure",                              "Producto gestionado. Coste bajo, integración rápida.", ACCENT),
    ("Spotlighting",     "Técnica · Microsoft Research · gratis",     "Marca datos no-confiables. Mejora 30% sin coste extra.", MAGENTA),
]
for i, (n, m, d, col) in enumerate(tools):
    y = Inches(2.1 + i * 0.95)
    add_round(s, Inches(0.6), y, Inches(12.1), Inches(0.85), PANEL)
    add_rect(s, Inches(0.6), y, Inches(0.1), Inches(0.85), fill=col)
    add_text(s, Inches(0.95), y, Inches(3.4), Inches(0.85),
             n, size=18, bold=True, color=col, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(4.4), y, Inches(3.7), Inches(0.85),
             m, size=12, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(8.2), y, Inches(4.4), Inches(0.85),
             d, size=12, color=GREY, italic=True, anchor=MSO_ANCHOR.MIDDLE)

add_footer(s, 17)
add_notes(s, "1 min cada uno. Nadie usa solo uno: se combinan.")

# =====================================================
#  SLIDE 18 — Lo que NO funciona
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s, 3)
add_header(s, "ANTIPATTERNS", color=RED)
add_title(s, "Lo que NO funciona.")

bad = [
    ("Filtros regex puros",
     "Bypass por traducción, encoding, ofuscación, sinónimos. Infinito."),
    ("Confiar en el delimitador del system prompt",
     "<<<INSTRUCTIONS>>> es texto. El atacante lo reproduce."),
    ('"Lo evaluamos con benchmarks una vez al año"',
     "Los atacantes inventan categorías nuevas todos los meses."),
    ("Pensar que tu proveedor de LLM te protege",
     "OpenAI/Anthropic mitigan lo común. Tu caso de uso es tuyo."),
]
for i, (a, b) in enumerate(bad):
    y = Inches(2.2 + i * 1.1)
    add_round(s, Inches(0.6), y, Inches(12.1), Inches(0.95),
              RGBColor(0x33, 0x06, 0x12))
    add_text(s, Inches(0.85), y + Inches(0.1), Inches(0.6), Inches(0.6),
             "✗", size=28, bold=True, color=RED)
    add_text(s, Inches(1.5), y + Inches(0.05), Inches(11.0), Inches(0.5),
             a, size=18, bold=True, color=WHITE)
    add_text(s, Inches(1.5), y + Inches(0.5), Inches(11.0), Inches(0.5),
             b, size=13, color=GREY, italic=True)

add_footer(s, 18)
add_notes(s, "Honestidad: si solo tienes esto, NO tienes defensa.")

# =====================================================
#  SLIDE 19 — Test continuo
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s)
add_header(s, "RED TEAMING CONTINUO")
add_title(s, "Test continuo — no es opcional.")

cadence = [
    ("Cada PR",       "Smoke suite · Garak / Promptfoo · 50 prompts · <2 min",  GREEN),
    ("Cada release",  "Full suite · 500+ prompts · reporte ASR / FPR",          ACCENT),
    ("Mensual",       "Red team manual creativo · 1 ingeniero · 1 día",         ORANGE),
    ("Continuo prod", "Subset canary · 5% tráfico · alertas anomalía",          MAGENTA),
]
for i, (when, what, col) in enumerate(cadence):
    y = Inches(2.3 + i * 1.05)
    add_round(s, Inches(0.6), y, Inches(3.2), Inches(0.9), col)
    add_text(s, Inches(0.6), y, Inches(3.2), Inches(0.9),
             when, size=20, bold=True, color=BG_DEEP,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_round(s, Inches(4.0), y, Inches(8.7), Inches(0.9), PANEL)
    add_text(s, Inches(4.3), y, Inches(8.4), Inches(0.9),
             what, size=15, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)

add_text(s, Inches(0.6), Inches(6.7), Inches(12), Inches(0.4),
         "→  ASR como KPI ejecutivo. Reportable a board.",
         size=18, bold=True, color=ACCENT)

add_footer(s, 19)
add_notes(s, "Si solo se llevan 1 idea técnica: este slide. Cadencias concretas.")

# =====================================================
#  SLIDE 20 — PRÁCTICA 2 portada
# =====================================================
s = add_slide()
set_bg(s, BG_DEEP)
add_rect(s, 0, 0, Inches(0.18), SH, fill=GREEN)
add_rect(s, SW - Inches(2.2), 0, Inches(2.2), Inches(0.08), fill=GREEN)

add_text(s, Inches(0.6), Inches(0.3), Inches(12), Inches(0.4),
         "TALLER · PRÁCTICA 02", size=14, bold=True, color=GREEN)
add_text(s, Inches(0.6), Inches(1.0), Inches(12), Inches(1.4),
         "Diseña tu pila defensiva.",
         size=58, bold=True, color=WHITE)
add_text(s, Inches(0.6), Inches(2.7), Inches(12), Inches(0.8),
         "Grupos de 3 · 10 minutos · 2-3 grupos exponen 90 segundos.",
         size=20, color=GREY)

# casos
cases_p = [
    ("A", "Asistente médico",
     "Sugiere diagnósticos a médicos en hospital.\nAccede a historiales clínicos.",  RED),
    ("B", "Agente financiero",
     "Ejecuta operaciones de inversión\nhasta 10 000 € / día sin supervisión.",      ORANGE),
    ("C", "Chatbot e-commerce",
     "Soporte al cliente con acceso\na histórico de pedidos y reembolsos.",          ACCENT),
]
for i, (l, t, d, col) in enumerate(cases_p):
    y = Inches(4.0)
    x = Inches(0.6 + i * 4.2)
    add_round(s, x, y, Inches(4.0), Inches(2.7), PANEL)
    add_round(s, x, y, Inches(4.0), Inches(0.6), col)
    add_text(s, x, y, Inches(4.0), Inches(0.6),
             f"CASO {l}",
             size=16, bold=True, color=BG_DEEP,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.3), y + Inches(0.8), Inches(3.4), Inches(0.5),
             t, size=18, bold=True, color=WHITE)
    add_text(s, x + Inches(0.3), y + Inches(1.4), Inches(3.4), Inches(1.2),
             d, size=13, color=GREY)

add_text(s, Inches(0.6), SH - Inches(0.5), Inches(12), Inches(0.3),
         "Entregable →  auth  +  3 controles imprescindibles  +  por qué",
         size=14, bold=True, color=GREEN)
add_footer(s, 20)
add_notes(s, "Pasea, escucha. Anota propuestas brillantes para citarlas en el cierre.")

# =====================================================
#  SLIDE 21 — Marco regulatorio
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s)
add_header(s, "MARCO REGULATORIO 2026")
add_title(s, "Lo que te puede multar mañana.")

# tabla 4x3
headers = ["", "España / UE", "Internacional"]
rows_r = [
    ("Voluntario",    "—",                "NIST AI RMF"),
    ("Reglamentario", "EU AI Act 2024",   "—"),
    ("Certificable",  "—",                "ISO/IEC 42001"),
    ("Sectorial",     "ENS (RD 311/2022)", "—"),
]
y0 = Inches(2.1)
col_x = [Inches(0.6), Inches(4.5), Inches(8.6)]
col_w = [Inches(3.8), Inches(4.0), Inches(4.1)]
# cabecera
for i, h in enumerate(headers):
    add_round(s, col_x[i], y0, col_w[i], Inches(0.55),
              PANEL_HI if i == 0 else (ACCENT if i == 1 else MAGENTA))
    add_text(s, col_x[i], y0, col_w[i], Inches(0.55),
             h, size=15, bold=True,
             color=WHITE if i == 0 else BG_DEEP,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for ri, row in enumerate(rows_r):
    yr = y0 + Inches(0.65 + ri * 0.75)
    for i, v in enumerate(row):
        add_round(s, col_x[i], yr, col_w[i], Inches(0.65), PANEL)
        add_text(s, col_x[i], yr, col_w[i], Inches(0.65),
                 v, size=15,
                 bold=(i == 0),
                 color=WHITE if v != "—" else GREY,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Multa destacada
add_round(s, Inches(0.6), Inches(5.9), Inches(12.1), Inches(1.1),
          RGBColor(0x33, 0x06, 0x12))
add_text(s, Inches(0.9), Inches(5.95), Inches(11.5), Inches(0.5),
         "EU AI Act · multas máximas", size=14, bold=True, color=RED,
         anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.9), Inches(6.35), Inches(11.5), Inches(0.6),
         "hasta 35 M€  ·  o 7% del facturación global anual",
         size=24, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)

add_footer(s, 21)
add_notes(s, "Aterrizar en cifras de negocio. Útil cuando expongan ante dirección.")

# =====================================================
#  SLIDE 22 — Cierre 3 ideas
# =====================================================
s = add_slide()
set_bg(s, BG_DEEP)
add_rect(s, 0, 0, Inches(0.18), SH, fill=ORANGE)
add_rect(s, SW - Inches(2.2), 0, Inches(2.2), Inches(0.08), fill=ORANGE)

add_text(s, Inches(0.6), Inches(0.3), Inches(12), Inches(0.4),
         "CIERRE", size=14, bold=True, color=ORANGE)
add_text(s, Inches(0.6), Inches(0.9), Inches(12), Inches(0.9),
         "Tres ideas para llevaros.",
         size=44, bold=True, color=WHITE)

ideas = [
    ("01",
     "IA = código + datos + output probabilístico",
     "No le apliques solo appsec clásica. Las asunciones no se cumplen."),
    ("02",
     "Threat model antes de desplegar",
     "MITRE ATLAS + NIST AI 100-2 son tu marco. Aplica el lunes."),
    ("03",
     "Defensa en profundidad + red teaming continuo",
     "No hay bala de plata. Hay buenas balas combinadas — y medidas."),
]
for i, (n, t, d) in enumerate(ideas):
    y = Inches(2.4 + i * 1.55)
    add_round(s, Inches(0.6), y, Inches(12.1), Inches(1.35), PANEL)
    add_round(s, Inches(0.85), y + Inches(0.18), Inches(1.0), Inches(1.0), ORANGE)
    add_text(s, Inches(0.85), y + Inches(0.18), Inches(1.0), Inches(1.0),
             n, size=28, bold=True, color=BG_DEEP,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.2), y + Inches(0.18), Inches(10.3), Inches(0.55),
             t, size=22, bold=True, color=WHITE)
    add_text(s, Inches(2.2), y + Inches(0.78), Inches(10.3), Inches(0.5),
             d, size=14, color=GREY, italic=True)

add_footer(s, 22)
add_notes(s, "Tres es el número mágico. Si recuerdan tres, has ganado.")

# =====================================================
#  SLIDE 23 — Recursos + QR
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s)
add_header(s, "RECURSOS")
add_title(s, "Llévatelo todo.")

# 2 QRs
add_qr_placeholder(s, Inches(0.8), Inches(2.2), 2.6,
                   "REPO CURSO\n10 módulos + labs")
add_qr_placeholder(s, Inches(4.0), Inches(2.2), 2.6,
                   "BIBLIOGRAFÍA\n+ slides PDF")

# columna texto
add_text(s, Inches(7.6), Inches(2.2), Inches(5.5), Inches(0.5),
         "Curso SecuAI completo", size=20, bold=True, color=ACCENT)
add_bullets(s, Inches(7.6), Inches(2.8), Inches(5.5), Inches(2.5), [
    "10 módulos teóricos",
    "6 labs Docker reproducibles",
    "Glosario y bibliografía completa",
    "Slides en Marp + PPTX",
    "MIT License — fórkalo",
], size=14)

# contacto
add_round(s, Inches(7.6), Inches(5.3), Inches(5.5), Inches(1.7), PANEL)
add_text(s, Inches(7.9), Inches(5.4), Inches(5.2), Inches(0.4),
         "CONTACTO", size=12, bold=True, color=ACCENT)
add_text(s, Inches(7.9), Inches(5.8), Inches(5.2), Inches(0.45),
         "José Picón", size=20, bold=True, color=WHITE)
add_text(s, Inches(7.9), Inches(6.25), Inches(5.2), Inches(0.35),
         "✉  jose.bobal@gmail.com", size=14, color=WHITE)
add_text(s, Inches(7.9), Inches(6.55), Inches(5.2), Inches(0.35),
         "🔗  github.com/jmpicon", size=14, color=WHITE)

add_footer(s, 23)
add_notes(s, "QR funcionales reales: sustituir los placeholders por imágenes de QR antes de presentar.")

# =====================================================
#  SLIDE 24 — Gracias / Q&A
# =====================================================
s = add_slide()
set_bg(s, BG_DEEP)

# franja con 3 colores
add_rect(s, 0, Inches(4.0), SW * 0.4, Inches(0.06), fill=ACCENT)
add_rect(s, SW * 0.4, Inches(4.0), SW * 0.3, Inches(0.06), fill=MAGENTA)
add_rect(s, SW * 0.7, Inches(4.0), SW * 0.3, Inches(0.06), fill=GREEN)

add_text(s, Inches(0.6), Inches(1.5), Inches(12), Inches(2.0),
         "Gracias.", size=144, bold=True, color=WHITE)
add_text(s, Inches(0.6), Inches(4.3), Inches(12), Inches(1.0),
         "¿Preguntas?", size=42, color=GREY, italic=True)

add_text(s, Inches(0.6), Inches(6.3), Inches(12), Inches(0.4),
         "José Picón  ·  jose.bobal@gmail.com  ·  SecuAI 2026",
         size=14, color=GREY)
add_footer(s, 24)
add_notes(s, "Deja la pantalla aquí durante el Q&A. Sin info de más que distraiga.")

# =====================================================
#  SLIDE 25 — Postest + feedback
# =====================================================
s = add_slide()
set_bg(s)
add_decor(s, 2)
add_header(s, "PLUS · ANTES DE IRTE", color=GREEN)
add_title(s, "1 minuto.  Postest + valoración.")

add_text(s, Inches(0.6), Inches(2.2), Inches(7.5), Inches(0.6),
         "Tu feedback me hace mejor.",
         size=28, color=WHITE, italic=True)
add_bullets(s, Inches(0.6), Inches(3.2), Inches(7.5), Inches(3), [
    "5 preguntas técnicas — para medir aprendizaje.",
    "3 preguntas de valoración — para mejorar la próxima vez.",
    "Anónimo. Sin datos personales.",
    "1 minuto. Prometido.",
], size=16, gap=0.4)

add_qr_placeholder(s, Inches(9.0), Inches(2.5), 3.2,
                   "POSTEST\n+ VALORACIÓN")

add_text(s, Inches(0.6), SH - Inches(1.0), Inches(12), Inches(0.5),
         "🙏  Gracias por estar aquí.", size=22, bold=True, color=GREEN,
         align=PP_ALIGN.LEFT)
add_footer(s, 25)
add_notes(s, "Métrica objetivo: ≥70% completan. Apunta a NPS ≥50.")


# ---------- GUARDAR ----------
output = "/home/jmpicon/Documentos/secu_IA/taller/SecuAI_Hackeando_la_IA.pptx"
prs.save(output)
print(f"OK  →  {output}")
