from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib

P=Path(__file__).resolve().parent
R=P.parent.parent
S=P/'sources'
master=R/'character/bill-video-north-v5/master-source.png'
jobs=[('original master',master,'authority'),
      ('crouch v2',S/'crouch-canvas-v2.png','provisional early squat'),
      ('push v2',S/'push-canvas-v2.png','reject: drawing density too small'),
      ('push v3',S/'push-canvas-v3.png','reject: lowered posture lost'),
      ('prone v1',S/'rejected-prone-canvas-v1.png','reject: foreshortening/width')]
board=Image.new('RGB',(1600,430),'#182932')
draw=ImageDraw.Draw(board)
records=[]
for col,(name,path,status) in enumerate(jobs):
    raw=Image.open(path).convert('RGBA')
    a=np.array(raw)
    if path==master:
        # Remove the original green screen for this diagnostic only.
        green=(a[:,:,1]>a[:,:,0]*1.35)&(a[:,:,1]>a[:,:,2]*1.35)&(a[:,:,1]>85)
        a[green]=0
    source=Image.fromarray(a)
    # Single master-defined physical density, never a pose bounding-box fit.
    density=(148/976)*(1254/raw.width)
    size=(round(raw.width*density),round(raw.height*density))
    im=source.resize(size,Image.Resampling.LANCZOS)
    b=np.array(im);opaque=b[:,:,3]>180
    y,x=np.where(opaque)
    sole=int(y.max())+1
    shift=(160-round(raw.width/2*density),224-sole)
    native=Image.new('RGBA',(320,352));native.paste(im,shift)
    output=S/(name.replace(' ','-')+'-audit-native.png');native.save(output)
    board.paste(native,(col*320,35),native)
    draw.line((col*320,259,col*320+319,259),fill='#6aa39e')
    draw.text((col*320+8,8),name,fill='white')
    draw.text((col*320+8,390),status,fill='#e2bfa2')
    records.append({'name':name,'status':status,'rawSize':raw.size,'masterDefinedDensity':density,
                    'wholeFigureTranslation':shift,'nativeAlphaBounds':native.getchannel('A').getbbox(),
                    'sourceSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'scope':'Fixed sole-line diagnostic only; not final water/root registration or pose approval.'})
board.save(P/'source-master-audit.png')
all_raw=[f for f in S.iterdir() if f.suffix in ['.png','.txt'] and '-audit-native' not in f.name]
e={'scope':'North entry source development; one provisional early crouch, later phases rejected/pending. No complete bank, animation timing, helmet, native integration or acceptance.',
   'authority':master.relative_to(R).as_posix(),'registrations':records,
   'provenance':{'rejected-crouch-canvas-v1.png':'exec-7fc85e68-4b58-44df-8d9d-c5af2064d803',
       'crouch-canvas-v2.png':'exec-7854b015-6129-4a7a-b52b-1ec82dca4ac4',
       'rejected-push-canvas-v1.png':'exec-b199412d-b476-4fd8-b660-d127c1794dd3',
       'push-canvas-v2.png':'exec-01afb59e-0e06-4c8b-b7a5-be6f0e5b4e87',
       'push-canvas-v3.png':'exec-734b2695-c517-4f08-9e6f-ee4d5afaa46a',
       'rejected-prone-canvas-v1.png':'exec-01209e51-a797-40f2-a7d7-10c53485da44'},
   'rawPromptSHA256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in all_raw},
   'visualReview':'Pending common-scale board; raw generated candidates inspected. All later phases need articulated lowered/foreshortened correction before packaging.'}
(P/'source-review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
(P/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Bill North water source audit</title>
<style>body{background:#182932;color:#eef;font:16px sans-serif}img{max-width:100%}</style>
<h1>Bill North water entry — source development</h1><p>Provisional crouch; later poses require revision.
Same master-defined drawing density. Sole-line registration is a comparison convention, not a water-contact proof.</p>
<img src="source-master-audit.png"><p>No complete animation bank or runtime selection yet.</p>''',encoding='utf-8')
print(json.dumps({'sourceCandidates':6,'reviewedColumns':5,'fixedMasterStandingRuler':148,'completeBank':False}))
