"""Freeze four whole fitted cargo-walk poses plus an unobstructed neutral ruler."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'character/marsh-south-carry-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
guide=json.loads((S/'guide-provenance.json').read_text())
for r in guide['primarySourceFrames']+guide['guideSourceFrames']+guide['guideArtifacts']+[guide['originalOwnMaster']]:assert sha(ROOT/r['path'])==r['sha256']
prompt='''Create FIVE complete adult Marsh figures in a horizontal row with wide transparent gutters, all facing SOUTH toward viewer at the exact elevated frontal camera of reference ONE. Reference ONE selected fitted South idle is PRIMARY for small adult head, face, adult shoulder/waist/thigh/shin proportions, armour size and quiet warm matte pixel grade. Reference TWO older cargo-walk poses controls ONLY the existing slate waist-held crate, hand support, cargo occlusion and alternating walking phases; do not copy its larger head, dense detailing or broad upper body. Reference THREE original own South master preserves identity, swept blond hair, implant on screen LEFT temple, collar/chest plate/harness/pouches and ivory/sage/slate suit. Keep the same anatomical proportions and equipment scale in every figure.

Figures1-4 WALK WHILE CARRYING the SAME existing crate in BOTH hands at waist level, forearms supporting its sides, hands overlap side edges naturally. Slate rectangular box, restrained flat front recessed panel and two small ivory latches near upper corners, same width/height/depth and elevated perspective across all four. No extra logos/handles/bulky attachments. Crate rests across waist, chest/face fully visible; it occludes lower belt/pouches/hip exactly as cargo does. Never float box away from hands, merge fingers into box or change crate scale between steps.
1 LEFT contact/support: screen LEFT boot forward toward viewer, flat and lowest; RIGHT boot behind with heel lifted, gentle short cargo stride.
2 LEFT support/passing: LEFT boot flat under hip, RIGHT knee passing low with RIGHT boot slightly lifted; mild natural compression, no high knee or squat.
3 RIGHT contact/support: screen RIGHT boot forward toward viewer, flat and lowest; LEFT boot behind with heel lifted, opposite complete leg posture.
4 RIGHT support/passing: RIGHT boot flat under hip, LEFT knee passing low with LEFT boot slightly lifted. Both cargo hands remain supporting the same crate throughout. Gentle walking, no running or airborne phase.
5 EXACT NEUTRAL standing ruler matching reference ONE, arms down and NO CRATE, complete unobstructed body for common calibration.

All five SAME small adult head, fitted adult body, limb lengths and elevated South perspective. Neutral occupied147 high calibration, metadata148,184canvas,p92/172 at production; a calibration target, never per-pose fitting or cargo-width fitting. Cargo width is not anatomy. Warm ivory fabric and plates, muted sage shoulders/pouches, slate joints, charcoal gloves/soles, crisp restrained warm matte pixel clusters. Preserve authentic ankle hardware. FIVE complete connected hair-to-sole figures and transparent empty gutters, no floor/cast shadow/glow/haze/text/labels. No mirrored identity or new equipment.'''
p=S/'carry-01.prompt.txt';assert not p.exists();p.write_text(prompt+'\n',encoding='utf-8')
refs=[S/'selected-idle0-only.png',S/'carry-motion-guide.png',ROOT/guide['originalOwnMaster']['path']]
(S/'carry-01.request.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(p),'orderedReferences':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in refs],'sourceFrames':guide['primarySourceFrames']+guide['guideSourceFrames'],'sheetGrid':[5,1],'transparentBackground':True},indent=2)+'\n')
print('Frozen four complete alternating South cargo poses plus unobstructed neutral ruler.')
