from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,re
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inputs['preCallSha256'].items())
code=(r/'scripts/grid_canvas.gd').read_text(encoding='utf-8');block=code[code.index('player.load_manifest("res://character/crew-runtime-matte-v1/branforth/'):code.index('func _load_major_bill_animations')];bank={}
for line in block.splitlines():
    match=re.search(r'player\.load_manifest\("res://(character/[^\"]+\.json)"',line)
    if not match:continue
    manifest=r/match[1];m=json.loads(manifest.read_bytes())
    for s in m['states']:bank[s['id']]=(manifest,m,s)
def get(key):
    manifest,m,s=bank[key];f=s['frameFiles'][0];file=r/f[6:] if f.startswith('res://') else manifest.parent/f
    assert m['standingHeight']==148
    im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(file).convert('RGBA'),(128-round(m['pivot'][0]),224-round(m['pivot'][1])));return im,file,manifest
idle,src,idle_manifest=get('idle-south');assert src.relative_to(r).as_posix()==inputs['source']
base=Image.open(p/'original.png').convert('RGBA');assert base.tobytes()==idle.tobytes()
raw=Image.open(p/'raw.png').convert('RGBA');assert raw.width==raw.height and raw.getchannel('A').getextrema()==(0,255)
crop=raw.resize((96,96),Image.Resampling.LANCZOS);new=base.copy();x0,y0,x1,y1=inputs['admissionRegion'];cx,cy=inputs['crop'][:2];new.paste(crop.crop((x0-cx,y0-cy,x1-cx,y1-cy)),(x0,y0))
outside=np.ones((256,256),bool);outside[y0:y1,x0:x1]=False;assert np.array_equal(np.asarray(base)[outside],np.asarray(new)[outside]);new.save(p/'carry-pose.png')
old,old_src,old_manifest=get('carry-south');west_path=r/'character/james-west-master-carry-v1/local-v3-carry-pose.png';west=Image.open(west_path).convert('RGBA')
rows=[('selected South idle',base),('current South carry',old),('new South carry',new),('new West carry',west)]
board=Image.new('RGB',(1280,680),'#303b40');draw=ImageDraw.Draw(board)
for j,(label,im) in enumerate(rows):
    draw.text((j*320+4,8),label,fill='white');board.paste(im,(j*320+32,24),im)
    upper=im.crop((80,56,176,152)).resize((320,320),Image.Resampling.NEAREST);board.paste(upper,(j*320,290),upper)
board.save(p/'master-comparison.png')
native=Image.new('RGB',(800,250),'#303b40')
for j,(_,im) in enumerate(rows):
    for h,y in [(82,25),(54,125),(27,195)]:
        small=im.resize((round(256*h/148),)*2,Image.Resampling.LANCZOS);native.paste(small,(j*200+80-small.width//2,y),small)
native.save(p/'station-scale.png')
detail=Image.new('RGB',(1536,800),'#303b40');draw=ImageDraw.Draw(detail)
for j,(label,im) in enumerate([('original crop',Image.open(p/'target.png').convert('RGBA')),('generated crop',raw)]):
    draw.text((j*768+4,8),label,fill='white');shown=im.resize((768,768),Image.Resampling.LANCZOS);detail.paste(shown,(j*768,30),shown)
detail.save(p/'crop-comparison.png')
refs=[r/'scripts/grid_canvas.gd',idle_manifest,src,old_manifest,old_src,west_path]
report={'selected':False,'visualReviewPending':True,'rawSize':list(raw.size),'protectedOriginalPixels':int(outside.sum()),'admissionRegion':inputs['admissionRegion'],'nativeBounds':list(new.getchannel('A').point(lambda x:255 if x>=180 else 0).getbbox()),'originalNativeBounds':list(base.getchannel('A').point(lambda x:255 if x>=180 else 0).getbbox()),'rawSha256':hashlib.sha256((p/'raw.png').read_bytes()).hexdigest(),'currentLoaderReadSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in refs},'registration':'Whole generated square->96,original crop80/96,no pose fit/grade','scope':'One bare South carrying source candidate, actual literal normal idle/carry resolved. Head/lower body/feet outside admitted torso/hip region exact; not full motion/helmet/native/owner acceptance.'}
(p/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['rawSize','protectedOriginalPixels','nativeBounds','originalNativeBounds']}))
