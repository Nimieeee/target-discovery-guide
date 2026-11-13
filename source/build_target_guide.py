#!/Users/mac/envs/dd/bin/python
"""build_target_guide.py: the "Target Discovery" guide as a 9:16 PDF (1080 x 1920 px pages),
in the same design language as guide/ai_drug_guide.html (cream grid paper, black Impact
titles, lemon highlighter, yellow tab, black boxes, framed screenshot cards).

Writes guide_target/target_guide.html, guide_target/TARGET_GUIDE.pdf and
guide_target/pages_png/page_NN.png. assets/shot_*.png are placeholders until real
screenshots are dropped in, then the script is re-run.
"""
import os, re, shutil, subprocess, pathlib
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE / "assets"
W, H, PAD = 1080, 1920, 84
PAPER, INK, LEMON, BODY, MUTE = "#F1EFE9", "#0A0A0A", "#FDE700", "#1D1D1D", "#6E6B64"

CSS = """
@page { size: 1080px 1920px; margin: 0; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: #444; }
.page { position: relative; width: 1080px; height: 1920px; overflow: hidden; color: #0A0A0A; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; page-break-after: always; break-after: page;
  background-color: #F1EFE9; background-image: linear-gradient(rgba(0,0,0,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(0,0,0,.06) 1px, transparent 1px);
  background-size: 36px 36px; background-position: -10px -10px; padding: 168px 84px 112px; display: flex; flex-direction: column; }
.page:last-child { page-break-after: auto; break-after: auto; }
.tab { position: absolute; left: 0; top: 0; background: #FDE700; color: #0A0A0A; font-size: 26px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase;
  padding: 34px 58px 24px 66px; border-radius: 0 0 56px 0; max-width: 860px; line-height: 1.2; }
.foot { position: absolute; left: 84px; right: 84px; bottom: 36px; display: flex; justify-content: space-between; align-items: center; font-size: 21px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: #6E6B64; }
.foot i { display: inline-block; width: 22px; height: 22px; background: #FDE700; border: 3px solid #0A0A0A; margin-right: 14px; vertical-align: -4px; }
h1, h2, h3 { font-family: Impact, "Haettenschweiler", "Arial Narrow", sans-serif; font-weight: 400; text-transform: uppercase; margin: 0; letter-spacing: -.005em; }
h2.big { font-size: 118px; line-height: 1.05; }
h2.mid { font-size: 84px; line-height: 1.06; }
em { font-style: normal; background: linear-gradient(transparent 9%, #FDE700 9%, #FDE700 91%, transparent 91%); padding: 0 .12em; -webkit-box-decoration-break: clone; box-decoration-break: clone; }
p { font-size: 34px; line-height: 1.38; font-weight: 500; color: #1D1D1D; margin: 0 0 22px; }
b { font-weight: 800; color: #0A0A0A; }
code { font-family: Menlo, "SF Mono", Monaco, monospace; font-size: .78em; background: rgba(0,0,0,.08); padding: 1px 6px; border-radius: 4px; overflow-wrap: anywhere; }
a, .lnk { color: #0A0A0A; background: rgba(253,231,0,.55); text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 4px; padding: 0 3px; }
.lead { font-size: 40px; line-height: 1.32; }
.box { background: #000; color: #fff; padding: 36px 44px; margin: 10px 0 22px; }
.box .k { font-size: 22px; font-weight: 800; letter-spacing: .24em; text-transform: uppercase; color: #FDE700; margin-bottom: 14px; }
.box p { color: #fff; font-size: 31px; margin: 0; line-height: 1.34; }
.box b { color: #FDE700; }
ol.big { list-style: none; counter-reset: s; padding: 0; margin: 10px 0 8px; }
ol.big li { counter-increment: s; position: relative; padding-left: 92px; margin-bottom: 24px; font-size: 33px; line-height: 1.34; font-weight: 500; min-height: 66px; }
ol.big li::before { content: counter(s); position: absolute; left: 0; top: -4px; width: 66px; height: 66px; background: #FDE700; border: 4px solid #0A0A0A; font-family: Impact, "Haettenschweiler", "Arial Narrow", sans-serif; font-size: 40px; text-align: center; line-height: 58px; }
.hero { display: grid; grid-template-columns: 470px 1fr; gap: 40px; align-items: start; margin-top: 30px; }
.card { width: 470px; height: 588px; background-size: cover; background-position: center; border: 6px solid #0A0A0A; }
.side .sub { font-family: Impact, "Haettenschweiler", "Arial Narrow", sans-serif; font-size: 58px; line-height: 1.02; text-transform: uppercase; margin: 0 0 18px; }
.side p { font-size: 31px; line-height: 1.36; margin: 0 0 14px; }
.pl { margin-top: 34px; display: grid; gap: 12px; }
.pl div { display: flex; align-items: center; gap: 18px; border: 4px solid #0A0A0A; background: #fff; padding: 10px 18px; font-size: 30px; font-weight: 700; line-height: 1.15; }
.pl b { font-family: Impact, "Haettenschweiler", "Arial Narrow", sans-serif; font-weight: 400; font-size: 38px; background: #FDE700; border: 3px solid #0A0A0A; min-width: 62px; text-align: center; padding: 0 6px; }
.find { display: grid; grid-template-columns: 54px 1fr; gap: 0 18px; margin-bottom: 16px; }
.find .n { font-family: Impact, "Haettenschweiler", "Arial Narrow", sans-serif; font-size: 40px; background: #FDE700; border: 3px solid #0A0A0A; text-align: center; height: 54px; line-height: 48px; }
.find b { font-size: 29px; display: block; line-height: 1.22; }
.find span { font-size: 27px; line-height: 1.3; color: #1D1D1D; font-weight: 500; }
.shot { margin: 14px 0 20px; border: 6px solid #0A0A0A; background: #fff; }
.shot img { display: block; width: 100%; }
.shot figcaption { background: #0A0A0A; color: #fff; font-size: 24px; font-weight: 600; padding: 10px 16px; line-height: 1.25; }
.shot figcaption b { color: #FDE700; }
.shots2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 14px 0 20px; }
.shots2 .shot { margin: 0; }
.cred { margin-bottom: 20px; display: grid; grid-template-columns: 130px 1fr; gap: 0 20px; align-items: center; }
.cred .lg { height: 96px; display: flex; align-items: center; justify-content: center; }
.cred .lg img { max-height: 96px; max-width: 130px; object-fit: contain; }
.cred b { display: inline-block; background: #FDE700; padding: 0 10px; font-size: 30px; margin-bottom: 4px; }
.cred div { font-size: 28px; line-height: 1.34; font-weight: 500; color: #1D1D1D; }
.note { font-size: 24px; color: #6E6B64; font-weight: 600; margin-top: 6px; }
"""

