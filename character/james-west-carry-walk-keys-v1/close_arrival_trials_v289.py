from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();audit=p/'arrival-turn-audit-v287';d=json.loads((audit/'inputs.json').read_bytes());assert all(sha(r/s['file'])==s['sha256'] for s in d['sources'])
(audit/'review.json').write_text(json.dumps(dict(chronologyBoardVisuallyReviewed=True,existingTurnPresent=True,runtimeSelection='carry-turn-west-north exists, but workshop arrival changes state carry to unload before generic carry-facing transition can run.',findings=['Existing six-pose turn800ms has broader torso/different detail and helmet height changes versus latest carry and north-unload endpoints.', 'Normal load order retains old west-north turn; return-bridgeV9 and helmet-dip override other states. Existence alone does not establish latest endpoint compatibility.'],normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
for version,execution in [(288,'44c2af0d-a3a4-4269-9450-e395bf76292d'),(289,'a8a39d8e-21b5-40a0-a71d-9582a9cf409a')]:
 o=p/f'arrival-turn-source-v{version}';i=json.loads((o/'inputs.json').read_bytes());assert all(sha(r/f)==h for f,h in i['referenceSha256'].items());assert sha(o/'prompt.txt')==i['promptSha256'];m=json.loads((o/'registration-diagnostic.json').read_bytes())
 reason='165px figure, crown62/sole226 after fixed256canvas conversion, versus148ruler/crown76/sole224. Large head/body and high placement.' if version==288 else '144px figure, crown65/sole208 after fixed256canvas conversion. Sole16px above pivot224 and body4px shorter than148; registration/fidelity cannot be repaired by body-fit scaling.'
 (o/'review.json').write_text(json.dumps(dict(disposition='rejected_before_native',rawVisuallyReviewed=True,endpointBoardReviewed=True,diagnostic=m,reason=reason,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,next='Edit already registered planted original turn pose as geometry target; original master is material/identity reference. Validate source extent, head/body proportions, perspective, tools and joins before helmet/native.'),indent=2)+'\n')
 (o/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,method='builtin_imagegen_whole_intermediate_turn',rawSha256=sha(o/'raw.png'),prompt='prompt.txt',disposition='rejected_before_native'),indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old);j['arrivalTurnReview']=dict(auditVersion=287,rejectedSourceTrials=[288,289],normalChanged=False);j['nextVisualRepair']='Arrival turn exists but mismatches latest endpoints and state carry->unload bypasses generic turn. Whole-source288/289 rejected for height/baseline. Next edit existing registered planted turn geometry with original-master material/identity references; exact source joins before shared helmet/lifecycle. Moving stance contacts, complete master fidelity and all-family polish remain.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James arrival-turn coverage and rejected whole-pose placement trials - October3,2026

V287 current latest west0 / existing six west-north turn / joined north-unload0
paired chronology inspected. Existing turn800ms is present, but current arrival
changes carry to unload, bypassing generic carry-facing turn selection. Old turn
has broader torso, different material and helmet-height changes; cannot connect
latest sources by wiring alone. V9 return/dip overlays do not replace this turn.

Two independent builtin whole intermediate poses with frozen master/endpoints:
V288 fixed canvas1254to256 gives165height,crown62,sole226; REJECTED.
V289 fraction/normalized placement retry gives144height,crown65,sole208; REJECTED.
Both raw and endpoint boards viewed; orientation/planted boots plausible but
height/registration incompatible. No body-fit rescale or translation to mask
proportion failure, no helmet/package/native/normal adoption. All frozen inputs
stable; generation terminal. Requested output1024 was actually1254 and numeric or
fractional placement instructions did not enforce the target canvas occupancy.

Lesson: output-size/coordinate instructions are not registration proof. Keep
original-master identity/material reference distinct from pose/canvas geometry;
a large full master can dominate requested source occupancy. Next use an existing
registered planted turn pose as geometry edit target, validate full source and
exact endpoint joins before helmet and actual arrival lifecycle. Whole moving
contact, master proportions/grade/helmet and all-family consistency remain.
Goal active/incomplete. Handoff:
character/james-west-carry-walk-keys-v1/arrival-turn-audit-v287/HANDOFF.md.
'''
guides=record_guides(r,section,'### James latest49 actual room distance coupling and arrival join')
handoff='''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James arrival-turn authoring

## Objective and acceptance
Full master-matched James animation set, complete lifecycle and cross-family polish.

## Accepted decisions and constraints
Matte master identity/grade/geometry, belt wrench, forward torch, diagnostics tablet.
Preserve native148ruler/pivot128224. Do not fit generated bodies to hide drift.

## Current state
V287 paired eight-cell turn chronology and coverage audit. Existing west-north turn
800ms differs from latest walk endpoints; arrival state switch bypasses generic turn.
V288/V289 independent whole bare-midpoint trials saved with prompts/references/raw,
fixed global canvas sources, endpoint boards, diagnostics and rejection records.
Latest ledger/five guides updated. No normal code/art selections changed.

## Verification
All16frozen existing sources stable; both generation input/prompt hashes verified,
raw and endpoint boards viewed.288height165/crown62/sole226;289height144/crown65/
sole208. Both rejected before helmet/native. Original endpoints untouched.

## Next action
Edit existing registered planted turn pose for original-master material/identity,
using separate pose and style references. Verify height, anatomical proportions,
equipment, camera and exact joins; then shared helmet and arrival lifecycle wiring.
Track planted feet against root movement; normal checkpoint adoption/interruptions/
Continue, complete action coverage and all-family consistency/polish remain.
'''
for name in ['arrival-turn-audit-v287','arrival-turn-source-v288','arrival-turn-source-v289']:(p/name/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for name in ['arrival-turn-audit-v287','arrival-turn-source-v288','arrival-turn-source-v289'] for f in (p/name).glob('*.png')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(existingTurnSourcesReviewed=16,rejectedWholeSources=2,guides=guides,lfsRasters=len(rasters),normalChanged=False,goalComplete=False)))
