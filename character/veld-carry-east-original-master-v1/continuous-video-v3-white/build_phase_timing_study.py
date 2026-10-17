"""Full two-step diagnostic pacing; unmodified source poses and original helmet."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,copy,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[2]
report=json.loads((P/'support-material-diagnostic-v2.json').read_text(encoding='utf-8'))
w=report['windows']
low=np.mean([w[0][key]['nativeBackwardPixelsPerFrame'] for key in ['toeCap','ankleStrap']])
high=np.mean([w[1][key]['nativeBackwardPixelsPerFrame'] for key in ['toeCap','ankleStrap']])
slots=list(range(18,55));count=len(slots);total=round(count*1000/24)
knots=[-18,-12,1,7,19,25,38,44,56,62]
rates=[low,low,high,high,low,low,high,high,low,low]
weights=np.interp(np.array(slots)+.5,knots,rates)
stride=float(weights.sum())
boundaries=np.rint(np.r_[0,np.cumsum(weights)]/stride*total).astype(int)
paced=np.diff(boundaries).tolist()
uniform=[round((i+1)*1000/24)-round(i*1000/24) for i in range(count)]
assert sum(paced)==sum(uniform)==total and min(paced)>0
checks=2;bindings={}
for gear in ['bare','helmet']:
    full=json.loads((P/f'{gear}-source-manifest.json').read_text(encoding='utf-8'))
    for label,durations in [('uniform',uniform),('paced',paced)]:
        data=copy.deepcopy(full);state=copy.deepcopy(full['states'][0])
        state.update(id='carry-east',frameCount=count,frameFiles=[full['states'][0]['frameFiles'][i] for i in slots],frameDurationsMs=durations,loop=True)
        for key in ['facings','waterKinds','waterPoses','depthOffsets']:
            if key in state:state[key]=[full['states'][0][key][i] for i in slots]
        data.update(name=f'Veld East37-pose {label} diagnostic {gear}',status='diagnostic_full_cycle_unaccepted_contacts',states=[state]+full['states'][1:],strideDistanceCells={'carry-east':stride*(65.28/148)/384})
        path=P/f'{gear}-{label}-phase-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
        bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
        for ref in state['frameFiles']:
            source=R/ref[6:];bindings[source.relative_to(R).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest();checks+=1
        frames=[Image.open(R/ref[6:]).convert('RGBA') for ref in state['frameFiles']]
        target=P/f'{gear}-{label}-phase-review.png'
        frames[0].save(target,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0)
        with Image.open(target) as replay:
            assert replay.n_frames==count
            for i in range(count):
                replay.seek(i);assert replay.convert('RGBA').tobytes()==frames[i].tobytes();assert abs(replay.info['duration']-durations[i])<.01;checks+=2

comparisons=[]
for label,durations in [('uniform',uniform),('paced',paced)]:
    cumulative=np.r_[0,np.cumsum(durations)]
    root={n:float(stride*(cumulative[i]+durations[i]/2)/total) for i,n in enumerate(slots)}
    windows=[]
    for win in w[:2]:
        for key in ['toeCap','ankleStrap']:
            values=np.array([row['nativeX']+root[row['frame']] for row in win[key]['rows']])
            windows.append({'frames':win['frames'],'material':key,'predictedWorldPointSpanNativePixels':float(np.ptp(values)),'spanAt93px':float(np.ptp(values)*93/148)})
    comparisons.append({'timing':label,'shortWindowPredictedContactSpans':windows})
out={'status':'full37-pose_timing_study_only','sourceSlots':slots,'durationMs':total,'uniformDurationsMs':uniform,'pacedDurationsMs':paced,'diagnosticStrideNativePixels':stride,'lowSupportPixelsPerRawFrame':float(low),'highSupportPixelsPerRawFrame':float(high),'checks':checks,'failures':0,'comparisons':comparisons,'bindings':bindings,'scope':'All37 unmodified raw poses18..54 retained, including both steps. Periodic linear rate interpolation from two short flat-support fits is provisional pacing only; other support/roll phases and near/far identity remain unverified. No physical contact, final stride, start/stop or normal integration acceptance.'}
(P/'phase-timing-study.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['checks','failures','diagnosticStrideNativePixels','pacedDurationsMs','comparisons']}))
