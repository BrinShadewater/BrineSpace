from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'character/krusher-cargo-family-v3';PROFILE=R/'character/krusher-cargo-settle-profile-v3'
read=lambda p:json.loads(p.read_text())
validation=read(P/'independent-validation.json');native=read(P/'review/native/report.json');run=read(P/'review/native/run-verification.json');media=read(P/'review/media.json')
assert not validation['errors'] and not validation['contactErrors'] and not native['errors'] and run['engineExit']==0 and not run['ownerFilesChanged']
encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(P/'review/cargo-preview.mp4')],text=True));assert abs(encoded-media['seconds'])<=1/60
media.update(encodedSeconds=encoded,scope='All171paired source slots replayed with original holds, concat1000fps inputs/output60fps/exact source duration cap. Not continuous native world recording.')
(P/'review/media.json').write_text(json.dumps(media,indent=2)+'\n')
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22);board=Image.new('RGBA',(1000,950),'#252b2e');draw=ImageDraw.Draw(board);draw.text((20,15),'KRUSHER DOM / CARGO HEAD FIT',font=font,fill='white');draw.text((20,45),'Original James motion / complete head and neck / matched visor fit',font=font,fill='#bed2d3')
for row,g in enumerate(['bare','helmet']):
 m=read(P/(g+'-manifest.json'));states={s['id']:s for s in m['states']}
 for col,(key,i) in enumerate([('carry-east',0),('carry-turn-east-north',2),('carry-turn-north-west',4)]):
  im=Image.open(P/states[key]['frameFiles'][i]).convert('RGBA').crop((58,35,198,230)).resize((280,390),Image.Resampling.NEAREST);x,y=col*333+25,row*430+115;board.alpha_composite(im,(x,y));draw.text((x,y-27),g+' / '+key.removeprefix('carry-'),font=font,fill='white')
