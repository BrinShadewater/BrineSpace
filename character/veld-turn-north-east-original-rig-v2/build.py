from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];G=R/'character/veld-gather-north-original-master-v1';M=R/'character/veld-turn-north-east-original-rig-v1';E=R/'character/veld-east-held-original-master-v1';H=R/'character/veld-helmet-original-turntable-v1/v3-study/shells';C=R/'character/veld-north-gather-turn-chain-v1'
refs={'bare':[],'helmet':[]};bindings={};fits=[];checks=0;board=Image.new('RGB',(1536,590),'#202a30');d=ImageDraw.Draw(board)
def bind(path):bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
for phase in range(6):
 if phase in (0,2,5):
  folder={0:G/'gather-frames',2:M/'frames',5:E/'frames'}[phase];pair={g:Image.open(folder/g/'000.png').convert('RGBA') for g in refs};files={g:'res://'+(folder/g/'000.png').relative_to(R).as_posix() for g in refs};fit={'phase':phase,'exactReviewedAliases':files}
 else:
  path={1:P/'early-candidate-v2.png',3:P/'near-candidate.png',4:P/'late-candidate-v2.png'}[phase];bare=Image.open(path).convert('RGBA');a=np.array(bare);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1]
  shellpath={1:H/'001.png',3:R/'character/veld-turn-north-east-helmet-aligned-v3/matched-skin-hair-shell.png',4:H/'005.png'}[phase];shell=Image.open(shellpath).convert('RGBA');_,sx=np.where(np.array(shell)[-4:,:,3]>160);pos=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),104-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,103);helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
  protected=np.ones((256,256),bool);protected[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(pos[0],clear[0]):max(pos[0]+shell.width,clear[2])]=False;assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1;pair={'bare':bare,'helmet':helmet};files={};bind(path);bind(shellpath)
  for gear,im in pair.items():
   dest=P/f'frames/{gear}/{phase:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);files[gear]='res://'+dest.relative_to(R).as_posix()
  fit={'phase':phase,'wholeBodySource':path.relative_to(R).as_posix(),'wholeShell':shellpath.relative_to(R).as_posix(),'shellSize':list(shell.size),'shellPosition':pos,'protectedBodyExact':True}
 fits.append(fit)
 for row,(gear,im) in enumerate(pair.items()):
  refs[gear].append(files[gear]);bind(R/files[gear][6:]);z=np.array(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1;board.paste(im,(phase*256,row*285+22),im);d.text((phase*256+4,row*285+4),gear+' phase'+str(phase),fill='white')
for gear in refs:
 m=json.loads((C/f'{gear}-manifest.json').read_text());m.update(name='Veld original-rig North-East turn chain '+gear,status='staged_not_installed')
 for s in m['states']:
  if s['id']=='carry-turn-north-east':s['frameFiles']=refs[gear]
  if s['id']=='carry-turn-east-north':s['frameFiles']=list(reversed(refs[gear]))
  s['frameCount']=len(s['frameFiles']);assert len(s['frameDurationsMs'])==s['frameCount'];checks+=1
  for ref in s['frameFiles']:bind(R/ref[6:])
 east=json.loads((E/f'{gear}-manifest.json').read_text())['states'][0];m['states'].append(copy.deepcopy(east));assert m['states'][0]['frameFiles'][-1]==east['frameFiles'][0];checks+=1
 states={s['id']:s for s in m['states']}
 for a,b in [('carry-gather-north','carry-turn-north-east'),('carry-turn-north-east','carry-turn-east-north'),('carry-turn-east-north','carry-spread-north')]:assert states[a]['frameFiles'][-1]==states[b]['frameFiles'][0];checks+=1
 (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
for path in list(P.glob('raw-*.png'))+list(P.glob('*source-audit*.json'))+[M/'registration.json',E/'registration.json']:bind(path)
board.save(P/'paired-turn-source.png');(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'bindings':bindings,'fits':fits,'durationMs':800,'scope':'Whole original-rig turn interiors with exact rear/mid/East aliases; gather/spread source aliases and finite clocks preserved. Existing complete angular helmets fitted with body protection; temporal artistic review/world integration incomplete.'},indent=2)+'\n',encoding='utf-8');print(checks,'whole-source/gear/endpoint/count/timing/clipping checks0failures')
