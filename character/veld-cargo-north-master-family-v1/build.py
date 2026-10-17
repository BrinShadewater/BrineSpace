"""Whole authored North action poses, shared material recipe and original rigid shell."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];H=R/'character/veld-cargo-turns-master-family-v1/north-west-candidate-v4'
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json';recipe=json.loads(recipepath.read_text());targets=np.array(recipe['clothTargetRGB'])
shellpath=R/'character/veld-shared-helmet-v1/fitted-north.png';shell=Image.open(shellpath).convert('RGBA');sa=np.array(shell);_,sx=np.where(sa[-5:,:,3]>160);axis=(sx.min()+sx.max())/2
bare=[Image.open(H/'frames/bare/000.png').convert('RGBA')];helmet=[Image.open(H/'frames/helmet/000.png').convert('RGBA')];fits=[{'phase':0,'wholeCanonicalHeldAlias':True}];grades=[];checks=0
for i in range(1,6):
    path=P/f'ungraded-unload/{i:03}.png';old=np.array(Image.open(path).convert('RGBA'));a=old.copy();rgb=a[:,:,:3].astype(float);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min())
    warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+28:]=False
    cloth=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+28]=False
    # Preserve the complete low central prop/contact region; never cut anatomy.
    protect=(105,198,153,228);x0,y0,x1,y1=protect;cloth[y0:y1,x0:x1]=False
    for ch in range(3):a[cloth,ch]=np.interp(rgb[cloth].mean(1),recipe['clothKnots'],targets[:,ch]).clip(0,255).astype('uint8')
    changed=cloth.copy()
    for material,mask in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:
        a[mask,:3]=(rgb[mask]+np.array(recipe['skinHairFixedRGBOffsets'][material])).clip(0,255).astype('uint8');changed|=mask
    assert np.array_equal(a[:,:,3],old[:,:,3]);assert np.array_equal(a[~changed],old[~changed]);assert np.array_equal(a[y0:y1,x0:x1],old[y0:y1,x0:x1]);checks+=3
    body=Image.fromarray(a);bare.append(body);wy,wx=np.where(warm);htop=int(wy.min());bodyaxis=(wx.min()+wx.max())/2;pos=(round(bodyaxis-axis),htop+27-shell.height);clear=(int(wx.min())-3,htop,int(wx.max())+4,htop+25)
    e=body.copy();e.paste((0,0,0,0),clear);e.alpha_composite(shell,pos)
    protected=np.ones((256,256),bool);protected[min(clear[1],pos[1]):max(clear[3],pos[1]+shell.height),min(clear[0],pos[0]):max(clear[2],pos[0]+shell.width)]=False
    assert np.array_equal(np.array(e)[protected],a[protected]);checks+=1;helmet.append(e)
    fits.append({'phase':i,'position':pos,'bodyClearBox':clear,'shellSize':shell.size,'shellScale':1,'shellGradeChanged':False,'bodyGasketAnchor':[bodyaxis,htop+27]})
    grades.append({'phase':i,'sourceSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'protectedContactRegion':protect,'clothPixels':int(cloth.sum()),'warmHeadPixels':int(warm.sum())})
bindings={};board=Image.new('RGB',(1536,860),'#202a30');d=ImageDraw.Draw(board)
for row,(gear,frames) in enumerate([('bare',bare),('helmet',helmet)]):
    refs=[]
    for i,f in enumerate(frames):
        dest=P/'frames'/gear/'unload-north'/f'{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);f.save(dest);refs.append('res://'+dest.relative_to(R).as_posix());bindings[dest.relative_to(R).as_posix()]=hashlib.sha256(dest.read_bytes()).hexdigest()
        a=np.array(f);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
        board.paste(f,(i*256,row*290+24),f);d.text((i*256+5,row*290+5),gear+' unload '+str(i),fill='white')
        if gear=='helmet':detail=f.crop((95,60,168,180)).resize((240,230),Image.Resampling.NEAREST);board.paste(detail,(i*256+8,620),detail)
    data=json.loads((R/f'character/veld-unload-north-consistent-v1/{gear}-manifest.json').read_text());unload=json.loads((R/'character/veld-unload-north-consistent-v1/original-state.json').read_text());unload.update(frameFiles=refs,frameCount=6)
    pickup=json.loads((R/'character/veld-pickup-north-consistent-v1/original-state.json').read_text());pickup.update(frameFiles=list(reversed(refs)),frameCount=6)
    data.update(name='Veld North master cargo actions '+gear,status='staged_not_installed',frameWidth=256,frameHeight=256,pivot=[128.0,224.0],standingHeight=148,precomposed=True,states=[unload,pickup]);(P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    for state,images in [(unload,frames),(pickup,list(reversed(frames)))]:
        previews=[]
        for f in images:bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(f);previews.append(bg)
        path=P/f"{gear}-{state['id']}.apng";previews[0].save(path,format='PNG',save_all=True,append_images=previews[1:],duration=state['frameDurationsMs'],loop=1,disposal=0,blend=0)
        with Image.open(path) as decoded:
            assert decoded.n_frames==6;checks+=1
            for i,f in enumerate(previews):decoded.seek(i);assert np.array_equal(np.array(decoded.convert('RGBA')),np.array(f));assert decoded.info['duration']==state['frameDurationsMs'][i];checks+=2
board.save(P/'paired-unload-contact.png')
record={'source':'raw-unload-v1.png','status':'staged_not_installed','sourceSHA256':hashlib.sha256((P/'raw-unload-v1.png').read_bytes()).hexdigest(),'sharedMaterialRecipe':recipepath.relative_to(R).as_posix(),'sharedMaterialRecipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),'grades':grades,'helmetSource':shellpath.relative_to(R).as_posix(),'helmetSourceSHA256':hashlib.sha256(shellpath.read_bytes()).hexdigest(),'helmetFits':fits,'heldAliasDirectory':H.relative_to(R).as_posix(),'pickupReverseAliases':[5,4,3,2,1,0],'newFrameBindings':bindings,'checks':checks,'failures':0,'visualReview':'pending','scope':'Staged whole authored North interiors/terminal source and exact canonical held; fixed original helmet, unchanged shared recipe. Prop retained inside whole sources; no independent floor ownership/contact lock, exact original idle join, native/world/cadence or normal adoption acceptance.'}
(P/'family-registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'exports':12,'states':4,'checks':checks,'failures':0,'fits':fits}))
