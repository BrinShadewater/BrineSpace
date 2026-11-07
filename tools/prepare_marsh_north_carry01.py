"""Freeze rear cargo poses; carried crate remains in front and occluded."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'character/marsh-north-carry-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
guide=json.loads((S/'guide-provenance.json').read_text())
for r in guide['primarySourceFrames']+guide['guideSourceFrames']+guide['guideArtifacts']+[guide['originalOwnMaster']]:assert sha(ROOT/r['path'])==r['sha256']
prompt='''Create FIVE complete adult Marsh figures in a horizontal row, wide clear transparent gutters, all facing NORTH/AWAY at the exact elevated rear camera of reference ONE. Reference ONE selected fitted rear idle is PRIMARY for small adult head, shoulders/waist/limbs, rear collar/back plate/harness/pouches, drawing density and quiet warm matte pixel grade. Reference TWO older rear cargo-walk poses controls ONLY cargo-arm placement, rear occlusion and alternating walking phases; do not copy its broader head/upper body or dense grade. Reference THREE own original North master preserves blond hair whorl, original rear equipment and small RIGHT-temple implant edge. No face, side view or mirrored identity.

Figures1-4 WALK WHILE CARRYING the existing waist-level crate in BOTH HANDS IN FRONT OF THEIR BODY, away from viewer. In this exact REAR projection the crate and hands are OCCLUDED by torso/hips, as in reference TWO. Do NOT place a box on the back or behind pelvis. Do NOT reveal the front of the crate through the body. Both elbows stay softly bent beside waist, forearms angle forward away; side cuffs visible, hands hidden ahead. Rear plate/harness/pouches stay visible, complete body silhouette remains. Same anatomical head/torso/limb/equipment size in all four. Gentle short cargo walk, no running/high knee/deep crouch/airborne phase.
1 LEFT support/contact: screen LEFT boot flat and lowest, RIGHT boot trails lifted behind toward viewer, authentic charcoal sole underside visible if raised. Short natural cargo stride.
2 LEFT support/passing: LEFT flat boot beneath pelvis, RIGHT knee passes low with whole RIGHT boot modestly raised, mild knee compression. Both arms retain cargo hold.
3 RIGHT support/contact: screen RIGHT boot flat and lowest, LEFT boot trails lifted behind toward viewer, authentic raised charcoal sole. Opposite complete leg posture.
4 RIGHT support/passing: RIGHT flat boot beneath pelvis, LEFT knee passes low with modestly raised LEFT boot. Retain two-handed cargo posture and occlusion.
5 EXACT NEUTRAL rear standing ruler matching reference ONE, arms down and NO CARGO HOLD, complete unobstructed body for common calibration.

All five same fitted adult build/small head, elevated REAR perspective and quiet warm matte pixel style. Neutral146 occupied calibration, metadata148,184canvas,p92/172 at production; calibration only, no per-pose fitting. Preserve authentic ivory upper panels/back plate, muted sage shoulders/pouches, slate joints, charcoal gloves/soles and original ankle hardware. Hair/back plate/harness/hip/shin/boot proportions match selected rear body. FIVE complete connected hair-to-sole figures, wide transparent empty gutters; no floor/shadow/glow/haze/text/labels, no newly visible rear cargo or equipment.'''
p=S/'carry-01.prompt.txt';assert not p.exists();p.write_text(prompt+'\n',encoding='utf-8')
refs=[S/'selected-idle0-only.png',S/'carry-motion-guide.png',ROOT/guide['originalOwnMaster']['path']]
(S/'carry-01.request.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(p),'orderedReferences':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in refs],'sourceFrames':guide['primarySourceFrames']+guide['guideSourceFrames'],'guideToolDependencies':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in [ROOT/'tools/prepare_marsh_north_carry_guides.py',ROOT/'tools/prepare_marsh_south_carry_guides.py']],'sheetGrid':[5,1],'transparentBackground':True},indent=2)+'\n')
print('Frozen four complete rear cargo poses plus neutral; front crate stays occluded.')
