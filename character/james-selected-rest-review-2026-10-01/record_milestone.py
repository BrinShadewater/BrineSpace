from pathlib import Path
import json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
source=json.loads((P/'source-evidence.json').read_bytes());native=json.loads((P/'native-clock-evidence.json').read_bytes());guard=json.loads((P/'native-clock-validation.json').read_bytes())
assert source['failures']==0 and native['complete'] and native['failures']==0
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
inputs=json.loads((P/'selected-inputs.json').read_bytes());changed=[r for r,h in inputs.items() if hashlib.sha256((R/r).read_bytes()).hexdigest()!=h];assert not changed,changed
note='''

## James current selected rest reconciliation and clock review — October 1, 2026

Correction to the recent South head repair study: its target was the superseded
`james-rest-material-continuity-v1` South source. Current ordered loader already
selects South/East/West `james-rest-*-identity-v2`, after ordinary rest material;
North remains ordinary rest material. Earlier historical head-board findings do
not establish defects in these current revisions. Two built-in generated study
outputs are retained unselected with prompts/hashes, never installed. Preserve
the existing whole-source identity revisions and supported South sleep template.

`character/james-selected-rest-review-2026-10-01` independently traces retained
catalog plus current loader order. All144 selected rest references and eight
registered idle0 masters reviewed in four full-pose/four head boards.56 checks
pass: exact visible registered standing entry/return, full RGBA lie/sleep/rise
joins and loop seams, reverse get-up and3600ms loop clocks. Initial16 apparent
standing failures were a review-registration error: idle184canvas/pivot92,172
and rest256canvas/pivot128,224 share148 ruler. Register by pivot(+36,+52), with
no body rescale; compare visible RGBA, not padding or unrelated canvas bounds.
Original failed comparison is not an artwork regression. Body dimensions lower
naturally through recline; current South head progression is more compact than
the historical pack, with supported upward pitch kept throughout sleep.

New native fixture passes15017checks0failures: four facings/both prescribed gears,
normal actor.update20ms stage progression, all18 rest slots per case, repeated
sleep cycles, fixed foot/facing/gear and zero-delta source freeze.248 chronological
native source-change captures reviewed across eight boards. Engine0/no timeout;
strict scratch APPDATA owner profile unchanged.736 selected source/manifest/
controller/registry inputs unchanged; only idle0 masters visually reviewed,
not every idle slot. No production/art/clock/metadata changes in this review.

Scope is prescribed initial life_lie on a clear corridor node: no furniture,
chooser/arrival, service event/fatigue benefit, Continue, acquired gear or natural
task proof. Prior actual North berth journeys remain separate evidence.12.6s
all-cardinal paired GIF is constructed source-clock playback, not native video.
Full James set/motion/context/owner acceptance remains incomplete. Next: actual
special East bunk and selected rest interruption/Continue contexts, plus remaining
full-family continuous and cross-family material/proportion reviews.
'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    data=path.read_bytes()
    if b'## James current selected rest reconciliation and clock review' in data:continue
    new=note.lstrip().encode()+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+note.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);os.replace(tmp,path)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: current James rest clock review

## Objective and acceptance
Full James animation/master/style/perspective/proportion/material and cross-family
polish goal remains active and incomplete. Do not infer full acceptance from this.

## Accepted decisions and constraints
Current loader/whole-source identity revisions govern, not older comparison boards.
Matte master grade, adult anatomy, supported sleep head and belt wrench persist.

## Current state
South/East/West identity-v2 and North ordinary rest material selected unchanged.
New ordered selection snapshot,144 source/four full/four head review boards,
native-clock.gd/.uid and strict runner,248 native captures/eight chronology boards,
constructed12.6s all-cardinal comparison GIF. Five guides record reconciliation.
Historical head-edit study and its two generated outputs remain unselected.

## Verification
56source joins/reverse/clock checks and15017normal timer/renderer checks pass.
All144 selected source references/eight idle0 masters and248native captures reviewed.
736 frozen inputs unchanged; engine0/no timeout/owner guardtrue. Initial raw-canvas
standing failures corrected by registration(+36,+52); no art changed to pass.
Prescribed life_lie initialization, corridor floor, no natural service/furniture/
Continue/gear acquisition or continuous native video claims. Native session65261
completed, image generation839 completed; no new live job.

## Next action
Actual special East bunk lifecycle/interruption/Continue review and remaining
cross-family source/motion/master context quality. Check latest loader again before
authoring: old folders and archived boards are evidence of their own revisions.
''')
old=R/'character/james-south-rest-head-polish-v1'
(old/'SUPERSEDED.md').write_text('''# Historical head edit study — superseded baseline

These targets came from rest-material-continuity-v1 South, which current loader
overrides with james-rest-south-identity-v2. Neither generated output nor extracted
representative is selected. Do not install or expand this study as a current fix.
See ../james-selected-rest-review-2026-10-01/HANDOFF.md and CURRENT_STATUS for the
current ordered-source review and native clock evidence. All originals retained.
''')
handoff=old/'HANDOFF.md';data=handoff.read_text();prefix='Historical study only: current loader selects South identity-v2. See SUPERSEDED.md.\n\n'
if not data.startswith(prefix):handoff.write_text(prefix+data)
print('Current selected rest milestone recorded; historical study explicitly superseded; full goal active.')
