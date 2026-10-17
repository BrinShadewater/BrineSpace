"""Stage master-derived cargo helmet quarters and half turns, preserving bodies."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
BOX=(96,65,169,105)
masters={'north':Image.open(ROOT/'character/veld-shared-helmet-v1/fitted-north.png').convert('RGBA'),'east':Image.open(ROOT/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA').crop((82,17,116,55)),'south':Image.open(ROOT/'character/veld-shared-helmet-south-v1/fitted-helmet.png').convert('RGBA'),'west':Image.open(ROOT/'character/veld-shared-helmet-v1/fitted-west.png').convert('RGBA')}
sources={'east-south':'east-south-source-v1.png','north-west':'north-west-source-v2.png','south-west':'south-west-source-v1.png'}
quarters={};provenance={};checks=0;states=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def protected(a,b):
    global checks
    aa=np.array(a);bb=np.array(b);mask=np.ones(aa.shape[:2],bool);mask[65:105,96:169]=False
    assert np.array_equal(aa[mask],bb[mask]);checks+=1
    assert not np.any(np.concatenate([bb[0,:,3],bb[-1,:,3],bb[:,0,3],bb[:,-1,3]])>20);checks+=1
def tone(im,start,end,i):
    a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    skin=(r>g*1.17)&(g>b*1.12)&(r>110);west=(int(start=='west')*(5-i)+int(end=='west')*i)/5
    rgb[skin]*=np.array([.83,.83,.85])*(1+west*np.array([.05,.06,.06]))
    neutral=(rgb.max(2)-rgb.min(2)<38)&(rgb.mean(2)>145);lamp=(np.indices(neutral.shape)[0]<12)&(rgb.mean(2)>205)
    rgb[neutral&~lamp]*=.86
    east=(int(start=='east')*(5-i)+int(end=='east')*i)/5;shell=(rgb.max(2)-rgb.min(2)<38)&~lamp
    rgb[shell]*=1-.18*east
    a[:,:,:3]=rgb.clip(0,255).astype('uint8');a[a[:,:,3]<4]=0
    return Image.fromarray(a)
for pair in ['north-east','east-south','north-west','south-west']:
    pack=ROOT/f'character/veld-carry-turn-{pair}-consistent-v1';manifest=json.loads((pack/'helmet-manifest.json').read_text());start,end=pair.split('-');row=[]
    if pair!='north-east':
        src=Image.open(HERE/sources[pair]).convert('RGBA');cells=[];boxes=[]
        for i in range(6):
            cell=src.crop((round(i*src.width/6),0,round((i+1)*src.width/6),src.height));a=np.array(cell)
            labels,n=label(a[:,:,3]>160);main=1+np.argmax(np.bincount(labels.ravel())[1:]);keep=binary_dilation(labels==main,iterations=3);a[~keep]=0;cell=Image.fromarray(a)
            y,x=np.where(a[:,:,3]>200);box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));boxes.append(box);cells.append(cell.crop(box))
        scale=(masters[start].height+masters[end].height)/(cells[0].height+cells[5].height)
    for i in range(6):
        original=pack/f'frames/helmet/carry-turn-{pair}/{i:03}.png';base=Image.open(original).convert('RGBA')
        if pair=='north-east':
            path=HERE/f'frames/helmet/carry-turn-north-east/{i:03}.png';out=Image.open(path).convert('RGBA')
        else:
            head=tone(cells[i].resize((round(cells[i].width*scale),round(cells[i].height*scale)),Image.Resampling.LANCZOS),start,end,i)
            if i==0:head=masters[start].copy()
            if i==5:head=masters[end].copy()
            aa=np.array(head);y,x=np.where(aa[-5:,:,3]>160);center=(x.min()+x.max())/2;pos=(round(128-center),105-head.height)
            out=base.copy();out.paste((0,0,0,0),BOX);out.alpha_composite(head,pos)
            path=HERE/f'frames/helmet/carry-turn-{pair}/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);out.save(path)
        protected(base,out);row.append(path)
        provenance[path.relative_to(HERE).as_posix()]={'body':original.relative_to(ROOT).as_posix(),'bodySha256':sha(original),'head': 'north-east-source-v5.png' if pair=='north-east' else sources[pair],'exactCardinalComponent':i in [0,5]}
    quarters[pair]=row
    for s in manifest['states']:
        state=dict(s);indices=range(6) if state['id']=='carry-turn-'+pair else reversed(range(6));state['frameFiles']=[row[i].relative_to(HERE).as_posix() for i in indices];states.append(state)
profile=json.loads((ROOT/'character/veld-carry-turn-north-east-consistent-v1/helmet-manifest.json').read_text());profile.update(name='Veld master-derived cargo helmet quarters',status='installed_master_repair_pending_owner_review',states=states)
(HERE/'quarter-helmet-manifest.json').write_text(json.dumps(profile,indent=2)+'\n')
canonical={'north':quarters['north-east'][0],'east':quarters['north-east'][5],'south':quarters['south-west'][0],'west':quarters['north-west'][5]}
routes={'east-west':[('east-south',False),('south-west',False)],'west-east':[('north-west',True),('north-east',False)],'north-south':[('north-east',False),('east-south',False)],'south-north':[('south-west',False),('north-west',True)]}
old=ROOT/'character/veld-carry-half-turns-consistent-v1';half=json.loads((old/'helmet-manifest.json').read_text());half.update(name='Veld master-derived cargo helmet half turns',status='installed_master_repair_pending_owner_review')
html='<meta charset="utf-8"><title>Veld master helmet turns</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}a{color:#8cc6e7}img{margin:10px}.masters{max-width:100%;height:auto}</style><h1>Veld master helmet turn family</h1><p>Four staged half turns using one master-derived helmet family. Accepted bodies retained; exact master components at cardinal views. Review slowed, runtime680ms. Quarters retain800ms. Installed locally; owner visual review remains open.</p><img class="masters" src="accepted-master-reference.png" width="1024">'
contact=Image.new('RGBA',(1536,760),'#202a30');draw=ImageDraw.Draw(contact)
for rowindex,(pair,paths) in enumerate(quarters.items()):
    for i,path in enumerate(paths):
        im=Image.open(path).convert('RGBA').crop((96,60,164,116)).resize((204,168),Image.Resampling.NEAREST);x=i*256;y=rowindex*190;draw.text((x+4,y+4),pair+' / '+str(i),fill='white');contact.alpha_composite(im,(x+25,y+20))
contact.save(HERE/'helmet-family-contact-v1.png')
for state in half['states']:
    direction=state['id'].removeprefix('carry-turn-');refs=[]
    for pair,reverse in routes[direction]:
        start,end=pair.split('-');seq=list(quarters[pair])
        if reverse:seq.reverse();start,end=end,start
        seq[0]=canonical[start];seq[5]=canonical[end];refs+=seq
    frames=[];paths=[]
    for i,ref in enumerate(refs):
        im=Image.open(ref).convert('RGBA');base=Image.open(old/state['frameFiles'][i]).convert('RGBA');protected(base,im)
        path=HERE/f'frames/helmet/carry-turn-{direction}/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);paths.append(path.relative_to(HERE).as_posix());frames.append(im)
        provenance[paths[-1]]={'quarter':ref.relative_to(HERE).as_posix(),'previousHalfBody':(old/state['frameFiles'][i]).relative_to(ROOT).as_posix()}
    assert frames[5].tobytes()==frames[6].tobytes();checks+=1;state['frameFiles']=paths
    rgbs=[];palette=Image.new('RGB',(3072,256))
    for i,f in enumerate(frames):
        bg=Image.new('RGB',(256,256),'#202a30');bg.paste(f,mask=f);rgbs.append(bg);palette.paste(bg,(i*256,0))
    pal=palette.quantize(colors=256);gif=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in rgbs]
    elapsed=0;previous=0;durations=[]
    for t in state['frameDurationsMs']:
        elapsed+=t*3;boundary=round(elapsed/10)*10;durations.append(boundary-previous);previous=boundary
    gif[0].save(HERE/f'helmet-{direction}-v1.gif',save_all=True,append_images=gif[1:],duration=durations,loop=0,disposal=2,optimize=False)
    html+=f'<h2>Helmet / {direction}</h2>'+''.join(f'<img src="helmet-{direction}-v1.gif" height="{h}">' for h in [256,142,93,47])
(HERE/'half-helmet-manifest.json').write_text(json.dumps(half,indent=2)+'\n');(HERE/'family-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n');(HERE/'family-fit-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'bodyOutsideHeadExact':True,'quarterFrames':48,'halfFrames':48,'duplicateSeamsExact':True,'originalMetadataRetained':True,'installed':True,'ownerVisualAcceptance':'pending'},indent=2)+'\n')
(HERE/'index.html').write_text(html+'<p><a href="helmet-family-contact-v1.png">All quarter head views</a> - <a href="north-east-comparison-v5.png">North/east before and after</a></p>')
import make_review
make_review.build()
print(f'{checks} exact-body/clipping/join checks pass; 8 quarter and4 half states staged.')
