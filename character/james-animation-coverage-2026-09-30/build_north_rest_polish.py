from pathlib import Path
import importlib.util,json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
out=R/'character/james-north-rest-polish-v1';out.mkdir(exist_ok=True)
src=R/'character/james-lying-north-v1'
spec=importlib.util.spec_from_file_location('lying_helpers',R/'character/james-lying-family-v1/build.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
cells=mod.extract(src/'source-lying-v6.png')
master_folder=R/'character/crew-runtime-matte-v1/branforth'
m=json.loads((master_folder/'manifest.json').read_text());s=next(s for s in m['states'] if s['id']=='idle-north')
master=Image.open(master_folder/s['frameFiles'][0]).convert('RGBA')
full=Image.new('RGBA',(256,256));full.alpha_composite(master,(36,52))
y,x=np.where(np.array(cells[0][0])[:,:,3]>180);scale=148/(y.max()-y.min()+1)
target=mod.foot(full);raw=[];tracking=[]
for i,(cell,box) in enumerate(cells):
    at=np.rint(target-mod.foot(cell)*scale).astype(int)
    im=Image.new('RGBA',(256,256));im.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),tuple(at))
    point,hb=mod.head(im,'north',i)
    raw.append(im);tracking.append(dict(sourcePose=i,sourceBox=box,translation=at.tolist(),headAnchor=point.tolist(),protectedHeadBox=hb))
# Breathing cells are registered to one cranial anchor, using uniform source scale.
for i in range(7,12):
    delta=np.rint(np.array(tracking[6]['headAnchor'])-np.array(tracking[i]['headAnchor'])).astype(int)
    im=Image.new('RGBA',(256,256));im.alpha_composite(raw[i],tuple(delta));raw[i]=im
    tracking[i]['translation']=(np.array(tracking[i]['translation'])+delta).tolist()
    point,hb=mod.head(im,'north',i);tracking[i].update(headAnchor=point.tolist(),protectedHeadBox=hb)
fa=np.array(full);_,mb=mod.head(full,'north',0)
gain=np.median(fa[:,:,:3][mod.gold(fa,mb)],axis=0)/np.median(np.array(raw[0])[:,:,:3][mod.gold(np.array(raw[0]),tracking[0]['protectedHeadBox'])],axis=0)
body=[]
for i,im in enumerate(raw):
    a=np.array(im);rgb=a[:,:,:3].astype(float);x0,y0,x1,y1=tracking[i]['protectedHeadBox'];protect=np.zeros(a.shape[:2],bool);protect[y0:y1,x0:x1]=True
    gm=mod.gold(a,tracking[i]['protectedHeadBox']);neutral=(a[:,:,3]>0)&~protect&~gm;lum=rgb.mean(2)
    mapped=np.interp(lum,[0,50,70,90,120,160,200,255],[0,50,68,80,99,126,149,170]);factor=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0)
    rgb[neutral]*=factor[neutral,None];rgb[gm]*=gain;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');body.append(Image.fromarray(a))
body[0]=full
helmet_source=Image.open(src/'source-helmet.png').convert('RGBA')
boxes=[[103,60,202,141],[392,165,491,243],[685,195,784,266],[987,216,1086,280],[1279,238,1380,302],[1567,247,1666,311]]
oldreg=json.loads((src/'helmet-registration.json').read_text());headscale=oldreg['headScale'];offset=np.array(oldreg['centerOffset'])
equipped=[];owned=[]
for i in range(12):
    donor=min(i,5);crop=helmet_source.crop(boxes[donor]);a=np.array(crop);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);neutral=(a[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);rgb[neutral]*=.9;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8')
    patch=Image.fromarray(a).resize((round(crop.width*headscale),round(crop.height*headscale)),Image.Resampling.LANCZOS)
    point=np.array(tracking[i]['headAnchor']);pos=np.rint(point+offset-[patch.width/2,patch.height/2]).astype(int)
    base=np.array(body[i]);yy,xx=np.indices(base.shape[:2]);erase=((xx-point[0])/15)**2+((yy-(point[1]-1))/13)**2<=1;base[erase]=0
    im=Image.fromarray(base);im.alpha_composite(patch,tuple(pos))
    x0,y0,x1,y1=tracking[i]['protectedHeadBox'];region=[min(x0,int(pos[0])),min(y0,int(pos[1])),max(x1,int(pos[0])+patch.width),max(y1,int(pos[1])+patch.height)]
    if i==0:
        im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(src/'selected-helmet-master.png').convert('RGBA'),(36,52))
    equipped.append(im);owned.append(dict(donor=donor,sourceBox=boxes[donor],scale=headscale,position=pos.tolist(),editRegion=region))
indices={'lie-down':[0,1,2,3,4,6],'sleep':[6,7,8,9,10,6],'get-up':[6,4,3,2,1,0]}
hashes={};base=json.loads((src/'bare-manifest.json').read_text());frames={}
status=json.loads((out/'selection.json').read_text()).get('status','staged_owner_review_pending') if (out/'selection.json').exists() else 'staged_owner_review_pending'
for mode,rows in [('bare',body),('helmet',equipped)]:
    pack=dict(name='James North rest anatomy polish '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status=status,states=[])
    for action,poses in indices.items():
        state=copy.deepcopy(next(s for s in base['states'] if s['id']==action+'-north'));files=[]
        for j,i in enumerate(poses):
            file=out/'frames'/mode/action/f'{j:03d}.png';file.parent.mkdir(parents=True,exist_ok=True);rows[i].save(file);rel=file.relative_to(out).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(file.read_bytes()).hexdigest()
        state.update(frameFiles=files,provenance=dict(source='character/james-lying-north-v1/source-lying-v6.png',fixedScale=float(scale),sourcePoses=poses,derivation='Coherent master-led North rest anatomy; corrected calves; exact standing master; common source6 neutral; rise exact reverse',helmetDonorSource='character/james-lying-north-v1/source-helmet.png' if mode=='helmet' else None))
        if action=='sleep':state['restHeadOffset']=((np.array(tracking[6]['headAnchor'])-[128,224])*65.28/148).tolist()
        pack['states'].append(state);frames[mode,action]=[rows[i] for i in poses]
    (out/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
(out/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
(out/'registration.json').write_text(json.dumps(dict(fixedScale=float(scale),calibration='148px upright source0 height, single scale for complete source; exact standing master replaces source0',sourceSha256=hashlib.sha256((src/'source-lying-v6.png').read_bytes()).hexdigest(),helmetSourceSha256=hashlib.sha256((src/'source-helmet.png').read_bytes()).hexdigest(),goldGain=gain.tolist(),tracking=tracking,helmetTracking=owned),indent=2)+'\n')
board=Image.new('RGB',(1536,960),'#303b40');d=ImageDraw.Draw(board)
for r,action in enumerate(indices):
    for i in range(6):
        for mode,y in [('bare',r*320+40),('helmet',r*320+175)]:
            im=frames[mode,action][i];sc=.75;small=im.resize((192,192),Image.Resampling.BILINEAR);board.paste(small,(i*256,y-70),small);d.text((i*256+4,y-25),action+' '+mode+' '+str(i),fill='white')
board.save(out/'contact.png')
print('Staged North rest3states/36paired refs,one source scale',scale,'shared neutral source6; visual selection pending')
