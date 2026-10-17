from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];source=json.loads((P/'source-registration-v2.json').read_text(encoding='utf-8'));shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA');_,sx=np.where(np.array(shell)[-4:,:,3]>160);refs={g:[] for g in ['bare','helmet']};fits=[];checks=0
board=Image.new('RGB',(1792,600),'#202a30');d=ImageDraw.Draw(board)
for i,row in enumerate(source['rows']):
 assert row['height']==148 and row['headRegionWidth']==27 and row['floor']==223;checks+=1
 bare=Image.open(P/f'diagnostic-frames-v2/{i:03}.png').convert('RGBA');a=np.array(bare);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];pos=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),top+28-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,top+27)
 helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos);protected=np.ones((256,256),bool);protected[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(pos[0],clear[0]):max(clear[2],pos[0]+shell.width)]=False;assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1;fits.append({'pose':i,'position':list(pos),'bodyOutsideHeadFittingExact':True})
 for row,(gear,im) in enumerate([('bare',bare),('helmet',helmet)]):
  path=P/f'key-frames/{gear}/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);refs[gear].append('res://'+path.relative_to(R).as_posix());z=np.array(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1;board.paste(im,(i*256,row*290+25),im);d.text((i*256+3,row*290+3),f'{gear} gait key{i}',fill='white')
for row,gear in enumerate(refs):
 old=json.loads((R/f'character/veld-east-held-original-master-v1/{gear}-manifest.json').read_text(encoding='utf-8'));template=old['states'][0];states=[]
 for name,files,durations in [('carry-east',refs[gear],[140]*6),('carry-held-east',[f'res://character/veld-east-held-original-master-v1/frames/{gear}/000.png'],[1000]),('idle-east',[f'res://character/veld-cargo-east-original-master-v3/frames/{gear}/005.png'],[1000])]:
  state=copy.deepcopy(template);state.update(id=name,frameCount=len(files),frameFiles=files,frameDurationsMs=durations,loop=True)
  for key,value in [('facings','east'),('waterKinds','carry' if name.startswith('carry') else 'idle'),('waterPoses',False),('depthOffsets',0.0)]:state[key]=[value]*len(files)
  states.append(state)
 old.update(name='Veld original East gait KEY SOURCE review '+gear,status='staged_source_keys_only',states=states,strideDistanceCells={});(P/f'{gear}-key-manifest.json').write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8');master=Image.open(R/f'character/veld-east-held-original-master-v1/frames/{gear}/000.png').convert('RGBA');board.paste(master,(1536,row*290+25),master);d.text((1540,row*290+3),gear+' exact held master',fill='white')
board.save(P/'paired-keys-master-review.png')
paths=[P/'raw-gait-v1.png',P/'raw-gait-v2.png',P/'prompt-gait-v1.txt',P/'prompt-gait-v2.txt',P/'register_source.py',P/'build_keys.py',P/'source-registration-v1.json',P/'source-registration-v2.json',shellpath,R/'character/veld-cargo-turns-master-family-v1/original-east-density-reference.png'];paths+=list((P/'diagnostic-frames-v2').glob('*.png'))+list((P/'key-frames').rglob('*.png'))+list(P.glob('*-key-manifest.json'))
for gear in refs:paths+=[R/f'character/veld-east-held-original-master-v1/frames/{gear}/000.png',R/f'character/veld-cargo-east-original-master-v3/frames/{gear}/005.png']
report={'checks':checks,'failures':0,'sourceGeneration':'1310316f-87b9-4f29-8b5f-42ca0790e7c0','sourceScale':source['sourceScale'],'headWidths':source['headWidths'],'heights':source['heights'],'floorSpan':source['floorSpan'],'helmetFits':fits,'bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'scope':'Six original-only gait KEY SOURCES and original held/idle references in paired gear. No stride calibration, start/stop, completed traveling gait or ordinary runtime admission. Continuous video trial pending.'};(P/'key-registration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='bindings'}))
