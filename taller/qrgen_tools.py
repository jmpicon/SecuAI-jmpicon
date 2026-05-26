"""
QRs adicionales para el workshop de herramientas.
Enlaces a docs oficiales + recursos del repo.
"""
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from pathlib import Path

OUT = Path("/home/jmpicon/Documentos/secu_IA/taller/qrs")
OUT.mkdir(exist_ok=True)

REPO = "https://github.com/jmpicon/SecuAI-jmpicon"

TARGETS = {
    # Ataque
    "tool_garak":     "https://github.com/NVIDIA/garak",
    "tool_pyrit":     "https://github.com/Azure/PyRIT",
    "tool_promptfoo": "https://www.promptfoo.dev",
    "tool_textattack": "https://github.com/QData/TextAttack",
    "tool_art":       "https://github.com/Trusted-AI/adversarial-robustness-toolbox",
    "tool_counterfit": "https://github.com/Azure/counterfit",
    "tool_harmbench": "https://www.harmbench.org",
    # Defensa
    "tool_llmguard":  "https://llm-guard.com",
    "tool_nemo":      "https://github.com/NVIDIA/NeMo-Guardrails",
    "tool_llamaguard": "https://huggingface.co/meta-llama/Llama-Guard-3-8B",
    "tool_rebuff":    "https://github.com/protectai/rebuff",
    "tool_vigil":     "https://github.com/deadbits/vigil-llm",
    "tool_presidio":  "https://github.com/microsoft/presidio",
    "tool_guardrails": "https://github.com/guardrails-ai/guardrails",
    "tool_promptshields": "https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection",
    "tool_lakera":    "https://www.lakera.ai/lakera-guard",
    # Modelo / supply chain
    "tool_modelscan": "https://github.com/protectai/modelscan",
    "tool_safetensors": "https://github.com/huggingface/safetensors",
    "tool_picklescan": "https://github.com/mmaitre314/picklescan",
    # Frameworks / referencia
    "ref_owasp_llm":  "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
    "ref_atlas":      "https://atlas.mitre.org",
    "ref_nist_rmf":   "https://www.nist.gov/itl/ai-risk-management-framework",
    # Workshop específicos
    "ws_lab_garak":   f"{REPO}/tree/main/labs/garak",
    "ws_lab_llmguard": f"{REPO}/tree/main/labs/llm-guard",
    "ws_lab_pickle":  f"{REPO}/tree/main/labs/pickle-rce",
    "ws_lab_extract": f"{REPO}/tree/main/labs/model-extraction",
    "ws_pptx_tools":  f"{REPO}/blob/main/taller/SecuAI_Tools_Workshop.pptx",
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
        color_mask=SolidFillColorMask(back_color=bg, front_color=fg),
    ).convert("RGB")
    img.save(path)


print("Generando QRs de herramientas:")
for name, url in TARGETS.items():
    make_qr(url, OUT / f"{name}.png")
    print(f"  {name:24s} → {url}")
print(f"\nTotal: {len(TARGETS)} QRs guardados en {OUT}")
