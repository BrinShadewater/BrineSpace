from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
rows=json.loads((ROOT/'manifest.json').read_text())
out=Image.new('RGB',(2400,880),(38,44,47));d=ImageDraw.Draw(out)
crew=Image.open(PROJECT/'character/major-bill-v3/rotations/south.png').convert('RGBA')
# Same standing height and source metadata as grid_canvas.gd, at CELL=384.
crew_scale=65.28/148
crew=crew.resize(tuple(round(v*crew_scale*2) for v in crew.size),Image.Resampling.NEAREST)
results=[]
for i,r in enumerate(rows):
 ox=i*800+16;oy=55
 def box(x,y,w,h): return (ox+2*x,oy+2*y,ox+2*(x+w),oy+2*(y+h))
 d.rectangle(box(0,0,384,384),fill=(99,105,103),outline=(188,191,181),width=2)
 # Conservative entry lanes: 86.4 visual door width + 10 units each side.
 for x,y,w,h in [(138.8,0,106.4,192),(138.8,192,106.4,192),(0,138.8,192,106.4),(192,138.8,192,106.4)]:
  d.rectangle(box(x,y,w,h),outline=(207,148,78),width=2)
 f=ROOT/'game-size'/(r['id']+'.png');im=Image.open(f).convert('RGBA')
 scale=r['suggested_display_width']/im.width
 width=im.width*scale;height=im.height*scale
 im=im.resize((round(width*2),round(height*2)),Image.Resampling.NEAREST)
 out.paste(im,(ox+20,oy+12),im)
 # Character feet beside the inner counter corner, at world (104,143).
 out.paste(crew,(round(ox+208-92*crew_scale*2),round(oy+286-172*crew_scale*2)),crew)
 north_gap=138.8-(10+width);west_gap=138.8-(6+height)
 assert north_gap>0 and west_gap>0
 d.text((ox,18),r['id'],fill='white')
 d.text((ox,835),f'Proposed NW placement; N lane gap {north_gap:.1f}, W lane gap {west_gap:.1f} world units',fill='white')
 results.append(dict(id=r['id'],canvas_world_size=[width,height],proposed_canvas_origin=[-182,-186],north_entry_lane_gap=north_gap,west_entry_lane_gap=west_gap,pixels_per_world_unit=1/scale,export_hash_ok=hashlib.sha256(f.read_bytes()).hexdigest()==r['export_sha256']))
out.save(ROOT/'crew-doorway-study.png')
(ROOT/'scale-checks.json').write_text(json.dumps(dict(kind='Static conservative bounding-box study, not runtime validation',room_cell=384,crew_standing_height=65.28,entry_lane_width=106.4,assets=results),indent=2))
print(json.dumps(results))
