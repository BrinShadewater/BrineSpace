from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
for name in ['inputs.json','local-inputs.json','local-v2-inputs.json','local-v3-inputs.json']:
    inventory=json.loads((p/name).read_bytes())['preCallSha256']
    assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inventory.items()),name
findings={
 'review.json':'Raw1254whole generation and original-master/selected-idle/turn/cargo/new whole+upper and82/54/27boards inspected. Face closer to detailed original reference, but original-standing-derived scale exposes native158px height/crown74/sole232 against148px/crown76/sole224; brighter material and belt equipment transfer. REJECTED. No generated-pose fitting used to conceal drift.',
 'local-review.json':'Generated torso crop/all crop/whole/upper/station boards inspected. Original selected standing head/lower legs/boots exact outside60726protected pixels, crown76/sole224. Readable two-hand case grip and subdued material, but near-hip meter moved12right/8down. REJECTED as final pose; retained source/arms study.',
 'local-v2-review.json':'Generated crop/all crop/whole/upper/station boards inspected. Requested equipment move produces upper partly occluded meter plus old lower-right duplicate. REJECTED; exact protected head/legs/feet remain but equipment continuity fails.',
 'local-v3-review.json':'Generated duplicate-removal crop/all crop/whole/upper/station boards inspected. Lower-right duplicate removed, one upper partly occluded belt meter retained; two-handed case/forearms readable, head/lower legs/boots exactly original outside region. Crown76/sole224 and subdued neutral material retained. Provisionally viable representative bare carrying pose ONLY. Shoulder/detail/seam/occlusion and actual transitional equipment continuity need full-family source/motion review; no full source-bank/helmet/native/owner acceptance.'
}
for name,finding in findings.items():
    path=p/name;review=json.loads(path.read_bytes());review.update(visualReviewPending=False,selected=False,sourceAcceptance=False,finding=finding)
    if name=='local-v3-review.json':review['representativePoseDisposition']='Provisional viable bare source pose,not admitted animation bank'
    atomic(path,(json.dumps(review,indent=2)+'\n').encode())
section='''### James West master-lineage carrying prototype — October 2, 2026

Traced actual West raw source to branforth-west-direct-v2/master-input.png;
its SHA matches terminal provider ledger. Adjacent selection.json records owner
approval of resulting West walk revision. This proves reference lineage, not
original concept/portrait or every derived current-frame acceptance. Original
chief-engineer concept and side-master prompts inspected; historical orange
superseded by explicit muted-yellow owner correction. Side-master02 still labelled
candidate, not relabelled approved. Source inputs/prompts frozen and unchanged.

New built-in1254whole carrying edit from detailed West master rejected: one
ORIGINAL-standing-derived scale148/1012 and offset37,58 exposes158px generated
height/crown74/sole232 against original148/76/224. Brighter finish and equipment
transfer also fail. No per-pose fit to conceal changed anatomy/framing.

Localized torso/arm/belt crop from current selected matte idle uses common256/
p128224 registration, crop86,96..166,176 enlarged8x. Detailed original is style/
identity support; case reference cropped narrowly to exclude wrong-side belt tool.
Generated1254square->80 wholecrop, region86,104..160,169 admitted.60726original
pixels outside exact each; head/lower legs/boots unchanged, native crown76/sole224.
Region includes torso/hip/upper knee pixels, not an arm-only protection assertion.
Local1 readable grip/material but meter12right/8down; local2 attempted relocation
duplicates meter. Both rejected. Local3 removes lower-right duplicate and retains
one partly occluded upper meter; candidate local-v3-carry-pose.png provisionally
viable representative BARE pose, not full animation/paired gear/native admission.

All four raw/source-crop/master/original/cargo/turn/82/54/27boards inspected; exact
precalls stable, review records closed. Four built-in outputs and exact prompts
retained. No video/Higgsfield/native/profile/normal bank/commit/export writes.
Normal cap/V9/riseV6/caseV7 preserved. Full James goal active/incomplete.

Lessons: prove original source/owner-selection lineage without conflating historical
candidate metadata; enlarging native exports adds no detail. If whole-source edit
changes height/foot placement, retain rejection and narrow actual visual edit;
do not normalize generated pose back to expected height. Pose references can pull
unwanted belt layout even when labelled pose-only; crop to intended object.
Moving an item may duplicate it: count actual visible equipment and permit natural
foreground occlusion instead of moving devices aside to show them. Exact protected
head/feet do not certify hip/shoulder seams, full material identity or motion.

Next expand canonical matched West carrying source family/connecting motion while
preserving body/head proportions and belt/tool continuity; existing endpoint-only
yaw repair superseded. Paired equipment, actual cargo/ordinary-turn/gait/physical
case/checkpoint evidence and revised strict source bindings before normal admission.
Remaining directions/contexts/full-master/cross-family polish still required.
Evidence:character/james-west-master-carry-v1/HANDOFF.md and local-v3-review.json.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West middle-pose failures expose endpoint-family consistency work');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James canonical West carry

## Objective and acceptance
Full James animations matching accepted masters/art/perspective/size/height/
proportions/matte grade, then full-set/cross-family polish. Active/incomplete.

## Accepted decisions and constraints
Normal cap/V9/riseV6/caseV7 unchanged. Repair source-family identity/proportions
before interpolation. Yellow owner correction supersedes historical orange.
Historical West walk approval proves lineage, not every source/current pose.

## Current state
Original detailed West input/ledger/approval hash lineage verified. Four built-in
raw/prompt pairs: whole carrying rejected (height/material/tool drift); local1
meter drift rejected; local2 duplicate meter rejected; local3 representative bare
carry provisionally viable after duplicate removal. local-v3-carry-pose.png and
local-v3-master-comparison.png saved. All review records closed; five guides updated.

## Verification
All four raw/crop/master/source/upper/82/54/27boards inspected. Exact precall
inventories stable. Whole source one original1012px-height scale148/1012/offset37,58
reveals158vs148px output, not fitted away. Each local80crop admitted in86,104..160,169;
60726original pixels outside exact, original selected head/lower legs/boots and
crown76/sole224 retained. Local3 one partly occluded belt meter, natural case grip.
Crop includes hips/upper knee pixels; no blanket arm-only/body protection claim.
One bare static source pose, not paired motion/native/owner acceptance. No live job,
new video/Higgsfield/owner-profile/normal bank/commit/export writes.

## Next action
Expand canonical West carry/connecting source family from local3, checking every
pose's head/body proportions, matte/detail/seams, case grip and belt continuity.
Then paired equipment and full native cargo/ordinary-turn/gait/case/checkpoint
evidence with versioned source bindings before admission. Current narrower yaw
trials superseded, retained in james-west-upper-video-v1. Other cardinals/contexts
and full cross-family polish remain open. No blocker.

Built-in raw/prompt pairs: raw.png/prompt.txt (exec-ef0de650-d30f-489f-a298-83aed4e8ae35);
local-raw.png/local-prompt.txt (exec-d0e53497-498f-428b-b34a-2c141909e492);
local-v2-raw.png/local-v2-prompt.txt (exec-d38ad6b9-c50f-4df7-98cf-489dbcda7858);
local-v3-raw.png/local-v3-prompt.txt (exec-54a64c74-9a74-4654-b7cd-3dda71f71207).
All use built-in image generation, generated alpha preserved.
''',encoding='utf-8')
print('Four reviews closed; original lineage verified; local3 representative source retained provisionally; five guides/handoff updated. No normal admission.')
