from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
d=json.loads((p/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in d['preCallSha256'].items())
for name in ['review.json','adjacent-review.json']:
    path=p/name;report=json.loads(path.read_bytes())
    report.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
        finding='Raw sources, four-column midpoint comparison, five whole/five upper adjacent views and fifteen station-size presentations inspected. Midpoint is a plausible provisional identity/size reference; not final accepted motion. Adjacent early and midpoint poses cluster in nearly the same orientation; late pose changes shoulder patch placement/breadth. Full progressive articulation not established. Do not expand helmet/native or install this bank yet.')
    atomic(path,(json.dumps(report,indent=2)+'\n').encode())
section='''### James single midpoint and adjacent source study — October 2, 2026

Three built-in image edits produce bare midpoint plus early/late upper poses using
actual carry-turn010/unloadWest0 endpoints. Exact prompts,1254 raw PNGs and frozen
input hashes retained in character/james-west-upper-midpoint-v1. Common80/1254
reduction/original(96,56) crop origin, no grade/translation/pose normalization.
Rect(104,64)..(162,134) only,61476 outside pixels exact per comparison candidate.
Adjacent review uses one common original middle body to isolate upper differences;
it is not a packaged final motion bank. No normal artwork/runtime selection changed.

Raw sources and midpoint whole/upper comparison reviewed; midpoint appears closer
to native endpoint identity/size and is retained as provisional source reference.
Five whole/five upper chronology views and15station-size presentations inspected:
early and midpoint cluster in nearly the same orientation; late shoulder patch
placement/breadth changes. Smooth progressive upper articulation remains unproven.
No helmet expansion or native tests; source gate precedes that work. No owner
profile access. Full James objective and master/cross-family polish remain open.

Lesson: using a midpoint as every edit target can lock adjacent outputs to the
same pose even with explicit phase prompts. Familiar face/grade is insufficient.
Next use incoming endpoint as early edit target and outgoing endpoint as late
edit target, retaining the midpoint as identity support; review both joins and
whole shoulder/collar geometry before assembling timing/body or paired equipment.
Prompts and review JSONs retain exact evidence; five guides and handoff updated.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James existing West donor trial');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West midpoint study

## Objective and acceptance
Complete James against masters/style/perspective/size/height/proportions/matte
grade, then cross-family polish. Incomplete; West upper join remains open.

## Accepted decisions and constraints
Actual normal endpoints and selected cap/V9/riseV6/caseV7 remain authoritative.
Source identity, geometry and progressive motion are separate acceptance checks.

## Current state
This folder stores three built-in imagegen raw sources, exact prompts/frozen
inputs, common-scale packages, midpoint and adjacent/native-size boards. Midpoint
retained as provisional reference; adjacent sequence not accepted or installed.
Five guides updated. No native/runtime or owner-profile writes this interval.

## Verification
Pre-call hashes unchanged;61476 outside pixels exact each. All raw sources,
midpoint four-column whole/upper board, five adjacent whole/upper views and15
station-size presentations inspected. Midpoint plausible, early/midpoint too
similar; late shoulder patch shifts. No smooth motion/master or owner acceptance.
Initial adjacent packaging syntax error corrected before successful checks.

## Next action
Author early from actual entry target and late from actual exit target, midpoint
as shared identity support. Review whole upper geometry and BOTH joins before
paired helmet/source bank/native work. Other directions/contexts/full-set and
cross-family polish remain. Goal active, no blocker/live job, no commit/export.
''',encoding='utf-8')
print('Three authored sources reviewed;midpoint provisional,adjacent motion unaccepted;five guides/handoff updated.')
