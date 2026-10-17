from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
PACKS=['common-props-calibrated-2026-09-26','plants-matte-2026-09-26','common-storage-2026-09-26','common-surfaces-2026-09-26','submarine-utilities-2026-09-26']
current={}
for pack in PACKS:
 p=PROJECT/'assets'/pack
 raw=json.loads((p/'manifest.json').read_text());rows=raw['assets'] if isinstance(raw,dict) else raw
 for r in rows:
  path=p/'game-size'/(r['id']+'.png');im=Image.open(path);a=im.getchannel('A');b=a.point(lambda v:255 if v>=16 else 0).getbbox()
  master=Path(r.get('master',p/'masters'/(r['id']+'.png')))
  current[r['id']]=dict(id=r['id'],pack=pack,path=str(path),size=im.size,visible_bounds=b,display_width=r['suggested_display_width'],pixels_per_world_unit=im.width/r['suggested_display_width'],mode=im.mode,alpha=a.getextrema(),export_hash_ok=hashlib.sha256(path.read_bytes()).hexdigest()==r['export_sha256'],master_hash_ok=hashlib.sha256(master.read_bytes()).hexdigest()==r['master_sha256'],master=str(master),border_clear=all(v==0 for v in [a.crop((0,0,im.width,1)).getextrema()[1],a.crop((0,im.height-1,im.width,im.height)).getextrema()[1],a.crop((0,0,1,im.height)).getextrema()[1],a.crop((im.width-1,0,im.width,im.height)).getextrema()[1]]))
rows=list(current.values())
refroot=Path('C:/Users/Alex/Desktop/BrineSpace Clean Prop Exports')
lock=json.loads((PROJECT/'docs/BRINESPACE_ART_REFERENCE_LOCK_2026-09-26.json').read_text())['assets']
refs=[]
for id in ['sp-recreation-extra3-6','sp-recreation-extra3-5','sp-science-extra3-3']:
 r=next(r for r in lock if r['id']==id);p=refroot/r['native']['path'];refs.append((id,p));assert hashlib.sha256(p.read_bytes()).hexdigest()==r['native']['sha256']
for page in range(math.ceil(len(rows)/12)):
 for tone,bg in [('light',(205,207,200)),('dark',(35,41,44))]:
  out=Image.new('RGB',(1320,1120),bg);d=ImageDraw.Draw(out);fg='white' if tone=='dark' else 'black'
  for i,(id,p) in enumerate(refs):
   im=Image.open(p).convert('RGBA');out.paste(im,(i*400+(400-im.width)//2,260-im.height),im);d.text((i*400+10,270),'REFERENCE '+id,fill=fg)
  for i,r in enumerate(rows[page*12:(page+1)*12]):
   im=Image.open(r['path']);x=i%4*330;y=300+i//4*270;out.paste(im,(x+(330-im.width)//2,y+235-im.height),im);d.text((x+8,y+242),r['id'],fill=fg)
  out.save(ROOT/f'page-{page+1}-{tone}.png')
(ROOT/'checks.json').write_text(json.dumps(dict(count=len(rows),assets=rows),indent=2))
print(json.dumps(dict(current_assets=len(rows),superseded_plant_exports=10,hash_failures=sum(not(r['export_hash_ok'] and r['master_hash_ok']) for r in rows),border_failures=sum(not r['border_clear'] for r in rows),density_range=[min(r['pixels_per_world_unit'] for r in rows),max(r['pixels_per_world_unit'] for r in rows)])))
