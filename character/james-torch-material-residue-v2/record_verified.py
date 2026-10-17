from pathlib import Path
import json,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
v=json.loads((P/'validate-validation.json').read_text());n=json.loads((P/'validate-evidence.json').read_text());k=json.loads((P/'package-checks.json').read_text());rebuild=json.loads((P/'rebuild-evidence.json').read_text())
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and n['failures']==0 and k['failures']==0 and rebuild['byteIdentical']
s=json.loads((P/'selection.json').read_text());s.update(status='installed_native_source_verified_owner_review_pending',nativeChecks=n['checks'],nativeCaptures=len(n['records']),nativeScope=n['scope'],profileGuard=v,rebuild=rebuild,visualReview='All696 corrected whole-source refs on16paired boards and all72 prescribed normal-renderer native poses on four paired boards reviewed. Shape/brightness/head/shell/flame/engineering yellow and32whole-source joins preserved. No actual construction-order or continuously watched full-motion claim.',remaining=['Actual construction-order cycle, material continuity and sparks placement in motion','Other families/cardinals/rotations/gear/travel contexts','Full James consistency, owner and export acceptance']);(P/'selection.json').write_text(json.dumps(s,indent=2)+'\n')
block=f'''## James torch neutral-material residue correction — October 1, 2026

Installed james-torch-material-residue-v2 overrides paired12states/696refs:
680interiors changed,16exact idle endpoints retained, zero new authored drawings.
Fixed equal-luminance green-residue correction extends prior cold-mask omission:
same threshold4/full10/chroma25..35 rule belowy60 across every facing/both gears.
Original red-minus-blue relationship retained, no per-frame exposure/scale/pose
fit. Whole alpha/shape/pivots/148rulers/head/shell abovey60 and saturated engineering
yellow/blue-cyan flame exact; max byte-rounded luma difference0.4496. All32whole-
source joins remain exact. Source bindings freeze696original hashes before normal
selection, so rebuild does not accidentally read its own later override.

3610package checks pass; all696corrected sources reviewed on16paired boards.
2257native checks/72prescribed first/middle/final views pass; allfour paired native
boards reviewed, q0 clear storage room, four facings/both equipment libraries,
normal loader/source clocks/renderer and fixed physical foot. Engine0/no timeout/
scratch APPDATA/strict owner unchangedtrue/delta[].699PNG/manifest/config files
rebuild byte-identical. Current references/state coverage unchanged.

Earlier candidate altered16flame-edge pixels: archived before explicit blue/cyan
protection and fresh package review. First native run failed680checks because old
helmet torch loads followed the new paired override; preserved under before-final-
helmet-loader, moved new pair after final old helmet loads, reran successfully.
ACTIVE_ASSETS now records paired revision. Low-chroma lower-suit green>4 sample
median fractions reduced East1.79→0.63%, North6.88→4.24%, South4.47→2.84%,
West1.53→0.21%; intended master color/protected pixels remain, not automatic zero-
green targets. Source interval GIFs are one authored pass, not full work timer.
No new actual construction-order/helmet eligibility/travel/interruption/Continue
or continuous native motion/owner/export acceptance claim. Native sparks overlay
is separate from PNG material; review its placement during actual work next.

Lesson: correct the processing mask omission without reauthoring approved motion.
Explicitly protect weak flame edges; low-chroma classification alone can include
them. Byte equality through the final loader is required: load order can silently
restore an old equipment revision after a successful earlier load. Freeze inputs,
keep exact family joins and separate PNG color from runtime sparks/light overlays.
Full James goal active/incomplete; full-family/native motion and cross-family
polish remain. Handoff: character/james-torch-material-residue-v2/HANDOFF.md.

'''
def atomic(p,b):
    t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(b);os.replace(t,p)
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,p in enumerate(paths):
    old=p.read_bytes();b=block.encode();assert b not in old;atomic(p,b+old if i==0 else old+b'\n\n'+b)
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James torch material residue

## Objective and acceptance
Full James animations and master/style/perspective/scale/proportion/color
consistency, then full cross-family polish. Active, installed; owner pending.

## Accepted decisions and constraints
Matte masters, forward torch/belt wrench, exact shape/timing/rulers/joins. Material
processing only: fixed green-residue correction, protected head/shell/gold/flame.

## Current state
New deterministic build/frozen source-bindings/verify/all-source/native review,
paired12state manifests/696PNG references, build/material/native/rebuild evidence.
Normal grid loader final paired override, ACTIVE_ASSETS/selection updated. Earlier
flame-edge candidate and wrong helmet-loader native report archived. Five guides
updated. Original accepted raw/source packs retained.

## Verification
3610package/2257native checks0fail,32exact joins. All696source refs/16boards and
72prescribed NPC renderer views/four paired native boards reviewed.699deterministic
files byte-identical; strict real profile unchanged/scratch APPDATA/engine0.
No actual construction-order/controller journey, eligibility or continuous native
motion/Continue claim; source GIF is one authored draw/weld/stow pass.

## Next action
Actual construction-order cycle and sparks placement/material continuity in
motion, broader family/gear/travel/rotation joins and full James owner/export
acceptance. Full goal remains open. No native/provider process live.
'''
atomic(P/'HANDOFF.md',handoff.encode());print(json.dumps({'status':s['status'],'packageChecks':k['checks'],'nativeChecks':n['checks'],'nativeCaptures':len(n['records']),'ownerUnchanged':v['realProfileUnchanged'],'guidesUpdated':5}))
