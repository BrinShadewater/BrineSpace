from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1]
panels=[];evidence={}
for study,kinds in [('visibility',['normal','crew-white','floor-hidden','foreground-hidden']),('readability',['normal','alpha62','alpha78','alpha90'])]:
 out=R/f'output/bill-floor-case-flood-{study}-v1'
 report=json.loads((out/'validation.json').read_text());assert report['passed']
 records=json.loads((out/'records.json').read_text());assert records['failures']==0
 copies=P/f'flood-{study}-captures';copies.mkdir(exist_ok=True)
 board=Image.new('RGB',(1000,420),'#182932');d=ImageDraw.Draw(board)
 hashes={}
 for j,gear in enumerate(['bare','helmet']):
  source_hash=None;foot=None
  for i,kind in enumerate(kinds):
   name=f'{gear}-{kind}';row=next(x for x in records['records'] if x['name']==name)
   for suffix in ['source','room']:
    src=out/f'{name}-{suffix}.png';dest=copies/src.name;shutil.copy2(src,dest)
    hashes[dest.name]=hashlib.sha256(dest.read_bytes()).hexdigest()
   im=Image.open(copies/f'{name}-source.png').convert('RGBA')
   digest=hashlib.sha256(im.tobytes()).hexdigest()
   if source_hash is None:source_hash=digest;foot=row['foot']
   assert digest==source_hash and row['foot']==foot
   # Crop from actual native capture, centred on the logged physical foot.
   x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
   crop=Image.open(copies/f'{name}-room.png').crop((round(x)-95,round(y)-135,round(x)+105,round(y)+65))
   board.paste(crop,(i*250,30+j*210));d.text((i*250,j*210+8),name,fill='white')
 board.save(P/f'flood-{study}-review.png')
 panels.append(f'<h2>{study.title()}</h2><img src="flood-{study}-review.png" width="1000">')
 evidence[study]={'validation':report,'records':records,'originalCaptureSHA256':hashes,'registration':'Native crop from logged foot and captured room camera; no source repaint/grade/resizing.'}
(P/'flood-readability-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill flood readability</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Bill — flood readability study</h1><p>Both gears, same source/clock/foot. Original water layers and drawing order. Candidate tint is staged only; no continuous motion acceptance.</p>'+''.join(panels))
(P/'flood-readability-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Two native boards; 32 original source/room captures retained and same-source/root checks pass.')
