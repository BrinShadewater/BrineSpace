from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'case-grip-phase24-v56';out.mkdir(exist_ok=True)
box=(80,104,160,184)
sources=[p/'master-material-phase24-v52/bare-head-protected.png',p/'master-head-review-v16/bare-024.png',p/'master-material-v49/bare-head-protected.png',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png']
roles=['edit-target','original-grip-geometry','matte-case-finish','standing-case-design']
board=Image.new('RGBA',(640,180),(47,58,63,255));draw=ImageDraw.Draw(board)
for col,(role,f) in enumerate(zip(roles,sources)):
    crop=Image.open(f).convert('RGBA').crop(box);crop.resize((960,960),Image.Resampling.NEAREST).save(out/(role+'.png'))
    board.alpha_composite(crop.resize((160,160),Image.Resampling.NEAREST),(col*160,20));draw.text((col*160+3,3),role,fill='white')
board.save(out/'input-contact-review.png')
prompt='''Edit Image1, a precise local crop of James carrying a small rectangular case. Image2 is the ORIGINAL SAME-POSE grip/case GEOMETRY authority. Image3 is the matte case/hardware finish reference, not a pose reference. Image4 is supporting standing-case design only.
Repair only case/hand contact in Image1: restore Image2's exact projected case outline, visible face angle, case corners/edge positions and both hand/wrist grip positions. Hands must wrap its side/bottom naturally, two separate gloves, wrist cuffs attached to forearms; case must not clip through hands, torso or belt. Preserve Image1's matte neutral charcoal finish and muted dull silver corner fittings like Image3. Case dimensions should be from Image2, not copied from larger standing Image4. No shiny white buttons/edges, new handles or duplicated equipment.
Strictly preserve Image1's torso, belt tools, leg/knee pixels and all content outside this local case-and-glove region. No changing body pose/proportions, no shifting crop, no rescaling/recentering, no invented tool. The case is in front of the body, both hands carrying it; wrench stays on belt. Return ONE transparent square local crop exactly matching input framing. Original crop80x80 native units enlarged960square. Material and contact repair only, no character sheet, text or background.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(out/'inputs.json').write_text(json.dumps(dict(cropBox=box,sourceSha256={f.relative_to(r).as_posix():sha(f) for f in sources},referenceSha256={str((out/(role+'.png')).relative_to(r)):sha(out/(role+'.png')) for role in roles},promptSha256=sha(out/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print('Four case/grip crops and exact source inputs saved.')
