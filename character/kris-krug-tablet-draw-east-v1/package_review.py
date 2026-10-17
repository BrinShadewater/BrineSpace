from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json

ROOT=Path(__file__).resolve().parent
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kris Krüg — alignment tablet</title><style>body{background:#252c30;color:#dde6e9;font:18px system-ui;margin:0}main{max-width:1100px;margin:auto;padding:24px}p{color:#bdcbd0;line-height:1.5}video,img{width:100%;height:auto}details{margin:20px 0}h1{margin-bottom:6px}</style><main><h1>Kris Krüg</h1><p>Cognitive Concordance Specialist · Intent Harmonisation</p><p>Staged east-facing alignment tablet action: draw, raise, consult and return. Eight authored whole poses, with an explicitly reversed return. The staged neutral pose is shared at both ends.</p><video src="action-preview.mp4" controls loop playsinline preload="metadata"></video><p>The coarse source sequence needs further timing, holster-hand and body continuity review. This is a standalone art candidate, with no normal roster or gameplay changes.</p><img src="source-review.png" alt="Eight complete chronological source poses at native and enlarged scale"><details><summary>Native Godot playback checks</summary><p>39 checks, zero failures; all 17 finite action slots captured. Actual player and renderer only, no main-scene navigation or station integration.</p><img src="native/output/slot-07.png" alt="Native consultation at four standing scales"><img src="native/output/slot-16.png" alt="Native shared neutral return"></details></main></html>'''
(ROOT/'index.html').write_text(html,encoding='utf-8')
native=json.loads((ROOT/'native/output/native-result.json').read_text());run=json.loads((ROOT/'native/output/run-verification.json').read_text())
assert not native['errors'] and len(native['native_slots'])==17 and run['engine_exit']==0 and not run['owner_files_changed'] and not run['logged_errors']
with ZipFile(ROOT/'Kris-Krug-alignment-tablet-preview.zip','w',ZIP_DEFLATED) as bundle:
    for name in ['index.html','README.md','action-preview.mp4','source-review.png','manifest.json','source-contract.json','native/output/native-result.json','native/output/run-verification.json','native/output/slot-07.png','native/output/slot-16.png']:
        bundle.write(ROOT/name,name)
    for path in sorted((ROOT/'frames').glob('*.png')):bundle.write(path,'frames/'+path.name)
print('Standalone 18-file action review ZIP; 39 native checks/17 captures/owner files unchanged verified.')