SHOTS = {
    "shot_ot_count.png":    ("1728x940", "SCREENSHOT 1", "Open Targets: Alzheimer's disease searched, 13,006 count visible, APP at rank 1"),
    "shot_ot_filter.png":   ("1728x940", "SCREENSHOT 2", "Filter panel (approved drug, small molecule) and the 732-gene list with ACHE"),
    "shot_swiss_structure.png": ("840x1000", "SCREENSHOT 3", "SwissTargetPrediction: Huperzine A structure entered"),
    "shot_swiss_result.png":    ("840x1000", "SCREENSHOT 4", "SwissTargetPrediction results: ACHE top hit with probability"),
    "shot_network.png":    ("1728x940", "SCREENSHOT 5", "Network graph: ACHE node connected to APP node"),
    "shot_pocket.png":     ("1728x940", "SCREENSHOT 6", "3D ACHE structure with the binding pocket circled"),
}


def dejavu(bold=True):
    import matplotlib
    p = os.path.join(matplotlib.get_data_path(), "fonts", "ttf",
                     "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(p, 44)


def make_placeholders():
    ASSETS.mkdir(exist_ok=True)
    src_cover = HERE.parent / "guide" / "pages_assets" / "photo_cover.jpg"
    if src_cover.exists():
        shutil.copy(src_cover, ASSETS / "cover.jpg")
    f_big, f_small = dejavu(True), dejavu(False)
    for name, (size, label, desc) in SHOTS.items():
        w, h = (int(x) for x in size.split("x"))
        im = Image.new("RGB", (w, h), PAPER)
        d = ImageDraw.Draw(im)
        for x in range(0, w, 36):
            d.line([(x, 0), (x, h)], fill=(222, 219, 210), width=1)
        for y in range(0, h, 36):
            d.line([(0, y), (w, y)], fill=(222, 219, 210), width=1)
        d.rectangle([10, 10, w - 11, h - 11], outline=INK, width=8)
        d.rectangle([10, 10, w // 2, 74], fill=LEMON, outline=INK, width=4)
        d.text((30, 22), label, font=f_big, fill=INK)
        # wrap desc
        words, lines, cur = desc.split(), [], ""
        for wd in words:
            if d.textlength(cur + " " + wd, font=f_small) > w - 120:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines.append(cur)
        y = h // 2 - len(lines) * 34
        for ln in lines:
            d.text(((w - d.textlength(ln, font=f_small)) / 2, y), ln, font=f_small, fill=BODY)
            y += 68
        d.text(((w - d.textlength("replace this file in assets/", font=f_small)) / 2, h - 80),
               "replace this file in assets/", font=f_small, fill=MUTE)
        if not (ASSETS / name).exists():   # never overwrite a real screenshot
            im.save(ASSETS / name)


def page(inner, tab, foot_left, foot_right, n):
    return (f'<section class="page" data-n="{n}"><div class="tab">{tab}</div>{inner}'
            f'<div class="foot"><span><i></i>{foot_left}</span><span>{foot_right}</span></div></section>')


def shot(img, cap):
    return f'<figure class="shot"><img src="assets/{img}" alt=""><figcaption>{cap}</figcaption></figure>'


def build_pages():
    P = []
    # 1 cover
    P.append(page(
        f'<h2 class="big">From 13,000 genes to <em>1 target</em></h2>'
        f'<div class="hero"><div class="card" style="background-image:url(assets/cover.jpg)"></div>'
        f'<div class="side"><div class="sub">The target discovery workflow</div>'
        f'<p class="lead" style="font-size:34px">How to use Open Targets, SwissTargetPrediction and AlphaFold to find a druggable target for Alzheimer\'s.</p>'
        f'<p>Five steps, all free, all on a laptop. The example: finding a small-molecule target for Alzheimer\'s disease.</p></div></div>'
        f'<div class="pl">'
        f'<div><b>1</b><span>Pull disease genes from Open Targets</span></div>'
        f'<div><b>2</b><span>Filter for targets with an approved small molecule pill</span></div>'
        f'<div><b>3</b><span>Test a natural compound with SwissTargetPrediction</span></div>'
        f'<div><b>4</b><span>Check the pathway network</span></div>'
        f'<div><b>5</b><span>Confirm the 3D binding pocket with AlphaFold</span></div></div>',
        "Free guide", "By Tolu (@toluwanimiso)", "AiSynth Labs", 1))
    # 2 intro
    P.append(page(
        f'<h2 class="mid">Start with the <em>target</em></h2>'
        f'<p class="lead" style="margin-top:36px"><b>The goal:</b> you want to discover a new drug for Alzheimer\'s disease. The first step is finding a biological target.</p>'
        f'<p>Ask a database for every gene linked to Alzheimer\'s and it hands back over <b>13,000 results</b>. The real challenge is filtering that list down to a single protein you can actually drug with a small molecule pill.</p>'
        f'<ol class="big">'
        f'<li>Pull the disease genes from <b>Open Targets</b>.</li>'
        f'<li>Filter for targets that already have an <b>approved small molecule drug</b>.</li>'
        f'<li>Test a natural compound, <b>Huperzine A</b>, with <b>SwissTargetPrediction</b>.</li>'
        f'<li>Check the <b>pathway network</b>.</li>'
        f'<li>Confirm the physical <b>3D binding pocket</b> with AlphaFold.</li></ol>'
        f'<p class="note">Counts in this guide are from my pull on the day I ran it. Open Targets updates, so your count may differ slightly.</p>',
        "Read this first", "@toluwanimiso", "Target guide", 2))
    # 3 step 1
    P.append(page(
        f'<h2 class="mid">Pull the <em>disease genes</em></h2>'
        f'<div style="margin-top:30px">'
        f'<div class="find"><div class="n">T</div><div><b>THE TOOL: Open Targets Platform</b><span>platform.opentargets.org, free, no account needed for browsing.</span></div></div>'
        f'<div class="find"><div class="n">A</div><div><b>THE ACTION</b><span>Search "Alzheimer\'s disease" and open the associated targets list.</span></div></div>'
        f'<div class="find"><div class="n">R</div><div><b>THE RESULT</b><span><b>13,006 genes</b>, ranked by evidence strength. The top-ranked gene is <b>APP</b> (amyloid precursor protein).</span></div></div></div>'
        + shot("shot_ot_count.png", "<b>Open Targets</b>: Alzheimer's disease searched, 13,006 genes counted, APP at rank 1")
        + f'<div class="box"><div class="k">The science: why APP is #1, and why it is not a pill target</div>'
        f'<p>APP ranks first on research volume: it produces the amyloid that forms plaques. But APP is a massive, flexible protein with <b>no clear pocket</b> for a small molecule, and shutting it off completely is not safe. The drugs that go after its amyloid, such as <b>lecanemab</b>, are large antibodies given by <b>IV infusion</b> that cross the blood-brain barrier poorly. For a pill, APP is not the best target.</p></div>',
        "Step 1: Open Targets", "@toluwanimiso", "Target guide", 3))
    # 4 step 2
    P.append(page(
        f'<h2 class="mid">Demand that a <em>pill exists</em></h2>'
        f'<div style="margin-top:30px">'
        f'<div class="find"><div class="n">T</div><div><b>THE TOOL: Open Targets advanced filters</b><span>Same platform, filter panel on the targets list.</span></div></div>'
        f'<div class="find"><div class="n">A</div><div><b>THE ACTION</b><span>Select tractability <b>"small molecule"</b> and <b>"approved drug"</b>. If you want a pill, only keep targets a pill already exists for.</span></div></div>'
        f'<div class="find"><div class="n">R</div><div><b>THE RESULT</b><span>The list drops from <b>13,006 to 732</b>. APP disappears. <b>ACHE</b> (acetylcholinesterase) survives, because the approved pill <b>donepezil</b> targets it.</span></div></div></div>'
        + shot("shot_ot_filter.png", "<b>The filter selected</b>, and the new list: 732 genes, ACHE among them")
        + f'<div class="box"><div class="k">The science: choose the target by the drug you want to build</div>'
        f'<p>This filter proves APP has <b>no approved small molecule drug</b>, and that ACHE is <b>druggable in practice</b>: a pill already exists for it. Filter before you fall in love with a target.</p></div>',
        "Step 2: The filter", "@toluwanimiso", "Target guide", 4))
    # 5 step 3
    P.append(page(
        f'<h2 class="mid">Test a <em>compound</em></h2>'
        f'<div style="margin-top:26px">'
        f'<div class="find"><div class="n">T</div><div><b>THE TOOL: SwissTargetPrediction</b><span>swisstargetprediction.ch, free.</span></div></div>'
        f'<div class="find"><div class="n">A</div><div><b>THE ACTION</b><span>Take <b>Huperzine A</b>, a natural compound from Chinese club moss (<i>Huperzia serrata</i>), traditionally used for memory. Paste its SMILES or draw the structure.</span></div></div>'
        f'<div class="find"><div class="n">R</div><div><b>THE RESULT</b><span>The tool predicts Huperzine A binds strongly to <b>ACHE</b>, with a probability score.</span></div></div></div>'
        f'<div class="shots2">'
        + shot("shot_swiss_structure.png", "<b>Huperzine A</b> in the predictor")
        + shot("shot_swiss_result.png", "<b>ACHE</b> as a top predicted target")
        + f'</div>'
        f'<div class="box"><div class="k">The science: rationale plus a hit</div>'
        f'<p>You now have both halves: a <b>reason to pick the compound</b> (traditional use for memory) and a <b>tool confirming it hits a protein</b> (ACHE) that sits on your filtered list of pill-druggable targets.</p></div>',
        "Step 3: SwissTargetPrediction", "@toluwanimiso", "Target guide", 5))
    # 6 step 4
    P.append(page(
        f'<h2 class="mid">Check the <em>network</em></h2>'
        f'<div style="margin-top:30px">'
        f'<div class="find"><div class="n">T</div><div><b>THE TOOL: STRING DB</b><span>string-db.org, free.</span></div></div>'
        f'<div class="find"><div class="n">A</div><div><b>THE ACTION</b><span>Build a network of ACHE and APP and see whether they connect.</span></div></div>'
        f'<div class="find"><div class="n">R</div><div><b>THE RESULT</b><span>ACHE connects to APP. They share a biological pathway.</span></div></div></div>'
        + shot("shot_network.png", "<b>The network</b>: the ACHE node connected to the APP node")
        + f'<div class="box"><div class="k">The science: a hypothesis, not a proof</div>'
        f'<p>This connection means hitting ACHE <b>may indirectly affect the amyloid pathway driven by APP</b>, without drugging APP directly. Treat it as a biological hypothesis to test in the lab, not as evidence the compound works.</p></div>',
        "Step 4: The pathway", "@toluwanimiso", "Target guide", 6))
    # 7 step 5
    P.append(page(
        f'<h2 class="mid">Find the physical <em>pocket</em></h2>'
        f'<div style="margin-top:30px">'
        f'<div class="find"><div class="n">T</div><div><b>THE TOOL: AlphaFold Database or PDB</b><span>alphafold.ebi.ac.uk or rcsb.org, free.</span></div></div>'
        f'<div class="find"><div class="n">A</div><div><b>THE ACTION</b><span>Pull the 3D structure of ACHE and look for a binding pocket.</span></div></div>'
        f'<div class="find"><div class="n">R</div><div><b>THE RESULT</b><span>ACHE has a clear, physical pocket that a small molecule like Huperzine A can fit into.</span></div></div></div>'
        + shot("shot_pocket.png", "<b>AlphaFold model of ACHE</b>, surface view: candidate pockets circled, #1 is the active-site gorge")
        + f'<div class="box"><div class="k">The science: a network edge is not a binding site</div>'
        f'<p>A pathway connection only says the proteins are related. The <b>3D pocket</b> is the physical check that a drug can actually fit and bind. Both checks together make ACHE a rational target.</p></div>',
        "Step 5: AlphaFold", "@toluwanimiso", "Target guide", 7))
    # 8 conclusion
    P.append(page(
        f'<h2 class="mid">The target: <em>ACHE</em></h2>'
        f'<p class="lead" style="margin-top:34px">Your final target is <b>acetylcholinesterase (ACHE)</b>. Why:</p>'
        f'<div class="pl">'
        f'<div><b>1</b><span>It is on the filtered list: an <b>approved small molecule</b> target</span></div>'
        f'<div><b>2</b><span>Your compound, <b>Huperzine A</b>, is predicted to hit it</span></div>'
        f'<div><b>3</b><span>It connects to the main Alzheimer\'s pathway, <b>APP</b></span></div>'
        f'<div><b>4</b><span>It has a physical <b>3D pocket</b> the drug can bind</span></div></div>'
        f'<div class="box" style="margin-top:34px"><div class="k">The limit, said plainly</div>'
        f'<p>This workflow gives you a <b>shortlist</b>. It does not prove Huperzine A treats Alzheimer\'s. What it does prove: ACHE is a rational, evidence-backed target for a small molecule. The next step is turning the molecule into computer code (SMILES) so it can be tested further.</p></div>',
        "Conclusion", "@toluwanimiso", "Target guide", 8))
    # 9 resources
    P.append(page(
        f'<h2 class="mid">Tools and <em>next steps</em></h2>'
        f'<div style="margin-top:30px">'
        f'<div class="cred"><div class="lg"><img src="assets/logos/ot_logo.svg" alt="Open Targets"></div><div><b>Open Targets Platform</b><div><a href="https://platform.opentargets.org">platform.opentargets.org</a></div></div></div>'
        f'<div class="cred"><div class="lg"><img src="assets/logos/stp_icon.png" alt="SwissTargetPrediction"></div><div><b>SwissTargetPrediction</b><div><a href="https://www.swisstargetprediction.ch">swisstargetprediction.ch</a></div></div></div>'
        f'<div class="cred"><div class="lg"><img src="assets/logos/string_logo.svg" alt="STRING"></div><div><b>STRING DB</b><div><a href="https://string-db.org">string-db.org</a></div></div></div>'
        f'<div class="cred"><div class="lg"><img src="assets/logos/deepmind_logo.webp" alt="AlphaFold"></div><div><b>AlphaFold Database</b><div><a href="https://alphafold.ebi.ac.uk">alphafold.ebi.ac.uk</a></div></div></div></div>'
        f'<div class="box"><div class="k">Next video</div>'
        f'<p><b>How a computer sees a molecule</b> (SMILES and fingerprints). Comment <b>TARGET</b> on the reel and I will send you the exact links and filters I used.</p></div>'
        f'<p style="font-size:32px"><b>Follow:</b> Instagram <b>@toluwanimiso</b><br>'
        f'<a href="https://www.linkedin.com/in/toluwanimi-odunewu-57a550328/">LinkedIn: Toluwanimi Odunewu</a><br>'
        f'<a href="https://x.com/lastbulletin6">X: @lastbulletin6</a><br>'
        f'<b>Email me directly:</b> <a href="mailto:odunewutolu2@gmail.com">odunewutolu2@gmail.com</a></p>',
        "Resources", "@toluwanimiso", "Target guide", 9))
    return P


CHECK_JS = """<script>
window.addEventListener('load',function(){
 if(location.hash!=='#check')return;var out=[];
 document.querySelectorAll('.page').forEach(function(pg){
  var lim=pg.clientHeight-110,last=0;
  pg.querySelectorAll(':scope > *:not(.foot):not(.tab)').forEach(function(e){last=Math.max(last,e.getBoundingClientRect().bottom-pg.getBoundingClientRect().top)});
  if(last>lim)out.push(pg.dataset.n+': bottom '+Math.round(last)+'>'+lim)});
 var d=document.createElement('pre');d.id='ovf';d.textContent='OVERFLOW['+out.join(' | ')+']';document.body.appendChild(d)});
</script>"""


def main():
    make_placeholders()
    pages = build_pages()
    body = "\n".join(pages)
    out = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1080">'
           '<title>The target discovery workflow: from 13,000 genes to 1 target</title>'
           f'<style>{CSS}</style></head><body>{body}{CHECK_JS}</body></html>')
    assert "\u2014" not in out, "em dash found"
    (HERE / "target_guide.html").write_text(out)
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    url = "file://" + str(HERE / "target_guide.html")
    dom = subprocess.run([chrome, "--headless", "--disable-gpu", "--virtual-time-budget=4000",
                          "--window-size=1080,1920", "--dump-dom", url + "#check"],
                         capture_output=True, text=True).stdout
    m = re.search(r'id="ovf">(OVERFLOW\[.*?\])</pre>', dom, re.S)
    print("overflow check:", m.group(1) if m else "NO RESULT")
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={HERE / 'TARGET_GUIDE.pdf'}", url], capture_output=True)
    info = subprocess.run(["pdfinfo", str(HERE / "TARGET_GUIDE.pdf")], capture_output=True, text=True).stdout
    print("pages in PDF:", re.search(r"Pages:\s+(\d+)", info).group(1), "(built", len(pages), ")",
          "| size:", re.search(r"Page size:\s+(.*)", info).group(1).strip())
    png = HERE / "pages_png"; png.mkdir(exist_ok=True)
    for f in png.glob("page*.png"):
        f.unlink()
    subprocess.run(["pdftoppm", "-r", "40", "-png", str(HERE / "TARGET_GUIDE.pdf"), str(png / "page")], check=True)


if __name__ == "__main__":
    main()
