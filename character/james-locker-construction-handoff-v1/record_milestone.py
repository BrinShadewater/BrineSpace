from pathlib import Path
import json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
def atomic(p,b):
    t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(b);os.replace(t,p)
def write(p,v):atomic(p,(json.dumps(v,indent=2)+'\n').encode('utf-8'))
before=read(P/'runtime-input-before.json');after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before};assert before==after
write(P/'runtime-input-after.json',after)
g=read(P/'validate-validation.json');assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and not g['profileDelta']
assert not any(s in (P/'validate.log').read_text(encoding='utf-8') for s in ['ERROR:','SCRIPT ERROR:'])
assert (P/'validate.gd.uid').exists()
e=read(P/'evidence.json');assert e['failures']==0 and len(e['cases'])==4
assert {c['direction'] for c in e['cases']}=={'north','east','south','west'}
assert all(c['completed'] and c['fittingSlots']==12 and c['lockerTravel']>80 for c in e['cases'])
review=read(P/'review-evidence.json');assert all(review['fittingEndpoints'].values())
nb=sum(len(d['nativeBoards']) for d in review['directions'].values());sb=sum(len(d['sourceBoards']) for d in review['directions'].values())
cg=read(P/'camera-review/validate-validation.json');assert cg['exitCode']==0 and not cg['timedOut'] and cg['realProfileUnchanged'] and not cg['profileDelta']
cr=read(P/'camera-review/review-evidence.json');assert cr['originalPoseClockSourceMatches'] and cr['records']==sum(1 for r in e['records'] if r['leg'].startswith(('south-','west-')))
review['cameraReview']='camera-review/review-evidence.json'
review['originalNativeLimit']='Some South/West original capture views UI-covered or offscreen. Camera-only repeat replaces visual evidence, identical source/pose/clock/route checks.'
review['visualReview']={'cameraNativeBoardsReviewed':sum(map(len,cr['boards'].values())),'originalNativeBoardsInspected':nb,'sourceBoardsReviewed':sb,'fittingAllTwelveReviewed':True,'masterFittingTorchJoinReviewed':True,'ownerAcceptance':'pending'}
write(P/'review-evidence.json',review)
checks=e['checks'];captures=len(e['records'])
archive=read(P/'before-support-port-correction/validate-validation.json');assert archive['realProfileUnchanged'] and not archive['profileDelta'] and not archive['timedOut']
scope='Four actual AirlockService requests in prescribed connected powered airlock setups, ordinary approach/all12fitting slots/exact master endpoints/normal fitted-gear travel and actual four-direction paid construction. Initial room/physical-foot/bare-gear reset per case. Distinct source slots captured once per journey leg, not every chronological visit or world position. No disk Continue, removal, interrupted fitting, natural owner-layout or continuous native-motion acceptance.'
selection={'status':'installed_sources_locker_to_construction_native_handoffs_reviewed_owner_pending','productionChanges':False,'newSourceStates':0,'fullSetComplete':False,'checks':checks,'failures':0,'captures':captures,'scope':scope,'review':'review-evidence.json','guard':{k:g[k] for k in ['exitCode','timedOut','realProfileUnchanged','profileDelta']},'fittingEndpoints':review['fittingEndpoints'],'archive':'before-support-port-correction retains failed South paid-queue assertion: original fixture tried to extend through sealed single-door airlock wall. Explicitly stopped confirmed matching engine after failure, no timeout; owner fingerprints unchanged. Corrected fixture puts airlock on another core port and retains genuine construction connection rules. No production change.'}
write(P/'selection-review.json',selection)
for rel in ['character/james-construction-helmet-v1/selection-review.json','character/james-construction-helmet-continue-matrix-v1/selection-review.json']:
    p=R/rel;v=read(p);v['lockerConstructionHandoff']='character/james-locker-construction-handoff-v1/selection-review.json';write(p,v)
