#!/Users/mac/envs/dd/bin/python
"""prep_screenshots.py: copy the real screenshots from "guide pictures/" into assets/,
downscaled to the slot widths. Re-run build_target_guide.py afterwards.

Mapping (verified by OCR against the source files):
  8.32.37  Open Targets, Alzheimer's, "1-25 of 13006"          -> shot_ot_count.png
  8.34.10  Applied filters: Approved Drug, "1-25 of 732"       -> shot_ot_filter.png
  8.35.36  SwissTargetPrediction, Huperzine A SMILES pasted    -> shot_swiss_structure.png
  8.36.03  STP results, Acetylcholinesterase ACHE top row      -> shot_swiss_result.png
  8.37.04  STRING network, 2 nodes 1 edge, APP-ACHE           -> shot_network.png
  (8.33.43 and 8.33.59 are the filter-menu stages, kept as alternates)
  shot_pocket.png stays a placeholder until an AlphaFold/PDB 3D pocket shot arrives.
"""
import glob, pathlib, shutil
from PIL import Image

SRC = pathlib.Path("/Users/mac/research and capacity building/guide pictures")
ASSETS = pathlib.Path(__file__).resolve().parent / "assets"

MAP = {
    "8.32.37": ("shot_ot_count.png", 1728),
    "8.34.10": ("shot_ot_filter.png", 1728),
    "8.35.36": ("shot_swiss_structure.png", 1200),
    "8.36.03": ("shot_swiss_result.png", 1200),
    "8.37.04": ("shot_network.png", 1728),
}

for f in sorted(SRC.glob("Screenshot*.png")):
    for stamp, (name, width) in MAP.items():
        if stamp in f.name:
            im = Image.open(f).convert("RGB")
            w, h = im.size
            im.resize((width, int(h * width / w)), Image.LANCZOS).save(ASSETS / name, optimize=True)
            print(f.name, "->", name, (width, int(h * width / w)))
