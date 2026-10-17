from pathlib import Path
from PIL import Image
import json,copy,hashlib,numpy as np
from scipy.ndimage import binary_dilation,label
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=R/'character/krusher-james-canonical-v4';records=[];cache={};checks=0;yy,xx=np.indices((184,184))
fitroot=R/'character/krusher-james-motion-fit-v2';helmroot=R/'character/krusher-james-helmet-fit-v2'
fits={(q['state'],q['frame']):q for q in json.load(open(fitroot/'verification.json'))['records']};helms={(q['state'],q['frame']):q for q in json.load(open(helmroot/'verification.json'))['records']}
tablets={};heads={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for g in ['bare','helmet']:
 for d in (['east','west'] if g=='bare' else ['east','west','south']):
  folder=R/'character'/('krusher-tablet-'+d+('-helmet' if g=='helmet' else '')+'-v1');tablets[(g,d)]=(folder,json.load(open(folder/'verification.json'))['records'])
for g in ['bare','helmet']:
 m=json.load(open(OLD/(g+'-manifest.json')))
 for state in m['states']:
  key=state['id'];d=key.rsplit('-',1)[1];files=[]
  for i,rel in enumerate(state['frameFiles']):
   src=OLD/rel;a=np.array(Image.open(src).convert('RGBA'));raw=hashlib.sha256(a.tobytes()).hexdigest();ck=(g,d,raw)
   if ck in cache:
    files.append(cache[ck]);records.append({'gear':g,'state':key,'index':i,'source':src.relative_to(R).as_posix(),'sourceHash':sha(src),'output':cache[ck],'alias':True});continue
   out=a.copy();mask=np.zeros((184,184),bool);details={};body_row=0
   if g=='bare' and d in ['east','west']:
    if key.startswith('interact-'):
     folder,rows=tablets[(g,d)];q=rows[i];mask=np.array(Image.open(folder/q['mask']))>0;mark=np.array(Image.open(folder/q['markingMask']))>0;mask&=~mark
     if 'tabletMask' in q:mask&=~(np.array(Image.open(folder/q['tabletMask']))>0)
    else:q=fits[(key,i)];mask=np.array(Image.open(fitroot/q['mask']))>0
    h=Image.open(R/'character/krusher-bill-base-test-v2/sources'/(d+'-head-native.png')).convert('RGBA');x,y=q['headPaste'];x+=-2 if d=='east' else 2;y+=2
    layer=Image.new('RGBA',(184,184));layer.paste(h,(x,y));new=np.array(layer);out[mask]=new[mask];body_row=54+q['headShift'][1];details={'headPaste':[x,y],'headShift':q['headShift']}
   elif g=='helmet' and d!='north':
    if key.startswith('interact-'):folder,rows=tablets[(g,d)];q=rows[i]
    else:folder=helmroot;q=helms[(key,i)]
    facefile=folder/q['allowedMask'].replace('-allowed.png','-face.png');old=np.array(Image.open(facefile))>0
    x0,y0,x1,y1=q['faceBox'];x0-=2 if d=='south' else 1;x1+=2 if d=='south' else 1;y0-=3
    mask=binary_dilation(old,iterations=2)&(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)&(a[:,:,3]>0)
    h=Image.open(R/'character/krusher-bill-base-test-v2/sources'/(d+'-head-native.png')).convert('RGBA').crop(tuple(q['faceSourceCrop']));size=(x1-x0,y1-y0);h=h.resize(size,Image.Resampling.LANCZOS);layer=Image.new('RGBA',(184,184));layer.paste(h,(x0,y0));new=np.array(layer);mask&=new[:,:,3]>60;out[mask,:3]=new[mask,:3];body_row=y1;details={'oldFaceSize':q['faceSize'],'faceSize':list(size),'faceBox':[x0,y0,x1,y1]}
   assert np.array_equal(a[~mask],out[~mask]);checks+=1
   if body_row:assert np.array_equal(a[body_row:],out[body_row:]);checks+=1
   target='frames/'+g+'/'+key+f'/{i:03}.png';dst=P/target;dst.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(dst);mf='masks/'+g+'/'+key+f'/{i:03}.png';(P/mf).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mf)
   rec={'gear':g,'state':key,'index':i,'source':src.relative_to(R).as_posix(),'sourceHash':sha(src),'output':target,'outputHash':sha(dst),'mask':mf,'bodyRow':body_row,'changedPixels':int(np.any(a!=out,axis=2).sum()),'details':details}
   records.append(rec);cache[ck]=target;files.append(target)
  state['frameFiles']=files
 (P/(g+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
# Corrected reference identity is exact for all eight neutral poses.
for g in ['bare','helmet']:
 m=json.load(open(P/(g+'-manifest.json')))
 for d in ['south','east','north','west']:
  s=next(q for q in m['states'] if q['id']=='idle-'+d);assert np.array_equal(np.array(Image.open(P/s['frameFiles'][0])),np.array(Image.open(R/'character/krusher-head-fit-v2/frames'/(g+'-'+d+'.png'))));checks+=1
  s=next(q for q in m['states'] if q['id']=='interact-'+d);idle=next(q for q in m['states'] if q['id']=='idle-'+d)
  for slot in [0,-1]:assert Image.open(P/s['frameFiles'][slot]).tobytes()==Image.open(P/idle['frameFiles'][0]).tobytes();checks+=1
(P/'provenance.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records,'scope':'All24canonical states; side bare head seating and visible helmet face fit propagated by original per-pose registration/masks. Entire old source metadata preserved. Shared RGBA poses reuse exact corrected output. Other directions protected.'},indent=2)+'\n')
print(json.dumps({'checks':checks,'records':len(records),'uniqueOutputs':len(cache),'changedUnique':sum(q.get('changedPixels',0)>0 for q in records)}))
