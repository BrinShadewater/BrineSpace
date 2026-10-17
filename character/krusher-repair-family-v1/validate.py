from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path('character/krusher-repair-family-v1');R=P.parent.parent;proof=json.loads((P/'provenance.json').read_text());inv=json.loads((R/'character/krusher-complete-animation-v1/source-coverage.json').read_text());checks=0;errors=[];joins=[]
def check(ok,why):
 global checks
 checks+=1
 if not ok:errors.append(why)
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
for r in proof['records']:
 a=arr(R/r['source']);o=arr(P/r['output']);allowed=np.array(Image.open(P/r['allowedMask']))>0
 check(sha(R/r['source'])==r['sourceHash'],r['source']+' hash');check(sha(P/r['output'])==r['outputHash'],'output hash');check(o.shape==(184,184,4),'native canvas')
 if r['headSource']:check(sha(R/r['headSource'])==r['headHash'],'head hash')
 check(np.array_equal(a[~allowed],o[~allowed]),'protected source pixels '+r['output'])
 check(np.array_equal(a[150:],o[150:]),'feet and lower legs '+r['output'])
 if r['gear']=='helmet':check(np.array_equal(a[:,:,3],o[:,:,3]),'helmet alpha '+r['output'])
for gear in ['bare','helmet']:
 m=json.loads((P/(gear+'-manifest.json')).read_text());states={s['id']:s for s in m['states']};canonical=json.loads((R/('character/krusher-james-canonical-v4/'+gear+'-manifest.json')).read_text())
 for s in m['states']:
  original=inv['resolved'][gear][s['id']]['state'];check({k:v for k,v in s.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in original.items() if k not in ['frameFiles','provenance']},'original timing/flags '+s['id']);check(len(s['frameFiles'])==len(original['frameFiles']),'pose count')
 for d in ['south','east','north','west']:
  idle=next(s for s in canonical['states'] if s['id']=='idle-'+d);idle_a=arr(R/'character/krusher-james-canonical-v4'/idle['frameFiles'][0])
  check(np.array_equal(arr(P/states['kneel-'+d]['frameFiles'][0]),idle_a),'kneel idle start '+gear+d);check(np.array_equal(arr(P/states['stand-'+d]['frameFiles'][-1]),idle_a),'stand idle end '+gear+d)
  for left,right in [('kneel','repair'),('repair','stand')]:
   ls=inv['resolved'][gear][left+'-'+d];rs=inv['resolved'][gear][right+'-'+d];la=arr(resolve(R/ls['manifest'][6:],ls['state']['frameFiles'][-1]));ra=arr(resolve(R/rs['manifest'][6:],rs['state']['frameFiles'][0]));lo=arr(P/states[left+'-'+d]['frameFiles'][-1]);ro=arr(P/states[right+'-'+d]['frameFiles'][0]);same=np.array_equal(la,ra);check(not same or np.array_equal(lo,ro),'shared source join '+gear+d+left);joins.append({'gear':gear,'direction':d,'join':left+' to '+right,'sourceEqual':same,'candidateEqual':bool(np.array_equal(lo,ro)),'sourceChangedPixels':int(np.any(la!=ra,axis=2).sum()),'candidateChangedPixels':int(np.any(lo!=ro,axis=2).sum())})
result={'checks':checks,'errors':errors,'joins':joins,'scope':'All source/output/head hashes, protected source pixels, lower limbs, helmet alpha, exact state metadata; complete idle endpoints and shared-source joins'};(P/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps({'checks':checks,'errors':errors,'joins':joins}));assert not errors
# chronological frames at each 1/8 of an action for visual head and tool review
for gear in ['bare','helmet']:
 m=json.loads((P/(gear+'-manifest.json')).read_text());board=Image.new('RGB',(1472,12*210),'#242c31');draw=ImageDraw.Draw(board)
 for row,s in enumerate(m['states']):
  draw.text((4,row*210+2),s['id'],fill='white')
  for j in range(8):
   im=Image.open(P/s['frameFiles'][round(j*(len(s['frameFiles'])-1)/7)]).convert('RGBA');board.paste(im,(j*184,row*210+20),im)
 board.save(P/(gear+'-temporal.png'))
