"""Record the completed North runtime milestone without rewriting older evidence."""
from pathlib import Path
import hashlib, json, os
from PIL import Image

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
def atomic_edit(path, transform):
    old = path.read_bytes()
    new = transform(old)
    temp = path.with_name(path.name + '.james-north.tmp')
    temp.write_bytes(new)
    assert path.read_bytes() == old, f'Concurrent modification: {path}'
    os.replace(temp, path)

world = json.loads((P/'native-world-evidence.json').read_text())
indexed = json.loads((P/'native-indexed-evidence.json').read_text())
assert (world['checks'], world['failures']) == (4076, 0)
assert (indexed['checks'], indexed['failures']) == (3752, 0)
assert len(indexed['matrix']) == 12
assert world['journeys'][0]['caseRestored']
frames = []
for sample in world['journeys'][0]['contactSamples']:
    path = ROOT / sample['native'].removeprefix('res://')
    frames.append(Image.open(path).convert('RGB'))
assert len(frames) == 21
frames[0].save(P/'native-world-review.gif', save_all=True, append_images=frames[1:],
               duration=[350]+[90]*19+[700], loop=0, disposal=2)

status = 'selected_runtime_north_empty_case_release'
atomic_edit(P/'build.py', lambda b: b.replace(b'staged_north_empty_case_release', status.encode()))
for name in ['registration.json','bare-manifest.json','helmet-manifest.json']:
    value = json.loads((P/name).read_text())
    value['status'] = status
    write_json(P/name, value)
for name in ['native-world.gd','native-indexed.gd']:
    uid = P/(name+'.uid')
    if not uid.exists():
        raise RuntimeError('Create canonical paired UIDs with the Godot prepare-uids.gd utility before recording.')

selection = {
    'status': status, 'ownerVisualAcceptance': False,
    'scope': 'North pickup1..5 cancellation; exact selected reverse entrances, independent empty-handed rear-prone bodies, original complete native case, exact selected empty swim0. Full James goal active.',
    'assetHashes': {name: hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['source.png','case.png','bare-manifest.json','helmet-manifest.json','registration.json']},
    'productionFiles': ['scripts/branforth_npc.gd','scripts/grid_canvas.gd','scripts/james_case_deposit.gd'],
    'evidence': {'package':'contract-evidence.json','actualReturnContinue':'native-world-evidence.json','indexedBranches':'native-indexed-evidence.json'},
    'limitations': ['Actual exterior dispatch uses helmet; paired bare evidence is normal-loader source/clock proof.', '12 controlled branches share one actual arrival and actor-only restores/site resets, not12 full trips/Continues.', 'Both strict owner-profile guards failed: last_session.json delta; causal attribution unproven; no owner-data restoration.', 'South release, world interruptions and full-set master/height/proportion/material/motion polish remain.']
}
write_json(P/'selection.json', selection)

handoff = '''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James North empty case release

## Objective and acceptance
Full James animation set and continual master/perspective/height/proportion/material/motion checks remain active. North release is integrated; owner visual acceptance is pending.

## Accepted decisions and constraints
Independent rear-overhead prone source, empty hands, torch holstered image-left and wrench fixed image-right. Source-v1 retained after small backpack/long legs review; selected source-v2 reauthors proportions. Complete bodies use one .23 ruler and pooled matte grades, selected cranial anchor and native North helmet. Preserve genuine glove foreground above the helmet. Original North case is a separate complete component; retain all860 opaque pixels at native scale1, plus nearest-owned fringe. No anatomy painting or per-pose height normalization.

## Current state
New pack includes raw sources/prompts, build.py/verify.py, six paired body poses, case.png, ten indexed profiles, registration/selection, native fixtures and paired UIDs, captures and runtime GIF. Runtime chronology is authored1,0,2,3,4 followed by exact selected swim0; source5 retained as a study. Case47x26 at[105,67], opaque core41x22. Release480..680ms with exact selected reverse pickup entrances. branforth_npc.gd, grid_canvas.gd and james_case_deposit.gd now support East/West/North. South remains unsupported; malformed-facing fixture negatives updated accordingly. Case anchor is captured before physical movement and belongs to the site. Route, extraction and reward rules unchanged.

## Verification
78 package checks pass. Native-world4,076 checks pass: one actual North dispatch/recall/airlock return, source2 release, moving empty join, fixed world case, no extraction/credit, paused fresh-scene disk Continue and dry alive completion. Normal loader checks all ten paired source boundaries/finite endpoints. Native-indexed3,752 checks pass:12 controlled work/pickup branches, all six naturally advanced indexes, exact entrances/empty joins, actor-only restoration and physical movement; pickup1..5 deposit cases. This is one actual arrival plus controlled branches, not12 full trips/Continues. Both engines exited0 without timeout/errors/warnings; scratch APPDATA resolved. Both strict full owner-profile guards FAILED with last_session.json delta. Attribution is unproven; owner data was not restored and fixtures were not rerun seeking a clean interval. Paired registered sheet and actual scene samples04/11 reviewed; runtime GIF uses only21 authoritative contactSamples.native captures. Metadata standingHeight148 is not anatomical-height acceptance.

## Next action
South independent empty-handed case release and native world integration. World invalidation/depletion/new attempt/death/traffic, remaining meals/cups/rest/life/mortality contexts and full cross-family master/height/material/motion polish remain. No commit/export requested; full goal stays active.
'''
(P/'HANDOFF.md').write_text(handoff, encoding='utf-8')
note = '''\n## James North empty case release — October 1, 2026

North pickup1..5 release integrated with independent rear-prone whole bodies, fixed .23 ruler, pooled matte grade, native North shell and original glove foreground. v1 small-pack/long-leg source retained; v2 selected. Raw chronology1,0,2,3,4 keeps wrists clear at release; exact selected reverse entrance/empty swim0 and480..680ms clocks. Original case separate component:860 opaque pixels preserved at native scale1,47x26 fringe at[105,67]. East/West/North now supported through normal loader/controller/site-owned crew-pass rendering; South next. Sourceindex0/work retain their legitimate existing tool-stow motion.
78package/4,076actual-world/3,752indexed checks pass. One actual North return and fresh-scene Continue, ten paired normal-loader source clocks,12 controlled branches from one actual arrival (actor-only restores/site resets). Actual exterior journey uses helmet; bare proof is source/clock only. Paired sheet and actual scene samples reviewed;21 contactSamples.native frames form native-world-review.gif. Both engines0/clean/no timeout/scratch resolved; both strict full owner-profile guards FAILED, last_session.json delta. Attribution unproven; no owner restore or clean-guard retry. Owner visual acceptance and anatomical master-height/full-set polish remain pending.
Lesson: inspect source semantics and wrist clearance at the first detached frame. Preserve genuine hand foreground when installing a shared helmet; paired pixel equality alone does not certify correct layer order. A complete separate source case may be reused exactly; do not synthesize it from a touching glove component. Keep cosmetic world anchor capture before movement and in the same render pass as James to avoid extra grading. See character/james-case-release-north-v1/HANDOFF.md for evidence scope. Full James goal active; South release, world interruptions and remaining contexts/full-set polish remain.
'''.encode('utf-8')
paths = [ROOT/'docs/CURRENT_STATUS.md', ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md', ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    if b'James North empty case release' not in path.read_bytes():
        atomic_edit(path, lambda old: note+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n'+note)
print(json.dumps({'selected':status,'gifFrames':len(frames),'guidanceFiles':len(paths),'checks':[78,4076,3752],'ownerProfileGuard':'failed: last_session.json'}))
