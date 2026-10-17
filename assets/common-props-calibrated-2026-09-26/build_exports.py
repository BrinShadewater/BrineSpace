"""Reproducible size-only exports; source artwork remains unchanged."""
from pathlib import Path
import json, hashlib, math
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
REFERENCE = Path('C:/Users/Alex/Desktop/BrineSpace Clean Prop Exports')
# Visible sprite bounds in library pixels, not equal-sized thumbnail cells.
GROUPS = {
 'common-props-2026-09-26-v2': {
  'common-crate-v2':(115,110), 'common-barrel-v2':(85,110),
  'common-couch-v2':(300,190), 'common-chair-v2':(145,165),
  'common-bookcase-v2':(300,165), 'common-standing-plant-v2':(110,130),
  'common-container-v2':(135,75), 'common-table-and-chairs-v2':(310,180),
  'common-lockers-v2':(250,175), 'common-workstation-v2':(290,210)},
 'common-props-batch2-2026-09-26': {
  'common-storage-bench':(235,110), 'common-utility-cart':(145,160),
  'common-open-shelving':(245,155), 'common-recycling-station':(195,155),
  'common-water-dispenser':(105,135), 'common-wall-cabinet':(210,110),
  'common-folding-stool':(80,100), 'common-coffee-table':(190,120)},
 'common-seating-2026-09-26-v2': {
  'seat-utility-chair':(125,125), 'seat-task-chair':(105,145),
  'seat-round-stool':(75,90), 'seat-square-stool':(80,80)},
 'common-seating-variants-2026-09-26': {
  'seat-utility-chair-blue':(125,125), 'seat-task-chair-olive':(105,145),
  'seat-utility-chair-metal':(125,125), 'seat-task-chair-metal':(105,145),
  'seat-round-stool-metal':(75,90), 'seat-square-stool-metal':(80,80)},
 'common-plants-2026-09-26': {
  'plant-broadleaf':(110,140), 'plant-fern':(120,105),
  'plant-snake-plant':(85,140), 'plant-palm':(130,140),
  'plant-succulent':(55,55), 'plant-trough':(200,95)},
 'tall-plants-2026-09-26': {
  'plant-tall-ficus':(145,240), 'plant-tall-palm':(170,250),
  'plant-tall-dracaena':(135,230)},
}
REFS=['sp-recreation-extra3-6','sp-recreation-extra3-5','sp-crew_lounge-4','sp-science-extra3-3']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def build():
 (ROOT/'game-size').mkdir(exist_ok=True)
 rows=[]
 for folder,items in GROUPS.items():
  base=PROJECT/'assets'/folder
  if (base/'masters').exists(): base=base/'masters'
  for ident,limit in items.items():
   source=base/(ident+'.png')
   if (ROOT/'revised-masters'/(ident+'.png')).exists(): source=ROOT/'revised-masters'/(ident+'.png')
   im=Image.open(source).convert('RGBA')
   # Bounds only: retain original alpha inside padded visible silhouette.
   # Alpha 1-15 exterior ghosts must not determine physical object size.
   b=im.getchannel('A').point(lambda v: 255 if v>=16 else 0).getbbox()
   bounds=(max(0,b[0]-4),max(0,b[1]-4),min(im.width,b[2]+4),min(im.height,b[3]+4))
   sprite=im.crop(bounds)
   scale=min(limit[0]/sprite.width,limit[1]/sprite.height)
   size=tuple(max(1,round(v*scale)) for v in sprite.size)
   sprite=sprite.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
   canvas=Image.new('RGBA',(size[0]+8,size[1]+8));canvas.paste(sprite,(4,4))
   dest=ROOT/'game-size'/(ident+'.png');canvas.save(dest)
   rows.append(dict(id=ident,master=str(source),master_sha256=sha(source),master_size=im.size,
    crop=bounds,visible_budget=limit,visible_size=size,canvas=canvas.size,
    export=str(dest),export_sha256=sha(dest),alpha=canvas.getchannel('A').getextrema(),
    suggested_display_width=round(canvas.width*.34,2),
    scale_status='proposed: calibrated to reference catalog, not installed'))
 (ROOT/'manifest.json').write_text(json.dumps({'resampling':'premultiplied-alpha LANCZOS, same as accepted reference exporter','world_units_per_library_pixel':.34,'assets':rows},indent=2))
 for name,bg in [('light',(205,207,200)),('dark',(35,41,44))]:
  for group,items in [('seating',[r for r in rows if r['id'].startswith('seat-')]),('plants',[r for r in rows if r['id'].startswith('plant-') or 'standing-plant' in r['id']]),('utility',[r for r in rows if r['id'].startswith('common-') and 'standing-plant' not in r['id']])]:
   entries=[(i,REFERENCE/'game-size'/(i+'.png')) for i in REFS]+[(r['id'],Path(r['export'])) for r in items]
   sheet=Image.new('RGB',(880,math.ceil(len(entries)/2)*300),bg);draw=ImageDraw.Draw(sheet)
   for n,(ident,path) in enumerate(entries):
    im=Image.open(path).convert('RGBA');x=n%2*440;y=n//2*300
    sheet.paste(im,(x+(440-im.width)//2,y+260-im.height),im)
    draw.text((x+12,y+273),('REFERENCE: ' if n<4 else '')+ident,fill='white' if name=='dark' else 'black')
   sheet.save(ROOT/(group+'-native-'+name+'.png'))
 # Small actual-world-unit preview with nearest filtering, matching grid_canvas.
 entries=[(i,REFERENCE/'game-size'/(i+'.png')) for i in REFS]+[(r['id'],Path(r['export'])) for r in rows]
 sheet=Image.new('RGB',(900,math.ceil(len(entries)/5)*130),(80,85,82));draw=ImageDraw.Draw(sheet)
 for n,(ident,path) in enumerate(entries):
  im=Image.open(path).convert('RGBA'); im=im.resize(tuple(max(1,round(v*.34)) for v in im.size),Image.Resampling.NEAREST)
  x=n%5*180;y=n//5*130;sheet.paste(im,(x+(180-im.width)//2,y+98-im.height),im)
  draw.text((x+3,y+106),ident.replace('common-','').replace('plant-','').replace('seat-',''),fill='white')
 sheet.save(ROOT/'world-scale-review.png')
 assert len(rows)==37
 assert all(r['alpha'][0]==0 and r['alpha'][1]>=250 for r in rows)
 assert all(sha(Path(r['master']))==r['master_sha256'] for r in rows)
 print('37 exports verified; source hashes unchanged; native and world-scale review sheets saved.')

if __name__=='__main__': build()
