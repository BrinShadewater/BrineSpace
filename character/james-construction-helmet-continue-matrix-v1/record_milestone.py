from pathlib import Path
import json, hashlib, os, uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
def atomic(p,data):
    t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,p)
def write(p,data):atomic(p,(json.dumps(data,indent=2)+'\n').encode('utf-8'))
before=read(P/'runtime-input-before.json')
after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before}
assert before==after
write(P/'runtime-input-after.json',after)
review=read(P/'review-evidence.json');guards={}
for direction in ['north','east','south','west']:
    guard=read(P/(direction+'-validation.json'))
    assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged'] and not guard['profileDelta']
    assert not any(term in (P/(direction+'.log')).read_text(encoding='utf-8') for term in ['ERROR:','SCRIPT ERROR:','FAILED'])
    assert (P/(direction+'.gd.uid')).exists()
    evidence=read(P/direction/'continue-evidence.json')
    assert evidence['failures']==0 and len(evidence['cases'])==9
    assert {(c['workPhase'],c['phase']) for c in evidence['cases']}=={(w,m) for w in ['torch-draw','weld','torch-stow'] for m in ['exit','hold','return']}
    assert all(c['direction']==direction and c['sourceExact'] and c['completed'] for c in evidence['cases'])
    assert all(row['helmet'] for row in evidence['records'])
    for work in ['torch-draw','weld','torch-stow']:
        for motion in ['exit','hold','return']:
            label=direction+'-'+work+'-'+motion
            a=next(r for r in evidence['records'] if r['label']==label+'-before')
            b=next(r for r in evidence['records'] if r['label']==label+'-after')
            assert all(a[k]==b[k] for k in ['sourceHash','key','index','motionPhase','timer','foot','helmet'])
    guards[direction]={k:guard[k] for k in ['exitCode','timedOut','realProfileUnchanged','profileDelta']}
checks=sum(f['checks'] for f in review['families'].values())
captures=sum(f['distinctCaptures'] for f in review['families'].values())
nb=sum(len(f['nativeBoards']) for f in review['families'].values())
sb=sum(len(f['sourceBoards']) for f in review['families'].values())
review['visualReview']={'nativeBoardsReviewed':nb,'sourceBoardsReviewed':sb,'masterReviewed':True,'ownerAcceptance':'pending'}
write(P/'review-evidence.json',review)
selection={'status':'installed_sources_full_cardinal_construction_checkpoint_matrix_reviewed_owner_pending','fullSetComplete':False,'productionChanges':False,'newSourceStates':0,'checks':checks,'failures':0,'freshMainSceneDiskContinues':36,'distinctNativeCaptures':captures,'review':'review-evidence.json','guards':guards,'scope':'Four facings x draw/held/stow x exit/hold/return; power-loss checkpoints, paused exact snapshot/player/source/work/order/Metal restoration and normal paid completion once. Initial scene/foot resets and supported prescribed worn gear; five first resumed source changes captured per case. No fresh process, repeated-loss checkpoint, safety checkpoint, locker integration, natural owner-layout or full-set acceptance.'}
write(P/'selection-review.json',selection)
for rel in ['character/james-construction-helmet-v1/selection-review.json','character/james-construction-helmet-cardinal-v1/selection-review.json']:
    p=R/rel;v=read(p);v['fullCardinalContinueMatrix']='character/james-construction-helmet-continue-matrix-v1/selection-review.json';write(p,v)
