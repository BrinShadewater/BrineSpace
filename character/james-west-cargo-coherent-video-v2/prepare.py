from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
entry=r/'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png'
exit=r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png'
im=Image.open(entry).convert('RGBA');assert im.size==(256,256)
canvas=Image.new('RGBA',(256,256),'white');canvas.alpha_composite(im)
canvas.convert('RGB').resize((1024,1024),Image.Resampling.NEAREST).save(p/'master-input.png')
Image.open(exit).save(p/'exit-reference.png')
prompt='''Locked orthographic camera. Animate this exact finely painted engineer holding a closed case in both hands, on plain white. Start exactly in the supplied left-profile carry pose. Over the first second, make ONE very small settling adjustment: turn head, collar, chest and shoulders a few degrees toward the viewer into a slightly three-quarter-left ready-to-unload pose; case becomes a little more front-facing with his shoulders. Face still looks left. Then hold the new pose completely still. Feet remain planted close together at their original positions, legs and height unchanged; no step, squat or knee bend. Head, neck, collar, shoulders and arms move coherently, no head bob, arm clipping or stretching. Same mature face, grey-brown hair, forehead goggles, moustache, backpack and belt wrench. Preserve exact size, proportions, graphite matte fabric and muted engineering yellow throughout. No changing insignia, purple/pink grade, brighter exposure, shine, zoom, camera movement, new tool or helmet. Entire character/case stay in frame; pure white background, no floor shadow, scene, text or extra movement. Do not return to the first pose.'''
(p/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[entry,exit,p/'master-input.png',p/'prompt.txt',r/'tools/minimax_video.py']
(p/'inputs.json').write_text(json.dumps({'entry':entry.relative_to(r).as_posix(),'exit':exit.relative_to(r).as_posix(),'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'registration':'Exact256canvas uniformly4x to1024,no grade/translation','selected':False},indent=2)+'\n')
print('Actual incoming carry source frozen;one continuous settle attempt prepared;normal selections untouched.')
