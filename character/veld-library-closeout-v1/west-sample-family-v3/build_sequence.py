from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];M=P.parent/'west-kneel-motion-v2';E=P.parent/'west-examine-kneeling-v1'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
checks=0;bindings={}
for gear in ['bare','helmet']:
 a=json.loads((M/f'{gear}-manifest.json').read_text());b=json.loads((E/f'{gear}-manifest.json').read_text());states=[a['states'][1],b['states'][0],a['states'][2]]
 assert [sum(x['frameDurationsMs']) for x in states]==[1000,4000,1000];checks+=3
 data={k:v for k,v in a.items() if k!='states'};data['name']='Veld original West complete sample sequence '+gear;data['states']=states
 f=P/f'{gear}-manifest.json';f.write_text(json.dumps(data,indent=2)+'\n');bindings[f.relative_to(R).as_posix()]=sha(f)
 refs=[];holds=[]
 for state in states:
  refs+=state['frameFiles'];holds+=state['frameDurationsMs']
  for ref in state['frameFiles']:bindings[ref[6:]]=sha(R/ref[6:])
 ims=[Image.open(R/ref[6:]).convert('RGBA') for ref in refs]
 ims[0].save(P/f'{gear}-sequence.png',save_all=True,append_images=ims[1:],duration=holds,loop=0,disposal=0,blend=0)
 groups=[]
 for im,hold in zip(ims,holds):
  if groups and im.tobytes()==groups[-1][0].tobytes():groups[-1][1]+=hold
  else:groups.append([im,hold])
 ap=Image.open(P/f'{gear}-sequence.png');assert ap.n_frames==len(groups);checks+=1
 for i,(im,hold) in enumerate(groups):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes();assert ap.info['duration']==hold;checks+=2
 board=Image.new('RGB',(1536,570),'#202a30');d=ImageDraw.Draw(board)
 pairs=[('Lower start',states[0]['frameFiles'][0]),('Lower end',states[0]['frameFiles'][-1]),('Examine start',states[1]['frameFiles'][0]),('Examine end',states[1]['frameFiles'][-1]),('Rise start',states[2]['frameFiles'][0]),('Rise end',states[2]['frameFiles'][-1])]
 for j,(label,ref) in enumerate(pairs):
  im=Image.open(R/ref[6:]).convert('RGBA');board.paste(im,(j*256,24),im);d.text((j*256+4,4),label,fill='white')
  crop=im.crop((100,110,165,180)).resize((130,140),Image.Resampling.NEAREST);board.paste(crop,(j*256+45,315),crop)
 board.save(P/f'{gear}-joins.png')
for f in [M/'FAMILY_REVIEW.json',E/'FAMILY_REVIEW.json',M/'CORRECTED_FRONT_TOE_REVIEW.json']:bindings[f.relative_to(R).as_posix()]=sha(f)
(P/'FAMILY_REVIEW.json').write_text(json.dumps(dict(checks=checks,failures=0,phasePoses=[57,142,57],phaseDurationsMs=[1000,4000,1000],scope='Full staged lower/examine/stow/rise per gear, exact reused source poses. No normal selection or anatomy/boot edits. Viewer looping is replay only.',bindings=bindings),indent=2)+'\n')
print('Joined family checks:',checks)
