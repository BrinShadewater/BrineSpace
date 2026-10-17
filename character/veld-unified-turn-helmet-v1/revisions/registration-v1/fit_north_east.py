"""Fit one coherent high-density helmet quarter onto untouched accepted bodies."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PACK=ROOT/'character/veld-carry-turn-north-east-consistent-v1'
source=Image.open(HERE/'north-east-source-v5.png').convert('RGBA')
cells=[];boxes=[]
for i in range(6):
    cell=source.crop((round(i*source.width/6),0,round((i+1)*source.width/6),source.height))
    a=np.array(cell);labels,n=label(a[:,:,3]>160);main=1+np.argmax(np.bincount(labels.ravel())[1:]);keep=binary_dilation(labels==main,iterations=3);a[~keep]=0;cell=Image.fromarray(a)
    y,x=np.where(a[:,:,3]>200);box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));boxes.append(box);cells.append(cell.crop(box))
scale=35/cells[0].height
components=[]
for i,cell in enumerate(cells):
    im=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS)
    a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    skin=(r>g*1.17)&(g>b*1.12)&(r>110);rgb[skin]*=[.83,.83,.85]
    neutral=(rgb.max(2)-rgb.min(2)<38)&(rgb.mean(2)>145)
    # Exclude high white lamp pixels from the shared master trim curve.
    lamp=(np.indices(neutral.shape)[0]<12)&(rgb.mean(2)>205)
    rgb[neutral&~lamp]*=.86
    # Directional accepted shell mute is blended once, never per-frame normalized.
    shell=(rgb.max(2)-rgb.min(2)<38)&~lamp
    rgb[shell]*=1-.18*i/5
    a[:,:,:3]=rgb.clip(0,255).astype('uint8');a[a[:,:,3]<4]=0
    components.append(Image.fromarray(a))
# Exact accepted cardinal components; intermediate generation is not a new master.
components[0]=Image.open(ROOT/'character/veld-shared-helmet-v1/fitted-north.png').convert('RGBA')
components[5]=Image.open(ROOT/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA').crop((82,17,116,55))
box=(100,65,160,105);contact=Image.new('RGBA',(1536,860),'#202a30');draw=ImageDraw.Draw(contact);checks=0;provenance=[];frames=[]
for i,head in enumerate(components):
    path=PACK/f'frames/helmet/carry-turn-north-east/{i:03}.png';base=Image.open(path).convert('RGBA');out=base.copy();out.paste((0,0,0,0),box)
    # Bottom gasket axis supplies registration; perspective changes head bounds.
    a=np.array(head);y,x=np.where(a[-5:,:,3]>160);center=(x.min()+x.max())/2
    pos=(round(128-center),105-head.height);out.alpha_composite(head,pos)
    before=np.array(base);after=np.array(out);protected=np.ones((256,256),bool);protected[65:105,100:160]=False
    assert np.array_equal(before[protected],after[protected]);checks+=1
    assert not np.any(np.concatenate([after[0,:,3],after[-1,:,3],after[:,0,3],after[:,-1,3]])>20);checks+=1
    f=HERE/f'frames/helmet/carry-turn-north-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);out.save(f);frames.append(out)
    provenance.append({'slot':i,'bodySource':path.relative_to(ROOT).as_posix(),'bodySha256':hashlib.sha256(path.read_bytes()).hexdigest(),'headSource':'accepted cardinal' if i in [0,5] else 'north-east-source-v5.png','extractionBox':boxes[i],'position':pos,'size':head.size})
    for row,im in enumerate([base,out]):contact.alpha_composite(im,(i*256,row*280+25));draw.text((i*256+5,row*280+4),f'{"previous" if row==0 else "master head"} / {i}',fill='white')
    crop=out.crop((96,60,164,116)).resize((204,168),Image.Resampling.NEAREST);contact.alpha_composite(crop,(i*256+25,585));draw.text((i*256+5,565),f'head detail / {i}',fill='white')
contact.save(HERE/'north-east-comparison-v5.png')
m=json.loads((PACK/'helmet-manifest.json').read_text());m['name']='Veld master-source north/east helmet repair';m['status']='staged_head_fit_review';m['states']=[dict(s) for s in m['states']]
for s in m['states']:
    indices=list(range(6)) if s['id']=='carry-turn-north-east' else list(reversed(range(6)))
    s['frameFiles']=[f'frames/helmet/carry-turn-north-east/{i:03}.png' for i in indices]
(HERE/'north-east-helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
rgb=[]
for f in frames:
    bg=Image.new('RGB',(256,256),'#202a30');bg.paste(f,mask=f);rgb.append(bg)
palette=Image.new('RGB',(1536,256))
for i,f in enumerate(rgb):palette.paste(f,(i*256,0))
pal=palette.quantize(colors=256);gif=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in rgb]
gif[0].save(HERE/'north-east-v5.gif',save_all=True,append_images=gif[1:],duration=[int(x*3) for x in m['states'][0]['frameDurationsMs']],loop=0,disposal=2,optimize=False)
(HERE/'north-east-fit-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'protectedRegion':'all pixels outside x100:160 y65:105','originalBodyBelow105Exact':True,'cardinalComponents':'exact accepted runtime component pixels','scale':scale,'sourceCropBoxes':boxes,'provenance':provenance},indent=2)+'\n')
(HERE/'index.html').write_text('<meta charset="utf-8"><title>Veld master-source helmet fit</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld rear-to-east master helmet fit</h1><p>Staged head-only repair, accepted body pixels unchanged outside head region. Original cardinal components; high-resolution master-derived intermediates. Preview slowed; runtime metadata remains 800ms. Complete family repair pending.</p>'+''.join(f'<img src="north-east-v5.gif" height="{h}">' for h in [256,142,93,47])+'<p><a href="north-east-comparison-v5.png">Before/after and head detail</a></p><img src="accepted-master-reference.png" width="1024" style="max-width:100%;height:auto">')
print(f'{checks} protected-body/clipping checks pass; north/east head fit staged.')
