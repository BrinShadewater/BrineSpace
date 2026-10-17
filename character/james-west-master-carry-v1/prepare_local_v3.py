from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
prompt='''Edit this exact transparent James carrying torso crop ONLY. There are accidentally TWO yellow-screen diagnostic meters at the belt. Keep the UPPER meter peeking above/behind the raised forearm at its original belt position. REMOVE ONLY the LOWER-RIGHT duplicate meter hanging below the wrist on the outside of the hip. It has a yellow square display above two yellow horizontal bars, at approximately x64..73percent,y57..75percent of the square canvas. Erase this entire lower-right rectangular duplicate, including black casing and yellow bars, and fill that small area with coherent dark matte quilted trouser/hip cloth continuing the surrounding material. Exactly ONE belt meter remains: the upper partly occluded device behind the forearm. Do not remove it or add another device. No glow or yellow trace left where the duplicate was.

Keep EVERYTHING ELSE exactly as the target: same two-handed carrying pose, case, fingers, wrist/cuff, forearm/elbow, shoulder badge, backpack, torso seams, belt buckle and pouches, hips/knees, silhouette, canvas framing and empty margins. No moving or scaling the subject or surviving meter; no redesign, new wrench, extra hands, exposure/colour/texture changes, purple cast or gloss. Genuine transparency unchanged. This is one tiny duplicate-object removal and cloth repair, not pose generation. Return the same complete square crop with clean alpha, no checkerboard/halo/text.'''
(p/'local-v3-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
previous=json.loads((p/'local-v2-inputs.json').read_bytes());inventory=previous['preCallSha256'].copy()
for n in ['local-v2-raw.png','local-v3-prompt.txt']:inventory[(p/n).relative_to(r).as_posix()]=hashlib.sha256((p/n).read_bytes()).hexdigest()
(p/'local-v3-inputs.json').write_text(json.dumps({'preCallSha256':inventory,'crop':previous['crop'],'admissionRegion':previous['admissionRegion'],'selected':False},indent=2)+'\n',encoding='utf-8')
print('Duplicate lower/right meter removal frozen; upper correctly placed partly occluded meter retained.')
