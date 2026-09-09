"""Package preserved authored sheets; do not generate or mirror body art."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
DIRS=['east','south','west','north']
FAMILIES={'seating':['sit-down','sit-idle'],'dining':['eat','drink'],'sleeping':['lie-down','sleep'],'reading':['read-seated','inspect'],'distress':['swim-distress','recover-air'],'cargo-turn':['carry-turn','swim-carry-turn'],'death':['death-ground','death-water'],'water-pickup':['swim-pickup']}
LOOPS={'sit-idle','eat','drink','sleep','read-seated','inspect','swim-distress'}
REVERSE={'sit-down':'sit-rise','lie-down':'get-up'}
def groups(values,gap):
 out=[]
 for v in values:
  if not out or v-out[-1][-1]>gap:out.append([])
  out[-1].append(int(v))
 return out
def clean(path):
 a=np.array(Image.open(path).convert('RGBA'));r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
 a[(r>g*1.4)&(b>g*1.4)&(r>80)&(b>80)]=0
 return Image.fromarray(a)
def source_rows(path):
 im=clean(path);a=np.array(im)
 bands=[g for g in groups(np.flatnonzero((a[:,:,3]>128).sum(axis=1)>10),8) if len(g)>20]
 rows=[]
 for band in bands:
  xs=np.flatnonzero((a[band[0]:band[-1]+1,:,3]>128).sum(axis=0)>0)
  columns=groups(xs,2)
  if len(columns)!=6 and 'water-pickup' in path.name:
   occupied=(a[band[0]:band[-1]+1,:,3]>128).sum(axis=0)>0
   gaps=[g for g in groups(np.flatnonzero(~occupied),1) if len(g)>3]
   cuts=[0]+[int(np.mean(min(gaps,key=lambda g:abs(np.mean(g)-i*im.width/6)))) for i in range(1,6)]+[im.width]
   columns=[range(cuts[i],cuts[i+1]) for i in range(6)]
  assert len(columns)==6,(path,band[0],[(c[0],c[-1]) for c in columns])
  rows.append([im.crop((c[0],band[0],c[-1]+1,band[-1]+1)) for c in columns])
 return [[c.crop(c.getbbox()) for c in row] for row in rows]
def head(crop,facing,prone=False):
 a=np.array(crop);r,g,b,alpha=a.astype(float).transpose(2,0,1);h,w=r.shape;y,x=np.mgrid[:h,:w]
 window=y<h*.32
 if prone:
  window=(x>w*.6) if facing=='east' else (x<w*.4) if facing=='west' else (y>h*.55) if facing=='south' else (y<h*.45)
 mask=window&(alpha>128)&(r>g*1.1)&(g>b*1.15)&(r>65)
 yy,xx=np.where(mask)
 if len(xx)>3:return np.array([float(np.median(xx)),float(np.median(yy))])
 return np.array([w*.5,h*.16])
def write(actor,name,crops,scale,source,water=False,reverse=None,facings=None,prone=False):
 out=ROOT/actor/name;out.mkdir(parents=True,exist_ok=True)
 facing=name.split('-')[-1];pivot=[64,64] if water else [64,112]
 facings=facings or [facing]*6
 files=[];poses=[];frames=[]
 for i,crop in enumerate(crops):
  direction=facings[i]
  sleeping=name.startswith('sleep-')
  lying=sleeping or (name.startswith('lie-down-') and i>=3)
  head_direction=({'east':'west','west':'east','south':'north','north':'north'}[direction] if lying else direction)
  anchor=head(crop,head_direction,water or (prone and i>=3) or sleeping)
  size=(max(1,round(crop.width*scale)),max(1,round(crop.height*scale)))
  small=crop.resize(size,Image.Resampling.NEAREST)
  if water:
   target=np.array({'east':[80,54],'west':[48,54],'south':[64,76],'north':[64,48]}[direction])
   offset=np.round(target-anchor*scale).astype(int)
  else:
   bottom=np.array(crop)[int(crop.height*.9):,:,3];yy,xx=np.where(bottom>0)
   foot=(xx.min()+xx.max())*.5 if len(xx) else crop.width*.5
   offset=np.array([round(64-foot*scale),112-small.height])
  assert small.width<=124 and small.height<=124,(name,size)
  offset=np.maximum([2,2],np.minimum(offset,[126-small.width,126-small.height]))
  frame=Image.new('RGBA',(128,128));frame.alpha_composite(small,tuple(offset))
  file=f'frame_{i:03}.png';frame.save(out/file);files.append(file);frames.append(frame)
  angle=(-70 if direction=='east' else 70) if lying and direction in ['east','west'] else (16 if direction=='east' else -16) if water and direction in ['east','west'] else 0
  poses.append({'head':(offset+anchor*scale).round(2).tolist(),'offset':offset.tolist(),'facing':direction,'helmetAngle':angle})
 durations=[160]*len(files) if name.rsplit('-',1)[0] in LOOPS else [100,120,140,160,160,120][:len(files)]
 if name.startswith('recover-air-'):durations=[500]*len(files)
 if name.startswith('death-'):durations=[250,300,350,400,400,300]
 if name.startswith('swim-pickup-'):durations=[70,80,90,100,100,80]
 loop=name.rsplit('-',1)[0] in LOOPS
 entry={'id':name,'frameFiles':files,'frameDurationsMs':durations,'loop':loop,'water':water,'facings':facings}
 if name.startswith(('sit-idle-','read-seated-')):entry['depthOffsets']=[40]*len(files)
 if name.startswith('sit-down-'):entry['depthOffsets']=[0,8,16,24,32,40]
 if name.startswith('sleep-'):entry['depthOffsets']=[96]*len(files)
 if name.startswith('lie-down-'):entry['depthOffsets']=[0,19,38,58,77,96]
 states=[entry]
 if reverse:
  back=dict(entry,id=reverse,frameFiles=list(reversed(files)),frameDurationsMs=list(reversed(durations)),facings=list(reversed(facings)),derived='reverse of '+name)
  if 'depthOffsets' in entry:back['depthOffsets']=list(reversed(entry['depthOffsets']))
  states.append(back)
 manifest={'frameWidth':128,'frameHeight':128,'pivot':pivot,'states':states,'status':'packaged_review_candidate'}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 registration={'source':str(source.relative_to(ROOT)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'frames':poses}
 (out/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
 contact=Image.new('RGBA',(128*len(frames),128),(23,38,45,255))
 for i,f in enumerate(frames):contact.alpha_composite(f,(128*i,0))
 contact.save(out/'contact.png')
def build(actor,family):
 path=ROOT/'source'/f'{actor}-{family}.png'
 if not path.exists():return
 rows=source_rows(path);dirs=['south','west','north'] if family=='death' else DIRS
 expected=len(dirs)*len(FAMILIES[family])
 if family=='seating' and actor=='bill' and len(rows)==7:rows.insert(6,[])
 assert len(rows)==expected,(path,len(rows),expected)
 standing=max(c.height for row in rows[:len(dirs)] for c in row)
 if family in ['reading','distress']:standing=max(c.height for row in rows[4:] for c in row)
 if family=='cargo-turn':return cargo(actor,rows,path)
 if family=='sleeping':
  refinement=source_rows(ROOT/'source'/f'{actor}-refinement.png')
  for n,di in [(0,1),(1,3)]:
   write(actor,'sleep-'+DIRS[di],refinement[n],72/max(c.height for c in refinement[n]),ROOT/'source'/f'{actor}-refinement.png',prone=True)
  if actor in ['bill','branforth']:rows[4],rows[6]=rows[6],rows[4]
 for row,crops in enumerate(rows):
  if not crops:continue
  state=FAMILIES[family][row//len(dirs)];d=dirs[row%len(dirs)]
  if family=='seating' and actor=='veld' and row==6:continue # Incorrect east-facing source retained, not shipped.
  if family=='dining' and actor=='bill' and row==7:continue # Source feet clipped; dedicated replacement required.
  if family=='sleeping' and row in [5,7]:continue
  if family=='death' and actor=='veld' and row==4:continue
  water=state.startswith('swim-') or state=='death-water'
  scale=82/max(max(c.width,c.height) for c in crops) if water else 74/standing
  if family=='reading' and row<4:
   seat=Image.open(ROOT/actor/('sit-idle-'+d)/'frame_000.png')
   scale=(seat.getbbox()[3]-seat.getbbox()[1])/max(c.height for c in crops)
  name=state+'-'+d;facings=None;reverse=REVERSE.get(state)
  if family=='cargo-turn':
   to=DIRS[(row%4+1)%4];name=state+'-'+d+'-'+to;facings=[d]*3+[to]*3;reverse=state+'-'+to+'-'+d
  elif reverse:reverse+='-'+d
  write(actor,name,crops,scale,path,water,reverse,facings,family in ['sleeping','death'])
 print(actor,family,'packaged')

def cargo(actor,rows,path):
 for ri in [0,1,3,4,5,7]:
  crops=rows[ri];indices=list(range(6));water=ri>=4
  if actor=='bill':indices={0:[0,1,2,3,3,5],1:[0,1,2,2,2,5],4:[0,1,2,3,3,3],5:[0,1,2,2,2,2]}.get(ri,indices)
  if actor=='branforth' and ri==1:indices=[0,1,2,3,3,5]
  selected_path=path
  if actor=='branforth' and ri==3:crops=rows[2];indices=[4,3,2,1,0,0]
  if actor=='bill' and ri==7:selected_path=ROOT/'source'/'bill-corrections.png';crops=source_rows(selected_path)[3]
  crops=[crops[i] for i in indices]
  d=DIRS[ri%4];to=DIRS[(ri%4+1)%4];state='swim-carry-turn' if water else 'carry-turn'
  scale=(82/max(max(c.width,c.height) for c in crops)) if water else 74/max(c.height for c in rows[ri])
  write(actor,state+'-'+d+'-'+to,crops,scale,selected_path,water,state+'-'+to+'-'+d,[d]*2+[to]*4)
 # Dedicated north-to-west fixes replace incorrect east-facing source rows.
 for water in [False,True]:
  p=ROOT/'source'/f'{actor}-refinement.png';idx=3 if water else 2
  if not water and actor=='bill':p=ROOT/'source'/'bill-final-fix.png';idx=0
  if not water and actor=='veld':p=ROOT/'source'/'veld-corrections.png';idx=2
  crops=source_rows(p)[idx];state='swim-carry-turn' if water else 'carry-turn'
  scale=(82/max(max(c.width,c.height) for c in crops)) if water else 74/max(c.height for c in crops)
  write(actor,state+'-north-west',crops,scale,p,water,state+'-west-north',['north']*2+['west']*4)

def corrections(actor):
 if actor=='branforth':return
 p=ROOT/'source'/f'{actor}-corrections.png';rows=source_rows(p)
 crops=rows[0];seat_source=p
 if actor=='veld':seat_source=ROOT/'source'/'veld-final-fix.png';crops=source_rows(seat_source)[0]
 # Match the authored seated endpoint rather than normalizing to standing height.
 endpoint=Image.open(ROOT/actor/'sit-down-west'/'frame_005.png').getbbox()
 write(actor,'sit-idle-west',crops,(endpoint[3]-endpoint[1])/max(c.height for c in crops),seat_source)
 if actor=='bill':write(actor,'drink-north',rows[1],74/max(c.height for c in rows[1]),p)
 else:write(actor,'death-water-west',rows[1],82/max(max(c.width,c.height) for c in rows[1]),p,True,prone=True)
if __name__=='__main__':
 for a in ['bill','veld','branforth']:
  for f in sys.argv[1:] or FAMILIES:
   if f=='reading':corrections(a)
   build(a,f)
