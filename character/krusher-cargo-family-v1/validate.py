from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;proof=json.load(open(P/'provenance.json'));inv=json.load(open(R/'character/krusher-complete-animation-v1/source-coverage.json'));checks=0;errors=[];joins=[]
def check(ok,why):
 global checks
 checks+=1
 if not ok:errors.append(why)
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
for r in proof['records']:
 a=arr(R/r['source']);o=arr(P/r['output']);allowed=np.array(Image.open(P/r['allowedMask']))>0
 for key,h in [('source','sourceHash'),('headSource','headHash')]:check(sha(R/r[key])==r[h],key+' hash')
 check(sha(P/r['output'])==r['outputHash'],'output hash');check(o.shape==(256,256,4),'source canvas');check(np.array_equal(a[~allowed],o[~allowed]),'protected source '+r['output']);check(np.array_equal(a[185:],o[185:]),'lower limbs/floor case '+r['output']);check(np.array_equal(a[r['headBox'][3]+48:],o[r['headBox'][3]+48:]),'case/hands/lower body below head '+r['output'])
 if r['gear']=='helmet':check(np.array_equal(a[:,:,3],o[:,:,3]),'helmet alpha')
for gear in ['bare','helmet']:
 m=json.load(open(P/(gear+'-manifest.json')));states={s['id']:s for s in m['states']};check(len(states)==25,'complete frozen cargo state set');check((m['pivot'],m['standingHeight'])==([128,224],148),'source registration')
 for s in m['states']:
  original=inv['resolved'][gear][s['id']]['state'];check({k:v for k,v in s.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in original.items() if k not in ['frameFiles','provenance']},'original timing/state flags '+s['id']);check(len(s['frameFiles'])==len(original['frameFiles']),'frame count')
  if s['id'].startswith('carry-') and s['id'].count('-')==1:check(m['strideDistanceCells'][s['id']]==inv['resolved'][gear][s['id']]['profile']['strideDistanceCells'][s['id']],'original per-direction stride')
 pairs=[]
 for d in ['south','east','north','west']:pairs.extend([('pickup-'+d,-1,'carry-'+d,0),('carry-'+d,0,'unload-'+d,0)])
 for key in states:
  if key.startswith('carry-turn-'):
   start,end=key.split('-')[-2:];pairs.extend([('carry-'+start,0,key,0),(key,-1,'carry-'+end,0)])
 for left,li,right,ri in pairs:
  ls=inv['resolved'][gear][left];rs=inv['resolved'][gear][right];a=arr(resolve(R/ls['manifest'][6:],ls['state']['frameFiles'][li]));b=arr(resolve(R/rs['manifest'][6:],rs['state']['frameFiles'][ri]));o=arr(P/states[left]['frameFiles'][li]);p=arr(P/states[right]['frameFiles'][ri]);same=np.array_equal(a,b);check(not same or np.array_equal(o,p),'source-equal join '+gear+left+right);joins.append({'gear':gear,'from':left,'to':right,'sourceEqual':bool(same),'candidateEqual':bool(np.array_equal(o,p))})
result={'checks':checks,'errors':errors,'joins':joins,'scope':'Input/output/head hashes; source body, case/hands/lower limbs; helmet alpha; source clocks/flags/stride/registration and exact shared-source endpoints'};(P/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps({'checks':checks,'errors':errors,'joins':len(joins),'exactSourceJoins':sum(j['sourceEqual'] for j in joins)}));assert not errors
# All unique whole poses, paired temporal review without duplicating reused frames.
for gear in ['bare','helmet']:
 rows=[r for r in proof['records'] if r['gear']==gear]
 for part in range((len(rows)+23)//24):
  subset=rows[part*24:(part+1)*24];board=Image.new('RGB',(1536,((len(subset)+5)//6)*280),'#242c31');draw=ImageDraw.Draw(board)
  for j,r in enumerate(subset):
   im=Image.open(P/r['output']).convert('RGBA');x=j%6*256;y=j//6*280;board.paste(im,(x,y),im);draw.text((x+2,y+259),r['state']+' '+str(r['frame'])+' '+r['view'],fill='white')
  board.save(P/(gear+f'-unique-{part}.png'))
