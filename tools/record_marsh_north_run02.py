"""Record North complete-source authoring and scoped staged actor evidence."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-run-material-v1'
MARKER='## Marsh North run02 complete-source and staged actor review — October 2, 2026'

def main():
    review=BASE/'actor-review-v1'
    evidence=json.loads((review/'verification.json').read_text())
    assessment=json.loads((review/'visual-assessment.json').read_text())
    assert evidence['failures']==0 and evidence['exitCode']==0 and evidence['engineErrors']==0
    assert evidence['exactSources']==8 and evidence['actorPlayerRestores']==6
    assert assessment['allEightViewsInspected']
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
    installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    lesson=f'''
{MARKER}

Full Marsh master/style/camera/size/height/proportion/grade goal remains active and
incomplete. North run02 is staged and UNSELECTED. The normal catalog remains at
76 body manifests, 228 selected states and 1190 slots (coverage only). No normal
North run admission or full RunSave/Title Continue proof belongs to this milestone.

Own selected rear idle is PRIMARY: occupied55x146, runtimeH148,184canvas,p92/172.
Original north-standing-identity-01 controls blond hair whorl, rear collar/back
plate/harness/pouches and small right-temple edge. Raised charcoal soles and small
ankle hardware are authentic; ivory uppers remain distinct. Both unchanged whole
guides and original master inspected. North guide wrapper depends on the West
guide helper; both dependency hashes frozen in the initial request.

Source01 exec-35310d7b-3b5c-4960-8e3e-fdaebde77cc0 has seven complete separated
figures. One neutral146 BOX scale .24292845257903495 gives six sizes59x144,
57x145,57x140,61x145,57x145,58x132 and ruler54x146. Contacts/passing repeat
left support; not a complete accepted alternating cycle. Rear body/material
improved compared with the old selected run; whole source comparison inspected.

Contacts02 exec-ef4d6379-f06c-4cdf-9858-33a62c898ded uses unchanged selected
North walk0/walk3 opposite support guides, selected idle primary and own original
master. Four complete cells, one neutral146 BOX scale .21128798842257598:
left contact58x148, right contact59x146, WRONG left-support passing59x146 and
ruler57x146. Opposite contacts retained; passing figure rejected for repeating
left support. First contact's raised sole projects below its flat support boot;
generic bbox alignment at172 is not anatomical support/contact certification.

Passing03 exec-cbba8b12-5290-42b2-8087-239e1a3fefda uses a complete unchanged
right contact stance guide, selected idle primary and original rear master.
Two complete cells, one neutral146 BOX scale .17016317016317017: right passing
61x146 and ruler57x146. Right support/raised left sole visible, but arm posture
remains contact-like and sole lift stronger than requested. Provisional for joins
review. Raw corners and middle gutter alpha0 and two separated alpha128 groups
confirmed; generated preview haze alone does not establish an opaque background.
All exact prompts, ordered reference/source SHAs, raw files, original paths and
generation IDs retained. Standard whole alpha128/BOX packing only; no limb patches,
mirroring, recolour or per-pose fitting. No clipped opaque pixels.

Candidate02 uses six BYTE-IDENTICAL complete packed sources: contacts02 left,
source01 left passing, source01 right-leading flight, contacts02 right, passing03
right passing, source01 left-leading flight. Sizes58x148/57x145/57x140/59x146/
61x146/58x132. Runtime184,p92/172,H148; existing six100ms loop and explicit North
stride .11027027027027027 unchanged. Six decoded APNG frames match exact source
pixels; illustrative holds are not realtime film. Whole selected/new comparison
inspected; body/head/quiet warm grade closer, rigid plate/leg/arm joins provisional.

Fresh staged actual Marsh.move/main/grid/player review uses the validated physical
South vertical168world interval in REVERSE. Actual North segment_clear checks
candidate+168 to candidate; signed negativeY progression, fixedX. This reverses
the route only, never artwork. Dedicated free fixture room, normal global economy/
failure flags remain false; not paid-construction proof. Fixture UIDcw4nhrunm7v90
paired. Scratch APPDATA, retargeted restored actor/player state, owner's save unused.
{evidence['checks']} checks, eight exact source/native framebuffer crop pairs,
{evidence['controlledSamples']} controlled20ms samples, {evidence['wraps']} wraps,
six actor/player restores and pause holds, normal slowing walk. Zero failures,
engine errors and exit0. {evidence['stableBoundedInputs']} bounded inputs stable,
{evidence['unchangedOwnerNonLogFiles']} owner non-log files unchanged. All eight
source/native crop views in two boards inspected. No full-scene occlusion,
continuous moving sole contact, natural traffic/equipment/full-family acceptance.

Lessons: a two-stance guide can still yield a third pose on the wrong support leg.
Inspect every whole leg/flat boot/raised sole relationship; labels and bbox bottoms
do not prove it. A correct support reference can also carry contact arms into a
passing request. Judge the complete posture and phase joins independently from
neutral ruler dimensions. Keep raw alpha evidence separate from preview appearance.

Next: review North passing arms/contact and flight joins, then independent normal
eight full checkpoints/fresh visible Title Continues if admitted. Carry/remaining
held families and full-set consistency/polish remain. Do not reuse West/East/South
normal proofs for North. Goal active/incomplete.
'''
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with p.open(encoding='utf-8') as stream: present=any(MARKER in line for line in stream)
        if not present:
            with p.open('a',encoding='utf-8') as stream: stream.write(lesson)
    installed.write_bytes(maintained.read_bytes())
    handoff=f'''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: North run02 staged source

## Objective and acceptance
Full master-matched animation set and consistency/polish active/incomplete.
North02 complete alternating source cycle remains unselected. No normal admission
or full RunSave/Title Continue acceptance in this milestone.

## Accepted decisions and constraints
Own selected55x146 rear body and original rear master. RuntimeH148,184canvas,
p92/172,six100ms/current distance cadence. Authentic charcoal raised soles,
back plate/harness/hair whorl/right-temple edge. Whole alpha128 cells, one neutral
BOX scale per authored sheet, whole translations only. No mirror/limb patch/recolour
or pose fitting. Scratch APPDATA; owner profile unchanged. No gameplay changes.

## Current state and changed files
North sources01/contacts02/passing03 with exact prompt/order/source hashes and raw
generation provenance. Candidate01, contacts02-unselected, passing03-unselected,
candidate02 with six byte-identical complete sources/APNG/whole comparison.
New prepare/build/assemble tools and native fixture+UID/fingerprint/publisher/
recorder; wrappers retain West guide/pack/assembly dependencies. Actor-review-v1
eight exact crops/two paired boards/verification/assessment/index. Pipeline,
bible, current status and maintained/installed master-repair skills appended.

## Verification and scope
Stage {evidence['checks']} checks,8 exact views,{evidence['controlledSamples']}
controlled20ms samples,{evidence['wraps']} wraps,6 restores+pause holds,normal
slowing walk. {evidence['stableBoundedInputs']} stable bounded inputs,
{evidence['unchangedOwnerNonLogFiles']} unchanged owner non-log files,0 failures,
engine errors and exit0. Physical vertical route reversed, signed North movement.
All source/ruler/whole cycle/two source-native boards inspected. Six decoded APNG
frames equal sources. This is not normal full-save/Continue, full-scene occlusion,
continuous motion/contact or equipment/full-family acceptance.

## Remaining work and next action
Source01 repeats left-support halves; contacts02 passing rejected, contacts retained.
Passing03 right support clear but contact-like arms and strong lifted sole remain.
Review complete joins/contact projection, then independent normal8 checkpoints/
visible Title Continues if admitted. Carry/held families/full consistency/polish
remain. Goal active. No live native process after this milestone.
'''
    (ROOT/'docs/MARSH_NORTH_RUN_02_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded North02 staged review, source corrections and lessons; skill mirrors identical; full goal incomplete.')

if __name__=='__main__':main()
