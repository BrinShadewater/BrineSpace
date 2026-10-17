from pathlib import Path
import json,hashlib,subprocess,sys
P=Path(__file__).resolve().parent;R=P.parents[1]
evidence_paths=[P/'motion-review-evidence.json',P/'join-review-evidence.json']
for path in evidence_paths:
    d=json.loads(path.read_text(encoding='utf-8'))
    for relative,digest in d['bindings'].items():assert hashlib.sha256((R/relative).read_bytes()).hexdigest()==digest,relative
motion=json.loads(evidence_paths[0].read_text(encoding='utf-8'))
motion['reviewedBoards']=motion['boards'];motion['reviewedSourceNativePairs']=104
motion['visualReview']='All4chronological boards/all104native presentations inspected. Body/material/shared helmet remain connected across sampled distance-driven loops; revised bare head matches master scale. Source/player rendering accepted as staged evidence, not actual actor/world/continuous-cadence or owner acceptance.'
evidence_paths[0].write_text(json.dumps(motion,indent=2)+'\n',encoding='utf-8')
joins=json.loads(evidence_paths[1].read_text(encoding='utf-8'))
joins['reviewedSourcePresentations']=12
joins['visualReview']='All12pivot-registered source presentations inspected. Candidate bare carry head matches idle/master better; current pickup/unload/quarter-turn endpoint heads remain larger and differ in facial/collar proportions. Whole-family join consistency FAILED for adoption. Equipped helmet construction remains shared, but case/body/contact pose continuity needs actual controller motion. Correct neighboring whole authored sources before replacing selected carry.'
evidence_paths[1].write_text(json.dumps(joins,indent=2)+'\n',encoding='utf-8')
paths=list((P/'frames').rglob('*.png'))+[P/'bare-manifest.json',P/'helmet-manifest.json',P/'package-registration.json',P/'paired-master-contact.png']
before={x.relative_to(P).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
with (P/'rebuild.log').open('w',encoding='utf-8') as log:subprocess.run([sys.executable,str(P/'build.py')],stdout=log,stderr=subprocess.STDOUT,check=True)
after={x.relative_to(P).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in paths};assert before==after
(P/'rebuild-checks.json').write_text(json.dumps({'deterministicFiles':len(paths),'before':before,'after':after,'failures':0,'providerCalls':0},indent=2)+'\n',encoding='utf-8')
block='''## Veld West corrected carry paired source/player review — October 2, 2026

West master-proportions candidate now has12paired256RGBAframes,H148/p128224,
original840msloop/stride/facing/dry/depth metadata. One pooled cloth curve against
original West master; fixedskinRGB+.5/+4/+7,hair+3/+1/+2, no contrast flattening or
per-frame exposure. Case/near hands and alpha protected. Exact shared44x46West
helmet component retains scale/grade, tracked with accepted+2pxrecipe adjustment.
64package checks0fail;16files byte-identical on local rebuild, no provider call.

Standalone actual CrewSpritePlayer distance-clock/native rendering passes633checks
0fail/7.94s/engine0,104samples (52/gear,30Hzsimulated time/1.7s,all six slots/loop
wraps) at47/93/148standing rulers.30targeted inputs/2931owner non-log files unchanged
under scratch APPDATA. All four chronological boards/104source-native pairs viewed;
104decoded lossless APNG frames exactly retain nativeRGB. Connected body/material/
shared shell in sampled playback accepted for staged review. No normal loader or
world/actor/controller/save acceptance; capture cadence is not real gameplay FPS.

All12cargo-join source presentations inspected: revised carry is closer to original
idle/master, but selected pickup/unload/turn endpoints still have larger bare heads.
Whole-family source continuity FAILS adoption; do not install correctedcarry alone.
Next repair the neighboring authored sources/shared held joins, review all frames,
case/foot/neck continuity and actual controller handoffs, then paired normal binding.
Candidate remains unselected. Source/body proportions and material are distinct
from checking metadata and exact pixel playback. Full set/natural gameplay/master
cross-library polish remain incomplete; no commit/export.

Review:character/veld-carry-west-master-proportions-v1/index.html (HTTP200/exactbytes;
app open queued, no visible-browser/continuous-watching claim). Handoff in samefolder.
Status/pipeline/bible/maintained+installed skill capture this source-join lesson.

'''
for dest in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    old=dest.read_text(encoding='utf-8')
    if block.splitlines()[0] not in old:dest.write_text(block+old,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld West carry master family

## Objective and acceptance
Full master-consistent Veld set, then cross-family polish. Correct side carry head
proportions without creating drift in pickup/unload/turn/body/helmet/case joins.

## Accepted decisions and constraints
Original approved West side foundation governs proportions/detail/grade. Authored
whole bodies, one148standing ruler/pooled material pass. Original840msstride and
shared native helmet retained. Preserve selected art until whole-family evidence.

## Current state
Two builtin source edits with raw/prompts/refs/execution preserved. V2head proxy
27–28px matches27master vs35–36selected. build.py produces12pairedframes/manifests,
pooled cloth/fixed skin-hair offsets, original metadata and exact44x46helmet fit.
Case/near hand grade protected. Paired contact and source cargo join boards viewed.
Native test/UID/isolated runner plus motion/lossless review artifacts added.
No production binding changed; candidate still staged_not_installed.

## Verification
64packagechecks0fail;16deterministic files stable on rebuild. Native standalone
CrewSpritePlayer distance-driven proof633checks0fail/7.94s/104samples/all6slots and
loopwraps/47/93/148rulers.30inputs/2931ownerfiles unchanged,scratchAPPDATA. All four
chronological boards/104source-native pairs viewed;104APNGdecodedframes exactRGB.
This is prescribed player rendering, not world/controller/save or natural cadence.
12cargo source joins reviewed: bare pickup/unload/turn heads still larger; family
continuity fails adoption. No continuously watched allclips or owner acceptance.
HTMLserved200/exactbytes, appopenqueued (not visibly confirmed). Source provenance,
rebuild checks and scoped acceptance retain original native interval hashes.

## Next action
Repair neighboring West unload/pickup whole authored sources and shared held/turn
joins from original masters; inspect reduced head proportions without flattening
detail. Keep currently selected sources until paired family source/native/controller
handoffs pass. Reuse candidategrade/helmet recipe only where anatomy/contact permits.
Actual-world gait/foot/case/neck handoffs and final viewer motion still open. East/
Southcarry, older side sit/read and full natural gameplay/master library polish
remain in objective. No commit/export/full-goal completion; no active native run.
''',encoding='utf-8')
print('Paired/native/failed-join scope recorded;16rebuild files stable;five references updated')
