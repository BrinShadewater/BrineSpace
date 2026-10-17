from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parent;OLD=P.with_name('bill-water-exit-south-v3')
report={}
for gear in ['bare','helmet']:
 files=[P/f'{gear}/frames/swim-land-south/{i:03}.png' for i in range(8)]
 frames=[Image.open(f).convert('RGBA') for f in files]
 unchanged=[i for i,im in enumerate(frames) if im.tobytes()==Image.open(OLD/f'{gear}/frames/swim-land-south/{i:03}.png').convert('RGBA').tobytes()]
 assert unchanged==[0,1,2,3,4,6,7],unchanged
 manifest=json.loads((P/gear/'manifest.json').read_text())
 durations=manifest['states'][0]['frameDurationsMs'];assert sum(durations)==500
 with Image.open(P/gear/'source-exit.png') as ap:
  assert ap.n_frames==8 and ap.info['loop']==1
  for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==durations[i]
 report[gear]=dict(unchangedFrames=unchanged,decodedFrames=8,holdsExact=True,finiteLoop=1)
(P/'revision-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
