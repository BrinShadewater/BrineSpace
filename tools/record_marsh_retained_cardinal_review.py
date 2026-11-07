"""Record reviewed cardinal candidate scope and master/asymmetry lessons."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-retained-gesture-material-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
notes={
    'east03-unselected':'Compact bent-glove gesture and bare near-left temple restored. More coherent/slimmer than coarse old bank; generated neutral body width33.923vs own32 remains a proportion concern. Head/collar/profile/material and continuous joins remain provisional.',
    'west03-unselected':'Pointing/open-palm substitutions removed; compact bent gloves restored, near-right temple hardware retained. Neutral body width31.241vs own31. Whole connected source and native bank improved; head/collar/implant readability and dynamic joins still provisional.',
    'north02-unselected':'Fourth pose now retains right glove at shoulder strap while left glove bends at waist. Rear backpack/straps/hair/boots stay connected; neutral body width55.087vs own55 and occupied body height146. Dynamic rear arm occlusion and material/head joins still provisional.'
}
for folder,note in notes.items():
    path=BASE/folder/'verification.json';r=json.loads(path.read_text())
    assert sha(ROOT/r['board'])==r['boardSha256']
    r['actuallyInspected']=True;r['visualAssessment']=note
    path.write_text(json.dumps(r,indent=2)+'\n')
path=BASE/'cardinal01-unselected/verification.json';r=json.loads(path.read_text())
for board in r['nativeEvidence']['boards']:
    assert sha(ROOT/board['path'])==board['sha256']
    board['actuallyInspected']=True
r['visualAssessment']={'method':'Three new whole-source cross-family boards and four complete native boards actually inspected, all24native poses at source and station height; prior South source evidence retained.',
                       'finding':'Slimmer, connected staged whole figures improve own-idle consistency over coarse retained bank. East neutral33.923vs32 remains unresolved; all directional head/collar/material/dynamic joins provisional.',
                       'normalAdmission':False,'fullGoalComplete':False}
path.write_text(json.dumps(r,indent=2)+'\n')
receipts=[]
for requestpath in sorted((BASE/'sources').glob('*.request.json')):
    request=json.loads(requestpath.read_text())
    for ref in request['references']:assert sha(ROOT/ref['path'])==ref['sha256']
    result=request.get('result');assert result and sha(ROOT/result['path'])==result['sha256']
    receipts.append({'request':requestpath.relative_to(ROOT).as_posix(),'sha256':sha(requestpath),'result':result})
assert len(receipts)==11
(BASE/'cardinal01-unselected/generation-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
note='''
## Marsh retained gesture cardinal01 staged family — October3,2026

Retained generic glove gesture now has staged East03,West03,North02 and prior
South03 whole-source banks in character/marsh-retained-gesture-material-v1.
cardinal01-unselected/manifest.json combines8source-identical aliases/48slots,
16new whole gesture sources, exact directional own idle first/last endpoints and
original six150ms finite holds. No actual helmet capability or controller change.
All11raw results/exact prompts/reference hashes/generation receipts retained.

New failures retained: East01 copied near-left temple hardware from conflicting
older support reference and invented pointing; East02 corrected that but neutral
width~37vs own32. East03 improves to33.923,still a proportion concern. West01
invented pointing/open-palm poses and inconsistent implant; West02 restored compact
gloves but neutral~34vs31. West03 neutral31.241vs31. North01 dropped fourth pose's
right glove early; North02 retains right shoulder glove plus bent left waist glove,
neutral55.087vs55 at own146occupied height. South03 remains unchanged.

Each bank uses ONE factor from its own occupied standing height/generated neutral,
not universal147: East147/650,West147/607,North146/705. Source body heights vary
at most1pixel in selected banks. Whole extraction plus fixed4px fringe preserves
connected figures without anatomy patch,recolour,mirror or per-pose fitting.
Three new APNGs decode6frames exact at original900ms duration. All three new
cross-family source boards inspected. Four complete native boards inspected:
24poses at source/station height,762checks/208samples/24player snapshot restores,
48exact sources,0errors/warnings/failures/exit0.1044bounded inputs and2931owner
non-log files unchanged under scratchAPPDATA. The loaded old comparison player's
whole source bank is included in the fingerprint, not just its24displayed frames.

Lessons: height agreement alone can conceal profile width/head drift. Measure
generated neutral width against its own directional ruler, and use occupied146
for North while retaining standing metadata148. Conflicting secondary identity
refs can override explicit implant instructions; current own-idle proportions and
accepted right-temple asymmetry remain authority. Repair whole sources and verify
all poses after edits; prompts do not prove glove action or consistent hardware.
Single-row layouts helped height consistency but did not prevent invented gestures.

Family remains unselected: East width/head/collar/material and continuous source
joins still need judgment; native passes do not establish smoothness/live actor
contact/fullRunSave/titleContinue/fullset acceptance. Next resolve that remaining
side-profile concern and continuously review this complete directional bank, then
coherent catalogue admission and remaining source/action/controller joins/polish.
Full Marsh goal stays active.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with path.open('rb') as stream:
        stream.seek(max(0,path.stat().st_size-100000));tail=stream.read().decode('utf-8',errors='ignore')
    if '## Marsh retained gesture cardinal01 staged family' not in tail:
        with path.open('a',encoding='utf-8') as stream:stream.write(note)
installed.write_bytes(canonical.read_bytes())
print('3new source boards and4native boards recorded;11generation receipts verified;four documentation references updated and skill copies identical')
