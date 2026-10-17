"""Complete native replay and read-only gait recurrence; no source modifications."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
R=P.parents[2]
N=R/'output/veld-east-neutral-source-v1'
manifest=json.loads((P/'bare-source-manifest.json').read_text(encoding='utf-8'))
durations=manifest['states'][0]['frameDurationsMs']
records=json.loads((N/'records.json').read_text(encoding='utf-8'))['records']
checks=0
for gear in ['bare','helmet']:
    images=[Image.open(N/f'{gear}-{i:03d}-native.png').convert('RGBA') for i in range(141)]
    target=P/f'{gear}-native-full-source.png'
    images[0].save(target,save_all=True,append_images=images[1:],duration=durations,loop=1,disposal=0,blend=0)
    with Image.open(target) as replay:
        assert replay.n_frames==141
        for i in range(141):
            replay.seek(i)
            assert replay.convert('RGBA').tobytes()==images[i].tobytes()
            assert abs(replay.info['duration']-durations[i])<.01
            checks+=2
    for b in range(3):
        board=Image.new('RGB',(1040,1430),'#202a30');draw=ImageDraw.Draw(board)
        draw.text((12,8),f'{gear}: actual native148px / frames {b*48}..{min(140,b*48+47)} / fixed original scale',fill='white')
        draw.text((12,35),'Held master / original empty (native148px)',fill='white')
        board.paste(images[0].crop((382,407,667,570)),(15,58))
        for k,i in enumerate(range(b*48,min(141,b*48+48))):
            x=(k%8)*130;y=240+(k//8)*195
            draw.text((x+5,y),str(i),fill='white')
            board.paste(images[i].crop((180,407,290,571)),(x+5,y+20))
        board.save(P/f'native-{gear}-chronology-{b:02d}.png')

frames=[np.array(Image.open(P/f'full-clip-frames/{i:03d}.png').convert('RGBA')) for i in range(141)]
scores=[]
for lag in range(10,73):
    errors=[]
    for n in range(20,68):
        a,b=frames[n][160:230,75:180],frames[n+lag][160:230,75:180]
        union=(a[:,:,3]>128)|(b[:,:,3]>128)
        errors.append(float(np.abs(a.astype(float)-b.astype(float))[union].mean()))
    scores.append({'lagFrames':lag,'meanLowerBodyRGBAError':float(np.mean(errors))})
scores.sort(key=lambda v:v['meanLowerBodyRGBAError'])
best=scores[0]['lagFrames']
board=Image.new('RGB',(1400,1260),'#202a30');draw=ImageDraw.Draw(board)
for k,i in enumerate(range(20,20+best+5)):
    x=(k%7)*200;y=(k//7)*140+25
    im=Image.fromarray(frames[i]).crop((75,155,180,230)).resize((168,120),Image.Resampling.NEAREST)
    board.paste(im,(x,y),im);draw.text((x,y-18),f'raw {i}',fill='white')
board.save(P/'near-far-cycle-review.png')
report={'scope':'Complete141-pose native source-clock replay, no world translation, gait loop admission or stride/contact acceptance. Recurrence is appearance evidence only; cannot identify physical near/far legs.',
        'nativeChecks':json.loads((N/'validation.json').read_text(encoding='utf-8')),
        'nativeReplayChecks':checks,'nativeReplayFailures':0,'durationMs':sum(durations),
        'rankedLags':scores,'candidateLagFrames':best,'loopAdmitted':False,
        'captureRecordSHA256':hashlib.sha256((N/'records.json').read_bytes()).hexdigest(),
        'visualReview':'Pending chronology and enlarged leg review.'}
(P/'native-cycle-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'replayChecks':checks,'durationMs':sum(durations),'bestLags':scores[:5],'loopAdmitted':False}))
