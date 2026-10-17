from pathlib import Path
import hashlib,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[2];V=P.parent
assert not (P/'generation.json').exists()
for name in ['original-idle-master.png','prepared-idle-master.png','master-input.png']:
    shutil.copyfile(V/name,P/name)
prompt='Fixed-camera full-body front-facing game character animation. Preserve this exact woman, warm skin, dark brown hair, matte charcoal quilted suit, blue patches, belt equipment, head size, height and proportions. Keep the head upright and facing forward at its reference angle throughout; only her eyes glance down. Feet remain planted in the exact reference stance. ONE scanner action: her LEFT hand on the RIGHT SIDE OF THE IMAGE draws the small scanner from the vertical tool pouch at that same image-right hip. The three pale cylinders on IMAGE LEFT stay untouched. Bring that small scanner to her upper abdomen; the other gloved hand presses its buttons. Its tiny screen stays a constant dim grey-blue, unlit and matte, without flashing, colour cycling or glow. Return it to the same IMAGE-RIGHT pouch, lower both arms and return to the starting stance. Hands stay attached to sleeves. No repeated action, head bow, turn, walk, body scaling or camera motion. Preserve original fine suit details and constant neutral lighting/colour grade. Begin and finish at the identical supplied reference. Flat dark background RGB12,18,24.'
(P/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[V/'master-input.png',P/'master-input.png',P/'prompt.txt',P/'original-idle-master.png']
(P/'INPUTS.json').write_text(json.dumps(dict(authority='character/veld-idle-south-original-master-v1/original-idle-master.png',priorTask='448629913780717',method='Byte-identical original V1 input and endpoints. Only prompt changes target observed scanner side/display and head bow.',registration=dict(scale=1/3,offset=[0,0],standingHeight=148),estimatedUSD=.28,billingVerified=False,bindings={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n',encoding='utf-8')
s=(V/'review_source.py').read_text(encoding='utf-8').replace('R=P.parents[1]','R=P.parents[2]').replace('res://character/veld-interact-south-original-master-v1/frames/','res://character/veld-interact-south-original-master-v1/correct-pouch-v2/frames/')
(P/'review_source.py').write_text(s,encoding='utf-8')
print('Correct-pouch South V2 inputs prepared; original input byte-identical.')
