# Target Discovery Guide

Free 9-page PDF guide (9:16, Instagram carousel format): **The Target Discovery Workflow, from
13,006 genes to 1 druggable target**, for Alzheimer's disease.

Direct link to the PDF:

```
https://raw.githubusercontent.com/Nimieeee/target-discovery-guide/main/TARGET_GUIDE.pdf
```

## What it covers

1. Pull disease genes from Open Targets (13,006 associated genes; APP ranks first).
2. Filter for targets with an approved small molecule drug (13,006 to 732; ACHE survives, donepezil).
3. Test a natural compound, Huperzine A, with SwissTargetPrediction (predicted ACHE hit).
4. Check the pathway network in STRING DB (ACHE connected to APP).
5. Confirm the physical binding pocket on the AlphaFold model of ACHE.

The guide states the limit plainly: this produces a shortlist and a rational target, not a
proof that the compound works.

Companion to the Instagram reel by @toluwanimiso (comment TARGET on the reel for this link).

## Files

- `TARGET_GUIDE.pdf` is the guide. View it or download it directly.
- `source/` is the HTML source, the screenshot assets and the build scripts, so every page
  can be regenerated or edited. Rebuild with:

```
/Users/mac/envs/dd/bin/python source/build_target_guide.py
```

(run from the `source/` folder; it writes `target_guide.html`, `TARGET_GUIDE.pdf` and
`pages_png/` there).

## Contact

- Instagram: @toluwanimiso
- LinkedIn: https://www.linkedin.com/in/toluwanimi-odunewu-57a550328/
- X: https://x.com/lastbulletin6
- Email: odunewutolu2@gmail.com

By Toluwanimi Odunewu.
