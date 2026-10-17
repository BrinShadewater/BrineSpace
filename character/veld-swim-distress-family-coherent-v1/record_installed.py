"""Bind normal-loader selection, real escapes and the scoped gesture-phase correction."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proofs={}
for label,folder,count in [('lifecycle','veld-swim-distress-family-installed-v1',763),('escape','veld-distress-escape-installed-v1',713)]:
 o=R/'output'/folder;v=json.loads((o/'validation.json').read_text(encoding='utf-8'))
 assert v['passed'] and not v['candidateOnly'] and not v['realProfileChanges']
 assert f'{count} checks,0 failures' in (o/'native.log').read_text(encoding='utf-8')
 proofs[label]={'checks':count,'result':v,'files':{f.relative_to(R).as_posix():sha(f) for f in o.iterdir() if f.is_file()}}
report=json.loads((R/'output/veld-distress-escape-installed-v1/journey-checks.json').read_text(encoding='utf-8'))
assert len(report['cases'])==8 and all(c['crossedDryAlive'] and c['safeRecoveryObserved'] for c in report['cases'])
reg=R/'output/veld-distress-phase-regressions-v1';comparison=json.loads((reg/'baseline-comparison.json').read_text(encoding='utf-8'))
assert comparison['noNewScriptFailures'] and all(t['errorsIdentical'] for t in comparison['tests'])
for t in comparison['tests']:
 assert sha(reg/t['test'])==t['currentSha256']
 assert sha(R/'output/veld-distress-phase-baseline-v1'/t['test'])==t['baselineSha256']
registry=json.loads((R/'character/ACTIVE_ASSETS.json').read_text(encoding='utf-8'))
assert registry['actionOverrides']['veld-swim-distress-family']=='character/veld-swim-distress-family-coherent-v1/bare-manifest.json'
assert registry['equipmentActionOverrides']['veld-swim-distress-family']=='character/veld-swim-distress-family-coherent-v1/helmet-manifest.json'
files=[R/n for n in ['scripts/grid_canvas.gd','scripts/grid_canvas.gd.uid','scripts/crew_sprite_player.gd','scripts/crew_sprite_player.gd.uid','character/ACTIVE_ASSETS.json','tests/test_veld_swim_distress_family_installed.gd','tests/test_veld_swim_distress_family_installed.gd.uid','tools/run_veld_swim_distress_family_installed.py','tools/review_veld_distress_escape_installed_v1.gd','tools/review_veld_distress_escape_installed_v1.gd.uid','tools/run_veld_distress_escape_installed_v1.py','tools/run_veld_distress_phase_regressions_v1.py','tools/run_veld_distress_phase_baseline_v1.py']]
files+=[P/n for n in ['bare-manifest.json','helmet-manifest.json','source-bindings.json','build.py','check_rebuild.py','rebuild-checks.json','make_motion_review.py','motion.html','motion-review-bindings.json']]+list((P/'frames').rglob('*.png'))
files+=list((reg/'baseline').glob('*.gd'))+[reg/'baseline-comparison.json',reg/'validation.json']
e={'status':'selected_local_family_motion_polish_pending','states':8,'references':48,'runtimeArtworkSelected':True,'clearanceProfileChanged':False,'normalLoaderProofs':proofs,'phaseEntryCases':48,'phaseExitCases':48,'physicalRoutes':8,'guardChecks':64,'existingRegressionFailures':comparison,'boundFiles':{f.relative_to(R).as_posix():sha(f) for f in files},'visualReview':'Selected master/cardinal and fresh installed native boards reviewed. Browser join review now permits exits after any phase. Continuous full-family perceived motion acceptance remains open.','remaining':'first-interior and arbitrary-exit motion polish; remaining death/rest/life/full-set cross-family consistency; crowd/exterior and locker completion separate'}
(P/'installed-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
lesson='''

## Veld swimming distress selected and gesture exit phase corrected — September 30, 2026

Normal grid loader and ACTIVE_ASSETS now select8 cardinal bare/helmet distress
states/48refs. Source pixels, native helmets, selected148px ruler and existing
clearance retained.16 exact swim0 entry/closure donors and32 authored interiors.
763 normal-loader lifecycle checks PASS34.2s, including48 distance-driven entry
phases and48 gesture exit phases.713 normal-loader escape checks PASS44.29s:
all8 real flooded-room routes cross doorways, consume air and recover alive;
64 lock/fire/wall negatives retained.2914 owner non-logfiles unchanged.
Two manifests/48frames/source bindings rebuild byte-exact. Installed native
master/cardinal and actual-route boards reviewed. Full perceived motion remains
open; motion.html now previews an exit after any chosen distress phase.

Initial installed phase gate failed40 exits: CrewSpritePlayer treats the first
hyphenated key component as state, so swim-distress appeared to be the swim gait.
The scoped fix excludes swim-distress keys from same_gait phase preservation.
A broader state parser altered compound cargo-turn phase behavior and was
rejected; preserve existing gait semantics while correcting this gesture exit.
Do not prove transitions only from neutral endpoints: exercise every incoming
distance phase and outgoing gesture phase through the actual player.

Older walk/swim/cargo-turn suites remain FAIL1/1024/12 respectively; isolated
pre-fix copies reproduce identical script ERROR sequences. They are not passing
regression evidence. Older walking native runs repeatedly log a GLES shader
initialization error; retained, with headless retry separating script failures.
No such renderer error in fresh installed763/713 native runs. Current normal
selection proof supersedes historical staged labels, without upgrading historical
injected furnished/restore evidence into normal-loader proof. Source and failed
intervals retained. First-interior/arbitrary-exit perceived motion, death/rest/life
and whole-set consistency remain. Full goal active;no commit/push/export.
'''
for name in ['docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld swimming distress selected and gesture exit phase corrected' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=R/'docs/CURRENT_STATUS.md';current=f.read_bytes()
if b'## Veld cardinal swimming distress selected locally' not in current:
 f.write_bytes('''## Veld cardinal swimming distress selected locally — September 30, 2026

Normal loader/registry select8gear states/48refs with exact master joins and
unchanged authored interiors/clearance.763 native lifecycle checks PASS34.2s,
including48 incoming swim phases/48 outgoing distress phases. Scoped player
fix prevents swim-distress from preserving gesture phase as swimming gait.
713 normal-loader real escape checks PASS44.29s:8 routes/64 lock/fire/wall
negatives.2914 owner non-logfiles unchanged; installed native boards reviewed.
Older walk/swim/turn suites still fail1/1024/12, identically under pre-fix
player copies; not a passing regression suite. Older walk native GLES startup
errors retained; headless retry distinguishes existing script failure.
Current installed-evidence.json supersedes historical staged status. Perceived
continuous first-interior/arbitrary-exit motion remains open; review offers
selectable exit phases. Death/rest/life and full-set consistency remain.
Full goal active;no commit/push/export.
[Handoff](../character/veld-swim-distress-family-coherent-v1/HANDOFF.md).

'''.encode('utf-8')+current)
f=P/'HANDOFF.md';s=f.read_text(encoding='utf-8')
if 'Normal selection milestone:' not in s:
 s=s.replace('This is staged source and candidate playback evidence, not full runtime or owner acceptance.','This family is selected locally; full-set motion and owner visual acceptance remain open.')
 s=s.replace('Preserve runtime and clearance until lifecycle and motion evidence supports selection.','Preserve selected source rulers and clearance; continuous motion polish remains separate from normal-loader selection.')
 s=s.replace('## Next action','Normal selection milestone:8states/48refs installed via final grid overrides and registry.763 normal-loader lifecycle checks PASS34.2s;48 swim entry phases/48 distress exit phases. Initial40 exit failures resolved by excluding swim-distress from swimming gait phase carryover.713 normal-loader physical escape checks PASS44.29s/all8 routes/64 negatives; owner2914 files unchanged. Fresh installed native boards reviewed. Two-manifest/48-frame rebuild exact. Historical furnished/restore checks remain injected scope. Older walk/swim/turn suites fail1/1024/12 identically under pre-fix copies; GLES startup errors in older walking native runs retained, headless script retry matches baseline. installed-evidence.json is current authority.\n\n## Next action')
 s=s.replace('Normal-loader selection verification and continuous-motion/first-interior/arbitrary-phase exit polish.','Continuous-motion/first-interior/arbitrary-phase exit polish, followed by missing death/rest/life coverage. Normal-loader selection is verified.')
 f.write_text(s,encoding='utf-8')
print('Bound installed763/713 proofs,96 phase transitions and existing baseline failures; updated status,pipeline,bible,both skills and handoff')
