from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
review=json.loads((p/'dense-start-v7-review.json').read_bytes());durations=review['sliceDurationsMs'];preview_durations=durations.copy();preview_durations[-1]+=600
sources=[p/('walk12-case-master-v5-seam.png' if i==12 else f'walk{i:02d}-case-master-v5.png' if i in (0,8) else 'walk03-contact-v7.png' if i==3 else f'walk{i:02d}-dense-carry-v6.png') for i in range(13)]
frames=[Image.open(f).convert('RGBA') for f in sources];out=p/'dense-start-v7-preview.apng'
frames[0].save(out,format='PNG',save_all=True,append_images=frames[1:],duration=preview_durations,loop=0,disposal=0,blend=0)
decoded=Image.open(out);assert decoded.n_frames==13
for i,frame in enumerate(frames):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==frame.tobytes();assert decoded.info['duration']==preview_durations[i]
(p/'dense-start-v7-preview.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},'previewSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'sourceDurationsMs':durations,'sourceSliceMs':sum(durations),'viewerDurationsMs':preview_durations,'viewerTerminalHoldMs':600,'viewerTotalMs':sum(preview_durations),'decodedFramesExact':13,'scope':'Finite13pose initial slice, 430ms; preview repeats with600ms terminal review hold. Not full gait, no runtime manifest or cadence/owner acceptance.'},indent=2)+'\n',encoding='utf-8')
print('13APNG decoded source frames/timings exact;430ms slice+600ms viewer terminal hold.')
