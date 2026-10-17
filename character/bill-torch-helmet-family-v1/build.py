from pathlib import Path
import json,copy,hashlib,shutil
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];B=P.parent/'bill-torch-actions-v1';S=P/'sources';S.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((B/'manifest.json').read_text());m=copy.deepcopy(m);records=[];hashes={};checks=[]
def head_axis(image):
    a=np.array(image);yy,xx=np.indices(a.shape[:2]);mask=(a[:,:,3]>180)&(xx>=100)&(xx<155)&(yy>=60)&(yy<100)
    top=int(np.where(mask)[0].min());y,x=np.where(mask&(yy<top+14));return [float(np.median(x)),top], [int(x.min()),int(x.max()+1)]
for d in ['east','west','south','north']:
    donor=P.parent/f'bill-seated-helmet-{d}-coherent-v1';bare=P.parent/f'bill-seated-{d}-coherent-v1'
    r=json.loads((donor/'helmet-registration.json').read_text());canonical=donor/'sources/canonical-head.png';shutil.copy2(canonical,S/(d+'-canonical.png'));head=Image.open(canonical).convert('RGBA')
    idle=Image.open(donor/f'frames/sit-down-{d}/000.png').convert('RGBA');bare_idle=Image.open(bare/f'frames/sit-down-{d}/000.png').convert('RGBA');authority,_=head_axis(bare_idle)
    bx,by=r['sourceBox'][:2];base=[bx+36,by+52]
    for state in [s for s in m['states'] if s['id'].endswith('-'+d)]:
        originals=state['frameFiles'].copy();outfiles=[]
        for i,f in enumerate(originals):
            source=B/f;body=Image.open(source).convert('RGBA');arr=np.array(body);axis,bounds=head_axis(body)
            endpoint=(state['id'].startswith('torch-draw-') and i==0) or (state['id'].startswith('torch-stow-') and i==5)
            position=[round(base[0]+axis[0]-authority[0]),round(base[1]+axis[1]-authority[1])]
            # All RGB classes of bare hair are removed, within a bounded head-only rectangle.
            erase=[bounds[0]-2,axis[1],bounds[1]+2,axis[1]+25]
            if endpoint:out=idle.copy()
            else:
                x0,y0,x1,y1=erase;arr[y0:y1,x0:x1]=0;out=Image.fromarray(arr);out.alpha_composite(head,position)
            dest=P/f;dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);literal='res://'+dest.relative_to(R).as_posix();outfiles.append(literal);hashes[literal]=sha(dest)
            records.append({'state':state['id'],'frame':i,'bareFile':'res://'+source.relative_to(R).as_posix(),'bareSha256':sha(source),'endpointExactSelected':endpoint,'canonicalSha256':sha(canonical),'componentSize':list(head.size),'nativeScale':1,'position':position,'eraseRect':erase,'headAxis':axis,'idleAxis':authority,'authorityRegistrationSha256':sha(donor/'helmet-registration.json')})
        state['frameFiles']=outfiles;state['provenance']='unchanged approved torch body/tool/flame outside bounded head; selected native shared helmet; exact equipped idle endpoints'
for d in ['east','west','south','north']:
    rows=[s for s in m['states'] if s['id'].endswith('-'+d)];entry,work,exit=rows
    pixels=lambda f:Image.open(R/f[6:]).convert('RGBA').tobytes()
    assert pixels(entry['frameFiles'][-1])==pixels(work['frameFiles'][0]) and pixels(work['frameFiles'][-1])==pixels(exit['frameFiles'][0]);checks.append(d+' exact draw/weld/stow joins')
m.update(name='Bill shared-helmet cardinal torch family',equipment='diving-helmet',status='selected_runtime',precomposed=True)
for name,data in [('manifest.json',m),('helmet-registration.json',{'frames':records,'scope':'native standing shared helmet registered by crown/axis against selected idle; approved body/tool/flame preserved, actual construction proof pending'}),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1536,3072),(34,52,62))
for j,state in enumerate(m['states']):
    for i,f in enumerate(state['frameFiles']):
        im=Image.open(R/f[6:]);board.paste(im,(i*256,j*256),im)
board.save(P/'contact-sheet.png')
print('Built12 equipped cardinal torch clips/72frames, native shared hardware and exact joins')
