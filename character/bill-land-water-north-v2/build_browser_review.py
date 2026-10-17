from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;D=P/'browser-review'
samples=json.loads((D/'playback.json').read_text());assert len(samples)==80
groups=[]
for gear in ['bare','helmet']:
    for speed in [4,1]:
        rows=[r for r in samples if r['gear']==gear and r['speed']==speed]
        observed=sorted(set(r['pose'] for r in rows));assert rows and rows[-1]['pose']==8
        if speed==4:assert observed==list(range(1,9))
        groups.append({'gear':gear,'speed':speed,'screenshots':len(rows),'observedAXPoses':observed,'terminalPose':8})
board=Image.new('RGB',(1800,1040),'#182932');draw=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
    for phase in range(9):
        if phase==0:file=gear+'-idle.png';stamp='paused idle'
        else:
            matches=[r for r in samples if r['gear']==gear and r['speed']==4 and r['pose']==phase]
            pick=matches[len(matches)//2];file=pick['file'];stamp=str(pick['elapsedMs'])+'ms after click return'
        im=Image.open(D/file).convert('RGB');assert im.size==(1265,712)
        # Fixed crop, never fit a separate pose; all figures remain fully visible.
        board.paste(im.crop((150,190,350,650)),(phase*200,row*520+50))
        draw.text((phase*200+5,row*520+5),f'{gear} AX pose{phase}',fill='white')
        draw.text((phase*200+5,row*520+25),stamp,fill='#aecbc8')
board.save(D/'advancing-browser-board.png')
e={'cases':groups,'screenshots':82,'quarterSpeedObservedInteriorAndEndpointLabels':True,
   'captureScope':'80 advancing browser screenshots plus two paused idle views. Accessibility pose sampled immediately before screenshot; hold boundary can occur between samples. Counts are UI playback evidence, not exact capture-to-source-phase binding or Godot/native motion acceptance. Elapsed time measured after click returned, not playback dispatch; no duration claim.',
   'sourceScope':'Source frames, registration and material unchanged in this browser pass. Responsive display preserves canvas aspect ratio; display size differs from original2x preview. No per-pose rescaling.',
   'SHA256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in D.glob('*.png') if f.name!='advancing-browser-board.png'},
   'visualReview':'pending sampled advancing board and native-scale master/grade conclusions'}
(D/'review.json').write_text(json.dumps(e,indent=2)+'\n')
(D/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill North browser playback review</title><style>body{background:#182932;color:#eef;font:16px sans-serif}img{max-width:100%}</style><h1>Bill North — sampled advancing browser playback</h1><p>'+e['captureScope']+'</p><p>Both helmet states and both playback speeds reached final pose8.</p><img src="advancing-browser-board.png">',encoding='utf-8')
print(json.dumps({'playbackCases':4,'advancingScreenshots':80,'idleScreenshots':2,'caseCoverage':groups}))
