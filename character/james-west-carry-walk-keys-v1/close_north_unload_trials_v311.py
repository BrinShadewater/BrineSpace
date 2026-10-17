from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();folders=[p/f'north-unload-bend-source-v{v}' for v in [310,311]]
for o in folders:
 d=json.loads((o/'inputs.json').read_bytes());assert sha(r/d['editTarget'])==d['editTargetSha256'];assert sha(o/'prompt.txt')==d['promptSha256'];g=json.loads((o/'generation.json').read_bytes());assert sha(o/'raw.png')==g['rawSha256']
o=folders[1];(o/'review.json').write_text(json.dumps(dict(disposition='rejected_before_native',rawAndNeighborBoardReviewed=True,crownDropPx=7,bootSoleRisePx=4,findings=['Smaller head descent than310, but boots rise from bottom225 to221 and legs look shortened rather than naturally flexed. Detached mark beneath feet in raw image. No body fitting or pixel erasure used to hide faults.'],normalChanged=False,selected=False,sourceAcceptance=False),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old);d['northUnloadBendSourceTrials']=dict(versions=[310,311],disposition='rejected_before_native',files=[(f/'review.json').relative_to(r).as_posix() for f in folders],normalChanged=False);d['nextVisualRepair']='311 shallow bend has modest crown descent but raises soles4px and shortens leg silhouette. Use specific planted-boot support reference for constrained source repair, then compare complete lower/return sequence.310 deep squat rejected.309 remains provisional; helmet/full-turn/carry master fidelity, actual arrival integration and whole-family consistency remain.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James north bend trials and planted-support constraint - October3,2026

V310/311 built-in edits of309 raw, exact prompts/target hashes frozen before
calls, raw receipts saved in checkout, whole nearest resize once to256. Both raw
and source-neighbor boards actually viewed; both REJECTED BEFORE native or normal
selection.310 crown descends26px versus requested approximate12, deep outward
knee squat makes hips bulky.311 restrained bend crown descends7px but soles rise
4px (bottom225to221), legs appear shortened and raw contains a detached mark below
feet. No body normalization, translation, resculpting or pixel erasure hides these
faults. Earlier30928check native static review remains its own evidence, not proof
for these trials.309 itself provisional, normal game unchanged, full goal incomplete.

Lesson: a modest silhouette-height decrease is not planted-foot proof. Separate
crown descent from boot support, leg articulation and gear/material identity.
Repeated verbal motion constraints drift; next constrained repair should use the
registered predecessor's actual boot support as explicit geometry reference and
review the whole descent/return. Do not promote a pose merely because it looks
smaller or the background is transparent. No new native run for rejected source.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-bend-source-v311/HANDOFF.md.
'''
guides=record_guides(r,section,'### James north unloading early bend source study')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James north unloading

## Objective and accepted direction
Complete master-matched full animation set and normal integration, then all-family
consistency/polish. Matte master identity/proportions; preserve belt wrench. Bend
height may lower but physical boot support must remain stable.

## Changed files/current state
310/311 frozen prompts/inputs, builtin raw sources/receipts, whole nearest256
exports, measured neighbor boards/rejections. Ledger and five maintained guides
updated. Both rejected before native;309 remains provisional,308 paired exact
turnend-to-unload0 cut retained. No normal selector/art replacement.

## Evidence and limitations
Both raw/neighbor boards viewed, target/prompt/raw hashes verified.310 drops26px
and creates bulky deep squat.311 drops crown7px but raises soles4px and shortens
leg appearance; raw detached mark. No procedural painting/fit/translation used.
No new native run, source approval or complete unloading motion proof.

## Next work
Explicit predecessor boot-support reference in constrained shallow-bend repair;
review actual knee articulation/support and whole lower/return. Complete helmet
fit, carry stop/turn start, turn material/height, controller arrival currently
bypassing turn, normal lifecycle/checkpoint/Continue/interruptions and all-family
consistency. Full goal active, no external blocker.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.iterdir() if f.suffix=='.png'];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(rejectedVersions=[310,311],nativeRuns=0,guides=guides,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
