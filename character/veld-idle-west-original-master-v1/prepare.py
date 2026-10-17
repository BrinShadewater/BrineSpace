from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
source=R/'character/veld-side-foundation-v1/west-standing.png'
im=Image.open(source).convert('RGBA');assert im.size==(184,184)
master=Image.new('RGBA',(256,256));master.alpha_composite(im,(36,52));master.save(P/'original-idle-master.png')
assert master.tobytes()==Image.open(R/'character/veld-interact-west-original-master-v1/master-native.png').convert('RGBA').tobytes()
large=master.resize((768,768),Image.Resampling.NEAREST);plate=Image.new('RGB',(768,768),(12,18,24));plate.paste(large,(0,0),large);plate.save(P/'master-input.png')
prompt='''Locked camera, preserve the supplied exact full-body West-facing woman artwork, facing left, in the original graphite station suit. Animate a quiet standing idle: one very small natural breath and a brief gentle blink, then return to the exact supplied pose. Keep both boots planted at their exact initial locations; preserve the original stance and the original head, neck, bun, shoulders, torso, hips, knees, arms and hands in their original positions and proportions. No stepping, turning, head bobbing, hand gestures, equipment use or body sway. The breath is subtle cloth movement only, with no change in body scale. Hold the original standing pose for the first and final second. Preserve the small detailed face, warm matte light skin, dark brown bun, neutral dark charcoal quilted suit, exact folds and panel layout, blue shoulder patch, silver knee pads, belt hardware and boot details. Do not brighten or blue-grey tint the suit, smooth its texture, enlarge the head or shift her stance. Flat unchanging lighting and the same dark background. No new shine, cast light, glow, scenery or camera motion. One calm idle motion with a clean return to the exact starting appearance.'''
(P/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
record=dict(reference=source.relative_to(R).as_posix(),referenceSHA256=hashlib.sha256(source.read_bytes()).hexdigest(),nativeMaster='original-idle-master.png',nativeSHA256=hashlib.sha256((P/'original-idle-master.png').read_bytes()).hexdigest(),firstAndLastImage='master-input.png',inputSHA256=hashlib.sha256((P/'master-input.png').read_bytes()).hexdigest(),inputScale=3,offset=[0,0],paddingNative=[36,52],background=[12,18,24],promptSHA256=hashlib.sha256((P/'prompt.txt').read_bytes()).hexdigest(),scope='Whole original independently drawn West standing master, same native appearance/ruler as scanner action; no artwork edits. Full source review required before loop/gear/native adoption.')
(P/'INPUTS.json').write_text(json.dumps(record,indent=2)+'\n')
print('Original West idle input prepared; same whole master/ruler as scanner action; no generation yet')
