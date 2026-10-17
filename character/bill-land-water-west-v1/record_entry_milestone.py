from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
f=P/'entry-review.json';e=json.loads(f.read_text(encoding='utf-8'));e['visualReview']='Full original West master/common148ruler seven-pose strip inspected. Compact endpoint-conditioned lift/prone retain smaller master-like build; earlier crouch/push heads and torsos visibly larger. Early pose proportion correction required before helmet pairing/native admission.500ms/APNG integrity is packaging evidence, not smoothness or full identity acceptance.';e['visualAcceptance']='incomplete: earlier crouch/push proportion mismatch';f.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note='''## Bill West compact lift/prone entry source trial — October 2, 2026

Added endpoint-conditioned compact lift and near-prone independently authored
poses to bare West entry. First lift from push reference rejected for elongated
torso/extended arms; retained exec-358c29b1-fcc7-444c-8b61-376d8c313e9d/raw/prompt.
Near-prone from exact West swim:exec-ec81c94a-f432-454c-bab5-947ccf2be471; compact
lift edited from that:exec-02899f8b-4977-4af1-b382-97351d14ee94. All raw sources/
prompts retained. Actual1254square→320wholecanvas scale only; largest opaque
component+3pxalpha fringe. Lift whole-pose translation(-1,-14)registers explicit
crown130,150; near-prone stays0,0/crown131,188. Painted support preserved, no
per-pose body-height fitting or rigid limb rotation. Prior five poses RGBA exact.

New unselected bare manifest/7frames/common320p160224H148 and source-enter APNG.
Holds60,70,80,60,80,90,60 total500ms;7decoded frames+durations exact. Original
idle/swim are exact padded context, not actual moving gait boundary admission.
Full common-ruler master/7pose board inspected. New compact lift/prone closer to
master endpoint build; EARLIER CROUCH/PUSH HEADS/TORSOS visibly larger. Visual
consistency INCOMPLETE; correct earlier anatomy before canonical helmet pairing.
Do not enlarge correct compact endpoint poses to match drifted early sources.
Packaging pass does not certify motion smoothness/master identity. No native run,
normal renderer/player/actor/save changes or West Continue proof. No commit/export.

Lesson: derive final tilt poses from the actual swimming endpoint to constrain
anatomical lengths. Intermediate-conditioned generation can compound size drift
without changing canvas dimensions. Review every pose on common master ruler;
pixel preservation of older poses is provenance, not a reason to retain mismatches.
Next early West crouch/push proportion repair, helmet pairing, actual phase/
material/clearance/native/Continue; North/South bridges, cargo lifecycle and full
Bill master/style/perspective/size/proportion/colour cross-family polish remain.
Full goal active/incomplete. Review:character/bill-land-water-west-v1/index.html.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel;t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
p=P/'HANDOFF.md';t=p.read_text(encoding='utf-8');t+='\n## Seven-pose bare entry trial\nAdded lift-v2/prone-v1 raw sources/prompts/native and rejected lift-v1. build_entry.py\npackages unselected bare7frames/manifest/APNG500ms, entry-review.json/master strip.\n7decoded frames+holds exact;prior5poses exact. Fixed320/1254canvas, liftwholepose\n(-1,-14)→crown130150,prone0→131188,painted support preserved. Full board reviewed:\nearly crouch/push heads/torso larger than compact endpoint-derived lift/prone.\nVisual identity consistency INCOMPLETE. Next repair early anatomy before helmet\nand native/Continue admission. No normal actor/save/source changes. Guidance updated.\n';p.write_text(t,encoding='utf-8')
print('Recorded seven-pose source trial and unresolved early proportion drift; goal active.')
