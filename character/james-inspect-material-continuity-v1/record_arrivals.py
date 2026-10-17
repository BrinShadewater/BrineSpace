from pathlib import Path
import json,os
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'native-arrival-continue-evidence.json').read_text());v=json.loads((P/'native-arrival-continue-validation.json').read_text());assert e['failures']==0 and len(e['results'])==8 and v['exitCode']==0 and not v['timedOut'];assert all(x['freshSceneMidpointContinue'] and x['actualMove'] and x['arrived']==x['incoming'] for x in e['results']);assert 'ERROR:' not in (P/'native-arrival-continue.log').read_text(encoding='utf-8')
board=Image.new('RGB',(960,8*344),'#303b40');draw=ImageDraw.Draw(board)
for row,x in enumerate(e['results']):
    for col,path in enumerate(x['captures']):
        im=Image.open(R/path.removeprefix('res://')).convert('RGB');im.thumbnail((320,320),Image.Resampling.LANCZOS);board.paste(im,(col*320+(320-im.width)//2,row*344+24));draw.text((col*320+6,row*344+8),x['mode']+' '+x['incoming']+' '+['entry','read / save','stowed / resumed'][col],fill='white')
board.save(P/'native-arrival-continue-review.png')
s=json.loads((P/'selection.json').read_text());s['actualDiagnosticApproachContinue']={'checks':e['checks'],'actualDryApproaches':8,'freshSceneDiskContinues':8,'allSourceSlots':1130,'captures':24,'clockActorPlaybackPausePixelsExact':True,'strictProfileUnchanged':v['realProfileUnchanged'],'profileDelta':v['profileDelta'],'scope':e['scope']};s['headMotionReview']={'allFrameHeadStrips':8,'sourceFrames':1130,'helmetCrownAdjacentSteps':1,'helmetCrownCenterAdjacentSteps':1.0,'soleAll171':True,'note':'All eight head strips and four bare bounded tool strips reviewed. Natural pitched bare head and translated common helmet retained; no new body or shell fit. Bounding diagnostics are not full anatomy proof.'};s['knownSourceDefect']={'east':'frames8..24 wrench leaves belt and becomes tablet; also reversed source descent. Colour fix did not repair this. Full-source replacement job staged separately, current source remains selected pending whole-motion review.','detail':'east-tablet-lift-detail.png','replacement':'character/james-tablet-east-belt-fixed-source-v1'}
(P/'selection.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
note='''

## James diagnostics Continue and East prop transformation — October 1, 2026

Selected material revision now checked through8 actual collision-checked dry
generic approaches (four facings/bare+helmet), all1130 source slots in NPC.update,
8 fresh-scene midpoint disk Continues retaining actor/playback/clock/pause/pixels,
fixed foot/facing/gear, six-second completion and normal need relief.4734checks,
0failures,24native captures; engine0/scratch/no timeout with600s eight-scene runner.
Strict owner guard false,last_session.json only, cause unproven. Not autonomous
pathfinder, actual locker/gear changes, workstation-specific rotation or exterior.

All8head strips/1130 references reviewed; helmet crown and crown-center adjacent
steps at most1pixel, soles171 throughout. Pitched bare head/common shell movement
retained. Four bounded bare hand/tablet/belt strips inspected. East8..24 exposes
actual wrench-to-tablet transformation: wrench leaves belt in lift, then meter
appears. Source/material checks and green loader tests do not prove prop identity.
This defect remains in selected motion; do not claim wrench continuity accepted.
Detail east-tablet-lift-detail.png. Full-motion remake from exact selected master
submitted once in james-tablet-east-belt-fixed-source-v1; preserve task ledger/poll
same job, no blind retry. Separate rectangular tablet pouch, fixed belt wrench.

Fixture save fixes preserve strict validator: original arrival fixture had oxygen
100 exceeding60tank/15breath, fabricated roster, then cleared required wreck
registry. Use normal capacities and real core release; retain architect/wreck
registry. Old240s run expired before all8fresh scenes finished; retained incomplete
report. Same full scope passes with600s runner, preserving scratch/fingerprint.
Full James/master/perspective/size/anatomy/grade and cross-family polish goal active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James diagnostics Continue and East prop transformation' not in data:
        enc=note.encode('utf-8');updated=enc.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+enc;tmp=path.with_name(path.name+'.tablet-continue.tmp');tmp.write_bytes(updated);os.replace(tmp,path)
h=P/'HANDOFF.md';text=h.read_text(encoding='utf-8');text+='''

## October1 continuation milestone
Actual8 dry authored collision-checked approaches and8 fresh midpoint disk
Continues4734pass; all1130 source slots, fixed foot/facing/gear, normal6s need relief,
actor/playback/pixels/clock/pause exact.24scene captures. Strict guard false only
last_session.json; no owner rollback. Same scope extended from240s to600s after
terminal timeout. Corrected fixture oxygen/real core roster/wreck registry; no
production save schema/validator change. Eight all-frame head strips and four bare
bounded tool strips reviewed. East tool morph found, remains selected; cannot claim
wrench continuity. Exact-master full-motion replacement job submitted once in
../james-tablet-east-belt-fixed-source-v1. Next poll saved task, review complete raw
clip, fix/package full East diagnostics motion if acceptable, then remaining
workstation/gear/physical and cross-family scopes. Native job terminal; generation
is separately pending and must be re-polled by its saved task ID.
''';h.write_text(text,encoding='utf-8')
candidate=R/'character/james-tablet-east-belt-fixed-source-v1';(candidate/'HANDOFF.md').write_text('''# Project handoff

Updated: October1,2026 · Project: Brine Space · Task: East diagnostics prop identity

## Objective and acceptance
Replace full East tablet draw/read/stow motion while wrench stays attached to belt;
master identity/material/proportions/perspective/size and planted feet remain.

## Accepted decisions and constraints
Exact selected directional master reused, separate rectangular graphite tablet
pouch. Existing routine direct video authorization. One submission, no blind retry.

## Current state
Exact native master/4x green reference and prompt saved. MiniMax single task in
generation.json. Original source remains installed. Defect closeup resides in
../james-inspect-material-continuity-v1/east-tablet-lift-detail.png.

## Verification
Input/source hashes checked against current exact idle. New generation pending;
no new source motion/registration/helmet/native or owner acceptance yet.
Prior current source completes8 actual generic approaches/Continues4734checks,
but that proves clock/save playback and does not repair wrench transformation.

## Next action
Poll generation.json same task; inspect complete raw motion. Freeze one master
ruler/material treatment, retain full authored motion, fit accepted shared shell
if selected and preserve exact endpoints. Review all tool/body/head poses and
normal NPC/source-clock/Continue handoffs before switching current source.
Full James goal active.
''',encoding='utf-8')
print(json.dumps({'checks':e['checks'],'actualApproaches':8,'diskContinues':8,'allSourceReferences':1130,'EastPropDefect':'confirmed; replacement source pending','fullGoal':'active'}))