note=f'''## James locker fitting into construction — October 1, 2026

Four actual AirlockService requests now lead through ordinary approach, all 12
helmet-fitting frames, equipped travel and paid construction in all four directions.
{checks:,} checks passed with no failures; {captures:,} distinct selected-source
captures. The helmet is granted only after fitting finishes and persists through
construction. Work stays planted, retains its 5 Metal cost and releases tool effects
at completion. Fitting entry/exit match the bare/helmet masters exactly after pivot
alignment. Matte identity and proportions remain consistent across the reviewed poses.
No artwork, manifest, timing or production changes.

All {nb} original native boards were inspected, with some South/West travel views
covered by UI or offscreen. Ten corrected camera boards replace those views;
574 source/pose/clock/physical-foot records and case outcomes match the original
run. All {sb} source boards and fitting/master/torch join boards were reviewed.
Both authoritative native runs exited normally with clean logs, isolated APPDATA
and unchanged owner fingerprints. Twelve production inputs stayed byte-identical.

The original fixture tried to build through the airlock's sealed wall; its failed
assertion and explicit engine stop are preserved in before-support-port-correction.
Support now occupies another core port. The unsuitable first camera repeat also
remains archived; it exited normally before the attempted stop found no process.

Scope: prescribed connected powered rooms and initial room/foot/bare-gear resets,
without a prescribed helmet grant. Per-leg unique source captures establish poses,
not continuously watched cadence or every world position. No disk Continue,
removal, interrupted fitting or natural owner-layout acceptance. Owner review and
the full James goal remain open. Evidence and handoff:
character/james-locker-construction-handoff-v1.

Next: removal/interrupted locker handoffs, then remaining motion and family polish.

'''
p=R/'docs/CURRENT_STATUS.md';atomic(p,note.encode('utf-8')+p.read_bytes())
lesson=f'''
## James locker acquisition into construction — October 1, 2026

Exercise actual AirlockService requests when checking fitting-to-work joins;
setting a worn flag bypasses acquisition and its route. Four prescribed connected
powered setups passed {checks:,} checks, all 12 fitting slots and paid construction
in every direction. Fitting endpoints match the masters exactly when their physical
pivots align: 256 fitting and 184 work canvases share the same 148 standing ruler.
Reviewed {sb} original-source boards, all original native boards and ten replacement
South/West camera boards. The 574 replacement poses/clocks/feet match exactly.
Matte identity remains consistent; no art, manifest, timing or production change.

A single-port airlock cannot support a build through its sealed wall: relocate
fixture support instead of weakening connection rules. Keep UI-covered/offscreen
captures as evidence limitations and correct the review camera before claiming
visual acceptance. The camera's normalized centre uses GRID_SIZE (40); the prior
80 denominator applies only to averaging two cell positions. Record camera-only
repeats separately from behaviour coverage. Both authoritative runs exited normally;
strict owner fingerprints and twelve production hashes were unchanged.

Evidence: character/james-locker-construction-handoff-v1. Initial room/foot/bare
resets and per-leg unique captures do not prove native cadence, removal/interrupted
fitting, Continue or natural owner-layout behaviour. Full James goal remains open.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:atomic(p,p.read_bytes()+lesson.encode('utf-8'))
handoff=f'''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: James locker-to-construction joins

## Objective and acceptance

Continue complete James animation set and master/style/proportion/material checks,
then cross-family polish. This milestone covers actual acquisition into paid jobs.
Full-set and owner acceptance remain open.

## Accepted decisions and constraints

Retain original matte masters,148standing ruler, source-pivot registration across
184/256canvases, wrench on belt and whole torch poses. No production/art/manifest/
timing change. Owner save and layouts unchanged.

## Current state

Four actual AirlockService requests followed by fitting and paid construction
in four directions, initial room/foot/bare-gear resets. Captures/reports/review
boards and two parent-review links in this folder. Five maintained guidance
documents updated atomically while preserving concurrent actor work.

## Verification

{checks}checks0failures/{captures}native original-source views, all12fitting slots,
exact normalized master endpoints, actual approach/fitted travel/contact and5Metal
completion. All{nb}original native boards inspected and10corrected South/West native boards
plus{sb}original source boards reviewed plus fitting and master/work joins
reviewed. Final terminal engine0/no timeout/clean log, strict owner fingerprints
unchanged, twelve production inputs frozen before launches/after terminal runs.
Archive preserves incorrect sealed-airlock-wall fixture failure and explicit stop
of confirmed matching engine; corrected support port, no production rules changed.
Original South/West captures include UI/offscreen occlusion; camera-review is a
camera-only repeat with identical574South/West source/pose/clock/foot records and case outcomes.
Per-leg unique source captures, not every visit/position or native cadence proof.
No Continue, removal, interrupted fitting or natural owner-layout acceptance.

## Next action

Exercise actual helmet removal and interrupted fitting/service-to-work handoffs,
then remaining full-set motion/master joins and cross-family polish.
'''
atomic(P/'HANDOFF.md',handoff.encode('utf-8'))
print(json.dumps({'checks':checks,'captures':captures,'nativeBoards':nb,'sourceBoards':sb,'endpoints':review['fittingEndpoints'],'guard':selection['guard']}))
