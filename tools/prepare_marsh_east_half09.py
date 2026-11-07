"""Freeze complete first half with selected anatomy and unchanged pose guide."""
from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1';S=BASE/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
guide=Image.new('RGBA',(2208,736));records=[]
for i in range(3):
    p=BASE/'candidate-02'/f'{i:03d}.png';f=Image.open(p).convert('RGBA');assert f.size==(184,184)
    guide.alpha_composite(f.resize((736,736),Image.Resampling.NEAREST),(i*736,0));records.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'offset':[i*736,0]})
p=S/'half-09-first-stance-guide.png';guide.save(p);(S/'half-09-guide.json').write_text(json.dumps({'sources':records,'operation':'Complete unchanged figures at nearest4x; motion only, not anatomy authority','sha256':sha(p)},indent=2)+'\n')
prompt='''Create FOUR complete full-body right-facing Marsh figures, separated widely on transparent background, all at one common scale. Reference ONE single selected idle is PRIMARY anatomy, fitted adult proportions, small head, chest/collar/waist size, camera and warm matte pixel grade. Reference TWO gives ONLY three leg arrangements, left to right, not its compressed body shape. Reference THREE original own East master supplies identity and authentic suit construction, including small right-temple plate and ankle buckles.

Figure1: NEAR foreground leg extended modestly forward RIGHT into a flat contacting boot; FAR leg trails LEFT with raised heel. Visible NEAR arm swings back LEFT, far arm forward. Natural short running contact, upright adult torso with slight forward lean. Figure2: NEAR foreground leg supports under pelvis on a flat boot; FAR knee passes LOW forward with its whole boot lifted. Visible near arm approaches neutral with bent elbow. Figure3: airborne FAR knee leads RIGHT, foreground NEAR thigh trails LEFT into rear knee and boot. Visible near arm swings forward RIGHT, far arm back. Both boots lifted; modest knee height, natural extended adult body, not a crouch. Figure4: neutral standing matching reference ONE.

Keep foreground/far thigh-to-knee-to-boot continuity from reference TWO. Preserve reference ONE head/torso/limb size in every pose; use natural small knee/hip compression, not shortened torso or giant head. Newer second half is relatively upright; these poses need restrained, similarly upright compression. Do not fit each pose to equal height. Same elevated right-side camera, fitted ivory panels, muted sage shoulders/pouches, slate joints, charcoal gloves/soles. Quiet crisp warm matte pixel clusters matching selected idle. FOUR COMPLETE connected adult figures from hair to soles, one neutral ruler scale, true transparent empty background and gutters, no floor/shadow/glow/labels/text.'''
path=S/'half-09.prompt.txt';assert not path.exists();path.write_text(prompt+'\n',encoding='utf-8');refs=[S/'selected-idle0-only.png',p,ROOT/'character/marsh-motion-polish-v1/sources/east-standing-identity-01.png']
(S/'half-09.request.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(path),'orderedReferences':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in refs],'sheetGrid':[4,1],'transparentBackground':True},indent=2)+'\n')
print('Frozen four complete first-half poses/neutral request and whole motion guide.')