note=f'''## James helmet construction full cardinal Continue matrix — October 1, 2026

character/james-construction-helmet-continue-matrix-v1 covers36actual power-loss
disk checkpoints: North/East/South/West x draw/held/stow x partial exit/neutral
hold/partial return. Each restores into a fresh main scene in its fixture's same
engine process. {checks}checks0failures/{captures}native captures. Exact actor/player/
sourceRGBA/clock/pause/paid order/Metal retained; paused update cannot advance;
normal60Hz controller completes every paid job once without charging again.
Before/after and first five resumed source changes captured per case; not every
resumed source slot. Initial scene/physical-foot resets and prescribed worn gear,
ordinary actual approach. No new repeated-loss/safety checkpoints, locker fitting
or natural owner-layout acceptance.

All{nb}native/{sb}source boards and four-direction helmet master comparison
visually reviewed. Original matte sources,184canvas/p92,172/148 ruler, helmet
attachment, proportion/contact and exact paused joins retained. No production,
PNG, manifest, grade or timing edits. Four engines terminal0/no timeout/cleanlogs;
separate scratch APPDATA and strict owner fingerprints unchanged. Ten whole-file
production inputs frozen before launches equal after terminal runs. Owner review
pending; full James goal active. Evidence and HANDOFF in the folder.

Lesson: a successful checkpoint in one facing/one work phase does not certify the
other source recipes. Cross actual authored work phases with interruption phases,
check paused source/player/paid-clock restoration, then normal completion. Same
process/fresh scene is narrower than fresh-process loading; capture counts are
narrower than every resumed-slot coverage. Next locker-to-job integration and
remaining full-set/cross-family polish.

'''
p=R/'docs/CURRENT_STATUS.md';atomic(p,note.encode('utf-8')+p.read_bytes())
lesson=f'''\n## James helmet construction checkpoint matrix — October 1, 2026

36actual disk Continues cover4facings x3work phases x3interruption phases.
{checks}checks0failures/{captures}native original-source captures; all{nb}native/
{sb}source boards and helmet masters reviewed. Exact paused actor/player/source,
paid clock/order/Metal and normal completion once; no new art/grade/ruler/timing.
Four clean terminal engines, scratch profiles unchanged, ten frozen production
hashes. Cross authored draw/held/stow with exit/hold/return rather than extrapolate
one successful saved pose. Fresh main scene in same process is not fresh process;
five resumed changes per case is not every source slot. Initial foot/world reset
and supported worn gear do not prove locker fitting or natural owner routing.
Evidence: character/james-construction-helmet-continue-matrix-v1. Full goal active.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:atomic(p,p.read_bytes()+lesson.encode('utf-8'))
handoff=f'''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: James helmet construction Continue matrix

## Objective and acceptance

Continue full James set, matching masters and cross-family polish. This milestone
adds the complete facing/work-phase/interruption-phase construction save matrix.
Full-set and owner acceptance remain open.

## Accepted decisions and constraints

Original matte sources, fixed184canvas/p92,172/148 standing ruler, physical foot,
paired helmet, whole-source recipes and paid10second construction retained.
Owner save and layouts untouched; no production/source/timing changes.

## Current state

Four nine-case native fixtures and isolated runner, captured before/after plus
five first changed resumed poses, review boards, measurements and two parent
review links. Current status, pipeline, bible and both skill references updated
atomically while preserving concurrent actor entries.

## Verification

36actual disk reads into fresh main scenes in same fixture process;
{checks}checks0failures/{captures}native exact original-source captures. Actor/player/
RGBA/paused clock/work/order/Metal exact, normal paid completion once. All{nb}
native/{sb}source boards and four-direction helmet master board reviewed.
Four terminal engine0/no timeout/clean logs, strict owner fingerprints unchanged,
ten production input hashes equal before launch/after terminal completion.
Initial world/foot resets, supported worn gear, ordinary actual approach. No
fresh-process, all resumed-slot, repeated-loss/safety checkpoint, locker fitting
or natural owner-layout proof.

## Next action

Exercise actual locker fitting into construction jobs, then remaining broader
animation/master joins and cross-family polish. Keep full goal active.
'''
atomic(P/'HANDOFF.md',handoff.encode('utf-8'))
print(json.dumps({'checks':checks,'captures':captures,'freshScenes':36,'nativeBoards':nb,'sourceBoards':sb,'guards':guards}))
