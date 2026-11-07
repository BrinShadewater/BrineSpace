"""Deterministic packaging of generated action sheets; original sources preserved."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
DIRECTIONS=['east','south','west','north']
WATER={'salvage','swim-start','swim-turn','swim-carry','swim-turn-north'}
NAMES={'torch':'torch-draw','carry':'carry','unload':'unload','salvage':'salvage','swim-start':'swim-start','swim-turn':'swim-turn','swim-carry':'swim-carry','interact':'interact','kneel':'kneel','repair':'repair'}
def clean(path):
 a=np.array(Image.open(path).convert('RGBA'));c=a[:,:,:3].astype(float)
 a[(c[:,:,1]>c[:,:,0]*1.5)&(c[:,:,1]>c[:,:,2]*1.5)&(c[:,:,1]>100)]=0
 a[(c[:,:,0]>c[:,:,1]*1.4)&(c[:,:,2]>c[:,:,1]*1.4)&(c[:,:,0]>80)&(c[:,:,2]>80)]=0
 return Image.fromarray(a)
def head(crop,d,water):
 a=np.array(crop);h,w=a.shape[:2];r,g,b,alpha=a.transpose(2,0,1).astype(float);y,x=np.mgrid[:h,:w]
 if not water: window=y<h*.25
 elif d=='east':window=(x>w*.58)&(x<w*.90)&(y<h*.58)
 elif d=='west':window=(x>w*.10)&(x<w*.42)&(y<h*.58)
 else:return np.array([w*.5,h*(.62 if d=='south' else .26)])
 mask=window&(alpha>128)&(r>g*1.13)&(g>b*1.12)&(r>65)
 yy,xx=np.where(mask)
 return np.array([float(np.median(xx)),float(np.median(yy))]) if len(xx)>4 else np.array([w*.5,h*.12])
def build(actor,family):
 sourcefamily='ground-cargo' if family in ['carry','unload'] else 'directional-work-v2' if family in ['interact','kneel','repair'] else family
 source=ROOT/'source'/f'{actor}-{sourcefamily}.png'
 if not source.exists():return []
 im=clean(source);water=family in WATER
 dirs=DIRECTIONS if family not in ['interact','kneel','repair'] else ['south','west','north']
 if family=='swim-turn-north':dirs=['east','west']
 states=[]
 a=np.array(im);ys=np.flatnonzero((a[:,:,3]>128).sum(axis=1)>12);groups=[]
 for y in ys:
  if not groups or y-groups[-1][-1]>8:groups.append([])
  groups[-1].append(int(y))
 groups=[g for g in groups if len(g)>25]
 expected=8 if sourcefamily=='ground-cargo' else 9 if sourcefamily=='directional-work-v2' else len(dirs)
 assert len(groups)==expected,(source,[(g[0],g[-1]) for g in groups])
 allgroups=groups
 if family=='carry':groups=groups[:4]
 elif family=='unload':groups=groups[4:]
 elif family in ['interact','kneel','repair']:
  first=['interact','kneel','repair'].index(family)*3;groups=groups[first:first+3]
 for row,d in enumerate(dirs):
  if family=='swim-turn' and row>1:continue # Rejected north joins replaced by dedicated source.
  crops=[];anchors=[]
  band=np.array(im)[groups[row][0]:groups[row][-1]+1,:,3]
  xs=np.flatnonzero((band>128).sum(axis=0)>0);columns=[]
  for x in xs:
   if not columns or x-columns[-1][-1]>2:columns.append([])
   columns[-1].append(int(x))
  assert len(columns)==6,(actor,family,row,[(c[0],c[-1]) for c in columns])
  for col in range(6):
   # One malformed empty-handed pose omitted; hold the correctly grounded end.
   index=5 if actor=='bill' and family=='unload' and col==4 else col
   cell=im.crop((columns[index][0],groups[row][0],columns[index][-1]+1,groups[row][-1]+1))
   bbox=cell.getbbox();assert bbox,(actor,family,row,col)
   crop=cell.crop(bbox);crops.append(crop)
   hd=d
   if family=='swim-turn':hd=(['east','south'][row] if col<3 else ['south','west'][row])
   if family=='swim-turn-north':hd='north' if col<3 else d
   anchors.append(head(crop,hd,water))
  size=(128,128);pivot=[64,64] if water else [64,112]
  scale=min(90/max(c.width for c in crops),90/max(c.height for c in crops)) if water else 74/max(c.height for c in crops)
  if family=='repair':
   g=allgroups[3+row];scale=74/(g[-1]-g[0]+1)
  name=(('swim-turn-'+['east','south'][row]+'-'+['south','west'][row]) if family=='swim-turn' else ('swim-turn-north-'+d) if family=='swim-turn-north' else NAMES[family]+'-'+d);out=ROOT/actor/name;out.mkdir(parents=True,exist_ok=True)
  registration={'source':str(source.relative_to(ROOT)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'frames':[]}
  previews=[];files=[]
  for i,(crop,anchor) in enumerate(zip(crops,anchors)):
   if water:
    target=np.array({'east':[80,54],'west':[48,54],'south':[64,76],'north':[64,48]}[d])
    if family=='swim-start': target=np.array([64,48])*(1-i/5)+target*(i/5)
    if family in ['swim-turn','swim-turn-north']:
     origin='north' if family=='swim-turn-north' else ['east','south'][row]
     dest=d if family=='swim-turn-north' else ['south','west'][row]
     targets={'east':[80,54],'west':[48,54],'south':[64,76],'north':[64,48]}
     target=np.array(targets[origin])*(1-i/5)+np.array(targets[dest])*(i/5)
    offset=np.round(target-anchor*scale).astype(int)
   else:
    a=np.array(crop);yy,xx=np.where(a[int(crop.height*.9):,:,3]>0)
    if family=='unload' and i>=3 and d in ['east','west']:
     xx=xx[xx<crop.width*.5] if d=='east' else xx[xx>crop.width*.5]
    footx=(xx.min()+xx.max())/2 if len(xx) else crop.width/2
    offset=np.array([round(64-footx*scale),round(112-crop.height*scale)])
   frame=Image.new('RGBA',size);small=crop.resize((max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),Image.Resampling.NEAREST)
   offset=np.maximum([0,0],np.minimum(offset,[128-small.width,128-small.height]))
   frame.alpha_composite(small,tuple(offset));file=f'frame_{i:03}.png';frame.save(out/file);files.append(file)
   hp=np.array(offset)+anchor*scale
   facing=d
   if family=='swim-turn':facing=['east','south'][row] if i<3 else ['south','west'][row]
   if family=='swim-turn-north':facing='north' if i<3 else d
   registration['frames'].append({'head':hp.round(2).tolist(),'offset':offset.tolist(),'facing':facing})
   previews.append(frame)
  loop=family in ['salvage','carry','swim-carry','interact','repair']
  durations=[140]*6 if loop else [70,90,100,100,90,70]
  entry={'id':name,'frameFiles':files,'frameDurationsMs':durations,'loop':loop,'water':water,'facings':[f['facing'] for f in registration['frames']]}
  manifest={'frameWidth':128,'frameHeight':128,'pivot':pivot,'states':[entry],'status':'integrated_owner_review_pending'}
  if family in ['carry','swim-carry']:manifest['strideDistanceCells']={NAMES[family]:.12 if family=='carry' else .16}
  (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(out/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
  sheet=Image.new('RGBA',(768,128),(25,34,37,255))
  for i,frame in enumerate(previews):sheet.alpha_composite(frame,(i*128,0))
  sheet.save(out/'contact.png');states.append(str(out/'manifest.json'))
  reverse=None
  if family=='torch':reverse='torch-stow-'+d
  elif family=='kneel':reverse='stand-'+d
  elif family=='swim-start':reverse='swim-stop-'+d
  elif family in ['swim-turn','swim-turn-north']:
   parts=name.split('-');reverse='swim-turn-'+parts[-1]+'-'+parts[-2]
  if reverse:
   reverseentry=dict(entry,id=reverse,frameFiles=list(reversed(files)),frameDurationsMs=list(reversed(durations)),facings=list(reversed(entry['facings'])),derived='reverse of '+name)
   manifest['states'].append(reverseentry)
   (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(actor,family,len(states)*6,'frames')
 return states
if __name__=='__main__':
 for actor in ['bill','veld','branforth']:
  for family in sys.argv[1:] or list(NAMES)+['swim-turn-north']:build(actor,family)

