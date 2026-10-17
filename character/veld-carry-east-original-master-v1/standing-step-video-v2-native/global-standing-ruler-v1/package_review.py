from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[3]
files=sorted((P/'frames').glob('*.png'));assert len(files)==142
frames=[Image.open(p).convert('RGBA') for p in files];durations=[round((i+1)*1000/24)-round(i*1000/24) for i in range(142)]
frames[0].save(P/'full-source-review.png',save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
replay=Image.open(P/'full-source-review.png');assert replay.n_frames==142
for i,im in enumerate(frames):
 replay.seek(i);assert replay.convert('RGBA').tobytes()==im.tobytes();assert round(replay.info['duration'])==durations[i]
before=json.loads((R/'output/veld-east-native-stride-probe-v1/inputs-after.json').read_text(encoding='utf-8'));assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==sha for p,sha in before.items())
report={'checks':284,'failures':0,'frames':142,'durationMs':sum(durations),'previousNativeInputsStillStable':len(before),'scope':'Exact complete globally registered alternate source replay. One new shared source ruler, no per-pose adjustments. No native/runtime/contact/artwork acceptance; pale contours and head/body proportions remain.'}
(P/'replay-record.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
