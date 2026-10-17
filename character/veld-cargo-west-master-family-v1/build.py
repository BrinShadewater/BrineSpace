from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];C=R/'character/veld-carry-west-master-proportions-v1'
recipe=json.loads((C/'package-registration.json').read_text(encoding='utf-8'))
knots=np.array(recipe['clothKnots']);target=np.array(recipe['clothTargetRGB'])
bare=[];helmet=[];fits=[]
headpath=R/recipe['nativeHelmetSource'];head=Image.open(headpath).convert('RGBA').crop((64,14,108,60))
for i in range(5):
    source=Image.open(P/f'ungraded-unload/{i:03}.png').convert('RGBA');a=np.array(source);rgb=a[:,:,:3].astype(float)
    ys,xs=np.where(a[:,:,3]>200);top=int(ys.min())
    warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+28:]=False
    cloth=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+28]=False;cloth[:,:110]=False
    for ch in range(3):a[cloth,ch]=np.interp(rgb[cloth].mean(1),knots,target[:,ch]).clip(0,255).astype('uint8')
    for material,mask in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:
        a[mask,:3]=(rgb[mask]+np.array(recipe['skinHairFixedRGBOffsets'][material])).clip(0,255).astype('uint8')
    bare.append(Image.fromarray(a.copy()))
    yy,xx=np.where(warm);htop=int(yy.min());center=round((xx.min()+xx.max())/2)-3
    body=a.copy();body[htop:htop+25,max(0,int(xx.min())-3):int(xx.max())+4]=0
    angle=[0,12,18,16,8][i];component=head.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
    position=(round(center+2-component.width/2),round(htop+13-component.height/2))
    equipped=Image.fromarray(body);equipped.alpha_composite(component,position);helmet.append(equipped)
    fits.append({'pose':i,'warmHeadTop':htop,'centerMinus3':center,'position':list(position),'rigidAngleDegrees':angle,'componentSize':list(component.size),'componentScale':1,'componentGradeChanged':False})
# The unobstructed authored prop avoids boot pixels in the older final crop.
casepath=P/'floor-case.png'
case=Image.open(casepath).convert('RGBA');case_position=(75,196)
for frames in [bare,helmet]:
    for i in [3,4]:frames[i].alpha_composite(case,case_position)
for frames,path in [(bare,R/'character/crew-runtime-matte-v1/veld/frames/idle-west-transition-matte-v1/000.png'),(helmet,headpath)]:
    out=Image.new('RGBA',(256,256));out.alpha_composite(Image.open(path).convert('RGBA'),(36,52));out.alpha_composite(case,case_position);frames.append(out)
bindings={};board=Image.new('RGB',(1536,584),'#202a30');draw=ImageDraw.Draw(board)
for row,(gear,frames) in enumerate([('bare',bare),('helmet',helmet)]):
    paths=[]
    for i,im in enumerate(frames):
        directory=P/'frames'/gear/'unload-west';directory.mkdir(parents=True,exist_ok=True);path=directory/f'{i:03}.png';im.save(path)
        relative=path.relative_to(R).as_posix();bindings[relative]=hashlib.sha256(path.read_bytes()).hexdigest();paths.append('res://'+relative)
        a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20)
        board.paste(im,(i*256,row*292+24),im);draw.text((i*256+4,row*292+4),gear+' unload '+str(i),fill='white')
    data=json.loads((C/f'{gear}-manifest.json').read_text(encoding='utf-8'))
    carry=dict(data['states'][0]);carry['frameFiles']=['res://'+(C/x).relative_to(R).as_posix() for x in carry['frameFiles']]
    unload=json.loads((R/'character/veld-unload-west-consistent-v1/original-state.json').read_text(encoding='utf-8'));unload.update(frameFiles=paths,frameCount=6)
    pickup=json.loads((R/'character/veld-pickup-west-consistent-v1/original-state.json').read_text(encoding='utf-8'));pickup.update(frameFiles=list(reversed(paths)),frameCount=6)
    data.update(name='Veld West master cargo family '+gear,status='staged_not_installed',states=[carry,unload,pickup])
    (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
board.save(P/'paired-unload-contact.png')
record={'source':'raw-unload-v1.png','sourceSHA256':hashlib.sha256((P/'raw-unload-v1.png').read_bytes()).hexdigest(),'sharedMaterialRecipe':'character/veld-carry-west-master-proportions-v1/package-registration.json','sharedMaterialRecipeSHA256':hashlib.sha256((C/'package-registration.json').read_bytes()).hexdigest(),'helmetSource':headpath.relative_to(R).as_posix(),'helmetSourceSHA256':hashlib.sha256(headpath.read_bytes()).hexdigest(),'helmetFits':fits,'caseSource':casepath.relative_to(R).as_posix(),'caseSourceSHA256':hashlib.sha256(casepath.read_bytes()).hexdigest(),'caseSourceBox':[0,0,case.width,case.height],'floorCasePosition':list(case_position),'fixedCaseAfterRelease':[3,4,5],'exactSelectedIdleBodyUnderForegroundProp':True,'pickupReverseAliases':[5,4,3,2,1,0],'newFrameBindings':bindings,'sourceArtAuthored':True,'status':'staged_not_installed','scope':'paired whole-body action source, same source-family colour recipe, native rigid helmet fit, clean authored floor prop reuse and exact original idle beneath foreground prop; no normal adoption/world/contact/ownership proof'}
(P/'family-registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('Paired3states/36slots,12newexports; pickup exact reversealiases; carry unchanged')
