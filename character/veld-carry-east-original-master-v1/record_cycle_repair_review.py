from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'native-cycle-art-repair-v1'
audit=json.loads((D/'AUDIT.json').read_text(encoding='utf-8'))
frozen=json.loads((R/'output/veld-east-native-stride-probe-v1/inputs-before.json').read_text(encoding='utf-8'))
changes=[p for p,h in frozen.items() if not (R/p).is_file() or hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
guide=json.loads((D/'INPUT.json').read_text(encoding='utf-8'))
guidechanges=[p for p,h in guide['bindings'].items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert not changes and not guidechanges,(changes,guidechanges)
verdict={'status':'Rejected full-cycle master-fidelity and grid-layout repair','artifactId':'exec-3792cae9-de82-4c2e-a153-4824acb96071','provider':'builtin imagegen','raw':'raw-cycle-repair-v1.png','prompt':'prompt.txt','audit':'AUDIT.json','priorAudit':'AUDIT-v0-gutter-contaminated.json','sourceCells':38,'standingCalibrationCell':38,'blankCellContamination':audit['blankCellsOpaquePixels'],'originalMaster':audit['master'],'returnedMaster':audit['rows'][38]['returned'],'ranges':audit['ranges'],'visualReview':'Complete returned atlas, original/detail comparison and all39 input/returned/original comparisons reviewed. Main bilateral phases broadly recognizable, but head, torso and case enlarge; body positions drift under fixed grid. Adjacent-row boot fragments occur in occupied and nominally blank cells. No preservation of exact38pose contact/phase geometry claimed. Pale outline reduced visually but not enough to offset identity/layout failures. Saturated flecks in initial tool view do not establish opaque material contamination; alpha-aware review supersedes that preliminary concern.','measurementCorrection':'V0 included previous-row boot fragments in the standing ruler. Corrected metrics isolate largest connected figure for measurement only; every returned pixel remains in extracted artwork. No per-cell recenter, rescale, RGB or anatomical repair.','frozenNativeInputsChecked':len(frozen),'frozenNativeInputChanges':changes,'originalGuideInputsChecked':len(guide['bindings']),'originalGuideInputChanges':guidechanges,'nativeRun':'Not run: rejected source already fails appearance and layout requirements. No candidate helmet or normal selection admission.','bindings':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'raw-cycle-repair-v1.png',D/'prompt.txt',D/'INPUT.json',D/'AUDIT.json',D/'audit_cycle.py']}}
(D/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
entry={'id':verdict['artifactId'],'idType':'builtin output artifact UUID','folder':D.name,'raw':D.name+'/raw-cycle-repair-v1.png','prompt':D.name+'/prompt.txt','status':verdict['status'],'verdict':D.name+'/VERDICT.json'}
ledger['generations']=[g for g in ledger['generations'] if g['id']!=entry['id']]+[entry]
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld complete-cycle appearance edit rejected — October 3, 2026'
note=title+'''\n\nBuiltin output exec-3792cae9-de82-4c2e-a153-4824acb96071 is retained in
character/veld-carry-east-original-master-v1/native-cycle-art-repair-v1 with exact
prompt/raw/39-cell comparisons/AUDIT/VERDICT. Input contains ALL38 bilateral poses
raw16..53 plus actual original native standing master,7x6 grid,last3 blank.
Returned1355x1161 redraw preserves broad alternating-leg chronology but violates
identity/layout. ONE common205-square plate/offset26,34 calibrated from standing
main component148: head33..35 vs original26, torso50..52 vs42; returned standing
itself head33/torso52,cloth62,61,61 vs66,64,63. Motion head axis123..131/floor223..238.
Blank cells carry223/192/189 alpha>20 pixels; previous-row boot fragments spill
into later cells. Complete atlas/detail and all39 three-way comparisons reviewed.

V0 ruler was contaminated by neighbour fragments and is retained INVALID for its
size/head claims. Corrected largest-component mask is for MEASUREMENT ONLY;
all raw pixels retained in extraction, no anatomy/region RGB/per-frame registration
rescue. Early coloured edge flecks in tool view are not a proven opaque material
defect; alpha-aware comparisons supersede that preliminary concern. Pale contour
is visually reduced but head/case/body growth and layout failure outweigh it.
308 previous native inputs and39 guide inputs hash unchanged. Source rejection
requires no native replay; no candidate helmet/normal selector adoption/new video.

Lessons: embedding the actual master as a calibration tile does not make a dense
atlas edit preserve its proportions or source layout. Verify the returned MASTER
as well as every motion pose; a shared height can hide broader head/torso growth.
Grid gutters and blank cells are part of the source contract. Exclude neighbour
fragments from measurements without deleting or repositioning returned artwork.
Next original faithful source contour/proportions and dense standing handoffs,
complete physical near/far contact/roll and ordinary runtime integration; full
direction/action/furniture/save/Continue acceptance and library polish remain.
Existing selected-library inventory includes swimming/death families, but inventory
alone does not establish original-master consistency or full runtime acceptance.
Full goal active/incomplete; generation terminal, no genuine blocker.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print(json.dumps({'verdict':verdict['status'],'previousNativeInputsUnchanged':len(frozen),'guideInputsUnchanged':len(guide['bindings']),'fullMotionCellsReviewed':38,'calibrationCellsReviewed':1}))
