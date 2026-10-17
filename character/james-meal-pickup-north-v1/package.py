"""Exact accepted endpoints around independently authored whole pickup figures."""
from pathlib import Path
import json, hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
R=P.parents[1]
runtime=R/'character/crew-runtime-matte-v1/branforth'
m=json.loads((runtime/'manifest.json').read_bytes())
idle=next(s for s in m['states'] if s['id']=='idle-north')
source=[runtime/idle['frameFiles'][0]]+[P/'frames'/f'{i:03d}.png' for i in [1,2,3,4]]+[R/'character/james-meal-north-v1/frames/eat/000.png']
durations=[100,150,200,200,150,100]
def canvas(path):
    im=Image.open(path).convert('RGBA')
    assert im.width==184 and im.height in [184,192]
    out=Image.new('RGBA',(184,192));out.alpha_composite(im)
    return out
files=[]
hashes=[]
for i,path in enumerate(source):
    out=P/'selected'/f'{i:03d}.png';out.parent.mkdir(exist_ok=True)
    im=canvas(path);im.save(out)
    assert Image.open(out).tobytes()==im.tobytes()
    files.append(f'selected/{i:03d}.png');hashes.append(hashlib.sha256(out.read_bytes()).hexdigest())
pack=dict(name='James North bowl acquisition',frameWidth=184,frameHeight=192,pivot=[92,172],standingHeight=148,textureFilter='linear',precomposed=True,status='selected_native_review_pending',states=[dict(id='meal-acquire-north',frameCount=6,frameFiles=files,frameDurationsMs=durations,loop=False,facings=['north']*6,waterPoses=[False]*6,depthOffsets=[0]*6,provenance=dict(source='source.png',sourcePoses=['exact accepted idle',1,2,3,4,'exact accepted held meal'],fixedScale=json.loads((P/'selection.json').read_bytes())['fixedScale'],derivation='Whole independently authored source poses; one fixed registration/grade; exact accepted endpoints, no body splices or per-pose warps.'))])
(P/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
frames=[]
for path in files:
    im=Image.open(P/path).convert('RGBA');view=Image.new('RGB',(820,330),'#303b40')
    ImageDraw.Draw(view).text((8,8),'James NORTH bowl pickup / idle master / held meal / 82px / 54px / 27px',fill='white')
    for sprite,x in [(im,30),(Image.open(source[0]),235),(Image.open(source[-1]),430)]:view.paste(sprite,(x,90),sprite)
    for h,x in [(82,630),(54,710),(27,780)]:
        s=h/148;small=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.BILINEAR);view.paste(small,(x,262-round(172*s)),small)
    frames.append(view)
frames[0].save(P/'selected-review.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
(P/'package-evidence.json').write_text(json.dumps(dict(frameCount=6,seconds=sum(durations)/1000,hashes=hashes,exactIdlePixels=Image.open(P/files[0]).tobytes()==canvas(source[0]).tobytes(),exactMealPixels=Image.open(P/files[-1]).tobytes()==canvas(source[-1]).tobytes(),scope='Packaged whole figures and exact endpoints; transparent canvas padding only for184px master; no native runtime assertion.'),indent=2)+'\n')
print('Six selected poses;900ms; exact idle/held endpoints; existing scale/grade')
