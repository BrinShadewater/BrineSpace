from pathlib import Path
import json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,data):
    before=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
    assert path.read_bytes()==before, str(path)+' concurrent edit'
    os.replace(tmp,path)
guard=json.loads((P/'native-arrival-continue-validation.json').read_bytes())
native=json.loads((P/'native-arrival-continue-evidence.json').read_bytes())
loader=json.loads((P/'validate-evidence.json').read_bytes())
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert native['failures']==0 and loader['failures']==0
original=json.loads((P/'inputs-before.json').read_bytes())
changed=[p for p,h in original.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert set(changed)=={'scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json'},changed
for mode in ['bare','helmet']:
    path=P/(mode+'-manifest.json');pack=json.loads(path.read_bytes());pack['status']='selected_native_validated'
    atomic(path,(json.dumps(pack,indent=2)+'\n').encode())
section=f'''## James East tablet matte correction selected — October 2, 2026

`character/james-tablet-east-matte-v3` now selected through the normal loader and
ACTIVE_ASSETS registry. All282 final source images reviewed in10boards plus paired
master/current/candidate comparisons. Tablet reads matte grey; original poses,
alpha bytes,148 standing ruler,92/172 pivot, clocks and exact master endpoints
retained. Native Godot material program corrects key-green RGB spill and bounded
bright low-chroma equipment pixels; source RGB outside that selector stays exact.
Non-key-spill shared-helmet difference pixels protected. Selector can include glove,
cuff or neutral hardware: it is not semantic tablet segmentation or a whole-body
grade. Hair/face/cross-family material acceptance remains separate.

1140package checks0fail; loader {loader['checks']}checks0fail and4native scale
captures reviewed. Actual prescribed diagnostics arrival/full source clock and
fresh main-scene disk Continue: {native['checks']}checks0fail. Full owner profile
unchanged under strict scratch APPDATA; terminal engine0/no timeout. Route capture
review recorded separately in VISUAL_REVIEW.md. Scope is prescribed task/initial
gear and stepped native actor, not natural chooser or continuous world video.
288of290frozen inputs unchanged; only loader/registry intentionally changed.

Lesson: local tablet/edge contamination does not justify darkening the whole suit.
Keep shared-shell pixels protected except the identified spill, retain original
alpha after native material rendering, and review every stowing pose to catch
threshold speckling. Integer-byte selectors keep exporter/verifier boundaries equal.
Rejected shader/export intermediates and generated redraw study retained.
Next: full side-carry/West tablet proportion and motion review beside current
masters, remaining context/interruption coverage and full-set cross-family polish.
Full James goal remains active/incomplete; no final owner acceptance/commit/export.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    path=R/rel;before=path.read_bytes();add=section.encode()
    atomic(path,add+b'\n'+before if rel.endswith('CURRENT_STATUS.md') else before+b'\n\n'+add)
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
atomic(path,path.read_bytes()+b'\n\n'+section.encode())
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October2,2026 · Project: {R} · Task: James East tablet matte correction

## Objective and acceptance
Full James set then cross-family master/style/perspective/height/proportion/grade
polish. This milestone corrects East tablet material only; full goal incomplete.

## Accepted decisions and constraints
Tablet diagnostics; belt wrench stays holstered. Torch repairs. Original motion,
alpha, shared helmet, body ruler and six-second inspection timing retained.

## Current state
Normal grid loader and ACTIVE_ASSETS select this paired pack. Native material
shader/exporter,282PNGs, manifests, complete source boards and paired GIF retained.
Previous sources/rejected studies retained. No commit/export.

## Verification
All282sources viewed;1140package/2356loader checks pass. Actual prescribed route/
fresh disk Continue {native['checks']}checks0fail; strict scratch full owner profile
unchanged.4native scale captures viewed; route review in VISUAL_REVIEW.md.
288/290frozen inputs unchanged; loader/registry intentional revisions only.

## Next action
Side-carry and West tablet full-motion/proportion review with current masters.
Full hair/body colour and all remaining context/cross-family acceptance open.
''')
(P/'selection-final-evidence.json').write_text(json.dumps({'productionInstalled':True,'frozenInputs':len(original),'changed':changed,'loaderChecks':loader['checks'],'routeChecks':native['checks'],'fullGoalComplete':False},indent=2))
print('Selected milestone and lessons recorded in five guides and handoff.')
