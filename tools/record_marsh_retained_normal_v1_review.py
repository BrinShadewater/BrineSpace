from pathlib import Path
import json,hashlib
root=Path.cwd();b=root/'character/marsh-retained-gesture-material-v1';normal=root/'character/marsh-v2/supplemental/retained-gesture-return-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for d,v in [('west','04'),('north','03'),('south','04')]:
 p=b/f'{d}-return{v}-unselected/selection.json';r=json.loads(p.read_text());assert sha(root/r['board']['path'])==r['board']['sha256'];r['board']['actuallyInspected']=True;r['normalAdmission']=True;r['admissionReceipt']='character/marsh-v2/supplemental/retained-gesture-return-v1/admission.json';p.write_text(json.dumps(r,indent=2)+'\n')
p=b/'cardinal04-unselected/verification.json';r=json.loads(p.read_text())
for board in r['nativeEvidence']['boards']:
 if board['direction']=='east':assert sha(root/board['path'])==sha(b/'cardinal03-unselected/east-native-contact.png')
 board['actuallyInspected']=True
r['normalAdmission']=True;r['normalAdmissionEvidence']={'path':(normal/'admission.json').relative_to(root).as_posix(),'sha256':sha(normal/'admission.json')};r['browserEvidence']={'viewerSha256':sha(b/'cardinal04-unselected/index.html'),'allSourcesLoaded':True,'returnSlotMs':601,'postFixClock':{'firstMs':116,'firstTicks':8,'laterMs':57963,'laterTicks':3454},'initialErrors':2,'newErrorsAfterClockFix':0,'fix':'Clamp negative first frame delta to0 before accumulating elapsed time.','method':'Advancing clock and sampled source/station screenshots; not continuously watched cadence.','screenshot':{'path':(b/'cardinal04-unselected/viewer-return-fixed.jpg').relative_to(root).as_posix(),'sha256':sha(b/'cardinal04-unselected/viewer-return-fixed.jpg'),'actuallyInspected':True}}
p.write_text(json.dumps(r,indent=2)+'\n')
p=normal/'verification.json';r=json.loads(p.read_text())
for board in r['nativeEvidence']['boards']:
 other=b/'cardinal04-unselected'/Path(board['path']).name;assert sha(root/board['path'])==sha(other);board['actuallyInspected']=True;board['reviewMethod']='Byte-identical to reviewed staged native board; East also matches earlier return06 board.'
r['normalAdmission']=True;r['admissionReceiptSha256']=sha(normal/'admission.json');r['fullGoalComplete']=False;p.write_text(json.dumps(r,indent=2)+'\n')
parts=['# Marsh selected retained generic gesture source prompts\n\nBuilt-in image generation. First3 whole poses per direction retain prior source; last uses new whole return. North selects new cell2, other directions new cell3. No anatomical fragment mixing.\n']
for d,v in [('east','04'),('east','06'),('west','03'),('west','04'),('north','02'),('north','03'),('south','03'),('south','04')]:
 q=json.loads((b/f'sources/{d}-gesture-{v}.request.json').read_text());parts.append(f"\n## {d}{v}\nGeneration: {q['result']['generationId']}\nSource SHA: {q['result']['sha256']}\n\n{q['prompt']}\n")
(normal/'prompts.md').write_text(''.join(parts),encoding='utf-8')
note='''
## Marsh retained generic gesture normal admission — October3,2026

Normal catalogue now selects a coherent four-direction retained generic gesture
bank: character/marsh-v2/supplemental/retained-gesture-return-v1.8latent aliases,
48ordered slots,24whole PNG copies, original six150ms finite holds and exact own
idle endpoints. Exactly8states changed;228normal body states remain,220unchanged.
No actual helmet capability/controller/room/save behavior enabled or altered.
This is source admission during ongoing polish, not owner/full-set visual acceptance.

First3whole gestures remain East04/West03/North02/South03. Return sources are
East06 cell3,West04 cell3,North03 cell2,South04 cell3. North generator changed
third pose too; its cell2 provides the appropriate right-glove waist intermediate.
Using cell3 would introduce a late left-hand pulse; selected right-lowering sequence
keeps the left arm relaxed. Record actual source cell, never infer from prompt.
Each strip uses ONE own-neutral-derived density, no per-pose fit/head/limb splice.
New West heights611/611/611/611/610,factor147/610, neutral32.533vs31;
North705×5,factor146/705, neutral55.501vs55; South626/627/626/626/626,
factor147/626, neutral57.532vs58. Full new strips were not substituted for stronger
prior poses.17raw/request/reference/source receipts verified; exact selected8source
prompts saved alongside normal admission. Each three new candidate APNGs decodes
6exact frames/900ms. Three whole-source comparison boards inspected.

Staged cardinal04 native762checks/208samples/24player restores/24captures passed,
1096bounded inputs and2931owner files stable,0Godot errors/warnings/failures/exit0.
West/North/South complete native boards inspected; East board byte-identical to
previously inspected return06. Normal-catalogue follow-up790checks loads actual
228body states and equipment profiles for28players, verifies48selected source slots,
208presentations/24restores/captures.3974bounded inputs and2931owner non-log files
unchanged under scratchAPPDATA,0Godot errors/warnings/failures/exit0. All four normal
native boards byte-identical to reviewed staged boards. This is NOT sampled motion
acceptance for every228state or live actor/contact/fullSave/titleContinue proof.

Timed preview first failed: negative initial rAF timestamp delta could produce
slot-1 and undefined-image error. Clamp delta>=0. After reload, elapsed116→57963ms
and advancing ticks8→3454; sources loaded, pause/restart/step verified, no NEW
errors after fix (two earlier errors retained). Screenshot of all four return poses
actually inspected at source/station height. Clock plus sampled snapshots does not
certify continuous cadence; body/head/boot/material joins still deserve polish.
Do not hide failing timing with a still frame or claim a browser clock is gameplay.

Current authoritative normal inventory:
character/marsh-selected-normal-audit-2026-10-03-post-gesture/inventory.json,
228states1190slots78ordered body manifests. Compared with earlier private-augmented
full-family audit:56states differ,0added/removed.8are these admitted gestures;
48are dry carry/pickup/unload/turn and loaded-water/pickup/drain states. Reconcile
those normal sources with reviewed private candidates next; do not treat dated
private/native evidence as proof of current normal selection. Full Marsh goal active.
'''
canonical=root/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert canonical.read_bytes()==installed.read_bytes()
for p in [root/'character/ANIMATION_PIPELINE.md',root/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',root/'docs/CURRENT_STATUS.md',canonical]:
 with p.open('rb') as f:f.seek(max(0,p.stat().st_size-100000));tail=f.read().decode('utf-8',errors='ignore')
 if '## Marsh retained generic gesture normal admission' not in tail:
  with p.open('a',encoding='utf-8') as f:f.write(note)
installed.write_bytes(canonical.read_bytes());print('Normal admission, reviews, preview fix, current228state inventory and remaining48state reconciliation documented')
