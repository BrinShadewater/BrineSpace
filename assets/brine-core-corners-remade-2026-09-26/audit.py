from pathlib import Path
import os,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
defaults=json.loads((REPO/'rooms/full-wall-v1/default-layouts.json').read_text())['layouts']
owner=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace/room_layouts.json'
overrides=json.loads(owner.read_text())['layouts'] if owner.exists() else {}
manifest=json.loads((ROOT/'manifest.json').read_text())
results=[]
def color(im,mask):
 a=np.array(im.convert('RGB')).astype(float)
 select=(np.array(mask)>240)&(a.min(2)>140)&((a.max(2)-a.min(2))<35)
 p=a[select]
 return {'median_rgb':np.median(p,axis=0).round(1).tolist(),'median_red_minus_blue':round(float(np.median(p[:,0]-p[:,2])),1),'pixels':len(p)}
for r in manifest:
 id=r['id']; reg=json.loads((REPO/'rooms/full-wall-v1/registrations'/f'{id}.json').read_text())
 old=Image.open(REPO/reg['source'].removeprefix('res://')).convert('RGBA')
 mask=Image.new('L',old.size); d=ImageDraw.Draw(mask)
 for poly in reg['pieces']: d.polygon([tuple(p) for p in poly],fill=255)
 new=Image.open(ROOT/'masters'/f'{id}.png').convert('RGBA')
 placements=[]
 for q in range(4):
  key=f'room-brine_core/{q}'; layout={**defaults.get(key,{}),**overrides.get(key,{})}
  at=layout['library/'+id]; scale=layout.get('size/library/'+id,[1,1])
  w=reg['display_width']*scale[0]
  for label,ratio in [('existing',reg['region'][3]/reg['region'][2]),('candidate_same_width',r['visible_size'][1]/r['visible_size'][0])]:
   h=reg['display_width']*ratio*scale[1]; x,y=at
   boxes=[[x+b[0]*w,y+b[1]*h,b[2]*w,b[3]*h] for b in reg['collision_boxes']]
   blocked=[]
   for side,(px,py) in enumerate([(0,-176),(176,0),(0,176),(-176,0)]):
    if any(bx-10<=px<bx+bw+10 and by-10<=py<by+bh+10 for bx,by,bw,bh in boxes): blocked.append(side)
   gap=(-36-(x+w)) if id.endswith('nw') else x-36
   placements.append(dict(rotation=q,scenario=label,at=at,world_size=[round(w,2),round(h,2)],north_72_lane_gap=round(gap,2),north_lane_with_10_padding_gap=round(gap-10,2),side_72_lane_gap=round(-36-(y+h),2),blocked_door_nodes=blocked))
 results.append(dict(id=id,original_pale_material=color(old,mask),candidate_pale_material=color(new,new.getchannel('A')),canvas=r['canvas'],placements=placements))
(ROOT/'audit-results.json').write_text(json.dumps({'method':'Read-only merged defaults plus owner saved placements. Candidate projected at existing registered width; existing collision fractions are provisional. Door-node math matches 176 reach / 10 padding but is not a native renderer test. Pale-material samples use RGB min>140 and channel spread<35, excluding background with alpha/polygon mask; not semantic material segmentation.','results':results},indent=2))
for r in results:
 print(r['id'], 'pale RGB old/new',r['original_pale_material']['median_rgb'],r['candidate_pale_material']['median_rgb'])
 for p in r['placements']:
  if p['rotation']==0: print(p)
