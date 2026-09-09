from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
from collections import deque
ROOT=Path(__file__).resolve().parent
DIRS=['south','north','east','west']
frames={}; entries=[]; source_records=[]
for name in ['walk','work','swim','death']:
 src=ROOT/'generated'/f'{name}.png'
 im=Image.open(src).convert('RGBA'); w,h=im.size
 source_records.append({'path':str(src.relative_to(ROOT)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
 for row,d in enumerate(DIRS):
  tiles=[]
  for col in range(6):
   tile=im.crop((round(col*w/6),round(row*h/4),round((col+1)*w/6),round((row+1)*h/4)))
   a=np.array(tile);rgb=a[:,:,:3].astype(int)
   key=(rgb[:,:,0]>rgb[:,:,1]+50)&(rgb[:,:,2]>rgb[:,:,1]+50)&(rgb[:,:,0]>120)
   a[key]=0
   # Discard tiny detached pixels from neighboring rows and generated specks.
   mask=a[:,:,3]>0; seen=np.zeros(mask.shape,bool)
   for yy,xx in zip(*np.where(mask)):
    if seen[yy,xx]:continue
    q=[(int(yy),int(xx))];seen[yy,xx]=True;component=[]
    while q:
     y0,x0=q.pop();component.append((y0,x0))
     for yn,xn in [(y0-1,x0),(y0+1,x0),(y0,x0-1),(y0,x0+1)]:
      if 0<=yn<mask.shape[0] and 0<=xn<mask.shape[1] and mask[yn,xn] and not seen[yn,xn]:seen[yn,xn]=True;q.append((yn,xn))
    if len(component)<30:
     for y0,x0 in component:a[y0,x0]=0
   tile=Image.fromarray(a);box=tile.getbbox()
   assert box, (name,row,col)
   tiles.append((tile,box))
  baseline=max(b[3] for _,b in tiles)
  top=min(b[1] for _,b in tiles)
  scale=74/(baseline-top)
  for col,(tile,box) in enumerate(tiles):
   body=tile.crop(box).resize((round((box[2]-box[0])*scale),round((box[3]-box[1])*scale)),Image.Resampling.BOX)
   body.putalpha(body.getchannel('A').point(lambda a:255 if a>=128 else 0))
   # Register around body center, preserving row baseline and reduced collapse height.
   x=46-body.width//2;y=86-round((baseline-box[1])*scale)
   assert min(x,y)>=0 and x+body.width<=92 and y+body.height<=92,(name,d,col,x,y,body.size)
   out=Image.new('RGBA',(92,92));out.alpha_composite(body,(x,y))
   rel=f'frames/{name}-{d}/frame_{col:03}.png';dest=ROOT/rel;dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest)
   frames[name,d,col]=rel
def add(state,source,indices,loop=True,ms=150):
 for d in DIRS:
  entries.append({'id':state+'-'+d,'frameFiles':['../'+frames[source,d,i] for i in indices],'frameDurationsMs':[ms]*len(indices),'loop':loop,'water':state.startswith(('swim','tread','death-water'))})
add('idle','death',[0],True,1000)
add('walk','walk',range(6));add('run','walk',range(6),True,100)
for state in ['weld','repair','interact','inspect','salvage','swim-pickup','unload']:add(state,'work',range(6))
for state in ['swim','tread','swim-distress']:add(state,'swim',range(6),True,180)
for state in ['death-ground','death-water']:add(state,'death',range(6),False,180)
add('kneel','death',[0,1,2],False,200);add('stand','death',[2,1,0],False,200)
# Deliberate shared poses for the first playable pack, not separately authored clips.
for state in ['sit-down','lie-down']:add(state,'death',[0,1,2,3],False,200)
for state in ['sit-rise','get-up']:add(state,'death',[3,2,1,0],False,200)
for state in ['sit-idle','read-seated']:add(state,'death',[3],True,1000)
add('sleep','death',[5],True,1000)
for state in ['eat','drink','pickup','recover-air','carry','cargo-unload','equip-helmet','remove-helmet','torch-draw','torch-stow']:add(state,'work',range(6),state not in ['pickup','cargo-unload','equip-helmet','remove-helmet','torch-draw','torch-stow'])
add('swim-carry','swim',range(6),True,180)
dest=ROOT/'final';dest.mkdir(exist_ok=True)
(dest/'manifest.json').write_text(json.dumps({'name':'Marsh','frameSize':[92,92],'pivot':[46,86],'strideDistanceCells':{'walk':.12,'run':.16},'states':entries},indent=2))
equipped={}
for (source,d,col),rel in frames.items():
 body=Image.open(ROOT/rel).convert('RGBA'); a=np.array(body); rgb=a[:,:,:3].astype(float)
 hair=(a[:,:,3]>0)&(rgb[:,:,0]>rgb[:,:,1]*1.06)&(rgb[:,:,1]>rgb[:,:,2]*1.15)&(rgb[:,:,0]>80)&(rgb[:,:,1]>60)
 ys,xs=np.where(hair)
 assert len(xs),(source,d,col)
 top=int(ys.min()); select=ys<top+12
 cx=int(round(float(np.median(xs[select]))));cy=top+8
 overlay=Image.open(ROOT.parents[1]/'character/crew-underwater-v1/equipment'/('front' if d=='south' else d)/'overlay.png').convert('RGBA').resize((19,22),Image.Resampling.NEAREST)
 body.alpha_composite(overlay,(cx-9,cy-10))
 target='helmet/'+rel;out=ROOT/target;out.parent.mkdir(parents=True,exist_ok=True);body.save(out);equipped[rel]=target
equipment_entries=[]
for entry in entries:
 row=dict(entry);row['frameFiles']=['../'+equipped[p[3:]] for p in entry['frameFiles']];equipment_entries.append(row)
(dest/'helmet-manifest.json').write_text(json.dumps({'frameSize':[92,92],'pivot':[46,86],'states':equipment_entries},indent=2))
clearance={}
for mode in ['bare','helmet']:
 clearance[mode]={}
 for d in DIRS:
  boxes=[]
  for (source,facing,col),rel in frames.items():
   if facing!=d:continue
   box=Image.open(ROOT/(equipped[rel] if mode=='helmet' else rel)).getbbox()
   boxes.append([(box[0]-46)*.8821621622,(box[1]-86)*.8821621622,(box[2]-46)*.8821621622,(box[3]-86)*.8821621622])
  clearance[mode][d]=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
(ROOT/'clearance.json').write_text(json.dumps(clearance,indent=2))
(ROOT/'provenance.json').write_text(json.dumps({'tool':'image_gen.imagegen','sources':source_records,'uniqueFrames':len(frames),'sharedPoses':'Idle from standing collapse frame; kneel/rest/stand from collapse poses; secondary activities share tool-work; swimming and treading share upright swim cycle.','runtimeStates':len(entries)},indent=2))
preview=Image.new('RGBA',(92*6,92*4),(20,35,40,255))
for row,d in enumerate(DIRS):
 for col in range(6):preview.alpha_composite(Image.open(ROOT/frames['walk',d,col]),(col*92,row*92))
preview.resize((1104,736),Image.Resampling.NEAREST).save(ROOT/'walk-review.png')
motion=[]
for col in range(6):
 canvas=Image.new('RGBA',(92*4,92),(20,35,40,255))
 for row,d in enumerate(DIRS):canvas.alpha_composite(Image.open(ROOT/frames['walk',d,col]),(row*92,0))
 motion.append(canvas.resize((736,184),Image.Resampling.NEAREST).convert('RGB'))
motion[0].save(ROOT/'walk-review.gif',save_all=True,append_images=motion[1:],duration=150,loop=0)
print(f'Marsh pack: {len(frames)} frames; {len(entries)} state/direction entries')
cryo=Image.open(ROOT/'generated/cryo.png').convert('RGBA')
a=np.array(cryo);rgb=a[:,:,:3].astype(int)
background=(rgb.min(axis=2)>155)&((rgb.max(axis=2)-rgb.min(axis=2))<25)
visited=np.zeros(background.shape,bool);q=deque([(0,0)])
while q:
 y,x=q.popleft()
 if not (0<=y<a.shape[0] and 0<=x<a.shape[1]) or visited[y,x] or not background[y,x]:continue
 visited[y,x]=True;a[y,x]=0
 q.extend([(y-1,x),(y+1,x),(y,x-1),(y,x+1)])
cryo=Image.fromarray(a).resize((418,627),Image.Resampling.LANCZOS)
cryo.save(ROOT/'cryo.png')
