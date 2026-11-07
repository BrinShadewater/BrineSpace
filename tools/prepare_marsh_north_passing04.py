"""Freeze a whole right-passing correction with selected body first."""
from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'character/marsh-north-run-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pose=ROOT/'character/marsh-north-run-material-v1/passing-03-unselected/right-passing.png'
target=S/'passing-04-whole-pose-guide.png'
Image.open(pose).convert('RGBA').resize((736,736),Image.Resampling.NEAREST).save(target)
prompt='''Create TWO complete rear-view NORTH Marsh figures, full bodies from blond hair to boots, horizontal row with wide clear transparent gutters. Reference ONE selected idle is PRIMARY for small adult head, fitted adult proportions, elevated rear camera, collar/back plate/harness/pouches and quiet warm matte pixel grade. Reference TWO is a complete right-support pose to CORRECT: keep its screen RIGHT flat supporting boot and screen LEFT raised boot, but change the whole posture into a LOW PASSING phase. Reference THREE own original rear master preserves identity, blond hair whorl, equipment and small right-temple edge. No face or side view.

FIGURE1 RIGHT-support LOW passing. Screen RIGHT boot is flat and lowest directly beneath hip, RIGHT knee slightly flexed for mild passing compression. Screen LEFT thigh nearly vertical beneath pelvis, LEFT knee gently flexed, LEFT whole boot raised only eight production rows above the flat right boot, instead of the much higher lifted boot in reference TWO. Both knees stay low near their neutral knee level, no high lifted thigh. BOTH elbows gently bent beside the waist, BOTH forearms foreshortened forward away from the viewer, BOTH hands near waist/pouches and above hip-bottom; neither arm hangs straight down like reference TWO. The two cuffs sit at similar waist height, small natural asymmetry only. This is the midpoint arm crossing between opposite contact swings. Preserve RIGHT support and raised LEFT charcoal sole; do not swap support. Same anatomical limb lengths, no shortened legs or body.

FIGURE2 exact rear neutral standing ruler matching reference ONE, arms down. Same head/torso/rigid equipment/limb size and rear projection in both figures, mild natural knee flexion only in passing. One common146 occupied neutral calibration, runtime metadata148, not forced per-pose dimensions. Warm ivory fabric/upper panels and back plate, muted sage shoulders/pouches, slate joints, charcoal gloves/soles. Crisp restrained warm matte pixel clusters matching selected body. Exactly TWO complete connected figures on transparent background; no floor, shadow, glow, haze, labels or text. No mirrored identity, extra equipment or altered back plate.'''
p=S/'passing-04.prompt.txt';assert not p.exists();p.write_text(prompt+'\n',encoding='utf-8')
refs=[S/'selected-idle0-only.png',target,ROOT/'character/marsh-motion-polish-v1/sources/north-standing-identity-01.png']
(S/'passing-04.request.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(p),'orderedReferences':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in refs],'poseSourceFrame':{'path':pose.relative_to(ROOT).as_posix(),'sha256':sha(pose)},'sheetGrid':[2,1],'transparentBackground':True},indent=2)+'\n')
print('Frozen whole low-passing arms/leg correction; selected idle first.')
