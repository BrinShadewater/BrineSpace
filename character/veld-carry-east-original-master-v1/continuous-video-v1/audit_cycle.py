"""Read-only recurrence diagnostic; no artwork edits or loop admission."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
frames = [np.array(Image.open(f).convert('RGBA')) for f in sorted((P/'full-clip-frames').glob('*.png'))]
scores = []
for lag in range(10, 37):
    differences = []
    for n in range(28, 96):
        a, b = frames[n][160:228, 75:180], frames[n+lag][160:228, 75:180]
        union = (a[:,:,3]>128) | (b[:,:,3]>128)
        differences.append(float(np.abs(a.astype(float)-b.astype(float))[union].mean()))
    scores.append({'lagFrames':lag,'meanLowerBodyRGBAError':float(np.mean(differences))})
scores.sort(key=lambda r:r['meanLowerBodyRGBAError'])
board = Image.new('RGB',(1800,1080),'#202a30')
draw = ImageDraw.Draw(board)
for j,n in enumerate(range(28,68,2)):
    im = Image.fromarray(frames[n]).crop((75,155,180,230)).resize((315,225),Image.Resampling.NEAREST)
    xy = ((j%5)*360,(j//5)*265+25)
    board.paste(im,xy,im)
    draw.text((xy[0]+4,xy[1]-20),f'frame {n}',fill='white')
board.save(P/'near-far-cycle-review.png')
report = {'method':'Fixed-coordinate lower-body RGBA recurrence, frames28..95. Similarity cannot establish near/far limb identity or support contact.', 'rankedLags':scores, 'loopAdmitted':False}
(P/'cycle-recurrence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
# These two windows were inspected on the enlarged board. The rightmost
# ground-band alpha run belongs to the visible supporting boot here only.
# Its centroid is a contact proxy, not a tracked rigid point on the sole.
windows = []
for start,end in [(33,41),(49,57)]:
    rows=[]
    for n in range(start,end+1):
        alpha=frames[n][:,:,3]>200
        floor=int(np.where(alpha)[0].max())
        columns=np.where(alpha[floor-2:floor+1].any(axis=0))[0]
        runs=np.split(columns,np.where(np.diff(columns)>1)[0]+1)
        run=runs[-1]
        rows.append({'frame':n,'floor':floor,'rightmostGroundRun':[int(run.min()),int(run.max())],'centerX':float(run.mean())})
    times=np.array([r['frame'] for r in rows],dtype=float)
    x=np.array([r['centerX'] for r in rows])
    slope,intercept=np.polyfit(times,x,1)
    residual=x-(slope*times+intercept)
    windows.append({'frames':[start,end],'rows':rows,'backwardPixelsPerFrame':float(-slope),'suggested32FrameTravelPixels':float(-slope*32),'proxyResidualSpanPixels':float(np.ptp(residual))})
contact={'scope':'Two visually inspected support windows only. Rightmost ground-band silhouette centroid changes with boot rolling; not rigid sole tracking, not near/far identity proof, not native/world contact acceptance. No stride value admitted.','windows':windows}
(P/'support-proxy-audit.json').write_text(json.dumps(contact,indent=2)+'\n',encoding='utf-8')
(P/'cycle-recurrence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'bestLags':scores[:3],'supportWindows':[{k:v for k,v in w.items() if k!='rows'} for w in windows],'loopAdmitted':False}))
