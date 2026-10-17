from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent
(P/'frames').mkdir(exist_ok=True)
canonical_path=R/'character/krusher-equipment-study-v1/review/fitted-west.png'
canonical=Image.open(canonical_path).convert('RGBA');original=np.array(canonical)
yy,xx=np.mgrid[:184,:184]
# The source contains newly authored arms AND underlying waist pixels. This
# bounded patch is deliberately documented as such, not as pixel-exact arm art.
mask=(xx>=49)&(xx<115)&(yy>=62)&(yy<106)
poses=[canonical];records=[]
for i in range(1,8):
    source=Image.open(P/f'registered/{i:03}.png').convert('RGBA');a=np.array(source);out=original.copy();out[mask]=a[mask]
    im=Image.fromarray(out);im.save(P/f'frames/{i:03}.png');poses.append(im)
    records.append({'frame':i,'outsidePatchExact':bool(np.array_equal(out[~mask],original[~mask])),'headAndBootsExact':bool(np.array_equal(out[:62],original[:62]) and np.array_equal(out[106:],original[106:]))})
canonical.save(P/'frames/000.png');Image.fromarray(mask.astype('uint8')*255).save(P/'patch-mask.png')
states=[{'id':'terminal-raise-west','indices':[0,1,2,3],'frameDurationsMs':[120,160,180,200],'loop':False}, {'id':'terminal-type-west','indices':[3,4,5,4,5,3],'frameDurationsMs':[180,160,160,160,160,180],'loop':True}, {'id':'terminal-lower-west','indices':[3,6,7,0],'frameDurationsMs':[120,180,200,120],'loop':False}]
for state in states:
    images=[poses[i] for i in state['indices']]
    state['frameFiles']=[f'frames/{i:03}.png' for i in state.pop('indices')];state['frameCount']=len(images)
    images[0].save(P/f'review/{state["id"]}.png',save_all=True,append_images=images[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
manifest={'name':'Krusher Dom / west terminal action candidate','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'precomposed':True,'status':'unselected pose-patch candidate; seam and motion review pending','states':states,'actionMeaning':'retrieve and open hip terminal, type on supported keyboard, close and stow','transitions':['idle-west -> terminal-raise-west -> terminal-type-west -> terminal-lower-west -> idle-west'],'canonicalIdleSource':str(canonical_path.relative_to(R)),'canonicalIdleSha256':hashlib.sha256(canonical_path.read_bytes()).hexdigest(),'patchBounds':[49,62,115,106],'limitations':['Patch contains authored arms, equipment and waist; torso seam has not passed visual acceptance','Eight authored poses; holds and repeated typing poses are not new inbetweens','West bare only; no helmet/cardinal counterparts or native station evidence']}
(P/'action-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
board=Image.new('RGB',(1000,520),'#272b2e');draw=ImageDraw.Draw(board)
draw.text((12,10),'KRUSHER / BOUNDED ARM-WAIST CANDIDATE / HEAD AND LEGS PRESERVED',fill='white')
for i,im in enumerate(poses):
    im=im.resize((230,230),Image.Resampling.NEAREST);board.paste(im,((i%4)*250,(i//4)*240+30),im)
    draw.text(((i%4)*250+15,(i//4)*240+255),str(i),fill='white')
board.save(P/'review/patch-candidate.png')
assert all(r['outsidePatchExact'] and r['headAndBootsExact'] for r in records)
(P/'candidate-checks.json').write_text(json.dumps({'records':records,'canonicalSourceUnchanged':hashlib.sha256(canonical_path.read_bytes()).hexdigest()==manifest['canonicalIdleSha256'],'joinsExact':states[0]['frameFiles'][0]==states[-1]['frameFiles'][-1] and states[0]['frameFiles'][-1]==states[1]['frameFiles'][0]==states[1]['frameFiles'][-1]==states[2]['frameFiles'][0],'visualAcceptance':False},indent=2)+'\n')
print('Built west raise/type/lower candidate; protected pixels and exact join aliases pass.')
