"""Source-only turn gate; never installs, constructs anatomy or fits equipment."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent; R=P.parents[1]
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json'
recipe=json.loads(recipepath.read_text(encoding='utf-8'))
knots=np.array(recipe['clothKnots']); target=np.array(recipe['clothTargetRGB'])
version=int(sys.argv[1]) if len(sys.argv)>1 else 4
pair=sys.argv[2] if len(sys.argv)>2 else 'south-west'
assert pair in ['south-west','north-west','north-east','east-south']
dest=P/(f'v{version}-study' if pair=='south-west' else f'{pair}-v{version}-study'); (dest/'graded'/pair).mkdir(parents=True,exist_ok=True)
frames=[]; bindings={}; checks=0
for i in range(6):
    original=np.array(Image.open(dest/f'ungraded/{pair}/{i:03}.png').convert('RGBA'))
    a=original.copy(); rgb=a[:,:,:3].astype(float); ys,xs=np.where(a[:,:,3]>200); top=int(ys.min())
    # All head pixels stay in an explicit upper band; the entire case/hand band
    # is excluded from suit grading for every projection, not merely the West one.
    warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15); warm[top+28:]=False
    cloth=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125)
    cloth[:top+28]=False; cloth[110:160]=False
    for ch in range(3): a[cloth,ch]=np.interp(rgb[cloth].mean(1),knots,target[:,ch]).clip(0,255).astype('uint8')
    for name,mask in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:
        a[mask,:3]=(rgb[mask]+np.array(recipe['skinHairFixedRGBOffsets'][name])).clip(0,255).astype('uint8')
    assert np.array_equal(a[:,:,3],original[:,:,3]); checks+=1
    assert np.array_equal(a[110:160],original[110:160]); checks+=1
    assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20); checks+=1
    im=Image.fromarray(a); frames.append(im); path=dest/f'graded/{pair}/{i:03}.png'; im.save(path)
    bindings[path.relative_to(P).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
heldpath=(R/'character/veld-side-foundation-v1/east-standing.png') if pair=='north-east' else (P/'candidate-v7/frames/bare/000.png') if pair=='east-south' else (R/'character/veld-cargo-west-master-family-v1/frames/bare/unload-west/000.png')
held=Image.open(heldpath).convert('RGBA')
heldlabel='Original East master' if pair=='north-east' else 'Canonical held comparison'
if held.size==(184,184):
    padded=Image.new('RGBA',(256,256));padded.alpha_composite(held,(36,52));held=padded
board=Image.new('RGB',(1536,864),'#202a30'); draw=ImageDraw.Draw(board)
for i,im in enumerate(frames):
    board.paste(im,(i*256,24),im); draw.text((i*256+4,4),f'New source {i}',fill='white')
    detail=im.crop((80,70,166,165)).resize((172,190),Image.Resampling.NEAREST)
    board.paste(detail,(i*256+42,320),detail); draw.text((i*256+4,292),'Head / grip / equipment x2',fill='white')
    board.paste(held,(i*256,584),held); draw.text((i*256+4,564),heldlabel,fill='white')
board.save(dest/'material-equipment-contact.png')
# This is a source preview, not native player capture. Preserve original finite
# pose durations; repeated playback is viewer-only and never changes runtime.
states=json.loads((R/f'character/veld-carry-turn-{pair}-consistent-v1/original-states.json').read_text())
durations=states[0]['frameDurationsMs']; assert sum(durations)==800; checks+=1
rgbframes=[]
for im in frames:
    bg=Image.new('RGB',im.size,'#202a30'); bg.paste(im,(0,0),im); rgbframes.append(bg)
movie=dest/f'bare-{pair}-source.apng'
rgbframes[0].save(movie,save_all=True,append_images=rgbframes[1:],duration=durations,loop=0,disposal=0,blend=0)
with Image.open(movie) as decoded:
    assert decoded.n_frames==6; checks+=1
    for i,expected in enumerate(rgbframes):
        decoded.seek(i); assert np.array_equal(np.array(decoded.convert('RGB')),np.array(expected)); checks+=1
        assert abs(decoded.info['duration']-durations[i])<1; checks+=1
record={'source':f'raw-{pair}-v{version}.png','sourceSHA256':hashlib.sha256((P/f'raw-{pair}-v{version}.png').read_bytes()).hexdigest(),
        'materialRecipe':recipepath.relative_to(R).as_posix(),'materialRecipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),
        'bindings':bindings,'checks':checks,'failures':0,'canonicalHeld':heldpath.relative_to(R).as_posix(),
        'canonicalHeldSHA256':hashlib.sha256(heldpath.read_bytes()).hexdigest(),'scope':'source-only extraction/one shared bounded grade/case-band pixel protection/lossless six-pose 800ms APNG',
        'nativeMotionReviewed':False,'visualReview':'pending','status':'unselected_source_gate'}
(dest/'review-evidence.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
html='''<meta charset="utf-8"><title>Veld turn source gate</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}img.board{max-width:100%}a{color:#9ccbea}</style><h1>Veld South–West source repair</h1><p>Unselected source review. Bare turn only; original 800ms finite timing, repeated here for inspection. Native/world motion and helmet fitting are pending. Equipment continuity must pass before admission.</p><img class="board" src="material-equipment-contact.png"><h2>Source preview</h2>'''
html=html.replace('South–West',pair.replace('-', '–').title())
for height in [256,148,93,47]: html+=f'<img src="bare-{pair}-source.apng" height="{height}">'
(dest/'index.html').write_text(html,encoding='utf-8')
print(f'{checks} source checks pass; 6 exact APNG presentations, original800ms. Visual/gear joins pending; no runtime admission.')
