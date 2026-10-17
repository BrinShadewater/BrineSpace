from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

ROOT = Path(__file__).resolve().parent
native = json.loads((ROOT/'native/output/native-result.json').read_text())
run = json.loads((ROOT/'native/output/run-verification.json').read_text())
samples = native['live_clock_samples']
assert native['checks'] == 202 and not native['errors']
assert len({s['slot'] for s in samples}) == 64
assert run['engine_exit'] == 0 and not run['owner_files_changed'] and not run['logged_errors']
html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kris Krüg — east walk review</title><style>body{background:#252c30;color:#dde6e9;font:18px system-ui;margin:0}main{max-width:1100px;margin:auto;padding:24px}p{color:#bdcbd0;line-height:1.5}video,img{width:100%;height:auto}details{margin:20px 0}</style><main><h1>Kris Krüg</h1><p>Cognitive Concordance Specialist · Intent Harmonisation</p><p>East walk candidate: neutral, start, two complete alternating gait cycles and a reversed cycle-boundary stop.</p><video src="locomotion-preview.mp4" controls loop playsinline preload="metadata"></video><p>Preserved source poses. Shape continuity, seam and weight remain under review. The displayed root stays fixed; station stride calibration and joins with the standing/tablet families remain pending.</p><img src="cycle-review.png" alt="Eighteen samples spanning the complete alternating gait"><details><summary>Native Godot review</summary><p>202 checks passed, 69 captures. All 64 cycle slots and two wraps observed using the production movement-driven player with synthetic distance. Owner save files unchanged.</p><img src="native/output/walk-east-032.png" alt="Native midpoint at four scales"><img src="native/output/walk-stop-east-016.png" alt="Native return to local neutral"></details></main></html>'''
(ROOT/'index.html').write_text(html, encoding='utf-8')
names = ['index.html','README.md','HANDOFF.md','locomotion-preview.mp4','cycle-review.png','manifest.json','source-contract.json','native/output/native-result.json','native/output/run-verification.json','native/output/walk-east-032.png','native/output/walk-stop-east-016.png']
with ZipFile(ROOT/'Kris-Krug-east-walk-preview.zip','w',ZIP_DEFLATED) as bundle:
    for name in names:
        bundle.write(ROOT/name, name)
    for path in sorted((ROOT/'frames').glob('*.png')):
        bundle.write(path, 'frames/'+path.name)
print('Packaged 91-file standalone walk review; native checks passed.')
