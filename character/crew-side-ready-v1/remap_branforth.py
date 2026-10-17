from pathlib import Path
import json, colorsys, hashlib
import numpy as np
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
root=P.parent/'chief-engineer-branforth-v2'
dst=P/'branforth-cardinal-colour';dst.mkdir(exist_ok=True)
catalog=json.loads((root/'catalog.json').read_text());states=[];audit=[];pairs=[]
target=np.array([[118,106,56],[179,161,83],[210,193,122]],dtype=float)
for rel in catalog['body']:
    mp=root/rel;m=json.loads(mp.read_text())
    for s in m['states']:
        if s['id'] not in ['walk-north','walk-south']:continue
        ns=dict(s);ns['frameFiles']=[]
        for n,f in enumerate(s['frameFiles']):
            src=mp.parent/f;im=Image.open(src).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float)/255
            hsv=np.array([colorsys.rgb_to_hsv(*c) for c in rgb.reshape(-1,3)]).reshape((*rgb.shape[:2],3))
            yy,xx=np.indices(a.shape[:2])
            # Confine to shoulder/chest uniform zone below exposed head and above gloves.
            mask=(a[:,:,3]>0)&(yy>=43)&(yy<=96)&((yy>=62)|(xx<72)|(xx>112))&(hsv[:,:,0]>=.055)&(hsv[:,:,0]<=.14)&(hsv[:,:,1]>.42)
            value=rgb.max(axis=2)*255
            mapped=np.empty_like(rgb)
            for k in range(3):mapped[:,:,k]=np.interp(value,[85,155,220],target[:,k])
            b=a.copy();b[mask,:3]=np.rint(mapped[mask]).astype('uint8')
            out=dst/'frames'/s['id']/f'{n:03d}.png';out.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(out)
            ns['frameFiles'].append(out.relative_to(dst).as_posix())
            assert np.array_equal(a[:,:,3],b[:,:,3])
            assert np.array_equal(a[~mask],b[~mask])
            audit.append(dict(source=str(src.relative_to(P.parent)),sourceSha256=hashlib.sha256(src.read_bytes()).hexdigest(),changedPixels=int(np.any(a!=b,axis=2).sum()),outsideMaskChanges=0,alphaChanges=0))
            if n==0:pairs.append((s['id'],im,Image.fromarray(b)))
        states.append(ns)
manifest={k:m[k] for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed'] if k in m}
manifest.update(name='Branforth cardinal engineering colour correction',status='candidate_not_installed',frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,states=states)
(dst/'manifest.json').write_text(json.dumps(manifest,indent=2))
(dst/'checks.json').write_text(json.dumps(audit,indent=2))
sheet=Image.new('RGB',(736,420*len(pairs)),'#263139');d=ImageDraw.Draw(sheet)
for row,(name,before,after) in enumerate(pairs):
    for col,im in enumerate([before,after]):
        d.text((col*368+8,row*420+8),f'{name} / {("BEFORE","MUTED YELLOW")[col]}',fill='white')
        im=im.resize((368,368),Image.Resampling.NEAREST);sheet.paste(im,(col*368,row*420+28),im)
sheet.save(P/'branforth-colour-review.png')
print(json.dumps(dict(frames=len(audit),changedPixels=sum(x['changedPixels'] for x in audit),alphaChanges=0,outsideMaskChanges=0)))
