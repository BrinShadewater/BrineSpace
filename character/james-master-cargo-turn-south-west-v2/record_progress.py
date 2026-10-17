from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1];south=r/'character/james-south-master-carry-v1'
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inputs['preCallSha256'].items())
job=json.loads((p/'generation.json').read_bytes());assert job['task_id']=='448180480450899'
review=json.loads((south/'review.json').read_bytes());assert not review['visualReviewPending'] and review['protectedOriginalPixels']==59802
section=f'''### James canonical South carry and matched quarter-turn submission — October 2, 2026

New South representative bare carrying source uses actual selected idle-south
from normal literal loader, not old cargo face. Current loader resolves South idle/
carry for honest source comparison; frozen selected/master/case/reference inputs
stable. Built-in transparent crop exec-c8c91666-d5e0-4dab-bcd4-d267a707ad8b,
1254whole square->96native at original80/96 crop origin; no per-pose fit/grade.
Region80,104..174,165 admits torso/arms/hips only;59802original outside pixels exact,
original head/lower legs/boots,crown76/sole224 preserved. Raw crop/all whole/upper/
current carry/West and82/54/27station views inspected. Readable two-hand front case,
one viewer-left wrench and viewer-right meter remain on anatomical belt sides,
partly occluded naturally. Provisional source, not full animation/gear/native or
owner acceptance. Detailed South reference labelled preserved candidate, not
promoted to locked master. New selected-head West counterpart remains provisional.

Actual new South/West256endpoints uniformly4x white1024, no whole-body fit or
grade. Exact source/helper/prompt/source-review hashes frozen AFTER source reviews
closed; mutable pre-review records not silently changed after submission. One
exclusive Hailuo02first/last6s768P job448180480450899 submitted; last verified
{job['status']}. EstimatedUSD0.28,billing unverified; reserved transfer untouched.
Simple shortest90-degree South->West path requested, planted local feet/no full
spin/no colour/proportion change. Requested constraints are not actual acceptance.

Raw142-style chronology/endpoint sample builder prepared but not yet evidence of
decoded source; never treat configured endpoints as proof of rendered terminal
match. Next poll SAME job, inspect every raw frame and actual joins/material/feet/
height before alpha, shared helmet, native lifecycle or versioned normal admission.
No native/profile/normal bank/commit/export writes. Normal cap/V9/riseV6/caseV7
unchanged. Full James/master/cardinal/context/cross-family goal active/incomplete.
Five guides/direct-video mirrors updated. Evidence:
character/james-master-cargo-turn-south-west-v2/HANDOFF.md,generation.json;
character/james-south-master-carry-v1/review.json.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West master-lineage carrying prototype');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
lesson='''
James master-family quarter-turn448180480450899 uses new canonical selected-head
South/West carried endpoints, not old endpoint face drift. South59802outside pixels
exact; West60726outside exact; complete source pose reviews closed BEFORE video
hash freeze. Review records themselves can be generation inputs: close them first
or record a fixed snapshot, not a silently mutable pending verdict. Preserve all
original source/geometry hashes and review actual whole-body chronology/terminal
frame; matched input families do not prove a correct generated quarter-turn.
Evidence:character/james-master-cargo-turn-south-west-v2.
'''
for path in [r/'skills/brinespace-character-pipeline/references/direct-video.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/direct-video.md')]:
    old=path.read_bytes()
    if b'quarter-turn448180480450899' not in old:atomic(path,old+lesson.encode())
(south/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James South canonical carry

## Objective and acceptance
Full master-matched James animations plus later cross-family polish. Incomplete.

## Accepted decisions and constraints
Use actual selected head/ground proportions; source details remain original
reference candidates where documented. Anatomical-right wrench/viewer-left and
left meter/viewer-right remain on belt. Natural foreground occlusion permitted.

## Current state
prepare.py/package.py/close_source.py,exact inputs/prompt,raw1254alpha,new carry-pose,
source/crop/full/upper/82/54/27boards. Source provisional, review closed. No normal
manifest/actor/profile change. Matched South/West quarter-turn generation in
character/james-master-cargo-turn-south-west-v2; follow its current ledger/handoff.

## Verification
All boards inspected.59802outside pixels exact; head/lower body/feet,crown76/sole224
retained. One natural two-hand case grip, wrench and meter on correct anatomical
sides. Actual normal idle/carry resolved and frozen hashes stable. Static bare
pose only; seams/tool occlusion/full-family material/motion/helmet/native remain.

## Next action
Review actual quarter-turn source/all joins before shared helmet/native/versioned
normal admission. Expand full matched cargo family/cardinals/contexts/master polish.
Generation exec-c8c91666-d5e0-4dab-bcd4-d267a707ad8b, built-in tool;
saved raw.png/prompt.txt, generated alpha preserved.
''',encoding='utf-8')
(p/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James matched cargo turn

## Objective and acceptance
Full master/style/perspective/size/height/proportion/matte James set, then full
cross-family polish. Active/incomplete; source endpoint and full path must pass.

## Accepted decisions and constraints
Normal cap/V9/riseV6/caseV7 still selected. South/West canonical carried prototypes
remain unselected. No per-pose fitting/grade; preserved source/closed review hashes.

## Current state
South new selected-head pose/four source/crop/station boards reviewed;59802outside
pixels exact,crown76/sole224. West local3 provisional,60726outside exact. Supplied
equal1024white whole inputs,exact prompt/helper/source hashes. One job448180480450899
last verified {job['status']}. No new native/profile/normal bank/commit/export writes.
Five guides/direct-video mirrors updated. Prepared review_raw.py, not executed yet.

## Verification
South original/actual normal loader inputs stable; all South boards and both full
video inputs inspected. Source material/gear/proportions are provisional; quarter
turn constraints only requested. EstimatedUSD0.28,billing unknown. No decoded
quarter-turn or paired/native/owner evidence yet.

## Next action
Poll SAME task via maintained tools/minimax_video.py poll --output this folder.
Never resubmit/reset ledger on a timeout. On Success/download run review_raw.py,
inspect all raw chronology and actual endpoints/feet/height/case/material before
extraction/helmet/native work. Full cargo/cardinal/context/master/cross-family
goal remains open. No blocker.
''',encoding='utf-8')
print('South provisional source and verified quarter-turn submission recorded; five guides/direct-video mirrors/handoffs updated.')
