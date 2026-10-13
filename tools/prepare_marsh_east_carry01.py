"""Freeze own side cargo with complete opposite selected stance guides."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-east-carry-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
g=json.loads((S/'guide-provenance.json').read_text())
for r in g['primarySourceFrames']+g['guideSourceFrames']+g['guideArtifacts']+[g['originalOwnMaster']]:assert sha(ROOT/r['path'])==r['sha256']
board=Image.new('RGBA',(1472,736));stances=g['primarySourceFrames'][2:4]
for i,r in enumerate(stances):board.alpha_composite(Image.open(ROOT/r['path']).convert('RGBA').resize((736,736),Image.Resampling.NEAREST),(i*736,0))
stance=S/'opposite-selected-walk-guide.png';board.save(stance)
prompt='''Create FIVE complete full-body adult Marsh figures in a horizontal row with wide transparent gutters, facing EAST toward screen RIGHT, exact elevated SIDE camera. Reference ONE single selected East idle is PRIMARY for small adult head/face, fitted shoulders/waist/limbs, camera and quiet warm matte pixel grade. Reference TWO shows two complete opposite selected walking stances: use LEFT guide figure for NEAR-leg contact/support and RIGHT guide figure for FAR-leg contact/support. These supply leg arrangement only, not swinging arms. Reference THREE old carry guide supplies ONLY existing slate waist crate and supported hand placement; use its FIRST crate projection consistently throughout, not its varying crate dimensions or bulky body/head. Reference FOUR original own East master preserves swept blond hair, visible RIGHT-temple metal implant, collar/chest plate/harness/pouches and authentic small ankle buckles. No mirrored identity, rear/front view or invented hardware.

Figures1-4 gently WALK WHILE CARRYING SAME slate crate in BOTH hands in front of waist toward screen RIGHT. Bent elbows, forearms reach forward to support the box; near glove overlaps its near side, far hand supports its far side with correct occlusion. Same crate width/height/depth and elevated side projection in all four. Plain restrained recessed front panel/two small original ivory latches; no extra logos/handles. Chest/face visible, box held close to waist, no floating crate, no fused fingers. Keep same adult head, torso, rigid equipment and anatomical limb lengths across phases.
1 NEAR support/contact, matches LEFT stance guide: foreground NEAR thigh extends forward to screen RIGHT, NEAR boot flat and lowest in front; FAR leg trails to screen LEFT with heel lifting. Short cargo stride, not running.
2 NEAR support/passing: NEAR boot flat directly under hip, FAR knee gently passes low with FAR boot slightly raised behind. Foreground NEAR thigh remains supporting leg. Mild natural compression, no high knee or squat.
3 FAR support/contact, matches RIGHT stance guide: foreground NEAR thigh extends BACKWARD to screen LEFT and its boot lifts behind; FAR thigh/leg extends FORWARD to screen RIGHT with FAR boot flat and lowest. The FOREGROUND thigh points backward; do not repeat near-leading pose. Correct connected whole hips/knees/shins/boots, no crossing limb identity.
4 FAR support/passing: FAR boot flat under pelvis, foreground NEAR leg gently passes with NEAR boot raised behind toward screen LEFT. Foreground NEAR thigh nearly vertical/slightly backward; FAR boot supports. Both arms maintain crate hold, no swing. Gentle four-phase cargo walk, never both feet airborne.
5 EXACT NEUTRAL East standing ruler matching reference ONE, arms down, NO CRATE, complete unobstructed body for one common calibration.

All five same elevated East side view and fitted adult build. One neutral147 occupied calibration, runtimeH148,184canvas,p92/172; calibration only, never per-pose or cargo-width fitting. Warm ivory fabric/plates, muted sage shoulders/pouches, slate joints, charcoal gloves/soles, crisp quiet warm matte pixel clusters. FIVE complete hair-to-sole connected figures, wide transparent empty gutters; no floor/shadow/glow/haze/text/labels. Preserve own asymmetric temple implant and authentic ankle hardware.'''
p=S/'carry-01.prompt.txt';assert not p.exists();p.write_text(prompt+'\n',encoding='utf-8')
refs=[S/'selected-idle0-only.png',stance,S/'carry-motion-guide.png',ROOT/g['originalOwnMaster']['path']]
(S/'carry-01.request.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(p),'orderedReferences':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in refs],'sourceFrames':g['primarySourceFrames']+g['guideSourceFrames'],'guideToolDependencies':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in [ROOT/'tools/prepare_marsh_east_carry_guides.py',ROOT/'tools/prepare_marsh_south_carry_guides.py']],'sheetGrid':[5,1],'transparentBackground':True},indent=2)+'\n')
print('Frozen four whole near/far cargo poses plus neutral, four ordered own references.')
