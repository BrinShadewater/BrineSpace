from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;F=P.parent/'bill-meal-north-family-v1'
OUT=ROOT/'output/bill-drink-entry-north-candidate-native-v1';NATIVE=ROOT/'output/bill-meal-north-family-candidate-native-v1'
for package,out,count in [(P,OUT,87),(F,NATIVE,299)]:
 assert json.loads((package/'verification.json').read_text())['passed']
 n=json.loads((out/'validation.json').read_text());assert n['passed'] and not n['realProfileChanges']
 assert f'{count} checks,0 failures' in (out/'native.log').read_text(encoding='utf-8')
cup='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill north cup pickup/return candidate

## Objective and acceptance
Complete Bill's master-consistent full animation set, then full-set polish.
North cup transitions join exact selected idle to current north drinking hold.

## Accepted decisions and constraints
Selected rear idle owns identity, perspective, matte materials and standing size.
Right arm reaches forward for cup; left arm stays down. Cup/hand remain physically
occluded in front, never drawn on backpack. Planted upright stance; no camera turn.
Do not change galley geometry or original6s eat/3s drink clocks for art fixtures.

## Current state
Raw built-in exec-3ce77744-5d35-4ba4-b961-f2b1f1dd8164/exact prompt retained.
Six413/413/414/414/414/414px figures; five interiors0..4. Redundant source5 low
hold retained unused. Fixed[.338,.3574] atlas ruler,density.94, selected north
neutral/hair/burgundy grade and sole223. Exact idle/current drink000 donors.
Two bare states/14refs, seven580ms slots/exact reverse return.256plane/pivot128,224/
H148/dry0. Build/verify/preview/registration/hash evidence retained. Source copy
tool uses word-bounded action substitution so seated paths/create methods survive.
No normal loader/actor/reward/geometry changes. Full north family remains staged.

## Verification
28package/87native PASS13.24s. Source/donor bindings, exact loaded pixels, metadata,
finite pacing/hold, reverse poses and exact idle/held joins. Native148/82/idle
boards reviewed; no obvious steps, extra hands or back props. Fine detail,
silhouette and return/contact readability remain for polish. All2,914 owner
non-log files unchanged under scratch APPDATA. Actual counter contact, saved
service phases, interruptions and disk restore pending.

## Next action
Full north meal family assembled separately; author south meal family next,
then normally install/test actual N/S service phases/contact/interruptions/restore.
West meals, generic rest/dry death, wider inspection audits and full polish remain.
Goal active; no commit/export requested.
'''
family='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill north full bare meal candidate family

## Objective and acceptance
Complete Bill's full master-consistent animation set, then full-set polish.
North six-state meal family assembled and native reviewed; service install pending.

## Accepted decisions and constraints
Four source parents keep generation/grade/ruler provenance. Shared256plane,
pivot128,224/H148/dry0; whole literal res paths, no duplicated rasters. Preserve
standing idle, matte grade, physically correct rear prop occlusion and planted feet.
580ms transitions,960ms loops, original6s eat/3s drink presentation. Helmets keep
inspection behavior; actual current galley approaches N/S. No geometry changes.

## Current state
Six staged states/42refs: eat-enter/eat/eat-exit/drink-enter/drink/drink-exit north.
Parents bill-meal-entry-north-v1, bill-meal-north-coherent-v1,
bill-drink-entry-north-v1 and bill-drink-north-coherent-v1. Build binds all parents'
manifest/hash/pacing and exact five adjacent joins, full idle closure and reversals.
Preview shows full meal beside selected idle. No normal loader/registry/actor
changes; old bare north meals remain normally active until service integration.

## Verification
39assembly/299native candidate checks PASS13.28s.42 exact source refs, metadata,
pacing, loop closure/repeats, finite holds, all joins and both reversals. Native82
six-row board reviewed, parents148/82/idle separately reviewed. Both native runs
preserve all2,914 owner non-log files in scratch APPDATA. Presentation clocks are
not proof of actual activity. Fine backpack/panel/suit detail and interior
alignment remain for full-set polish. Actual worktop reach, saved phase clock,
interruption/restore, normal selection and autonomous service acceptance pending.

## Next action
Author south bare meal family; install actual N/S activity phases with saved-clock,
power loss/contact/hazard interruption and disk restore proof. Keep full cardinal
art coverage, finish west/rest/drydeath and inspection wider audits, then full
cross-animation polish. Goal active; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(cup,encoding='utf-8');(F/'HANDOFF.md').write_text(family,encoding='utf-8')
note='''
Bill north cup transitions/full meal candidate family — September30,2026.
Built-in cup exec-3ce77744-5d35-4ba4-b961-f2b1f1dd8164/exact prompt retained.
Six413/413/414/414/414/414px figures; five interiors0..4, source5 retained unused.
Fixed[.338,.3574] ruler,density.94, selected north matte grade/sole223 and exact
idle/drink-held donors. Right arm reaches, free left arm stays down; physically
occluded front cup. Two bare states/14refs/seven580ms slots/exact reverse.
28package/87native PASS13.24s;148/82/idle reviewed. North family assembled:
sixstates/42whole literal refs/no raster copies;39assembly/299native PASS13.28s.
All adjacent joins, closures, reversals, pacing and metadata checked; native82
family board reviewed. All2,914 owner non-log files intact in both scratch runs.
No normal loader/actor/geometry/reward changes; original6+3s preview only.
Lesson: check all source-family joins and retain rear front-prop occlusion;
exact endpoint pixels and passing loader fixtures do not prove worktop contact
or saved activity phases. Fine backpack/panel/suit and interior proportion polish
remain. Next south meals, normal actual N/S phase/contact/interruption/restore
integration, remaining west/rest/drydeath and full-set polish. Full goal active.
Handoffs:character/bill-drink-entry-north-v1/HANDOFF.md and
character/bill-meal-north-family-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill north full meal candidate family assembled — September30,2026\n'+note+'\n').encode()+status.read_bytes())
for package,out,counts,extra in [(P,OUT,{'package':28,'native':87},['source-rulers.json','registration.json','frame-hashes.json','verify.py','build_preview.py','contact-sheet.png']),(F,NATIVE,{'package':39,'native':299},[])]:
 files=[package/name for name in ['build.py','manifest.json','verification.json','HANDOFF.md','index.html']+extra]+list((package/'sources').glob('*'))+[out/'validation.json',out/'loaded-water-carry.png']
 (package/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':counts,'native':json.loads((out/'validation.json').read_text()),'scope':'source/candidate native joins only; normal service/contact/interruptions/restore/full polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded cup transitions and full north meal assembly; south/service/polish pending')
