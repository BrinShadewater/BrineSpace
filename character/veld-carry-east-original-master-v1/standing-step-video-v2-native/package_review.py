from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;files=sorted((P/'full-clip-frames').glob('*.png'));frames=[Image.open(p).convert('RGBA') for p in files]
probe=json.loads((P/'raw-review/probe.json').read_text(encoding='utf-8'));stream=next(s for s in probe['streams'] if s['codec_type']=='video');num,den=map(int,stream['avg_frame_rate'].split('/'));fps=num/den
durations=[round((i+1)*1000/fps)-round(i*1000/fps) for i in range(len(frames))]
frames[0].save(P/'full-source-review.png',save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
replay=Image.open(P/'full-source-review.png');assert replay.n_frames==len(frames)
for i,im in enumerate(frames):
 replay.seek(i);assert np.array_equal(np.array(replay.convert('RGBA')),np.array(im));assert round(replay.info['duration'])==durations[i]
raw=json.loads((P/'raw-review/review.json').read_text(encoding='utf-8'));raw['visualReview']='All six chronological raw boards containing142frames inspected, then all six fixed-registration alpha boards and whole master/endpoint head/body comparison inspected. Final in-place/master consistency rejected:41.5nativepx horizontal axis excursion, darkening/material and body/case-angle drift. No ordinary/native acceptance.';(P/'raw-review/review.json').write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
report={'frames':len(frames),'fps':fps,'durationMs':sum(durations),'checks':len(frames)*2,'failures':0,'scope':'Exact full142source-frame replay at authored source FPS, finite once. Rejected candidate review media, not completed animation/native station recording or accepted motion. No pose insertion/colour/geometry normalization.'}
(P/'replay-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
