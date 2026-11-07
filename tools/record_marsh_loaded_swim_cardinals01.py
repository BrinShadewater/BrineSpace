"""Record new North/South and scoped four-loop coverage, preserving open art gates."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';S=B/'sources'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results={}
for facing,revision,inputs,generation,sizes in [('north','04',55,'exec-62533b5e-dc87-4bf9-b792-6f3b1021be11',[[69,104],[70,85],[70,107],[69,96],[55,146]]),('south','01',35,'exec-e7ba9892-3229-457b-bca0-39b2768fbe1b',[[75,106],[76,83],[76,101],[76,97],[62,146]])]:
    name=f'{facing}-loop-{revision}';r=read(S/f'{name}.request.json');recipe=read(B/f'{name}-unselected/recipe.json')
    assert r['generationId']==generation and sha(S/f'{name}.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
    assert sha(S/f'{name}.prompt.txt')==r['promptSha256']
    for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
    assert [q['occupiedSize'] for q in recipe['records']]==sizes
    a=ROOT/f'output/marsh-animation-audit/loaded-swim-{facing}-native-{revision}-2026-10-02';report=read(a/'report.json')
    assert (report['checks'],report['failures'],len(report['samples']),len(report['captures']))==(244,0,109,6)
    assert (a/'native-exit.txt').read_text().strip()=='0';log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
    for kind,count in [('inputs',inputs),('owner',2931)]:
        before=read(a/f'{kind}-before.json');assert len(before)==count and before==read(a/f'{kind}-after.json')
    o=B/f'{name}-actor-review';o.mkdir(exist_ok=True)
    for c in report['captures']:shutil.copy2(a/c['file'],o/c['file'])
    order=[0,1,2,3,2,1];frames=[Image.open(B/f'{name}-unselected/{i:03}.png').convert('RGBA') for i in order]
    apng=B/f'{name}-unselected/player-holds.apng';frames[0].save(apng,format='PNG',save_all=True,append_images=frames[1:],duration=[180]*6,loop=0,disposal=0,blend=0)
    with Image.open(apng) as im:
        decoded=[f.copy().convert('RGBA') for f in ImageSequence.Iterator(im)];assert len(decoded)==6
        for d,f in zip(decoded,frames):assert d.tobytes()==f.tobytes()
    v={'normalAdmission':False,'fullGoalComplete':False,'generationId':generation,'nativeChecks':244,'failures':0,'samples':109,'captures':6,'playerRestores':6,'sameClockHolds':6,'inputsStableDuringInterval':inputs,'ownerFilesUnchanged':2931,'errors':0,'warnings':0,'exitCode':0,'decodedAPNGHolds':6,'nativeBoardsInspected':6,'scope':report['scope']}
    (o/'verification.json').write_text(json.dumps(v,indent=2)+'\n');results[facing]=v
    finding=('North04 whole rewrite improves head size and elbow span versus North03. Own neutral55x146 matches selected55x146 bounds. Swimmers69-70wide,85-107high. Initial top105 packing clips two poses; all figures translated five pixels upward to top100, no rescale or cropped pixels. Diagnostic registration not world-root acceptance. Quiet rear armor/forward-held case preserved; head/body/grade/hardware and linked joins provisional.' if facing=='north' else 'Own South01 four complete prone swimmers75-76wide,83-106high. Both frontal ivory latches and RIGHT-temple implant on viewerLEFT retained; connected two-hand grip, distinct kicks. Neutral62x146 versus current selected59x147: slight broadness/grade remains provisional. Leading case bottom178 and midpoint112 diagnostic whole registration. Used current catalogue idle master, not historical marsh-v2 idle. No linked joins or actual actor/world scope.')
    (o/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'findings':finding,'wholeStudyAndSixNativeBoardsInspected':True},indent=2)+'\n')
    r['status']='Whole source/native player/cardinal cross-reviewed; staged, proportions/grade/root/linked joins remain provisional; no normal admission';(S/f'{name}.request.json').write_text(json.dumps(r,indent=2)+'\n')
cross=B/'cardinal01-cross-review';v=read(cross/'verification.json');assert (v['uniqueWholeFigures'],v['states'],v['timingSlots'],v['authoredSwimmingFigures'])==(24,4,24,16)
for p,h in v['sourceParity'].items():assert sha(ROOT/p)==h
(cross/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeBoardsInspected':2,'uniqueWholeFiguresInspected':24,'findings':'Four own-direction staged loaded loops,16drawings/24timing slots. All figures retain own body/camera/case authority; North rear case naturally occluded, South two-latch frontal case, side edge latches/temple visibility distinct. Similar muted matte family; remaining neutral differences East35x147/master32x147,West33x146/master31x147,North55x146/master55x146,South62x146/master59x147. Natural kick/perspective extents not per-pose fitted. Cardinal source coverage is not a completed linked water family. Old water turns/pickup/drain, cross-source proportions/grade/case/root/contact and world/persistence/helmet acceptance remain open.'},indent=2)+'\n')
lesson='''

## Marsh loaded-swim four-cardinal source milestone — October 2, 2026

North04 whole source exec-62533b5e-dc87-4bf9-b792-6f3b1021be11 improves head/
elbow scale versus North03 while preserving prone camera and muted rear armor.
Own neutral55x146/master55x146; one neutral146 BOX scale .2225609756097561,
swimmers69x104/70x85/70x107/69x96. Old diagnostic top105 clips two poses;
whole translation to top100 prevents clipping without shrinking/cropping the
physical adult. This five-pixel root difference needs actual linked-state world
review; do not reject correct physical proportions solely to satisfy an arbitrary
study anchor, or present moved study anchor as accepted physical contact.

Own-South source exec-e7ba9892-3229-457b-bca0-39b2768fbe1b, one neutral147 BOX
scale .23824959481361427:75x106/76x83/76x101/76x97; neutral62x146/master59x147.
Nominal147 becomes146 after threshold: disclose, do not refit each figure.
Forward visible case keeps TWO frontal ivory latches; RIGHT-temple implant on
viewerLEFT. Toward-camera crown/face and receding legs are own perspective,
not mirrored North. Whole case-bottom178/midpoint112 registration diagnostic.
Resolve current idle from ordered catalogue: South uses
character/marsh-south-idle-material-v1/candidate-01/000.png, not historical
marsh-v2 idle. Standing width/grade still provisional. Both complete sources,
exact prompts/ordered references/raw originals/SHA retained; no part patches,
mirrors/recolour or per-pose fits. All used local refs/raw/whole study seen.

Independent native North04 and South01 each244checks,109samples/two1080ms wraps,
six player restores/same-clock holds; all12native boards inspected. Each six
180ms slots alias four drawings0,1,2,3,2,1; six APNG holds decode exact RGBA.
North55 bounded inputs/South35 stable DURING respective intervals,2931owner
nonlog files unchanged each under scratch APPDATA;0errors/warnings/fails,exit0.
No actor/world/fullSave/visibleContinue/helmet/contact gate this interval.

Cardinal01 private family contains East02/West01/North04/South01 only:4states,
24timing slots/16swimming drawings. Two boards/24whole figures seen alongside
four own neutrals/current masters. Similar quiet matte family; North proportions
improved, remaining neutral width differences and body/head/grade/case/root
provisional. No normal catalogue/runtime selection changes. Old linked water
turns/pickup/drain still need whole-source reauthoring and all family joins.
Coverage is not acceptance. Next author whole loaded water turns using these own
cardinals and intermediate yaw, then pickup/drain, scoped real routes/persistence/
helmet/contact and normal family admission. Remaining dry cargo/full Marsh
families/cross-library consistency/polish remain active and incomplete.
Handoff: docs/MARSH_LOADED_SWIM_CARDINALS01_HANDOFF_2026-10-02.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(lesson)
shutil.copyfile(canonical,installed)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh cardinal loaded swimming

## Objective and acceptance
Full master-matched Marsh set and cross-library consistency/polish remain active.
Cardinal loaded-loop sources are now available; connected water family unaccepted.

## Accepted decisions and constraints
Own cardinal masters/case identity, organic camera foreshortening, one neutral
scale per source. Whole figures only; no mirrors/patches/per-pose fits. Scratch APPDATA.

## Current state
character/marsh-loaded-swim-material-v1: North04/South01 retained sources/prompts/
requests, unselected frames/manifest/APNG, actor reviews. Cardinal01 cross-review
contains four private loops East02/West01/North04/South01 and two full boards.
New South/North04 preparation, retention/packing/native/fingerprint tools and paired
GDScript UIDs; cardinal compare/record tools. Pipeline/bible/status/both skill refs
updated. No normal catalogue/runtime change. All jobs terminal.

## Verification
North04 and South01 independently244checks each,109samples each,6restores/holds
and6exact APNG holds each. All12native/2cross boards reviewed. North55inputs/South35
stable in their intervals;2931ownerfiles unchanged each;0errors/warnings/fails,exit0.
4states/24slots/16drawings are coverage only. Width/grade/case/root/joins open.
North whole top100 differs five pixels from old study top105; not world acceptance.

## Next action
Whole loaded water turns from own cardinals with intermediate yaw, then pickup/
drain. Current staged family needs actual routes/physical joins/persistence/helmet
and normal admission. Remaining full Marsh families and cross-library polish.
'''
(ROOT/'docs/MARSH_LOADED_SWIM_CARDINALS01_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
print('North04/South01 source/native and cardinal evidence published; skills/docs updated; goal active.')
