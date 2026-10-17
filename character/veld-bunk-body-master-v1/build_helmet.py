"""Refit exact native and independently authored reclining helmets to new anatomy."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];OLD=R/'character/veld-bunk-master-helmet-v1'
native=Image.open(R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head.png').convert('RGBA')
raw=Image.open(OLD/'reclining-raw-v1.png').convert('RGBA');reg=json.loads((OLD/'package-checks.json').read_text());curves=json.loads((OLD/'pooled-material-grade.json').read_text())
parts=[raw.crop(b) for b in reg['boxes']];parts[0].paste((0,0,0,0),(121,143,157,158));scale=reg['fixedRecliningRuler']
def materials(a):
    r,g,b=[a[:,:,c].astype(float) for c in range(3)];opaque=a[:,:,3]>160
    skin=opaque&(r>150)&(g>95)&(r>g*1.18)&(r>b*1.35);hair=opaque&~skin&(r>g*1.18)&(r>b*1.3);glass=opaque&(b>r*1.12)&(b>g*1.025)&(b>90);shell=opaque&~skin&~hair&~glass
    return {'skin':skin,'hair':hair,'glass':glass,'shell':shell}
donors=[]
for im in parts:
    a=np.array(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS));masks=materials(a)
    for kind in curves:
        for c,curve in enumerate(curves[kind]):a[:,:,c][masks[kind]]=np.interp(a[:,:,c][masks[kind]],curve['input'],curve['master']).round().clip(0,255).astype('uint8')
    donors.append(Image.fromarray(a))
components=[native]*4+donors
body_reg=json.loads((P/'bare-registration.json').read_text());records=[];frames=[];regions=[];checks=0
first=Image.new('RGBA',(256,272));first.alpha_composite(Image.open(R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA'),(36,52));frames.append(first)
def face_mean(a,area):
    r,g,b=[a[:,:,c].astype(float) for c in range(3)];mask=area&(a[:,:,3]>180)&(r>145)&(g>90)&(r>g*1.18)&(r>b*1.35);y,x=np.where(mask)
    return np.array([x.mean(),y.mean()])
for i in range(1,7):
    bare=Image.open(P/f'frames/bare/bunk-enter-east/{i:03}.png').convert('RGBA');a=np.array(bare);hx,hy=body_reg['frames'][i]['headCenter'];yy,xx=np.indices(a.shape[:2]);head=(xx-hx)**2+(yy-hy)**2<24**2
    desired=face_mean(a,head)+np.array([1.183103,-2.266247]) # exact selected bare->sealed face landmark difference
    comp=components[i];center=face_mean(np.array(comp),np.ones((comp.height,comp.width),bool));pos=tuple(np.round(desired-center).astype(int))
    # Remove original scalp/face only. Preserve the supported front neck and
    # science patch rather than clearing one oversized head/body rectangle.
    warm=((a[:,:,0].astype(float)>a[:,:,1]*1.12)&(a[:,:,1].astype(float)>a[:,:,2]*1.2))
    erase=head&warm
    # Native hairband is gray and belongs to the head. Limit its mask to the
    # upper skull, leaving gray throat/suit below the original warm face.
    skin=materials(a)['skin']&head;sy,sx=np.where(skin);erase|=head&(yy<=sy.min()+3)&(a[:,:,3]>0)
    a[erase]=0;out=Image.fromarray(a);out.alpha_composite(comp,pos)
    region=erase.copy();x,y=pos;region[y:y+comp.height,x:x+comp.width]=True
    assert np.array_equal(np.array(out)[~region],np.array(bare)[~region]);checks+=1
    assert out.getbbox()[3]==bare.getbbox()[3];checks+=1
    frames.append(out);regions.append(region);records.append({'pose':i,'bareHeadCenter':[hx,hy],'targetFace':desired.tolist(),'componentFace':center.tolist(),'position':[int(x),int(y)],'componentSize':list(comp.size),'componentSource':'exact native' if i<4 else 'independent reclining','nativeScale':1,'erase':'warm scalp/face plus spatial gray upper hairband; supported front neck protected'})
for i,im in enumerate(frames):
    f=P/f'frames/helmet/bunk-enter-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f)
for i in range(3):
    im=Image.open(P/f'frames/bare/death-bunk-east/{i:03}.png').convert('RGBA');a=np.array(im);final=np.array(frames[6]);a[regions[-1]]=final[regions[-1]];out=Image.fromarray(a)
    assert np.array_equal(np.array(out)[~regions[-1]],np.array(im)[~regions[-1]]);checks+=1
    f=P/f'frames/helmet/death-bunk-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);out.save(f)
assert frames[6].tobytes()==Image.open(P/'frames/helmet/death-bunk-east/000.png').convert('RGBA').tobytes();checks+=1
m=json.loads((P/'bare-manifest.json').read_text());m['name']='Veld complete master-body and master helmet bunk candidate';m['equipment']='diving-helmet'
for s in m['states']:s['frameFiles']=[f.replace('/frames/bare/','/frames/helmet/') for f in s['frameFiles']]
(P/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n');(P/'helmet-registration.json').write_text(json.dumps({'frames':records,'checks':checks,'failures':0,'uprightSource':'exact native35x39','recliningSource':'character/veld-bunk-master-helmet-v1/reclining-raw-v1.png','sharedRecliningRuler':scale,'sharedMaterialGrade':'character/veld-bunk-master-helmet-v1/pooled-material-grade.json','scope':'master-body/head fit candidate, native bed contact and full lifecycle pending'},indent=2)+'\n')
board=Image.new('RGB',(1792,580),'#202a30');d=ImageDraw.Draw(board)
for row in range(2):
    for i in range(7):
        im=Image.open(P/f'frames/{"bare" if row==0 else "helmet"}/bunk-enter-east/{i:03}.png').convert('RGBA');board.paste(im,(i*256,row*285+15),im);d.text((i*256+6,row*285),('Bare' if row==0 else 'Helmet')+f' {i+1}',fill='white')
board.save(P/'paired-source-review.png')
print(f'{checks} original new-body/contact/held-death join checks,0failures')
