"""
Genera los QRs reales que se incrustarán en el PPTX.
URLs apuntan al repo público https://github.com/jmpicon/SecuAI-jmpicon
"""
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw
from pathlib import Path

OUT = Path("/home/jmpicon/Documentos/secu_IA/taller/qrs")
OUT.mkdir(exist_ok=True)

REPO = "https://github.com/jmpicon/SecuAI-jmpicon"

TARGETS = {
    "repo":          REPO,
    "slides":        f"{REPO}/blob/main/taller/SecuAI_Hackeando_la_IA.pptx",
    "biblio":        f"{REPO}/blob/main/Modulo1/bibliografia.md",
    "lab_chat":      f"{REPO}/tree/main/labs/prompt-injection",
    "lab_rag":       f"{REPO}/tree/main/labs/rag-poisoning",
    "pretest":       f"{REPO}/blob/main/taller/formularios/pretest.md",
    "postest":       f"{REPO}/blob/main/taller/formularios/postest.md",
    "kit":           f"{REPO}/tree/main/taller/kit-asistentes",
    "guion":         f"{REPO}/blob/main/taller/guion-ponente.md",
    "glosario":      f"{REPO}/blob/main/GLOSARIO.md",
    "modulos":       f"{REPO}/tree/main/Modulo1",
}


def make_qr(data, path, fg=(10, 14, 39), bg=(245, 247, 250)):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=18,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(radius_ratio=1.0),
        color_mask=SolidFillColorMask(
            back_color=bg,
            front_color=fg,
        ),
    ).convert("RGB")
    img.save(path)
    print(f"  {path.name:18s} → {data}")
    return img


print("Generando QRs:")
for name, url in TARGETS.items():
    make_qr(url, OUT / f"{name}.png")

# Verifica un par
print("\nQRs guardados en:", OUT)
