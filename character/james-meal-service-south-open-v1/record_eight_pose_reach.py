"""Record source fidelity progress and bounded contact-depth evidence."""
from pathlib import Path
import json, os, hashlib
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'native-reach-candidate-evidence.json').read_text());v=json.loads((P/'native-reach-candidate-validation.json').read_text())
d=json.loads((P/'native-contact-depth-evidence.json').read_text());dv=json.loads((P/'native-contact-depth-validation.json').read_text())
f=json.loads((P/'native-contact-depth-fine-evidence.json').read_text());fv=json.loads((P/'native-contact-depth-fine-validation.json').read_text())
assert all(x['failures']==0 for x in [e,d,f]);assert all(x['exitCode']==0 and not x['timedOut'] for x in [v,dv,fv])
assert sorted(s['index'] for s in e['samples'])==list(range(8))
depth=json.loads((P/'depth-fine-comparison.json').read_text());assert depth['sharedContactDepth']==49
coarse=json.loads((P/'depth-comparison.json').read_text());assert next(x for x in coarse['rows'] if x['depth']==48)['differentPixelsFrom64']>0
m=json.loads((P/'reach-manifest.json').read_text());state=m['states'][0];assert state['depthOffsets']==[0,0,0,49,49,0,0,0]
frames=[]
for i in range(8):
 path=P/'depth-fine-captures'/f'contact-{i:02d}-depth-49.png' if i in [3,4] else P/'depth-fine-captures'/f'source-{i:02d}.png'
 im=Image.open(path).convert('RGB');view=Image.new('RGB',(432,458),'#303b40');view.paste(im,(0,26));ImageDraw.Draw(view).text((8,8),f'South pickup {i} / revised staged source / review restarts',fill='white');frames.append(view)
frames[0].save(P/'reach-native-review.gif',save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0)
audit=json.loads((P/'reach-foot-audit.json').read_text());reg=json.loads((P/'middle-pair-registration.json').read_text())
selection=json.loads((P/'selection.json').read_text());selection['status']='south_eight_pose_reach_staged_cup_returns_lifecycle_pending'
selection['reachCandidate'].update(frameCount=8,checks=e['checks'],failures=0,sourceVisualAcceptance=False,productionInstalled=False,remainingSourceDefects=['Other supported placements/rotations and adjacent props need context review before generic depth selection','Cup/returns/interruption/normal loader and Continue proofs remain'],middleSource='middle-pair-source.png',middlePrompt='middle-pair-prompt.txt',middleFixedScale=reg['fixedScale'],maxSoleBandShift=audit['maxAbsSoleShift'],materialCalibration='reach-material-calibration.json',depth=49,depthCoarseChecks=d['checks'],depthFineChecks=f['checks'],nativeDepthEvidence='depth-fine-comparison.json',ownerVisualAcceptance=False)
selection['reachCandidate']['exports']={p:hashlib.sha256((P/p).read_bytes()).hexdigest() for p in state['frameFiles']}
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
note='''

## James South eight-pose pickup / master palette — October 1, 2026

Full James/master/style/perspective/size/height/proportion/grade plus later full
cross-family polish goal stays active. Previous237green seven-pose candidate
retained under prior-seven-pose-reach: actor stayed planted, source boots drifted
4.612native px and lift jumped. New four-pose source middle-pair-source.png uses
canonical deep empty stance as a matching-pose crown/sole ruler: .20609756 across
all4whole figures. Only its independent middle-empty and middle-lift are used;
original max empty/contact and exact selected standing/held endpoints retained.
Eight complete poses/900ms at256/p128,224/H148. Sole-band maximum now2.092native
px; middle poses -.963left and -.052/-.298right against standing. This improves
source planting; the band metric alone is not a complete anatomy proof.

Same matte facing curve did not stop a source brightness flash: max empty neutral
median[76,74,74], contact[61,59,58]. Added one POOLed material transform per
independent source (shared across its poses), master neutral quantile curve and
gold RGB gain; warm pixels/alpha/anatomy retained, exact endpoint exports untouched.
Final neutral medians about[61..64,59..63,58..61], muted gold matching master.
No per-pose gain, body splices, limb painting, mirroring or per-part size fitting.
Whole edit prompts demanding density were insufficient: rejected prior lift
sources duplicated tools or changed skull/stance ruler; retained with prompts.

Actual corrected-source native239checks/0fail, all8selected textures, exact
registered held join, fixed actual supported South contact[48,128]. Engine0,
clean log/no timeout. Native2/4/5 reviewed: midpoint now connects empty reach and
bowl lift, matte grade coherent. Nine coarse depth samples266checks; fine empty
and grasp boundary293checks. Actual bowl48 offset still occluded193pixels;
49 matches64 exactly in bounded contact ROI, both empty/grasp. Staged manifest
reduces contact metadata64->49 only on max empty/grasp. The final GIF uses actual
49captures for those two poses. Minimum integer offset proves only this tested
open prep placement, not every layout/rotation/adjacent-prop context. Actual PNG
exports unchanged after metadata reduction. All scratch APPDATA; strict full
real-profile guards false,last_session.json only; attribution unproven.

Source/art metadata, audit, grade curves, scene captures/GIF and selected49 fine
evidence are in character/james-meal-service-south-open-v1. Eight-pose pre-palette
proof archived prior-eight-pose-before-palette. No production controller/loader
binding or owner visual acceptance/Continue claim. Next cup acquisition and bowl/
cup returns, correctly registered interruption prefixes and shared South lifecycle;
then normal binding, actual service journeys/Continue and remaining contexts/full
set polish. Keep North service/masters/paired equipment and belt identity intact.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes()
 if b'## James South eight-pose pickup / master palette' in old:continue
 data=note.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+note.encode()
 temp=path.with_name(path.name+'.james-eight-pose.tmp');temp.write_bytes(data);os.replace(temp,path)
handoff=P/'HANDOFF.md';handoff.write_text(handoff.read_text()+note)
print(json.dumps({'reachChecks':e['checks'],'depthChecks':[d['checks'],f['checks']],'contactDepth':49,'maxSoleBandShift':audit['maxAbsSoleShift'],'productionInstalled':False,'fullGoal':'active'}))
