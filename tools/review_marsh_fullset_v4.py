"""Compare every selected family to the idle references at original pixel size."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from prepare_marsh_full_polish import material_mask
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-quality-pass-v4'
DIRS=('south','north','east','west')
def main():
 states=json.loads((BASE/'baseline-contract.json').read_text())['states'];refs={};rows=[];families={}
 for d in DIRS:
  im=Image.open(ROOT/states['idle-'+d]['files'][0]).convert('RGBA');m,l,_=material_mask(im);refs[d]=float(l[m].mean())
 for key,s in states.items():
  values=[]
  for f in s['files']:
   im=Image.open(ROOT/f).convert('RGBA');m,l,_=material_mask(im)
   if m.sum()>80:values.append(float(l[m].mean()))
  d=key.rsplit('-',1)[-1];mean=float(np.median(values)) if values else None
  rows.append({'key':key,'ivoryMean':mean,'reference':refs.get(d),'gap':mean-refs[d] if mean and d in refs else None})
  if d in DIRS:families.setdefault(key.rsplit('-',1)[0],{})[d]=s
 for page,start in enumerate(range(0,len(families),6)):
  board=Image.new('RGB',(1536,6*204),'#293b40');draw=ImageDraw.Draw(board)
  for row,family in enumerate(sorted(families)[start:start+6]):
   for col,d in enumerate(DIRS):
    s=families[family].get(d)
    if not s:continue
    for j,slot in enumerate((len(s['files'])//2,len(s['files'])-1)):
     im=Image.open(ROOT/s['files'][slot]).convert('RGBA');b=im.getbbox()
     # Original pixels, including tall/wide frames; crop transparent padding.
     im=im.crop(b);x=(col*2+j)*192+(192-im.width)//2;y=row*204+25
     if im.height>170 or im.width>190:
      im.thumbnail((190,170),Image.Resampling.NEAREST)
     board.paste(im,(x,y),im);draw.text(((col*2+j)*192+2,row*204+2),family+' / '+d+' '+str(slot),fill='white')
  board.save(BASE/f'family-overview-{page:02}.png')
 (BASE/'material-review.json').write_text(json.dumps({'references':refs,'states':rows,'policy':'Ivory mask means flag review; posture, illumination and skin can affect statistics.'},indent=2)+'\n')
 print('204 states; '+str(len(families))+' families; '+str((len(families)+5)//6)+' overview boards')
 print('Largest material gaps:',[(r['key'],round(r['gap'],1)) for r in sorted((r for r in rows if r['gap'] is not None),key=lambda r:abs(r['gap']),reverse=True)[:25]])
if __name__=='__main__':main()
