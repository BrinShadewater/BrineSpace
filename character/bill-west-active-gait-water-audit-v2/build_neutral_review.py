from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();records=[]
def mask(im):
 lab,n=label(np.array(im)[:,:,3]>=180);counts=np.bincount(lab.ravel());return lab==int(counts[1:].argmax()+1)
def bounds(m,box):
 x,y,x1,y1=box;ys,xs=np.where(m[y:y1,x:x1]);return [int(xs.min()+x),int(ys.min()+y),int(xs.max()+x+1),int(ys.max()+y+1)] if len(xs) else None
for gear in ['bare','helmet']:
 revision=1 if gear=='bare' else 2
 j=json.loads((OUT/f'generation-provenance-{gear}-neutral-v{revision}.json').read_text());assert j['status']=='completed';assert sha(Path(j['savedPath']))==sha(Path(j['originalPath']))==j['sha256'];assert sha(Path(j['promptFile']))==j['promptSha256']==j['submittedPromptSha256'];assert sha(Path(j['sourcePath']))==j['sourceSha256']
 for ref in j['references']:assert sha(Path(ref['path']))==ref['sha256']
 old=Image.open(j['sourcePath']).convert('RGBA');raw=Image.open(j['savedPath']).convert('RGBA');assert raw.width==raw.height
 full=raw.resize((352,352),Image.Resampling.LANCZOS);new=full.crop((0,0,352,320));new.save(OUT/f'{gear}-neutral-candidate.png');a=mask(old);b=mask(new);regions={}
 for name,box in [('head',[130,60,180,115]),('gloves',[125,130,185,170]),('boots',[125,195,195,235])]:
  aa=bounds(a,box);bb=bounds(b,box);regions[name]={'old':aa,'candidate':bb,'delta':[v-u for u,v in zip(aa,bb)] if aa and bb else None}
 rec={'gear':gear,'revision':revision,'rawCanvas':list(raw.size),'uniformScale':352/raw.width,'restoredOriginalCanvas':[352,320],'paddingCropOnly':[0,0,352,320],'translation':[0,0],'silhouetteIoU':float((a&b).sum()/(a|b).sum()),'regions':regions,'normalAdmission':False,'nativeAcceptance':False};records.append(rec)
 master=Image.open(ROOT/'character/bill-water-exit-west-master-v8/sources/master-west-reference.png').convert('RGBA');master=master.resize((round(master.width*148/956),round(master.height*148/956)),Image.Resampling.LANCZOS);mc=Image.new('RGBA',(352,320));mc.alpha_composite(master,(160-master.width//2,224-master.height))
 ready=Image.open(ROOT/f'character/bill-land-water-west-v15/{gear}/frames/land-swim-west/001.png').convert('RGBA');rise=Image.open(ROOT/f'character/bill-water-exit-west-master-v13/{gear}/frames/swim-land-west/006.png').convert('RGBA');board=Image.new('RGB',(1760,800),(23,42,51));d=ImageDraw.Draw(board)
 for i,(name,im) in enumerate([('Original master',mc),('Old neutral endpoint',old),('Edited neutral candidate',new),('Adjacent entry ready',ready),('Adjacent exit rise',rise)]):
  d.text((352*i+5,5),gear+' / '+name,fill='white');board.paste(im,(352*i,30),im);c=im.crop((120,55,190,145)).resize((210,270),Image.Resampling.NEAREST);board.paste(c,(352*i+70,410),c)
 board.save(OUT/f'{gear}-neutral-master-review.png')
(OUT/'neutral-assessment.json').write_text(json.dumps({'status':'shared_neutral_source_candidates_unselected','records':records,'scope':'Two sources shared by entry0/exit7; geometric windows are diagnostics, not anatomy or movement acceptance'},indent=2)+'\n');print(json.dumps(records))
