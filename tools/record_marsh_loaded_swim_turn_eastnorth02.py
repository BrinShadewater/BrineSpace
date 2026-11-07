"""Record the provisional paired turn, failed art correction and remaining full topology."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';S=B/'sources'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for stem,generation in [('east-north-01','exec-e2328df4-1aeb-4006-9e84-add2b1680951'),('east-north-02','exec-de3c97d0-0d3a-46b7-9553-835d82bf45c5'),('east-north-shallow-03','exec-2a70319a-148b-4229-be2b-75819d1ef1cb')]:
    r=read(S/f'{stem}.request.json');assert r['generationId']==generation
    assert sha(S/f'{stem}.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath'])) and sha(S/f'{stem}.prompt.txt')==r['promptSha256']
    for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
    r['status']=('Retained whole study/native player reviewed; head/case drift; superseded by provisional source02' if stem.endswith('01') else 'Whole source/native directed player and source comparisons reviewed; preferred provisional turn bank; no normal admission; head/case/root/grade joins remain open' if stem.endswith('02') else 'Rejected whole shallow correction: head/case recovered but swimmer161x109 and neutral36x147 broaden/elongate relative endpoints/master; retained for evidence, no native test or normal admission')
    (S/f'{stem}.request.json').write_text(json.dumps(r,indent=2)+'\n')
for rev,inputs in [('01',49),('02',61)]:
    a=ROOT/f'output/marsh-animation-audit/loaded-swim-turn-eastnorth-native-{rev}-2026-10-02';report=read(a/'report.json')
    assert (report['checks'],report['failures'],len(report['samples']),len(report['captures']),report['playerRestores'])==(185,0,44,10,10)
    for kind,count in [('inputs',inputs),('owner',2931)]:
        before=read(a/f'{kind}-before.json');assert len(before)==count and before==read(a/f'{kind}-after.json')
    assert (a/'native-exit.txt').read_text().strip()=='0';log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
    v=read(B/f'east-north-{rev}-actor-review/verification.json');assert len(v['nativeParity'])==10 and v['finiteAPNGHolds']==10
    for q in v['nativeParity']:assert sha(ROOT/q['source'])==q['sourceSha256'] and sha(B/f'east-north-{rev}-actor-review'/q['capture'])==q['captureSha256']
    assessment={'normalAdmission':False,'fullGoalComplete':False,'wholeSourceAndNativePairedBoardsInspected':True,'nativePairsInspected':10,'nativePairedBoardsInspected':2,'findings':'Three prone rearward yaw figures, progressive case occlusion ahead of torso, correct own East RIGHT implant visibility. Exact staged own East02/North04 endpoint pixels unchanged; return reverses complete sequence without mirroring. Source01 first angle head/case visibly small; source02 correction only modestly improves it. All anatomy/head/case/grade/yaw/root joins remain provisional. Player selects both finite400ms turns, handoff destination loop0, ten restored same-clock holds. No actual actor/world, fullSave/Continue/helmet/contact or coherent family admission.'}
    (B/f'east-north-{rev}-actor-review/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
for n in ['manifest.json','family-manifest.json']:
    p=B/'east-north-03-unselected'/n;m=read(p);m.update(rejectedStudy=True,normalAdmission=False,scope='Rejected broad/elongated shallow03 source; retained evidence only. Preferred provisional turn bank is east-north-02.');p.write_text(json.dumps(m,indent=2)+'\n')
# Correct only descriptive revision metadata after the scoped test freeze; textures/timing unchanged.
p=ROOT/'tools/pack_marsh_loaded_swim_turn_eastnorth02.py';p.write_text(p.read_text().replace('marsh-loaded-swim-turn-eastnorth01-staged','marsh-loaded-swim-turn-eastnorth02-staged'))
p=B/'east-north-02-unselected/manifest.json';m=read(p);m['revision']='marsh-loaded-swim-turn-eastnorth02-staged';p.write_text(json.dumps(m,indent=2)+'\n')
family=read(ROOT/'character/marsh-loaded-swim-material-v1/cardinal01-cross-review/family-manifest.json');family['revision']='marsh-loaded-swim-cardinal-plus-eastnorth02-staged';family['states']+=m['states'];assert len(family['states'])==6 and sum(len(s['frameFiles']) for s in family['states'])==34
(B/'east-north-02-unselected/family-manifest.json').write_text(json.dumps(family,indent=2)+'\n')
recipe=read(B/'east-north-02-unselected/recipe.json');assert [q['occupiedSize'] for q in recipe['records']]==[[137,86],[102,102],[78,104],[54,145]]
topology=read(S/'selected-turn-topology.json');assert (topology['selectedTurnStates'],topology['selectedTimingSlots'])==(12,76)
assert [q['middleMatchesSelectedOldLoop0'] for q in topology['oppositeMiddlePixelMatches']]==[['north'],['north'],['east'],['east']]
lesson='''

## Marsh loaded-water East-North paired turn studies — October 2, 2026

Current ordered catalogue has12loaded-water turns/76timing slots:8quarter five
poses400ms and4opposite nine poses800ms. Pixel-identity audit of OLD middle
poses shows EastWest/WestEast viaNorth, NorthSouth/SouthNorth viaEast. Preserve
own intermediate yaw, not mirrored artwork, when composing later opposites.

Whole EastNorth source01 exec-e2328df4-1aeb-4006-9e84-add2b1680951 and whole02
exec-de3c97d0-0d3a-46b7-9553-835d82bf45c5 retained with exact prompts/ordered
refs/SHA/originals. Three organic horizontal-prone rearRIGHT yaw figures22.5/
45/67.5degrees plus own North neutral; forward case progressively hidden by
head/torso, never across back. Own East RIGHT implant visible shallow then
naturally hidden. Source01 neutral146 scale .24092409240924093 yields136x84/
104x101/80x102/neutral55x146. Source02 one neutral146 BOX scale
.24373956594323873 yields137x86/102x102/78x104/neutral54x145 (nominal146 becomes
145 after threshold; disclose). Alpha128 observed unequal whole cells, integer
whole midpoint interpolation between exact staged East02/North04 endpoint
midpoints; no clipping/mirror/patch/recolour/per-pose fit. Diagnostic midpoint
is not accepted anatomical world root. Exact endpoint bytes unchanged; whole
reverse sequence gives NorthEast. Two400ms finite states/10slots, THREE authored
intermediates plus reused cardinal endpoints, not ten new drawings.

Independent native source01 and source02 each185checks/44samples at20ms,
tenplayer restores/same-clock holds, both directed400ms turns and destination
loop0 handoff, final finite clamp. Each ten APNG holds decode exact RGBA and
play once. All20native old/staged actor pairs seen on4paired2080x400boards;
whole opaque bounds checked before native screenshot crops, no native resize.
49inputs/61inputs stable DURING respective intervals,2931ownerfiles unchanged
each scratchAPPDATA,0errors/warnings/fails,exit0. Scope PLAYER only, not actual
actor/grid/controller/world/fullSave/visibleContinue/helmet/physical contact.
Published raw ten native captures per interval preserve full scene context.

Source01 first shallow head/case drift remains; source02 improves only modestly.
Focused whole shallow03 exec-2a70319a-148b-4229-be2b-75819d1ef1cb uses own-East
neutral147 (.203601108033241) and recovers volume but grows body161x109 and
neutral36x147/master32x147: REJECTED broad/elongated study, no native test.
Do not fix one head/case mismatch by allowing whole body/grade drift. Comparing
entire correction/neutral/endpoint at2x exposes it; never paste enlarged heads.
Source02 remains provisional, not accepted. Narrow magenta proxy0 on tested
East endpoint/01shallow/02shallow/02neutral does not prove whole grade alignment.

Private preferred family adds paired turn02 to four staged cardinal loops:
6states/34slots/19unique swimming figures. Coverage only. Revision/request/
assessment/APNG/family metadata written after the freezes, so interval stability
claims apply to the dated runs, not all current files. No normal catalogue or
runtime selection change. Remaining10loaded turns/other quarter sources, whole
pickup/drain, real route/physical joins/persistence/helmet, admission and full
Marsh families/cross-library consistency/polish remain active/incomplete.
Next own WestNorth rearLEFT quarter (nearLEFT temple bare, LEFT case edge,
no mirrored EastNorth), then EastSouth/WestSouth and composed opposites.
Handoff: docs/MARSH_LOADED_SWIM_TURN_EASTNORTH02_HANDOFF_2026-10-02.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(lesson)
shutil.copyfile(canonical,installed)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh loaded East/North turns

## Objective and acceptance
Full master-matched Marsh set and cross-library polish active/incomplete.
Paired loaded-water quarter source available, coherent whole water family unaccepted.

## Accepted decisions and constraints
Own directional masters/body/head/case/camera/grade. Whole figures/one neutral
scale, no mirror/patch/per-pose fit. Forward case occlusion, scratch APPDATA.

## Current state
character/marsh-loaded-swim-turn-material-v1 contains frozen refs and three retained
whole sources:01,02 and rejected shallow03. Preferred provisional02 manifest pairs
EastNorth/NorthEast at5poses/400ms, exact own staged East02/North04 endpoints.
Private preferred family6states/34slots, not normal admission. Rejected03 manifest
marked accordingly. Prepare/pack/compare/native/publish/fingerprint/inventory/
record tools and both native GDScript UID pairs retained. Pipeline/bible/status/
both skill refs updated. No normal catalogue/runtime change. All jobs terminal.

## Verification
Native01/02 each185checks/44samples/10restores and same-clock holds; destination
loop0 handoff and final finite clamp. All20native pairs/4boards seen,10exact
finite APNG holds each.49/61 bounded inputs stable respective intervals,
2931ownerfiles unchanged each,0errors/warnings/fails,exit0. Whole source/master/
correction boards reviewed. Only player scope; no actor/world/save/helmet gate.
02first angle head/case still provisional; rejected03 broad body161x109.

## Next action
Own WestNorth rearLEFT quarter, then EastSouth/WestSouth and composed opposites.
Old topology12turns/76slots: EastWest viaNorth, NorthSouth viaEast (whole reverse
for return). Then pickup/drain, all physical/source joins/real routes/persistence/
helmet/admission, remaining full Marsh families and consistency/polish.
'''
(ROOT/'docs/MARSH_LOADED_SWIM_TURN_EASTNORTH02_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
print('Paired turn02 source/player milestone recorded; shallow03 rejected; full Marsh objective active.')
