"""Fit native selected shared helmets; preserve authored seated bodies."""
from pathlib import Path
import copy,json,hashlib,os
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def crown(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>180);top=int(y.min());yy=np.indices(a.shape[:2])[0];y,x=np.where((a[:,:,3]>180)&(yy<=top+4));return np.array([x.mean(),top])
def rgba(path,canvas=(184,192)):
 im=Image.open(path).convert('RGBA');out=Image.new('RGBA',canvas);out.alpha_composite(im);return out
pack=json.loads((HERE/'bare-manifest.json').read_text());eq=copy.deepcopy(pack);eq['name']='James seated family shared helmets';records={};hashes={}
inspect_folder=ROOT/'character/james-inspect-tablet-v1';inspect=json.loads((inspect_folder/'helmet-manifest.json').read_text())
bare_master_folder=ROOT/'character/crew-runtime-matte-v1/branforth';bm=json.loads((bare_master_folder/'manifest.json').read_text())
for state in eq['states']:
 d=state['id'].rsplit('-',1)[1];folder=ROOT/'character'/('james-seated-'+d+'-v1');master=rgba(folder/'selected-helmet-master.png');bs=next(s for s in bm['states'] if s['id']=='idle-'+d);bare_master=rgba(bare_master_folder/bs['frameFiles'][0]);mc=crown(bare_master)
 files=[];tracking=[]
 for i,f in enumerate(state['frameFiles']):
  body=rgba(HERE/f);bc=crown(body);donor=master;donor_crown=mc;donor_path=str(folder/'selected-helmet-master.png')
  # Accepted inward-looking diagnostics supply pitched head poses for tablet reading.
  if state['id'].startswith('read-seated') and i in [1,2,3,4]:
   ds=next(s for s in inspect['states'] if s['id']=='inspect-'+d);idx=int(len(ds['frameFiles'])*{1:.18,2:.4,3:.6,4:.8}[i]);donor_path=str(inspect_folder/ds['frameFiles'][idx]);donor=rgba(donor_path)
   # Equipped crowns differ from bare by a fixed directional shell extension.
   donor_crown=crown(donor)-(crown(master)-mc)
  at=np.rint(bc-donor_crown).astype(int);cut=round(bc[1]+29);patch=np.array(donor);yy,xx=np.indices(patch.shape[:2]);patch[(yy>=donor_crown[1]+29)|(abs(xx-donor_crown[0])>23)]=0
  overlay=Image.new('RGBA',(184,192));overlay.alpha_composite(Image.fromarray(patch),tuple(at));oa=np.array(overlay);oa[cut:]=0
  base=np.array(body);yy,xx=np.indices(base.shape[:2]);erase=(yy<bc[1]+24)&(abs(xx-bc[0])<18);base[erase]=0;out=Image.fromarray(base);out.alpha_composite(Image.fromarray(oa));a=np.array(out);a[cut:]=np.array(body)[cut:];out=Image.fromarray(a)
  endpoint=state['id'].startswith('sit-down') and i==0
  if endpoint:out=master.copy()
  dest=folder/'frames/helmet'/state['id']/f'{i:03d}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);files.append(Path(os.path.relpath(dest,HERE)).as_posix());hashes[files[-1]]=hashlib.sha256(dest.read_bytes()).hexdigest();tracking.append(dict(donor=donor_path,translation=at.tolist(),nativeScale=1,headCutoff=cut,bodyCrown=bc.tolist(),exactStandingMaster=endpoint))
 state['frameFiles']=files;state['provenance']['helmet']='Native selected idle shell; accepted pitched diagnostic donors for seated reading, body below headCutoff exact';records[state['id']]=tracking
# Exact shared arrivals, breathing endpoints and reversed rise also apply to equipment.
for d in ['east','south','west','north']:
 states={s['id']:s for s in eq['states']};down=states['sit-down-'+d];up=states['sit-rise-'+d]
 for action in ['sit-idle','read-seated']:
  row=states[action+'-'+d]
  for i in [0,5]:rgba(HERE/down['frameFiles'][-1]).save(HERE/row['frameFiles'][i]);records[row['id']][i]=copy.deepcopy(records[down['id']][-1])
 for i,f in enumerate(up['frameFiles']):rgba(HERE/down['frameFiles'][5-i]).save(HERE/f);records[up['id']][i]=copy.deepcopy(records[down['id']][5-i])
 for s in [states[a+'-'+d] for a in ['sit-down','sit-idle','read-seated','sit-rise']]:
  for f in s['frameFiles']:hashes[f]=hashlib.sha256((HERE/f).read_bytes()).hexdigest()
 boards=[];times=[];contact=Image.new('RGB',(1536,1280),'#303b40');draw=ImageDraw.Draw(contact)
 for row,action in enumerate(['sit-down','sit-idle','read-seated','sit-rise']):
  s=states[action+'-'+d]
  for i,f in enumerate(s['frameFiles']):
   im=rgba(HERE/f);full=Image.new('RGBA',(256,256));full.alpha_composite(im,(36,52));contact.paste(full,(i*256,55+row*320),full);draw.text((i*256+8,row*320+8),action+' '+d+' '+str(i),fill='white')
   b=Image.new('RGB',(900,330),'#303b40');dd=ImageDraw.Draw(b);dd.text((8,8),'James seated / '+action+' '+d+' / bare / helmet / 82px / 54px / 27px',fill='white');bare=rgba(HERE/next(st for st in pack['states'] if st['id']==s['id'])['frameFiles'][i]);b.paste(bare,(35,122),bare);b.paste(im,(260,122),im)
   for h,x in [(82,510),(54,690),(27,810)]:sc=h/148;small=full.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);b.paste(small,(x,294-round(224*sc)),small)
   boards.append(b);times.append(s['frameDurationsMs'][i])
 contact.save(ROOT/'character'/('james-seated-'+d+'-v1')/'helmet-contact.png');boards[0].save(ROOT/'character'/('james-seated-'+d+'-v1')/'paired-review.gif',save_all=True,append_images=boards[1:],duration=times,loop=0)
(HERE/'helmet-manifest.json').write_text(json.dumps(eq,indent=2)+'\n');(HERE/'helmet-registration.json').write_text(json.dumps(records,indent=2)+'\n');(HERE/'helmet-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');print('96 equipped references; native selected head scale; bodies preserved below head cutoff')
