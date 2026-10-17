import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
m=json.loads((P/'manifest.json').read_text());source=json.loads((R/'character/james-helmet-fitting-east-v1/manifest.json').read_text());proof=json.loads((P/'provenance.json').read_text());checks=0;errors=[]
def check(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
check((m['frameWidth'],m['frameHeight'],m['pivot'],m['standingHeight'])==(256,256,[128,224],148),'registration')
for state,old in zip(m['states'],source['states']):
 check({k:v for k,v in state.items() if k not in ['frameFiles','provenance','sourcePoseIndices']}=={k:v for k,v in old.items() if k not in ['frameFiles','provenance']},'state metadata:'+state['id'])
 for i,f in enumerate(state['frameFiles']):
  n=state['sourcePoseIndices'][i];r=proof['records'][n];a=np.array(Image.open(R/r['source']).convert('RGBA'));b=np.array(Image.open(P/f).convert('RGBA'));mask=np.array(Image.open(P/r['allowedMask']))>0
  check(hashlib.sha256((R/r['source']).read_bytes()).hexdigest()==r['sourceHash'],'source hash')
  check(b.shape==(256,256,4),'canvas')
  check(np.array_equal(a[~mask],b[~mask]),'protected body')
  check(np.array_equal(a[138:],b[138:]),'boots and utility gear')
  if n not in (0,1,2,3,4,11):check(np.array_equal(a[:,:,3],b[:,:,3]),'shell/alpha')
  check(np.array_equal(b,np.array(Image.open(P/m['states'][0]['frameFiles'][n]).convert('RGBA'))),'reversal')
for gear,n in [('bare',0),('helmet',11)]:
 cm=json.loads((R/'character/krusher-james-canonical-v4'/f'{gear}-manifest.json').read_text());idle=next(s for s in cm['states'] if s['id']=='idle-east');im=Image.open(R/'character/krusher-james-canonical-v4'/idle['frameFiles'][0]).convert('RGBA');pad=Image.new('RGBA',(256,256));pad.alpha_composite(im,(36,52))
 check(np.array_equal(np.array(pad),np.array(Image.open(P/m['states'][0]['frameFiles'][n]).convert('RGBA'))),'exact canonical endpoint:'+gear)
result={'checks':checks,'errors':errors,'scope':'Source hashes, clock/events, protected pixels, exact reversal and complete canonical idle joins'};(P/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not errors
