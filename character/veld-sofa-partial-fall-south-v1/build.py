"""Exact selected partial entrances and unchanged authored collapse source aliases."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];P.mkdir(exist_ok=True);bindings={};checks=0;outputs={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(path):
    p=R/path.removeprefix('res://');bindings[p.relative_to(R).as_posix()]=sha(p);return Image.open(p).convert('RGBA')
def padded(path,destination):
    global checks
    image=load(path);canvas=Image.new('RGBA',(256,272));canvas.alpha_composite(image)
    assert canvas.crop((0,0,256,256)).tobytes()==image.tobytes();checks+=1
    file=P/destination;file.parent.mkdir(parents=True,exist_ok=True);canvas.save(file);return 'res://'+file.relative_to(R).as_posix()
for gear in ['bare','helmet']:
    sitting=json.loads((R/f'character/veld-seated-south-selected-v1/{gear}-manifest.json').read_text())
    entries=next(s for s in sitting['states'] if s['id']=='sit-down-south')['frameFiles']
    selected=json.loads((R/f'character/veld-sofa-fall-south-selected-v1/{gear}-manifest.json').read_text())
    neutral=next(s for s in selected['states'] if s['id']=='death-sofa-neutral-south')['frameFiles']
    ground={i:padded(f'res://character/veld-death-ground-south-coherent-v1/frames/{gear}/death-ground-south/{i:03}.png',f'frames/{gear}/ground/{i:03}.png') for i in [1,2,3]}
    states=[];outputs[gear]=[]
    for pose in range(6):
        original=load(entries[pose])
        if pose==5:
            first=neutral[0];assert load(first).crop((0,0,256,256)).tobytes()==original.tobytes();checks+=1
        else:first=padded(entries[pose],f'frames/{gear}/entrance/{pose:03}.png')
        files=[first]+([ground[1],ground[2],ground[3],neutral[4],neutral[5]] if pose<2 else neutral[1:])
        durations=[180,160,180,180,220,500] if pose<2 else [180,180,200,220,240,500]
        for path in files:
            im=load(path);assert im.size==(256,272);box=im.getbbox();assert box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272;checks+=1
        states.append({'id':f'death-sofa-pose{pose}-south','frameFiles':files,'frameDurationsMs':durations,'loop':False,'terminalFrame':5,'facings':['south']*6,'depthOffsets':[0]*6})
        outputs[gear].append(files)
    manifest={'name':'Veld South partial sit/rise floor fall '+gear,'equipment':'diving-helmet' if gear=='helmet' else '', 'frameWidth':256,'frameHeight':272,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_candidate','sofaPartialFallDeathMode':'partial-south-v1','states':states}
    (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
for gear in ['bare','helmet']:
    board=Image.new('RGB',(1536,1764),'#202a30');d=ImageDraw.Draw(board)
    for pose,files in enumerate(outputs[gear]):
        for col,path in enumerate(files):
            im=load(path);board.paste(im,(col*256,pose*294+20),im);d.text((col*256+5,pose*294+3),gear+' entrance '+str(pose)+' / fall '+str(col),fill='white')
    board.save(P/(gear+'-source-review.png'))
(P/'source-registration.json').write_text(json.dumps({'checks':checks,'failures':0,'bindings':bindings,'profile':{'canvas':[256,272],'pivot':[128,224],'standingHeight':148},'method':'exact whole authored source files and transparent bottom16 padding only; no new anatomy, scaling, regrading or equipment fitting','scope':'all6selected South sit entrances, rise reverse; early0/1 ground-collapse interiors, later2-5 supported neutral interiors; source and native join acceptance pending'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'statesPerGear':6,'normalSelection':False}))
