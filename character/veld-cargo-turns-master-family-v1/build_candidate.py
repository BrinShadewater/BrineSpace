"""Staged whole-body turn with existing authored shared helmet components."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
pair=sys.argv[1] if len(sys.argv)>1 else 'south-west'
version=int(sys.argv[2]) if len(sys.argv)>2 else 7
body_version=int(sys.argv[3]) if len(sys.argv)>3 else version
assert pair in ['south-west','north-west','north-east','east-south']
start,end=pair.split('-')
D=P/(f'candidate-v{version}' if pair=='south-west' else f'{pair}-candidate-v{version}');D.mkdir(exist_ok=True)
study=P/(f'v{body_version}-study' if pair=='south-west' else f'{pair}-v{body_version}-study')
H=R/'character/veld-unified-turn-helmet-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
masters={'south':Image.open(R/'character/veld-shared-helmet-south-v1/fitted-helmet.png').convert('RGBA'), 'west':Image.open(R/'character/veld-shared-helmet-v1/fitted-west.png').convert('RGBA')}
masters['north']=Image.open(R/'character/veld-shared-helmet-v1/fitted-north.png').convert('RGBA')
masters['east']=Image.open(R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA').crop((82,17,116,55))
srcpath=R/sys.argv[4] if len(sys.argv)>4 else H/({'south-west':'south-west-source-v1.png','north-west':'north-west-source-v2.png','north-east':'north-east-source-v5.png','east-south':'east-south-source-v1.png'}[pair]);src=Image.open(srcpath).convert('RGBA');cells=[]
for i in range(6):
    a=np.array(src.crop((round(i*src.width/6),0,round((i+1)*src.width/6),src.height)))
    lab,n=label(a[:,:,3]>160); main=1+np.argmax(np.bincount(lab.ravel())[1:]);a[~binary_dilation(lab==main,iterations=3)]=0
    y,x=np.where(a[:,:,3]>200);cells.append(Image.fromarray(a).crop((int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))))
scale=(masters[start].height+masters[end].height)/(cells[0].height+cells[5].height)
if pair=='north-east':scale=35/cells[0].height
def tone(im,i):
    # Exact pre-existing selected helmet family recipe; no new shell design.
    a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    skin=(r>g*1.17)&(g>b*1.12)&(r>110);west_weight=i/5 if end=='west' else 0
    rgb[skin]*=np.array([.83,.83,.85])*(1+west_weight*np.array([.05,.06,.06]))
    neutral=(np.ptp(rgb,axis=2)<38)&(rgb.mean(2)>145);lamp=(np.indices(neutral.shape)[0]<12)&(rgb.mean(2)>205);rgb[neutral&~lamp]*=.86
    if pair=='north-east':rgb[(np.ptp(rgb,axis=2)<38)&~lamp]*=1-.18*i/5
    if pair=='east-south' and version>=3:rgb[(np.ptp(rgb,axis=2)<38)&~lamp]*=1-.18*(5-i)/5
    a[:,:,:3]=rgb.clip(0,255).astype('uint8');a[a[:,:,3]<4]=0;return Image.fromarray(a)
bare=[];helmet=[];fits=[];checks=0;paths={};rows=[]
for i in range(6):
    b=Image.open(study/f'graded/{pair}/{i:03}.png').convert('RGBA');a=np.array(b)
    if pair=='east-south' and i in [0,5]:
        canonical=P/('north-east-candidate-v5' if i==0 else 'candidate-v7')
        slot='005.png' if i==0 else '000.png'
        b=Image.open(canonical/'frames/bare'/slot).convert('RGBA')
        e=Image.open(canonical/'frames/helmet'/slot).convert('RGBA')
        fits.append({'pose':i,'wholeFrameCanonicalAlias':start if i==0 else end});checks+=1
    elif pair=='north-east' and i==0:
        b=Image.open(P/'north-west-candidate-v4/frames/bare/000.png').convert('RGBA')
        e=Image.open(P/'north-west-candidate-v4/frames/helmet/000.png').convert('RGBA')
        fits.append({'pose':i,'wholeFrameCanonicalNorthAlias':True});checks+=1
    elif i==5 and end=='west':
        b=Image.open(R/'character/veld-cargo-west-master-family-v1/frames/bare/unload-west/000.png').convert('RGBA')
        e=Image.open(R/'character/veld-cargo-west-master-family-v1/frames/helmet/unload-west/000.png').convert('RGBA')
        fits.append({'pose':i,'wholeFrameCanonicalHeldAlias':True});checks+=1
    else:
        head=tone(cells[i].resize((round(cells[i].width*scale),round(cells[i].height*scale)),Image.Resampling.LANCZOS),i)
        if i==0:head=masters[start].copy()
        if i==5:head=masters[end].copy()
        ha=np.array(head); y,x=np.where(ha[-5:,:,3]>160);center=(x.min()+x.max())/2
        first=108 if start=='south' else 107 if start=='east' else 104
        last=108 if end=='south' else 107
        gasket=round(first+(last-first)*i/5);pos=(round(128-center),gasket-head.height)
        rgb=a[:,:,:3].astype(float);warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[104:]=False
        yy,xx=np.where(warm);top=int(yy.min());left=int(xx.min())-3;right=int(xx.max())+4
        clear=(max(0,left),top,min(256,right),top+25)
        body=b.copy();body.paste((0,0,0,0),clear);e=body.copy();e.alpha_composite(head,pos)
        protected=np.ones((256,256),bool); protected[min(clear[1],pos[1]):max(clear[3],pos[1]+head.height),min(clear[0],pos[0]):max(clear[2],pos[0]+head.width)]=False
        assert np.array_equal(np.array(b)[protected],np.array(e)[protected]);checks+=1
        fits.append({'pose':i,'headSize':list(head.size),'position':list(pos),'gasketBottom':gasket,'bodyClearBox':list(clear),'originalSharedAngularRecipe':True})
    bare.append(b);helmet.append(e)
board=Image.new('RGB',(1536,816),'#202a30');draw=ImageDraw.Draw(board)
for row,(gear,frames) in enumerate([('bare',bare),('helmet',helmet)]):
    refs=[]
    for i,im in enumerate(frames):
        path=D/'frames'/gear/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
        paths[path.relative_to(P).as_posix()]=sha(path);refs.append('res://'+path.relative_to(R).as_posix())
        board.paste(im,(i*256,row*288+22),im);draw.text((i*256+4,row*288+3),f'{gear} candidate {i}',fill='white')
        detail=im.crop((94,62,164,118)).resize((210,168),Image.Resampling.NEAREST)
        if gear=='helmet':board.paste(detail,(i*256+23,614),detail);draw.text((i*256+4,590),'Shared shell / gasket x3',fill='white')
        a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
    manifest=json.loads((R/f'character/veld-carry-turn-{pair}-consistent-v1/{gear}-manifest.json').read_text(encoding='utf-8'))
    for state in manifest['states']:
        state['frameFiles']=refs if state['id']=='carry-turn-'+pair else list(reversed(refs))
        assert sum(state['frameDurationsMs'])==800 and not state['loop'];checks+=1
    manifest.update(name=({'south-west':'Veld master South–West turn candidate ','north-west':'Veld master North–West turn candidate ','north-east':'Veld master North–East turn candidate ','east-south':'Veld master East–South turn candidate '}[pair])+gear,status='staged_not_installed')
    (D/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
board.save(D/'paired-turn-contact.png')
record={'bodySource':f'raw-{pair}-v{body_version}.png','bodySourceSHA256':sha(P/f'raw-{pair}-v{body_version}.png'),'sharedAngularHelmetSource':srcpath.relative_to(R).as_posix(),'sharedAngularHelmetSHA256':sha(srcpath),'singleSharedAngularHelmetScale':scale,'fits':fits,'frameBindings':paths,'checks':checks,'failures':0,'status':'staged_not_installed','visualReview':'pending','scope':'one authored body ruler/shared fixed material recipe; immutable existing helmet source/recipe, exact starting cardinal component and whole West held frame aliases; original reverse finite timing retained, no normal/world adoption'}
if pair=='south-west':record['scope']='one authored body ruler/shared fixed material recipe; immutable existing helmet source/recipe, exact South component and whole West held frame aliases; original reverse finite timing retained, no normal/world adoption'
if pair=='north-east':record['scope']='one authored body ruler/shared fixed material recipe; immutable existing North-East angular helmet source/recipe, exact East helmet component and canonical whole North held frame aliases; new authored East held pose, original reverse finite timing retained, no normal/world adoption'
if pair=='east-south':record['scope']='one authored body ruler/shared material recipe; existing East-South angular helmet source/recipe, whole canonical East and South held endpoint aliases; original reverse finite timing retained, intermediate angular helmet progression pending review, no normal/world adoption'
if pair=='east-south' and version>=3:record['scope']='preserved authored body v2 with independently authored angular helmet source from isolated original cardinal references; existing East-South tone recipe, exact whole East/South held aliases, original reverse finite timing; staged, no normal/world adoption'
(D/'registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(f'{checks} staged pair protection/clipping/metadata checks pass; 12exports/4quarter states; no admission.')
