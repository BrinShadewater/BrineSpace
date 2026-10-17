"""Fit accepted authored pitch donors onto complete revised source bodies."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
bare=json.loads((P/'bare-manifest.json').read_text());reg=json.loads((P/'registration-v3.json').read_text())
original_dir=R/'character/james-lying-east-v1'
baseline_reg=P/'baseline-helmet-registration.json'
if not baseline_reg.exists():baseline_reg.write_bytes((original_dir/'helmet-registration.json').read_bytes())
hr=json.loads(baseline_reg.read_text())
source=Image.open(original_dir/'source-helmet.png').convert('RGBA')
baseline_pack=P/'baseline-helmet-manifest.json'
if not baseline_pack.exists():baseline_pack.write_bytes((R/'character/james-rest-material-continuity-v1/helmet-manifest.json').read_bytes())
oldpack=json.loads(baseline_pack.read_text())
oldmaster=next(s for s in oldpack['states'] if s['id']=='lie-down-east')['frameFiles'][0]
master=Image.open(R/'character/james-rest-material-continuity-v1'/oldmaster).convert('RGBA')
boxes=[[108,139,189,211],[413,225,495,299],[661,258,745,332],[938,287,1029,356],[1257,316,1347,386],[1596,365,1677,440]]+[[20+319*j,630,106+319*j,708] for j in range(6)]
scale=hr['headScale'];offset=np.array(hr['centerOffset']);rows=[];tracking=[]
xx,yy=np.meshgrid(np.arange(256),np.arange(256))
for i,box in enumerate(boxes):
    crop=source.crop(box);a=np.array(crop);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1)
    neutral=(a[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);rgb[neutral]*=.9
    a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');crop=Image.fromarray(a)
    patch=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
    point=np.array(reg['tracking'][i]['headAnchor']);target=point+offset+[0,3]
    pos=np.rint(target-[patch.width/2,patch.height/2]).astype(int)
    action='lie-down' if i<6 else 'sleep';index=i if i<6 else i-6
    # Sleep0/5 already exact neutral; middle slots use revised source7..10.
    file=P/'frames'/action/f'{index:03}.png';body=Image.open(file).convert('RGBA');base=np.array(body)
    erase=((xx-point[0])/15)**2+((yy-(point[1]-1))/13)**2<=1;base[erase]=0
    out=Image.fromarray(base);out.alpha_composite(patch,tuple(pos))
    hb=reg['tracking'][i]['protectedHeadBox'];region=[min(hb[0],int(pos[0])),min(hb[1],int(pos[1])),max(hb[2],int(pos[0])+patch.width),max(hb[3]-5,int(pos[1])+patch.height)]
    if i==0:out=master.copy()
    rows.append(out);tracking.append({'sourceHeadBox':box,'position':pos.tolist(),'editRegion':region,'fixedHeadScale':scale,'eraseEllipse':[float(point[0]),float(point[1]-1),15,13]})
rows[6]=rows[5].copy();rows[11]=rows[5].copy()
pack=copy.deepcopy(bare);pack['name']='James East compact-head whole-source common-shell candidate'
for state in pack['states']:
    state['frameFiles']=[]
    for j,i in enumerate(state['provenance']['sourcePoses']):
        file=P/'frames'/'helmet'/state['id']/f'{j:03}.png';file.parent.mkdir(parents=True,exist_ok=True);rows[i].save(file);state['frameFiles'].append(file.relative_to(P).as_posix())
    state['provenance'].update(helmetSource='res://character/james-lying-east-v1/source-helmet.png',helmetSourceSha256=hashlib.sha256((original_dir/'source-helmet.png').read_bytes()).hexdigest(),fixedHeadScale=scale,helmetDerivation='Accepted pitch donors and standing-master-calibrated shell ruler reused; complete revised source body outside recorded ownership region. Source0 exact accepted helmet master.')
(P/'helmet-manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
(P/'helmet-registration-v3.json').write_text(json.dumps({'tracking':tracking,'headScale':scale,'centerOffset':offset.tolist(),'runtimeInstalled':False},indent=2)+'\n')
board=Image.new('RGB',(7*256,6*280),'#303b40');d=ImageDraw.Draw(board)
for gear_i,(mode,m) in enumerate([('bare',bare),('helmet',pack)]):
    mode_master=Image.open(P/m['states'][0]['frameFiles'][0]).convert('RGBA')
    for action_i,state in enumerate(m['states']):
        row=gear_i*3+action_i;board.paste(mode_master,(0,row*280+24),mode_master);d.text((4,row*280+4),mode+' standing master',fill='white')
        for j,f in enumerate(state['frameFiles']):
            im=Image.open(P/f).convert('RGBA');board.paste(im,((j+1)*256,row*280+24),im);d.text(((j+1)*256+4,row*280+4),mode+' '+state['id']+' '+str(j),fill='white')
board.save(P/'paired-all-candidate-poses-v3.png')
print(json.dumps({'candidateReferences':36,'helmetScale':scale,'runtimeInstalled':False}))
