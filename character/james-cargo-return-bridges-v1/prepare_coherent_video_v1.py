from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-west-cargo-coherent-video-v1'
out.mkdir(exist_ok=True)
source=r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png'
idle=r/'character/crew-runtime-matte-v1/branforth/frames/idle-west-breathing-v1/000.png'
im=Image.open(source).convert('RGBA');assert im.size==(256,256)
bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im)
# Provider input framing only: whole registered source, uniform4x, no pose or material edit.
bg.convert('RGB').resize((1024,1024),Image.Resampling.NEAREST).save(out/'master-input.png')
prompt='''Locked camera, orthographic finely painted game sprite on pure white background. Animate this exact engineer holding the closed case in both hands. He keeps facing left, feet planted together, same face, goggles, matte charcoal armor, muted engineering yellow, belt wrench and backpack. Make one small coherent cargo settling motion: turn his shoulders slightly toward a strict left profile while keeping head calmly facing left, bring the case a little closer to his torso, then smoothly return his shoulders and case to the original ready-to-unload pose and hold still. A gentle controlled movement, no walking or knee bend, no head bob or helmet, no waving, no clipping hands through case/body, no new tools. Head, neck, collar, shoulders and arms articulate together naturally. Preserve original size, height, proportions, detailed matte materials and color throughout; no zoom, camera movement, brighter exposure, purple color, glossy highlights, changing face or growing anatomy. Keep the whole character and case in frame, on plain white with no floor shadow, text or scene.'''
(out/'prompt.txt').write_text(prompt+'\n')
files=[source,idle,out/'master-input.png',out/'prompt.txt',r/'tools/minimax_video.py']
(out/'inputs.json').write_text(json.dumps({'sha256':{str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'sourcePivot':[128,224],'standingHeight':148,'inputScale':4,'method':'Whole original source uniformly enlarged for provider input, composited on white; no invented raster or per-pose fitting.','scope':'New coherent whole-body motion source study; no normal selection replacement or bound endpoint claim.','pricingSource':'https://platform.minimax.io/docs/guides/pricing-paygo','pricingChecked':'2026-10-02','estimatedUSD':0.19,'actualBillingVerified':False},indent=2)+'\n')
print('Single coherent source study input/prompt/hashes saved; no job submitted by this helper.')
