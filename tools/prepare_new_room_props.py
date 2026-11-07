"""Reproducible cutout/export preparation. Preserves source alpha; no repaint."""
from pathlib import Path
import json, hashlib, html
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/new-room-props-2026-09-26'
SOURCE=Path(r'C:/Users/Alex/Desktop/Projects/Gaming/Brine Space Art/BrineSpace Clean Prop Exports/New Room Art - Organized 2026-09-26')
LABELS={
'echo-chamber':['resonance chambers','specimen vessels','analysis console','signal recorder','sealed chamber'],
'fold-chamber':['containment gate','field test bench','field controls','cable drum','field equipment cabinet'],
'pressure-garden':['pressure terrarium','plant chamber','pressure pump','specimen bench','vessel trolley'],
'stillwater-observatory':['observation basin','optical instrument','observation controls','recording cabinet','observation sofa'],
'atmospheric-scrubber':['scrubber tower','twin blower','filter cabinet','air manifold','air quality console'],
'habitat-recovery':['recovery chamber','soil mixer','recovery planter','nutrient vessels','recovery console'],
'seed-vault':['seed cabinet','cold chest','seed workbench','germination chamber','seed console'],
'water-reclamation':['filter vessels','purification unit','water pump','water reservoir','water quality console'],
'bulkhead-control':['bulkhead controls','valve manifold','manual valve pedestal','pressure vessels','control cabinet'],
'cargo-dispatch':['dispatch terminal','cargo hoist','weighing platform','cargo trolley','freight rack'],
'damage-control':['hull repair bench','emergency pump trolley','patch plate rack'],
'sonar-mapping':['sonar desk','mapping table','signal recorder'],
'aquarium':['large tank','round tank','tank console','aquarium service cabinet','aquarium sofa'],
'art-studio':['easel station','sculpture bench','materials cabinet','drawing bench','art console'],
'bathhouse':['bath tub','shower column','changing bench','towel cabinet','laundry trolley','mirror and sink'],
'botanical-conservatory':['planter bench','glasshouse cabinet','potting bench','seed drawers','botanical console'],
'crew-cinema':['cinema screen','cinema seats','projection equipment','refreshment counter','cinema console'],
'crew-fitness':['treadmill','exercise bike','weight bench','weight rack','fitness console','orange yoga mat A','orange yoga mat B'],
'games-room':['game table','arcade cabinet','game console','game storage','games sofa','table tennis'],
'memorial-room':['memorial display','book of remembrance','memorial clock','flower pedestal','memorial sofa','logs console'],
'music-room':['piano','keyboard station','recording desk','speaker cabinet','instrument cabinet'],
'reading-room':['tall bookcase','reading chair','reading desk','low bookcase','reading console'],
'tea-lounge':['tea counter','tea sofa','tea table','tea cabinet','tea console'],
'battery-service-bay':['charging bank','battery inspection bench','battery locker','power unit','battery console'],
'droid-workshop':['droid nest','component bench','shell cabinet','charging perches','droid console'],
'drone-repair-depot':['repair cradle','repair bench','parts cabinet','battery station','repair console'],
'sensor-calibration-lab':['calibration turntable','calibration targets','optical bench','sensor cabinet','calibration console'],
'survey-probe-bay':['launcher study','spare survey probe','probe storage','survey workstation','survey control pedestal']}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def split(path):
 im=Image.open(path).convert('RGBA'); a=np.asarray(im)
 lab,n=ndimage.label(a[:,:,3]>100)
 sizes=np.bincount(lab.ravel()); ids=np.where(sizes>1500)[0];ids=ids[ids!=0]
 # Associate detached antialias/detail islands with closest substantial body,
 # preserving every original nontransparent pixel rather than thresholding edges.
 seeds=np.isin(lab,ids)
 _,ix=ndimage.distance_transform_edt(~seeds,return_indices=True)
 owner=lab[tuple(ix)]
 bodies=[]
 for k in ids:
  mask=(owner==k)&(a[:,:,3]>0)
  y,x=np.where(lab==k);box=(max(0,int(x.min())-3),max(0,int(y.min())-3),min(im.width,int(x.max()+4)),min(im.height,int(y.max()+4)))
  b=a[box[1]:box[3],box[0]:box[2]].copy()
  b[:,:,3][~mask[box[1]:box[3],box[0]:box[2]]]=0
  bodies.append((box,Image.fromarray(b)))
 # All current room sheets are two visual rows; sort by row then horizontal.
 bodies.sort(key=lambda b: (0 if (b[0][1]+b[0][3])/2<im.height*.52 else 1,b[0][0]))
 return bodies
