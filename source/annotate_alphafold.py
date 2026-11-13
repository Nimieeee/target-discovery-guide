#!/Users/mac/envs/dd/bin/python
"""annotate_alphafold.py: draw lemon numbered circles on the AlphaFold surface shot
("image copy 4.png" at the workspace root) at the dark-cavity clusters found by
thresholding, and write assets/shot_pocket.png (1728 px wide) for the guide.
Cluster centroids were found with lum < 40 connected components; the five kept are
on the main globular body. Re-run build_target_guide.py afterwards.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont
import matplotlib, os

SRC = pathlib.Path("/Users/mac/research and capacity building/image copy 4.png")
HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE / "assets"
LEMON, INK = "#FDE700", "#0A0A0A"

# (cx, cy, radius) in full-res pixels, from dark-cluster detection; norm coords x2102x1354
MARKS = [
    (970, 398, 120),   # 1: deepest cavity, active-site gorge entrance
    (869, 585, 100),   # 2: central hole
    (653, 719, 80),    # 3: lower-left flank hole
]

f_big = ImageFont.truetype(os.path.join(matplotlib.get_data_path(), "fonts/ttf/DejaVuSans-Bold.ttf"), 64)
f_cap = ImageFont.truetype(os.path.join(matplotlib.get_data_path(), "fonts/ttf/DejaVuSans-Bold.ttf"), 40)

im = Image.open(SRC).convert("RGB")
W, H = im.size
d = ImageDraw.Draw(im)
for i, (cx, cy, r) in enumerate(MARKS, start=1):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LEMON, width=14)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
    bx, by = cx + r - 10, cy - r - 10
    d.rectangle([bx - 8, by - 8, bx + 76, by + 76], fill=LEMON, outline=INK, width=5)
    d.text((bx + 6, by + 2), str(i), font=f_big, fill=INK)
# caption strip
strip = 150
d.rectangle([0, H - strip, W, H], fill=INK)
d.text((40, H - strip + 28), "AlphaFold model of ACHE, surface view. Circles: candidate pockets visible on the surface;", font=f_cap, fill="white")
d.text((40, H - strip + 82), "#1 is the active-site gorge entrance. Confirm with a pocket detector or a bound ligand.", font=f_cap, fill=LEMON)

im.save(ASSETS / "annotated_alphafold_full.png")
w = 1728
im.resize((w, int(H * w / W)), Image.LANCZOS).save(ASSETS / "shot_pocket.png", optimize=True)
print("wrote", ASSETS / "shot_pocket.png", (w, int(H * w / W)))
