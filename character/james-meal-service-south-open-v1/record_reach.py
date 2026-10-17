"""Record actual candidate evidence, source defects, and full-goal open scope."""
from pathlib import Path
import json, os, hashlib
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'native-reach-candidate-evidence.json').read_text())
v=json.loads((P/'native-reach-candidate-validation.json').read_text())
assert e['failures']==0 and v['exitCode']==0 and not v['timedOut']
assert sorted(s['index'] for s in e['samples'])==list(range(7))
assert not any('ERROR:' in line for line in (P/'native-reach-candidate.log').read_text().splitlines())
m=json.loads((P/'reach-manifest.json').read_text());durations=m['states'][0]['frameDurationsMs']
frames=[]
for i in range(7):
 im=Image.open(P/'reach-captures'/f'source-{i:02d}.png').convert('RGB')
 view=Image.new('RGB',(432,458),'#303b40');view.paste(im,(0,26));ImageDraw.Draw(view).text((8,8),f'Candidate pickup pose {i} / staged / review restarts',fill='white');frames.append(view)
frames[0].save(P/'reach-native-review.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
audit=json.loads((P/'reach-foot-audit.json').read_text())
selection=json.loads((P/'selection.json').read_text());selection['status']='south_seven_pose_reach_staged_source_motion_polish_required'
selection['reachCandidate']={
 'manifest':'reach-manifest.json','sourceSheet':'reach-sheet-source-v2.png','prompt':'reach-sheet-prompt-v2.txt',
 'sourceSheetSha256':hashlib.sha256((P/'reach-sheet-source-v2.png').read_bytes()).hexdigest(),
 'wholeIndependentEmptyContactSource':'empty-contact-source.png','sourcePrompts':['empty-contact-prompt.txt'],
 'frameCount':7,'durationMs':sum(durations),'checks':e['checks'],'failures':e['failures'],
 'nativeReview':'reach-native-review.gif','footAudit':'reach-foot-audit.json',
 'sheetFixedScale':json.loads((P/'reach-registration.json').read_text())['scale'],
 'sourceVisualAcceptance':False,'productionInstalled':False,
 'remainingSourceDefects':['Frame2 sole-band left -4.612/right+3.457 native px versus standing: stance drift remains','Contact-to-retract still lacks intermediate lift; rejected lift sources contain duplicated tools then changed ruler/stance'],
 'strictProfileUnchanged':v['realProfileUnchanged'],'profileDelta':v['profileDelta']}
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
note='''

## James South seven-pose reach candidate — October 1, 2026

Full James animation/master/style/perspective/height/proportion/grade and later
cross-family polish goal remains active. Source v1 six-pose sheet is retained
rejected for large heads and widening deep stance. v2 improves both at one whole
147/467=.314775 ruler. Added whole independent empty-contact source at contact's
.13 ruler/boot anchor; this preserves deep torso/head/feet through grasp. Seven
frames/900ms now stage exact registered idle, early empty reach, deep empty,
empty contact, exact bowl contact, retract and exact held. Only whole source
extraction/translation/fixed density and existing matte grade; no limb paint,
mirroring/splicing or part scaling. Rejected lift v1 has duplicate belt tools;
tool correction v2 removes duplicates but changes source ruler/boot separation.
Both retained with exact prompts; neither is packaged. Same-source density
instructions alone are not evidence of preserved anatomical scale after edits.

Actual supported South chooser/player fixture:237checks/0fail, all7textures,
fixed actor contact/heading, registered exact held pixels at900ms, clean log,
engine0/no timeout, paired Godot-generated fixture UID. Reviewed native2/3/4/5
captures: empty hands advance to worktop before visible bowl grasp; depth64
remains diagnostic for max empty/contact only. This does NOT establish smooth
or fully master-consistent motion. Sole-band audit catches frame2 left-4.612,
right+3.457native px versus master despite unchanged actor foot; contact-to-
retract still jumps. Native actor planting cannot prove source boots planted.
Strict owner-profile guard false,last_session.json only; attribution unproven.
No production selection/loader change or owner visual acceptance. Artifacts in
character/james-meal-service-south-open-v1/reach-native-review.gif,
reach-master-contact.png, reach-foot-audit.json and native-reach-candidate reports.

Next correct whole deep-empty stance and independently author correctly scaled,
single-tool intermediate lift. Audit skull/shoulders/sole band and palette against
both master and adjacent sources, then native motion/appropriate contact depth.
Cup/returns/interruptions/normal binding/Continue and remaining contexts/full-set
polish stay open. Do not turn these narrow237checks into full-set acceptance.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
 old=f.read_bytes()
 if b'## James South seven-pose reach candidate' in old:continue
 data=note.encode()+b'\n'+old if f.name=='CURRENT_STATUS.md' else old+note.encode()
 tmp=f.with_name(f.name+'.james-reach.tmp');tmp.write_bytes(data);os.replace(tmp,f)
f=P/'HANDOFF.md';f.write_text(f.read_text()+note)
print(json.dumps({'checks':e['checks'],'drawnSourceCount':len(e['samples']),'sourcePolishRequired':True,'productionInstalled':False,'fullGoal':'active'}))
