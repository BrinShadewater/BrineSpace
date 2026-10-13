"""Freeze a targeted complete RIGHT-support passing pose and neutral ruler."""
from pathlib import Path
from PIL import Image
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'character/marsh-north-run-material-v1/sources'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
pose = ROOT / 'character/marsh-north-run-material-v1/contacts-02-unselected/right-contact.png'
target = S / 'passing-03-right-support-guide.png'
Image.open(pose).convert('RGBA').resize((736,736), Image.Resampling.NEAREST).save(target)
prompt = '''Draw TWO complete NORTH/rear-view adult Marsh figures in a horizontal row with wide transparent empty gutters. Figure1 is a running RIGHT-SUPPORT PASSING pose. Figure2 is a neutral standing ruler. Reference ONE is the correct RIGHT supporting leg arrangement, a complete unchanged rear figure: the screen RIGHT leg is straight down to the LOWEST FLAT boot; screen LEFT leg bends with its whole boot raised, charcoal sole visible. Retain this exact support arrangement in figure1. Move only the complete posture into gentle passing: RIGHT boot flat directly beneath right hip, LEFT thigh lowered closer to pelvis, LEFT knee only mildly bent, its entire LEFT boot still clearly above the flat RIGHT boot by about eight production rows. BOTH arms near waist with modest bent elbows, no dangling contact arm, no high knee, no crouch. Screen RIGHT foot supports. Screen LEFT foot is raised. Do not repeat left support.

Reference TWO selected North idle is PRIMARY for adult body and small head proportions, elevated rear camera, fitted shoulders/waist/limbs, collar/back plate/harness/pouches and quiet warm matte pixel grade. Reference THREE original own North master controls blond hair whorl, rear equipment and small right-temple edge. Match selected neutral body size throughout. Figure2 exact neutral selected North standing ruler, arms down. One common146 occupied neutral calibration, metadata148, not pose-specific fitting. Same head/torso/limb/rigid plate scale in both figures, natural small running compression only. Warm ivory fabric/upper panels, muted sage shoulders/pouches, slate joints, charcoal gloves and authentic raised soles. Preserve connected whole anatomy, rear view, no face or side profile. TWO complete hair-to-sole figures on transparent background, crisp warm matte pixel clusters, no shadows/floor/glow/haze/labels/text. No mirrored identity or equipment.'''
path = S / 'passing-03.prompt.txt'
assert not path.exists()
path.write_text(prompt + '\n', encoding='utf-8')
refs = [target, S/'selected-idle0-only.png', ROOT/'character/marsh-motion-polish-v1/sources/north-standing-identity-01.png']
(S/'passing-03.request.json').write_text(json.dumps({'normalAdmission':False, 'fullGoalComplete':False, 'status':'frozen before generation', 'promptSha256':sha(path), 'orderedReferences':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in refs], 'poseSourceFrame':{'path':pose.relative_to(ROOT).as_posix(),'sha256':sha(pose)}, 'sheetGrid':[2,1], 'transparentBackground':True}, indent=2)+'\n')
print('Frozen complete RIGHT-support passing request and original ordered references.')
