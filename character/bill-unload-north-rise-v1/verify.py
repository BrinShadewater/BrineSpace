from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;reg=json.loads((P/'registration.json').read_text());Y,X=np.indices((256,256));protect=(Y<164)|(((X<112)|(X>=146))&(Y<181));checks=0;inserts={}
def check(ok,message):
 global checks
 checks+=1
 assert ok,message
for f,h in reg['sourceSha256'].items():check(hashlib.sha256((R/f).read_bytes()).hexdigest()==h,'Original input/source bytes unchanged')
for rec in reg['frames']:check(rec['scale']==reg['scale'],'One full-figure ruler across inserted legs')
for gear in ['bare','helmet']:
 old=next(s for s in json.loads((R/'character/bill-cargo-north-master-head-v1'/('manifest.json' if gear=='bare' else 'helmet-manifest.json')).read_text())['states'] if s['id']=='unload-north');m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0];master=np.array(Image.open(R/old['frameFiles'][-1].removeprefix('res://')).convert('RGBA'));inserts[gear]=[]
 check(m['status']=='staged_visual_review' and m['standingHeight']==148 and m['pivot']==[128,224],'Original ruler/pivot, staged only')
 check(len(s['frameFiles'])==14 and sum(s['frameDurationsMs'])==640 and not s['loop'],'Finite640ms visual source,2second controller remains external')
 crowns=[]
 for i,f in enumerate(s['frameFiles']):
  path=R/f.removeprefix('res://');a=np.array(Image.open(path));check(a.shape==(256,256,4),'RGBA native canvas')
  if i<=10 or i==13:
   src=R/old['frameFiles'][i if i<=10 else 11].removeprefix('res://');check(path.read_bytes()==src.read_bytes(),'Every original source row and final endpoint byte-exact')
  else:
   dy=reg['frames'][i-11]['upperTranslation'][1];expected=master.copy();expected[~protect]=0;canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(Image.fromarray(expected),(0,dy));expected=np.array(canvas);p=(Y<164+dy)|(((X<112)|(X>=146))&(Y<181+dy));check(np.array_equal(a[p],expected[p]),'Original upper RGBA translated only, no generated head/body leaking through')
   check(np.array_equal(a[200:215,123:132],master[200:215,123:132]),'Visible original case core remains fixed')
   inserts[gear].append((a,dy))
  ys,xs=np.where(a[:,:,3]>180);check(xs.min()>0 and xs.max()<255 and 222<=ys.max()<=224,'Complete body and same floor contact')
  if i>=10:crowns.append(int(ys.min()))
 check(max(abs(a-b) for a,b in zip(crowns,crowns[1:]))<=8,'Rise crown progression capped8px instead of22px')
for (a,dy),(b,other) in zip(inserts['bare'],inserts['helmet']):check(dy==other and np.array_equal(a[(Y>=164+dy)&(X>=112)&(X<146)],b[(Y>=164+dy)&(X>=112)&(X<146)]),'Exact paired lower-leg/case pixels')
(P/'validation.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'Canonical byte-copy source/endpoints, exact translated protected upper, shared source ruler/paired legs/case core and discrete crown steps only; no anatomical or full motion acceptance.'},indent=2)+'\n');print('BILL NORTH UNLOAD RISE: %d checks pass'%checks)
