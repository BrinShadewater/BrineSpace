from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;F=P.parent;R=P.parents[2]
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json';recipe=json.loads(recipepath.read_text(encoding='utf-8'));targets=np.array(recipe['clothTargetRGB'])
path=P/'original-master-idle-ungraded.png';old=np.array(Image.open(path).convert('RGBA'));a=old.copy();rgb=a[:,:,:3].astype(float);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min())
warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+28:]=False
cloth=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+28]=False
for ch in range(3):a[cloth,ch]=np.interp(rgb[cloth].mean(1),recipe['clothKnots'],targets[:,ch]).clip(0,255).astype('uint8')
changed=cloth.copy()
for material,mask in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:a[mask,:3]=(rgb[mask]+np.array(recipe['skinHairFixedRGBOffsets'][material])).clip(0,255).astype('uint8');changed|=mask
assert np.array_equal(a[:,:,3],old[:,:,3]);assert np.array_equal(a[~changed],old[~changed]);checks=2
bare=Image.fromarray(a);shellpath=R/'character/veld-shared-helmet-v1/fitted-north.png';shell=Image.open(shellpath).convert('RGBA');sa=np.array(shell);_,sx=np.where(sa[-5:,:,3]>160);axis=(sx.min()+sx.max())/2;wy,wx=np.where(warm);htop=int(wy.min());bodyaxis=(wx.min()+wx.max())/2;pos=(round(bodyaxis-axis),htop+27-shell.height);clear=(int(wx.min())-3,htop,int(wx.max())+4,htop+25)
helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
protected=np.ones((256,256),bool);protected[min(clear[1],pos[1]):max(clear[3],pos[1]+shell.height),min(clear[0],pos[0]):max(clear[2],pos[0]+shell.width)]=False;assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1
rawpath=P/'raw-floor-case-v2.png';raw=Image.open(rawpath).convert('RGBA');ra=np.array(raw);y,x=np.where(ra[:,:,3]>200);box=(max(0,int(x.min())-2),max(0,int(y.min())-2),min(raw.width,int(x.max())+3),min(raw.height,int(y.max())+3));crop=raw.crop(box);prop=crop.resize((33,round(crop.height*33/crop.width)),Image.Resampling.LANCZOS);prop.save(P/'floor-case.png')
casepos=(112,217-prop.height);canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(prop,casepos);canvas.save(P/'floor-case-canvas.png');bindings={};board=Image.new('RGB',(1536,610),'#202a30');d=ImageDraw.Draw(board)
for row,(gear,body) in enumerate([('bare',bare),('helmet',helmet)]):
    refs=[]
    for i in range(6):
        image=Image.open(F/f'frames/{gear}/unload-north/{i:03}.png').convert('RGBA') if i<5 else body
        dest=P/'frames'/gear/'unload-north'/f'{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);image.save(dest);refs.append('res://'+dest.relative_to(R).as_posix());bindings[dest.relative_to(R).as_posix()]=hashlib.sha256(dest.read_bytes()).hexdigest()
        if i<5:assert np.array_equal(np.array(image),np.array(Image.open(F/f'frames/{gear}/unload-north/{i:03}.png')));checks+=1
        display=canvas.copy() if i==5 else Image.new('RGBA',(256,256));display.alpha_composite(image);board.paste(display,(i*256,row*300+24),display);d.text((i*256+4,row*300+3),gear+' / unload '+str(i),fill='white')
    data=json.loads((F/f'{gear}-manifest.json').read_text(encoding='utf-8'));unload=data['states'][0];pickup=data['states'][1];unload['frameFiles']=refs;pickup['frameFiles']=list(reversed(refs))
    idle={'id':'idle-north','frameFiles':[refs[5]],'frameDurationsMs':[1000],'frameCount':1,'loop':False,'facings':['north'],'waterKinds':['idle'],'waterPoses':[False]}
    data.update(name='Veld North staged original-master idle join '+gear,status='staged_static_endpoint_not_complete_idle_animation',states=[unload,pickup,idle],floorPropStudy={'canvas':'res://'+(P/'floor-case-canvas.png').relative_to(R).as_posix(),'bodyOnlyEndpoint':refs[5],'displayWhenUnloadIndex':5,'worldOwnership':'fixture only, not normal lifecycle'})
    (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    for state,images in [(unload,refs),(pickup,list(reversed(refs)))]:
        previews=[]
        for ref in images:
            bg=Image.new('RGBA',(256,256),'#202a30')
            if ref==refs[5]:bg.alpha_composite(canvas)
            bg.alpha_composite(Image.open(R/ref.removeprefix('res://')).convert('RGBA'));previews.append(bg)
        out=P/f"{gear}-{state['id']}.apng";previews[0].save(out,format='PNG',save_all=True,append_images=previews[1:],duration=state['frameDurationsMs'],loop=1,disposal=0,blend=0)
        with Image.open(out) as decoded:
            assert decoded.n_frames==6;checks+=1
            for i,im in enumerate(previews):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==im.tobytes();assert decoded.info['duration']==state['frameDurationsMs'][i];checks+=2
board.save(P/'paired-idle-join.png')
record={'checks':checks,'failures':0,'originalMasterExtraction':'master-idle-extraction.json','recipe':recipepath.relative_to(R).as_posix(),'recipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),'originalMasterIdleSourceSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'shellSource':shellpath.relative_to(R).as_posix(),'shellSHA256':hashlib.sha256(shellpath.read_bytes()).hexdigest(),'helmetFit':{'position':pos,'clearBox':clear,'bodyGasket':[bodyaxis,htop+27],'shellSize':shell.size,'scale':1,'gradeChanged':False},'floorCaseRawSHA256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'floorCaseCrop':box,'floorCaseSize':prop.size,'floorCasePosition':casepos,'newFrameBindings':bindings,'scope':'Exact whole original-master static North standing endpoint; shared recipe/rigid shell; body-only source and independent authored prop. First5action frames exact reused. Not full idle animation, continuous contact/motion, production ownership/checkpoint/adoption acceptance.'}
(P/'join-registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'caseSize':prop.size,'casePosition':casepos,'helmetFit':record['helmetFit']}))
