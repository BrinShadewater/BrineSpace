"""Measure whole-pose bob edits against original geometry and registered neighbors."""
from pathlib import Path
import json, hashlib, shutil
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-east-walk-halfcycle-polish-v1'
BASE=ROOT/'character/marsh-east-walk-bob-contact-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
refs=json.loads((OUT/'references.json').read_text())['references']
for r in refs:
    assert sha(ROOT/r['path'])==r['sha256']
    if 'guide' in r: assert sha(ROOT/r['guide'])==r['guideSha256']
inv=json.loads((ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-contact/inventory.json').read_text())
frames=[]; old=[]; registered=[]; records=[]
for slot in range(6):
    entry=inv['states']['walk-east']['frames'][slot]
    p=ROOT/entry['path'];assert sha(p)==entry['sha256']
    original=Image.open(p).convert('RGBA');prior=Image.open(BASE/f'{slot:03}.png').convert('RGBA')
    path=OUT/f'{slot:03}.png'
    if slot==4:
        rawpath=OUT/f'phase-{slot:03}.raw.png';raw=Image.open(rawpath).convert('RGBA')
        assert raw.width==raw.height
        receipt=json.loads((OUT/f'phase-{slot:03}.result.json').read_text())
        assert sha(rawpath).lower()==receipt['rawSha256'].lower()
        candidate=raw.resize((184,184),Image.Resampling.LANCZOS);candidate.save(path)
        method='Single whole-canvas resample184/rawWidth, raw alpha preserved; no fitting, translation, anatomical splice or recolour.'
    else:
        shutil.copyfile(BASE/f'{slot:03}.png',path);candidate=prior.copy();method='Exact registered neighbor byte copy.'
    masks=[np.asarray(im)[:,:,3]>=128 for im in [original,prior,candidate]]
    bounds=[Image.fromarray(m.astype('uint8')*255).getbbox() for m in masks]
    ob,pb,cb=bounds
    records.append({'slot':slot,'source':entry,'registeredSha256':sha(BASE/f'{slot:03}.png'),'frameSha256':sha(path),'originalBounds':ob,'registeredBounds':pb,'candidateBounds':cb,'crownDisplacement':cb[1]-ob[1],'soleDisplacement':cb[3]-ob[3],'heightRatio':(cb[3]-cb[1])/(ob[3]-ob[1]),'opaqueIoU':int((masks[0]&masks[2]).sum())/int((masks[0]|masks[2]).sum()),'method':method,'reviewed':False,'normalAdmission':False})
    frames.append(candidate);old.append(original);registered.append(prior)
board=Image.new('RGB',(1104,1498),'#293b40');draw=ImageDraw.Draw(board)
def place(im,col,row,label,pivot=(92,172)):
    board.paste(im,(184*col+round(92-pivot[0]),214*row+25+round(172-pivot[1])),im)
    draw.text((184*col+3,214*row+3),label,fill='white')
master=Image.open(ROOT/'character/marsh-motion-polish-v1/sources/east-standing-identity-01.png').convert('RGBA')
factor=147/1232
master=master.resize((round(master.width*factor),round(master.height*factor)),Image.Resampling.LANCZOS)
board.paste(master,(31,25+round(172-1393*factor)),master);draw.text((3,3),'original master',fill='white')
idle=Image.open(ROOT/inv['states']['idle-east']['frames'][0]['path']).convert('RGBA');place(idle,1,0,'own idle')
for row,imgs,label in [(1,old,'current'),(2,registered,'registered'),(3,frames,'half-cycle study')]:
    for slot,im in enumerate(imgs):place(im,slot,row,f'{label} /{slot}')
for row,key in enumerate(['walk-start-east','walk-stop-east','run-east'],4):
    state=inv['states'][key]
    for slot,entry in enumerate(state['frames']):
        p=ROOT/entry['path'];assert sha(p)==entry['sha256'];place(Image.open(p).convert('RGBA'),slot,row,f'{key} /{slot}',state['pivot'])
board.save(OUT/'family-joins-native.png')
head=Image.new('RGB',(1020,440),'#293b40');hd=ImageDraw.Draw(head)
for row,imgs in enumerate([old,registered,frames,[idle]*6]):
    for slot,im in enumerate(imgs):
        crop=im.crop((50,12,135,57)).resize((170,90),Image.Resampling.NEAREST)
        head.paste(crop,(slot*170,row*110+20),crop);hd.text((slot*170+3,row*110+3),['current','registered','half-cycle study','own idle'][row]+f' /{slot}',fill='white')
head.save(OUT/'heads-2x.png')
manifest=json.loads((BASE/'manifest.json').read_text())
manifest['states'][0]['frameFiles']=['res://'+(OUT/f'{i:03}.png').relative_to(ROOT).as_posix() for i in range(6)]
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
report={'scope':'Unselected whole-pose half-cycle study. Source bounds and held boards only; no native/cadence acceptance inferred.','records':records,'normalAdmission':False,'fullGoalComplete':False,'boards':[{'path':(OUT/n).relative_to(ROOT).as_posix(),'sha256':sha(OUT/n),'reviewed':False} for n in ['family-joins-native.png','heads-2x.png']]}
(OUT/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['slot','candidateBounds','crownDisplacement','soleDisplacement','heightRatio','opaqueIoU']} for r in records]))
