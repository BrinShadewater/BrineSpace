from pathlib import Path
import json, hashlib, subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent; r=p.parents[1]; o=p/'north-unload-return-match-v319'
sha=lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((o/'inputs.json').read_bytes())
assert all(sha(r/f)==h for f,h in d['references'].items())
assert sha(o/'prompt.txt')==d['promptSha256']
g=json.loads((o/'generation.json').read_bytes()); assert sha(o/'raw.png')==g['rawSha256']
m=json.loads((o/'source-measurements.json').read_bytes())['sources']
assert m[1]['boundsAlpha128']==[90,106,165,224]
assert m[2]['boundsAlpha128']==[89,97,166,218]
master=r/'character/branforth-west-direct-v2/master-input.png'
review=dict(disposition='rejected_before_native',rawAndNeighborBoardReviewed=True,originalMasterReviewed=True,originalMaster=master.relative_to(r).as_posix(),originalMasterSha256=sha(master),crownRisePx=9,soleRisePx=6,widthChangePx=2,findings=['Appearance-neighbor edit raises crown9px and soles6px despite preserving bent pose being requested. Silhouette becomes2px broader, so it does not repair bulk discontinuity. Coarse quilt, equipment and hand proportions still differ across neighboring poses and from original master material identity. West master is appearance authority, not rear-view geometry.'],normalChanged=False,selected=False,sourceAcceptance=False,nativeRuns=0)
(o/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json'; old=ledger.read_bytes(); d=json.loads(old)
d['northUnloadReturnMatchTrial']=dict(version=319,review=(o/'review.json').relative_to(r).as_posix(),disposition='rejected_before_native',normalChanged=False)
d['nextVisualRepair']='319 neighbor-appearance transfer raises soles6px, crown9px and widens body2px. Reject without correction by translation. Return to original unload4 geometry as target; use actual original master fabric/hardware appearance and constrained neighbor identity. Review complete low/return/rise chronology before native.317 seven-pose bank remains provisional; helmet, actual arrival selection, lifecycle and all-family polish remain.'
assert ledger.read_bytes()==old; ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James unloading appearance-transfer rejection - October3,2026

V319 built-in transparent edit of316 bent return, with317 next rise as appearance
reference only. Frozen prompt/reference hashes and raw receipt preserved. Whole
1254 canvas nearest resize to256 once; raw and five-pose neighbor board viewed.
Rejected before native: crown rises9px (106to97), soles rise6px (224to218), width
increases2px (75to77). Bulk discontinuity persists. No translation, body fitting,
painting or grading masks the failed pose. Original West master viewed separately:
quilt/hardware/hand identity still differs;317 is a candidate, not master authority.
Current317 seven-pose bank and normal runtime remain unchanged and provisional.

Lesson: asking an appearance reference not to change geometry does not prove that
geometry was preserved. Compare crown, soles, actual limb articulation and body
bulk independently before native packaging. Avoid compounding generated-pose
drift: next return repair starts with original unload4 geometry and actual master
material reference. The West master supplies appearance, not rear-view geometry.
Full goal remains incomplete: unload support/material/rise and floor-case joins,
helmet propagation, cargo/arrival integration, lifecycle and all-family polish.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-return-match-v319/HANDOFF.md.
'''
guides=record_guides(r,section,'### James unloading advancing playback comparison - October3,2026')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James unloading return

## Objective and acceptance
Full James animation set matching masters, with integrated motion and all-family
consistency/polish. Source measures and native checks do not establish acceptance.

## Accepted decisions and constraints
Matte master identity; belt wrench retained, empty return hands, floor case in
front between legs. Fixed support with natural bent body; no procedural body fix.

## Current state
319 prompt/inputs, builtin raw/receipt, nearest256 export, neighbor board and
rejection. Ledger and five guides updated.317 review bank still provisional;
normal runtime unchanged. No gameplay edits or new native probe.

## Verification
Raw, five-pose board and original West master viewed. Frozen inputs/prompt/raw
hashes verified.319 sole rises6px, crown rises9px and width grows2px. Rejected
before native. Review rasters checked for LFS attributes.

## Next action
Use original unloading4 geometry for constrained return repair, with actual
master fabric/hardware appearance. Compare complete chronology, then native
sizes if viable. Unload support/rise/case joins, helmet propagation, carry/turn
and actual arrival selection, normal lifecycle/Continue and full-family polish
remain. Full goal active; no external blocker.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f: f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in o.iterdir() if f.suffix=='.png']
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(version=319,rejected=True,crownRisePx=9,soleRisePx=6,widthChangePx=2,guides=guides,lfsRasters=len(rasters),nativeRuns=0,normalChanged=False,fullGoalComplete=False)))
