from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];S=P.parent/'west-unload-source-v1';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();checks=0;bindings={}
for gear in ['bare','helmet']:
 m=json.loads((S/f'{gear}-manifest.json').read_text());raw=m['states'][0];states=[]
 for key,indices,total in [('unload-west',list(range(97)),2000),('pickup-west',list(reversed(range(97))),520)]:
  refs=[raw['frameFiles'][i] for i in indices];dur=[total/len(refs)]*len(refs);state={k:v for k,v in raw.items() if k not in ['id','frameFiles','frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets']};kind=key.split('-')[0];state.update(id=key,frameFiles=refs,frameDurationsMs=dur,facings=['west']*len(refs),waterKinds=[kind]*len(refs),waterPoses=[False]*len(refs),depthOffsets=[0.0]*len(refs));states.append(state)
  ims=[Image.open(R/ref[6:]).convert('RGBA') for ref in refs];ims[0].save(P/f'{gear}-{kind}.png',save_all=True,append_images=ims[1:],duration=dur,loop=0,disposal=0,blend=0)
  # APNG rationals quantize fractional holds; retain manifest precision as clock authority.
  ap=Image.open(P/f'{gear}-{kind}.png');groups=[]
  for im,hold in zip(ims,dur):
   if groups and groups[-1][0].tobytes()==im.tobytes():groups[-1][1]+=hold
   else:groups.append([im,hold])
  assert ap.n_frames==len(groups)
  for i,(im,hold) in enumerate(groups):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes();assert abs(ap.info['duration']-hold)<.05;checks+=2
  for ref in refs:bindings[ref[6:]]=sha(R/ref[6:])
 data={k:v for k,v in m.items() if k!='states'};data.update(name='Veld West cargo timing audition '+gear,status='staged_unload2s_pickup520ms_audition_not_installed',states=states);f=P/f'{gear}-manifest.json';f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8');bindings[f.relative_to(R).as_posix()]=sha(f)
 for kind in ['unload','pickup']:
  # 60Hz presentation schedule, explicit visited source indices.
  state=next(x for x in states if x['id']==kind+'-west');total=sum(state['frameDurationsMs']);ticks=[]
  for n in range(round(total*.06)+1):
   t=min(n*1000/60,total);slot=min(int(t/(total/97)),96);ticks.append({'timeMs':t,'slot':slot})
  (P/f'{gear}-{kind}-60hz.json').write_text(json.dumps({'scope':'Declared-clock prediction; native player capture verifies separately','durationMs':total,'visitedSlots':sorted({x['slot'] for x in ticks}),'ticks':ticks},indent=2)+'\n',encoding='utf8')
(P/'FAMILY_REVIEW.json').write_text(json.dumps({'checks':checks,'failures':0,'sourcePhase':[0,96],'contiguousSourceSlots':97,'rawPhaseDurationMs':4042,'unloadMs':2000,'pickupAuditionMs':520,'scope':'Complete movement, source0..96; later neutral hold omitted. Pickup520 is cadence audition only: existing workshoppickup showsidle; no controller change or admission.','bindings':bindings},indent=2)+'\n',encoding='utf8');print('Timing build checks',checks)