board.save(H/'cargo-head-fit-sheet.png')
(P/'review/visual-review.json').write_text(json.dumps({'allChangedContexts':120,'sourceBoards':['source/heads-00.png','source/heads-01.png','source/heads-02.png'],'nativeViews':['bare-carry-turn-east-north-000.png','bare-carry-turn-east-north-002.png','helmet-carry-turn-north-west-003.png','helmet-carry-turn-north-west-004.png','helmet-carry-turn-north-west-005.png','bare-pickup-west-003.png'],'scope':'All120revised source head/collar contexts inspected; targeted real-display fullbody/game-size views reviewed, including corrected formerly detached turns and restored helmet hardware. Native source selection/gait/turn admission is not continuous station/world contact or owner acceptance.','pending':'Residual yellow shoulders/cyan audit, coherent all-family bank and station refresh.'},indent=2)+'\n')
handoff=f'''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Krusher cargo head correction

## Objective and acceptance
Complete Krusher animations with attached head/neck, clean brown hair and fitted helmet face. Goal active/incomplete. These H3 candidates supersede rejected head construction for this family only; owner/station acceptance not inferred from tests.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics; James utility suit, matte muted cyan #527C80. Original motion/clocks/pivots/density and case/hands retained. Station first; normal roster and owner saves not changed.

## Current state
Cargo-family-v3 and cargo-settle-profile-v3:50states/342frame refs/148unique/120revised,28rear retained. Original v1 full cargo manifests byte exact. Original nearest West-settle profile retargeted to whole v3 paths, all other fields exact. Complete H3 cardinal and new four quarter head/neck sources compose original v1 bodies. Raw generated-cargo-quarters.png, exact cargo-quarter-prompt.txt, cargo-quarter-extraction.json and extract_cargo_quarters.py preserve builtin generation/alpha/hash and nearest native sizing. No invented body or neck bridges.
Two East-to-North turns initially detached; original body retained and complete authored heads registered down4px(frame0) and2px(frame2). Tiny disconnected inherited face fragments removed only within original head envelopes, never current head or connected body. North-to-West bare4 inherited profile-nose fragments connected only by faint alpha removed from observed [110,78,114,97] envelope above shoulder. Previous rejected source boards retained under review/rejected-head-contact. North-to-West helmet pose4's old warm-metal face hull had painted original shell; original helmet RGB restored outside explicit observed narrow visor polygon. Independent restored-shell pixels check added.
Build_cargo.py, cargo-family-v3/validate.py, prepare_cargo_review.py, cargo_source_boards.py and record_cargo.py retain reproducible proof. New mobile cargo-head-fit-sheet.png, full original-hold paired review/cargo-preview.mp4 and HTML. Whole selected bank/package still old pending coherent full-library migration.

## Verification
1549independent checks0:all342refs/148hashes/canvases/body masks and protected lower body, original helmet alpha, full manifests, original root/clocks/stride/state flags,63complete bare-head source/mainbody contact checks,64join comparisons preserving12source-equal joins, original nearest settle profile, restored shell. All120changed source contexts on3boards inspected; targeted native fullbody/game-size formerly detached turns, intermediate quarter, restored shell and West pickup reviewed.
Final native4482checks0/154prescribed captures/engine0/{run['seconds']:.2f}s/noerrors.1920distance-driven carry ticks visit all6gait poses;24automatic turns source-select correctly. Scratch APPDATA;{run['ownerFilesFingerprinted']}owner nonlog files unchanged. Own .gd/.uid paired.
171paired source slots replay20.880s, encoded{encoded:.6f}s within1frame. Every concat input including final1000fps; output60fps/exact duration cap. Not continuous native station footage, strict West release/service-loss, or final body/department palette acceptance. Original yellow shoulder trim remains visible pending palette pass. LFS raw PNG/MP4 filters confirmed; no commits.

## Next action
Remaining rest/water-cargo/interruption/death/recovery head migration, rear/quarter identity and yellow-to-muted-cyan shoulder audit. Coherent full bank/package, strict West cue retargeting and observed service-loss diagnosis, then changed actual station/bare-water/full-library checks. No live generation/native process, approval gate or blocker.
'''
for target in [H/'CARGO_HANDOFF.md',P/'HANDOFF.md',PROFILE/'HANDOFF.md']:target.write_text(handoff,encoding='utf-8')
progress=R/'character/krusher-complete-animation-v1/progress.json';d=read(progress);v=d['visualReview'];v['status']='head-construction-v3-water-canonical-inspection-actions-meals-equipment-cargo-partial';v['remaining']='Remaining rest/water-cargo/interruption/death/recovery head migration; rear/quarter identity and residual yellow shoulder cyan palette pass; coherent full bank/package; strict West cues/service-loss and changed actual station/bare-water/full-library closeout.'
v['headConstructionV3']['cargo']={'manifests':['res://character/krusher-cargo-family-v3/bare-manifest.json','res://character/krusher-cargo-family-v3/helmet-manifest.json','res://character/krusher-cargo-settle-profile-v3/bare-manifest.json','res://character/krusher-cargo-settle-profile-v3/helmet-manifest.json'],'states':50,'refs':342,'unique':148,'revised':120,'independentChecks':1549,'bareHeadContactChecks':63,'nativeChecks':4482,'nativeCaptures':154,'ownerFilesUnchanged':run['ownerFilesFingerprinted'],'scope':'Partial H3 complete-head migration. Original bodies/clocks/case/pivots retained; all120source contexts reviewed. Existing full-bank selection unchanged; no station acceptance.','handoff':'res://character/krusher-head-fit-v3/CARGO_HANDOFF.md'}
progress.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
original=(H/'update_actions_status.ps1').read_text();start=original.index('    $krusherHeader = @'+chr(39));end=original.index('\n'+chr(39)+'@',start)+3
header=f'''## Krusher cargo complete-head candidate - October 4, 2026

Full goal active/incomplete. Cargo-family-v3/cargo-settle-profile-v3:50states,
342refs/148unique/120revised/28rear retained. Original whole cargo manifests,
body/case/hands/lower body, helmet alpha and clocks preserved; nearest West
settle root profile exact except whole candidate paths. New four quarter full
head/neck masters preserve builtin raw/prompt/alpha extraction/native hashes.
Detached East-to-North poses registered whole heads down4/2pixels; inherited
isolated face scraps removed, no painted neck. North-to-West helm4 restored
original hardware outside observed visor polygon (old warm-metal hull error).
1549independent checks0/63complete bare source/topology/collar contacts,
64join comparisons/12source-equal joins. All120changed contexts/3boards and
targeted native full/small formerly detached/quarter/restored shell views reviewed.
Final native4482checks0/154captures/engine0/{run['seconds']:.2f}s;1920distance-driven gait
ticks/24automatic turns. ScratchAPPDATA;{run['ownerFilesFingerprinted']}owner nonlog files unchanged.
171paired source holds20.880s/encoded{encoded:.6f}s within1frame; not continuous
station/world contact acceptance. Mobile overview/HTML/MP4 delivered. Full selected
bank remains old; residual yellow shoulders remain open for cyan palette audit.
Next rest/water-cargo/interruption/death/recovery, rear/quarter/cyan audit,
coherent bank/package, strict West cues/service-loss and station/barewater refresh.
Handoff:character/krusher-head-fit-v3/CARGO_HANDOFF.md. No live job/approval gate.

'''
new=original[:start]+'    $krusherHeader = @'+chr(39)+'\n'+header+chr(39)+'@'+original[end:];new=new.replace('CURRENT_STATUS.krusher-head-construction-actions.tmp','CURRENT_STATUS.krusher-head-construction-cargo.tmp');(H/'update_cargo_status.ps1').write_text(new,encoding='utf-8')
print(json.dumps({'status':'active-incomplete','selectedBankChanged':False,'handoff':'character/krusher-head-fit-v3/CARGO_HANDOFF.md'}))
