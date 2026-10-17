from pathlib import Path
import json,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'review-evidence.json').read_text());a=json.loads((P/'material-and-joins.json').read_text())
assert e['sourceReferences']==696 and len(e['boards'])==16 and all(x['exactRGBA'] for x in a['joins'])
report={'status':'selected_sources_reviewed_material_polish_pending','runtimeOrArtChanged':False,'sourceReferences':696,'pairedStates':24,'boardsReviewed':e['boards'],'masterBoardsReviewed':[f'{d}-masters.png' for d in ['east','north','south','west']],'exactRGBAJoins':32,'visualReview':'All696 selected dry torch draw/weld/stow references inspected on16 paired boards against four bare/helmet idle masters. Stable adult build, boots, shared helmet and forward torch orientation. Interior lower-suit/hand green residue needs bounded source-material review, most evident North draw1. No per-pose size normalization warranted by this source review.','materialDiagnostic':a['summary'],'causeEvidence':'Existing direct-v1 grade.py neutral selector requires blue>=green-4; greener source material is excluded from the neutralization. This explains a plausible residual route, not a proof that every green pixel is unwanted.','limitations':['No new native/controller/route/Continue evidence','No continuously watched full-motion claim from contact sheets or generated source GIF','No full-set or owner acceptance','Bounds include raised torch/flame; do not force source alpha bounds to master stature']}
(P/'selection-review.json').write_text(json.dumps(report,indent=2)+'\n')
text='''## James full standing torch source consistency — October 1, 2026

Current loader inventory refreshed337bare/4280refs,247helmet/3764refs; zero
retained is selection coverage, not acceptance. New read-only torch review freezes
696selected references (348per gear),24paired directional draw/weld/stow states,
paths/hashes/pivots/148rulers/durations. All16paired chronological source boards
and four paired idle master boards reviewed. All32whole-RGBA idle→draw→weld→stow→
idle joins exact. Adult build/boots/shared shell/forward torch retained; no new
anatomy/scale/grade/selection/runtime edits. Source one-pass GIFs do not reproduce
longer controller work timers or establish continuously watched native motion.

Material polish remains: opaque lower-suit low-chroma y90..165 sampling flags
green excess >4 in8.54% North draw1 pixels vs3.44% North idle; South6.10% vs4.09%,
East2.31%/West2.00% vs0%. Same suit sample in both gears. Not all flagged pixels
are spill: diagnostic is evidence to inspect, not an automatic color target.
Existing direct-v1 grade.py cold neutral mask blue>=green-4 excludes greener
residue; median material and exact joins do not prove interior chroma continuity.

Lesson: review every selected source slot inside clips as well as exact endpoint
joins. Freeze source revision and compare the same body material in both gears;
preserve engineering yellow/skin/hair/flame/helmet and geometry when correcting
residual key color. Source alpha height includes raised tools/flame and must not
drive per-pose resizing. Next bounded residual-material correction, complete
chronological/native controller review and broader cross-family polish. Full
James goal active/incomplete; no new Godot/profile/Continue/owner acceptance claim.
Handoff: character/james-standing-torch-consistency-v2/HANDOFF.md.

'''
def atomic(p,data):
    t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,p)
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,p in enumerate(paths):
    old=p.read_bytes();b=text.encode();assert b not in old;atomic(p,b+old if i==0 else old+b'\n\n'+b)
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James standing torch consistency

## Objective and acceptance
Full James animations/master/art/perspective/scale/proportions/grade consistency,
then full cross-family polish. Active; source review is not full-set acceptance.

## Accepted decisions and constraints
Matte accepted masters, forward torch, belt wrench, stable adult build and shared
helmet. Fixed148ruler and source pivots; raised tool bounds are not body height.

## Current state
New build_review.py/analyze.py, four master boards,16paired all-source boards,
four source interval GIFs, frozen review-evidence/material-and-joins/selection-
review.json. No art/runtime selection changes. Current inventory refreshed.

## Verification
All696selected refs reviewed;32RGBA joins exact. Interior material residue
flagged, strongest North draw1; existing cold mask excludes green pixels.
No new Godot/native/profile/continuous motion evidence. Prior seated controller,
12power-loss and6fresh-scene Continue evidence remains separately scoped.

## Next action
Bounded residual-material correction with exact protected pixels/alpha/tools/
shell and unchanged source rulers/clocks/endpoints; then complete source/native
motion and handoff review. Other families/rotations/gear/travel and full owner/
export acceptance remain open. No process/provider job live.
'''
atomic(P/'HANDOFF.md',handoff.encode())
print(json.dumps({'allSourceReferencesReviewed':696,'exactJoins':32,'guidesUpdated':5,'materialPolishPending':True}))
