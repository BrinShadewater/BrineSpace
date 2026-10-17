"""One native master ruler; authored reclining shell/gasket, original bunk body."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1]
SOURCE=R/'character/dr-veld-v2/supplemental/bunk-east'
native=Image.open(R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head.png').convert('RGBA')
raw=Image.open(P/'reclining-raw-v1.png').convert('RGBA')
# Fixed35/157 shared shell ruler. Original generated bodies are excluded.
scale=35/157
boxes=[(95,525,252,683),(618,585,775,736),(1161,688,1317,809)]
positions=[(108,78),(111,94),(83,116),(96,152),(71,150),(49,169),(44,196)]
erase=[(114,82,142,113),(114,95,146,129),(85,115,117,147),(100,152,129,186),(73,152,108,182),(49,171,85,200),(47,192,80,223)]
parts=[raw.crop(b) for b in boxes]
# Retain the authored back gasket below the crown, exclude adjacent chest badge.
parts[0].paste((0,0,0,0),(216-95,668-525,157,683-525))
reclining=[im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS) for im in parts]
def materials(a):
    r,g,b=[a[:,:,j].astype(float) for j in range(3)];opaque=a[:,:,3]>160
    skin=opaque&(r>150)&(g>95)&(r>g*1.18)&(r>b*1.35)
    hair=opaque&~skin&(r>g*1.18)&(r>b*1.3)
    glass=opaque&(b>r*1.12)&(b>g*1.025)&(b>90)
    shell=opaque&~skin&~hair&~glass
    return {'skin':skin,'hair':hair,'glass':glass,'shell':shell}
# One pooled semantic grade from all authored angles to the exact native master.
# Never grade an already fitted output or independently normalise individual poses.
arrays=[np.array(im) for im in reclining];ref=np.array(native);refm=materials(ref);curves={}
for kind in refm:
    rows=[a[materials(a)[kind],:3] for a in arrays];pooled=np.concatenate(rows)
    target=ref[refm[kind],:3]
    if len(pooled)<8 or len(target)<8:continue
    curves[kind]=[]
    for channel in range(3):
        old=np.quantile(pooled[:,channel],[0,.1,.25,.5,.75,.9,1]);new=np.quantile(target[:,channel],[0,.1,.25,.5,.75,.9,1]);old,idx=np.unique(old,return_index=True);curves[kind].append((old,new[idx]))
for a in arrays:
    masks=materials(a)
    for kind in curves:
        for channel,(old,new) in enumerate(curves[kind]):a[:,:,channel][masks[kind]]=np.interp(a[:,:,channel][masks[kind]],old,new).round().clip(0,255).astype(np.uint8)
components=[native]*4+[Image.fromarray(a) for a in arrays]
(P/'pooled-material-grade.json').write_text(json.dumps({k:[{'input':old.tolist(),'master':new.tolist()} for old,new in v] for k,v in curves.items()},indent=2)+'\n')
checks=0;frames=[];regions=[]
for i in range(7):
    bare=Image.open(SOURCE/f'bare/{i:03}.png').convert('RGBA');out=bare.copy();out.paste((0,0,0,0),erase[i])
    if i==5:out.paste((0,0,0,0),(49,200,72,204)) # rear bun only; original front neck/collar remain supported
    out.alpha_composite(components[i],positions[i])
    region=np.zeros((256,256),bool);x0,y0,x1,y1=erase[i];region[y0:y1,x0:x1]=True;x,y=positions[i];region[y:y+components[i].height,x:x+components[i].width]=True
    if i==5:region[200:204,49:72]=True
    assert np.array_equal(np.array(out)[~region],np.array(bare)[~region]);checks+=1
    assert out.getbbox()[3]==bare.getbbox()[3];checks+=1
    if i<4:
        expected=bare.copy();expected.paste((0,0,0,0),erase[i]);expected.alpha_composite(native,positions[i]);assert out.tobytes()==expected.tobytes();checks+=1
    dst=P/f'frames/helmet/bunk-enter-east/{i:03}.png';dst.parent.mkdir(parents=True,exist_ok=True);out.save(dst);frames.append(out);regions.append(region)
m=json.loads((SOURCE/'bare/manifest.json').read_text())
base=json.loads(json.dumps(m));base['name']='Veld staged original bare bunk and supported death';base['status']='staged_master_bunk_helmet_native_review_pending'
equipped=json.loads(json.dumps(base));equipped['name']='Veld staged master helmet bunk and supported death';equipped['equipment']='diving-helmet'
for target,gear in [(base,'bare'),(equipped,'helmet')]:
    for state in target['states']:
        if gear=='bare':state['frameFiles']=[f'res://character/dr-veld-v2/supplemental/bunk-east/bare/{f}' for f in state['frameFiles']]
        else:state['frameFiles']=[f'res://character/veld-bunk-master-helmet-v1/frames/helmet/bunk-enter-east/{f}' for f in state['frameFiles']]
    target['states'].append({'id':'death-bunk-east','frameFiles':[f'res://character/veld-bunk-death-east-v1/frames/bare/death-bunk-east/{i:03}.png' if gear=='bare' else f'res://character/veld-bunk-master-helmet-v1/frames/helmet/death-bunk-east/{i:03}.png' for i in range(3)],'frameDurationsMs':[180,280,420],'loop':False,'furnitureFrames':['bunk']*3,'depthOffsets':[100]*3})
    (P/f'{gear}-manifest.json').write_text(json.dumps(target,indent=2)+'\n')
for i in range(3):
    source=Image.open(R/f'character/veld-bunk-death-east-v1/frames/bare/death-bunk-east/{i:03}.png').convert('RGBA');out=source.copy();out.paste((0,0,0,0),erase[6]);out.alpha_composite(components[6],positions[6])
    assert np.array_equal(np.array(out)[~regions[6]],np.array(source)[~regions[6]]);checks+=1
    dst=P/f'frames/helmet/death-bunk-east/{i:03}.png';dst.parent.mkdir(parents=True,exist_ok=True);out.save(dst)
assert frames[6].tobytes()==Image.open(P/'frames/helmet/death-bunk-east/000.png').convert('RGBA').tobytes();checks+=1
board=Image.new('RGB',(1792,810),'#202a30');d=ImageDraw.Draw(board)
for row in range(3):
    for i in range(7):
        im=Image.open(SOURCE/f'{"bare" if row==0 else "helmet"}/{i:03}.png').convert('RGBA') if row<2 else frames[i]
        board.paste(im,(i*256,row*270+14),im);d.text((i*256+8,row*270),['Original bare','Previous helmet','Master helmet candidate'][row]+f' {i}',fill='white')
board.save(P/'paired-source-review.png')
tiles=[]
for im in frames:
    tile=Image.new('RGB',(256,256),'#202a30');tile.paste(im,(0,0),im);tiles.append(tile)
tiles[0].save(P/'helmet-bunk-enter.gif',save_all=True,append_images=tiles[1:],duration=[360,720,900,900,900,900,840],loop=0)
tiles[-1].save(P/'helmet-bunk-exit.gif',save_all=True,append_images=list(reversed(tiles[:-1])),duration=[840,900,900,900,900,720,360],loop=0)
deps=[R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head.png',R/'character/veld-helmet-east-fit-v3/source.png',P/'reclining-raw-v1.png']+[SOURCE/f'bare/{i:03}.png' for i in range(7)]
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'fixedRecliningRuler':scale,'boxes':boxes,'positions':positions,'erase':erase,'sourceBindings':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in deps},'scope':'staged seven-pose bunk helmet and supported held-death gear; no normal selection; one pooled semantic native-master material grade; independently authored reclining components, no rigid whole-collar roll'},indent=2)+'\n')
print(f'{checks} original body/contact/native head/held-death join checks,0failures')