records=[]
def export(path,dept,room,labels,scale=.6,replace=False):
 bodies=split(path)
 assert len(bodies)==len(labels),(path,len(bodies),labels)
 for i,((box,im),label) in enumerate(zip(bodies,labels),1):
  src=path;replacement=path.parent/'replacement-console.png'
  if replace and replacement.exists() and i==len(labels):
   src=replacement;im=Image.open(src).convert('RGBA');box=(0,0,*im.size)
  local_scale=scale
  ident='sp-new-'+room+'-'+str(i)
  master=OUT/'masters'/room/(ident+'.png');master.parent.mkdir(parents=True,exist_ok=True);im.save(master)
  size=tuple(max(1,round(v*local_scale)) for v in im.size)
  native=im.resize(size,Image.Resampling.LANCZOS)
  dest=OUT/'game-size'/room/(ident+'.png');dest.parent.mkdir(parents=True,exist_ok=True);native.save(dest)
  floor='yoga mat' in label
  records.append(dict(id=ident,label=room.replace('-',' ').title()+'  -  '+label,category=dept.lower().replace(' ','_'),room=room,source=str(src),source_sha256=digest(src),source_box=list(box),master=str(master.relative_to(ROOT)).replace('\\','/'),export=str(dest.relative_to(ROOT)).replace('\\','/'),export_sha256=digest(dest),native_size=size,scale=local_scale,display_width=round(size[0]*.34,3),floor_piece=floor,footprint=[0,.45,1,.55] if not floor else [0,0,0,0],collision_boxes=[[.04,.4,.92,.6]] if not floor else [],stage='exported',native_review='pending'))
OUT.mkdir(parents=True,exist_ok=True)
for f in sorted((SOURCE/'01-current-room-candidates').glob('*/*/room-sheet.png')):
 export(f,f.parent.parent.name,f.parent.name,LABELS[f.parent.name],replace=True)
export(SOURCE/'01-current-room-candidates/Recreation/botanical-conservatory/domed-centerpiece-v2.png','Recreation','botanical-dome',['domed conservatory'],.30)
export(SOURCE/'01-current-room-candidates/Recreation/crew-cinema/rear-seating-v3.png','Recreation','cinema-rear-seating',['rear cinema seats'],.19)
export(OUT/'cleaned-sheets/survey-extra.png','Robotics','survey-probe-additions',['probe rack','probe service bench','probe telemetry terminal','sensor parts cabinet','launch pressure unit'],.60)
export(OUT/'cleaned-sheets/operations-computers.png','Operations','operations-computers',['operations desk','operations pedestal','operations server bank'],.40)
export(OUT/'cleaned-sheets/anomaly-computers.png','Anomaly','anomaly-computers',['pressure garden terminal','fold chamber dual terminal','stillwater terminal'],.45)

(OUT/'manifest.json').write_text(json.dumps({'records':records,'scope':'Selected room concepts. Exported with source alpha preserved. Native review pending.','source_root':str(SOURCE)},indent=2),encoding='utf-8')
catalog=[]
for r in records:
 w,h=r['native_size']
 catalog.append(dict(id=r['id'],label=r['label'],category=r['category'],source='res://'+r['export'],region=[0,0,w,h],pieces=[[[0,0],[w,0],[w,h],[0,h]]],footprint=r['footprint'],collision_boxes=r['collision_boxes'],display_width=r['display_width'],wall_contact=[],default_rooms=[],floor_piece=r['floor_piece'],design=r['room'],role=''))
(OUT/'catalog.json').write_text(json.dumps(catalog,indent=2),encoding='utf-8')
for dept in sorted(set(r['category'] for r in records)):
 rows=[r for r in records if r['category']==dept]
 board=Image.new('RGB',(1500,((len(rows)+4)//5)*235),'#424950');d=ImageDraw.Draw(board)
 for i,r in enumerate(rows):
  im=Image.open(ROOT/r['export']);im.thumbnail((285,195))
  x=(i%5)*300;y=(i//5)*235
  board.paste(im,(x+(300-im.width)//2,y+25),im)
  d.text((x+5,y+5),r['label'].split('  -  ')[1],fill='white')
  d.text((x+5,y+218),r['id'].replace('sp-new-',''),fill='#b5c8d0')
 board.save(OUT/(dept+'-exports.jpg'))
print(json.dumps({'props':len(records),'rooms':len(LABELS),'output':str(OUT)}))

