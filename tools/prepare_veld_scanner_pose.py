"""Register the representative east scanner pose; no runtime selection."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary,chroma,HelmetRebaker

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-action-detail-v2'

def main(actor='veld'):
    source=BASE/f'sources/{actor}-role-interact-east-candidate-01.png'
    raw=binary(chroma(source));bounds=raw.getbbox()
    # This is a standing pose without an overhead prop: crown-to-sole is a
    # valid ruler here, unlike kneeling or tool-extended work poses.
    scale=148/(bounds[3]-bounds[1])
    a=np.asarray(raw)
    y,x=np.where(a[bounds[3]-6:bounds[3],:,3]>0)
    support_x=float(np.median(x));support_y=bounds[3]-1
    dense=binary(raw.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.BOX),True)
    pose=Image.new('RGBA',(184,184))
    pose.alpha_composite(dense,(round(92-support_x*scale),round(172-support_y*scale)))
    out=BASE/f'review/{actor}-role-interact-east-01';out.mkdir(parents=True,exist_ok=True)
    pose.save(out/'registered.png')
    reference=Image.open(BASE/f'sources/{actor}-role-interact-east-reference-01.png').convert('RGBA')
    sheet=Image.new('RGB',(368,208),'#293b40')
    sheet.paste(reference,(0,24),reference);sheet.paste(pose,(184,24),pose)
    labels=ImageDraw.Draw(sheet)
    labels.text((4,4),'Selected identity',fill='white');labels.text((188,4),'Instrument study',fill='white')
    labels.line((0,196,367,196),fill='#839597')
    sheet.save(out/'comparison.png')
    report={'status':'unselected_representative_pose','source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceSize':raw.size,'bounds':bounds,'scale':scale,'support':[support_x,support_y],'pivot':[92,172],'standingHeight':148,'limits':'Standing source registration only; identity proportions, motion and fitted equipment need review.'}
    if actor=='marsh':report['limits']='Standing source registration only; identity proportions and motion need review. Marsh has no helmet equipment.'
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

def strip(actor='veld'):
    revision='02' if actor=='marsh' else '01'
    source=BASE/f'sources/{actor}-role-interact-east-strip-{revision}.png'
    raw=binary(chroma(source))
    expected=(2083,755) if actor=='marsh' else (2172,724)
    if raw.size!=expected:raise ValueError('Remeasure scanner strip')
    height,sole={'veld':(547,638),'branforth':(566,644),'marsh':(544,635)}[actor]
    scale=148/height
    out=BASE/f'review/{actor}-role-interact-east-strip-01';out.mkdir(parents=True,exist_ok=True)
    identity=Image.open(BASE/f'sources/{actor}-role-interact-east-reference-01.png').convert('RGBA')
    frames=[identity.copy()];anchors=[]
    for i in range(4):
        tile=raw.crop((i*raw.width//4,0,(i+1)*raw.width//4,raw.height));a=np.asarray(tile)
        y,x=np.where(a[sole-5:sole+1,:,3]>0);support_x=float(np.median(x));anchors.append([support_x,sole])
        dense=binary(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX),True)
        pose=Image.new('RGBA',(184,184));pose.alpha_composite(dense,(round(92-support_x*scale),round(172-sole*scale)))
        frames.append(pose)
    ending=Image.open(BASE/'sources/marsh-role-interact-east-end-reference-01.png').convert('RGBA') if actor=='marsh' else identity.copy()
    frames.append(ending)
    sheet=Image.new('RGB',(1104,208),'#293b40');preview=[]
    for i,frame in enumerate(frames):
        frame.save(out/f'interact-east-{i:03}.png');sheet.paste(frame,(184*i,24),frame)
        matte=Image.new('RGB',(184,184),'#293b40');matte.paste(frame,(0,0),frame);preview.append(matte)
    sheet.save(out/'contact.png')
    preview[0].save(out/'motion.gif',save_all=True,append_images=preview[1:],duration=150,loop=0)
    assert frames[0].tobytes()==identity.tobytes() and frames[-1].tobytes()==ending.tobytes()
    report={'status':'unselected_scanner_sequence','source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'supports':anchors,'pivot':[92,172],'frames':6,'limits':'Source review only; fitted helmet and native integration pending. GIF timing is a review default.'}
    if actor=='marsh':report['limits']='Source review only; identity/style and native integration pending. No helmet equipment. GIF timing is a review default.'
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

def equipment(actor='veld'):
    out=BASE/f'review/{actor}-role-interact-east-strip-01'
    shell_size=(34,36) if actor=='veld' else (38,40)
    shell=HelmetRebaker(None).overlay('east',shell_size)
    rows=[];fits=[]
    for index in range(6):
        body=Image.open(out/f'interact-east-{index:03}.png').convert('RGBA');a=np.asarray(body)
        ys,xs=np.where(a[:,:,3]>0);crown=int(ys.min())
        cy,cx=np.where(a[crown:crown+12,60:120,3]>0)
        center=60+float(cx.min()+cx.max()+1)/2
        angle=-6 if index==3 else 0
        helmet=shell.rotate(angle,Image.Resampling.NEAREST,expand=True)
        pos=(round(center-helmet.width/2),round(crown+shell_size[1]/2-4-helmet.height/2))
        fitted=body.copy();fitted.alpha_composite(helmet,pos)
        rows.append(fitted);fits.append({'frame':index,'centerX':center,'crown':crown,'angle':angle,'topLeft':pos})
    # Keep selected equipped idle endpoints exact, independently of the new fit.
    rows[0]=Image.open(BASE/f'sources/{actor}-role-interact-east-equipped-endpoint-01.png').convert('RGBA');rows[5]=rows[0].copy()
    sheet=Image.new('RGB',(1104,208),'#293b40')
    for index,frame in enumerate(rows):
        frame.save(out/f'helmet-interact-east-{index:03}.png');sheet.paste(frame,(index*184,24),frame)
    sheet.save(out/'helmet-contact.png')
    (out/'helmet-registration.json').write_text(json.dumps({'status':'unselected_fitting_study','view':'east','shellSize':shell_size,'fits':fits,'endpoints':'exact selected equipped interact-east idle','limits':'Source fit only; native review pending.'},indent=2)+'\n')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actor',choices=['veld','branforth','marsh'],default='veld')
    actor=parser.parse_args().actor
    main(actor)
    strip(actor)
    if actor!='marsh':equipment(actor)
