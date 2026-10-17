"""Audition fixed cranial scale against installed swimming endpoints; no selection."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
SCALES={'east':25/43,'south':25/55,'west':25/44,'north':22/55}
ANCHORS={'east':[142,118],'south':[128,143],'west':[114,118],'north':[128,110]}
for d,scale in SCALES.items():
 p=P.parent/('james-water-cargo-'+d+'-v1'); water=P.parent/('james-water-'+d+'-v1')
 points=json.loads((p/'head-candidates.json').read_text())['heads']
 corrections={'south':{4:[76,153]}}.get(d,{})
 for i,point in corrections.items():points[i]=point
 m=json.loads((water/'bare-manifest.json').read_text());st=next(s for s in m['states'] if s['id']=='swim-'+d)
 reference=Image.open(water/st['frameFiles'][0]).convert('RGBA')
 board=Image.new('RGB',(1792,950),'#303b40');draw=ImageDraw.Draw(board)
 records=[]
 for i,point in enumerate(points):
  im=Image.open(p/'source-crops'/f'{i:03d}.png').convert('RGBA');small=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
  pos=np.rint(np.array(ANCHORS[d])-np.array(point)*scale).astype(int)
  out=Image.new('RGBA',(256,276));out.alpha_composite(small,tuple(pos));folder=p/'registered-audition';folder.mkdir(exist_ok=True);out.save(folder/f'{i:03d}.png')
  at=(i%6*256,40+i//6*300);board.paste(out,at,out);draw.text((at[0]+5,at[1]-24),d+' source '+str(i),fill='white')
  draw.line((at[0],at[1]+ANCHORS[d][1],at[0]+255,at[1]+ANCHORS[d][1]),fill='#60777b')
  records.append(dict(sourcePose=i,sourceCropHead=point,position=pos.tolist(),headAnchor=(np.array(point)*scale+pos).tolist(),bounds=out.getbbox()))
 for row in range(3):board.paste(reference,(1536,40+row*300),reference);draw.text((1541,16+row*300),'Installed swim '+d,fill='white')
 board.save(p/'registration-audition.png')
 (p/'registration-audition.json').write_text(json.dumps(dict(status='audition_not_selected',fixedScale=scale,sourceSha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),registration='Visually inspected cranial proxies, fixed full-cranium width estimates; no per-frame size normalization',manualCorrections=corrections,tracking=records),indent=2)+'\n')
 print(d,'fixed scale',round(scale,5),'18 source comparisons; not installed')
