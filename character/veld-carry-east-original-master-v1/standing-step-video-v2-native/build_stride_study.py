from pathlib import Path
from PIL import Image
import copy,json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parents[2]
diagnostic=json.loads((P/'support-window-diagnostic.json').read_text(encoding='utf-8'))
count=38;slots=list(range(16,54));durations=[round((i+1)*1000/24)-round(i*1000/24) for i in range(count)]
rate=float(np.mean([w['candidateConstantRootSpeedPxPerSecond'] for w in diagnostic['windows']]))
stride=rate*count/24;checks=0;bindings={}
for gear in ['bare','helmet']:
 full=json.loads((P/f'{gear}-source-manifest.json').read_text(encoding='utf-8'))
 data=copy.deepcopy(full);state=copy.deepcopy(full['states'][0])
 state.update(id='carry-east',frameCount=count,frameFiles=[full['states'][0]['frameFiles'][i] for i in slots],frameDurationsMs=durations,loop=True)
 for key in ['facings','waterKinds','waterPoses','depthOffsets']:state[key]=[full['states'][0][key][i] for i in slots]
 data.update(name=f'Veld38-pose original-native stride study {gear}',status='diagnostic_full_cycle_contact_unaccepted',states=[state]+full['states'][1:],strideDistanceCells={'carry-east':stride*(65.28/148)/384})
 path=P/f'{gear}-uniform-phase-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
 frames=[]
 for ref in state['frameFiles']:
  src=R/ref[6:];bindings[src.relative_to(R).as_posix()]=hashlib.sha256(src.read_bytes()).hexdigest();frames.append(Image.open(src).convert('RGBA'));checks+=1
 target=P/f'{gear}-uniform-phase-review.png'
 frames[0].save(target,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0)
 replay=Image.open(target);assert replay.n_frames==count
 for i,im in enumerate(frames):
  replay.seek(i);assert replay.convert('RGBA').tobytes()==im.tobytes();assert abs(replay.info['duration']-durations[i])<.01;checks+=2
report={'sourceSlots':slots,'durationMs':sum(durations),'uniformDurationsMs':durations,'diagnosticStrideNativePixels':stride,'sourceSupportRateNativePxPerSecond':rate,'checks':checks,'failures':0,'bindings':bindings,'scope':'All38 original source poses16..53, complete two-leg appearance cycle, byte-exact unchanged. Uniform original FPS durations, provisional106.4native-pixel stride from two five-frame material fits. Near first frame has NCC.698/1px vertical change, heel/sole/occlusion/full support and boundary unaccepted. No source recentering/pacing/geometry/RGB edits; complete142source remains preserved. No final start/stop or normal integration.'}
(P/'phase-timing-study.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['checks','failures','diagnosticStrideNativePixels','durationMs']}))
