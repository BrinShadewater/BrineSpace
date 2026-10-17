from pathlib import Path
import hashlib,json,shutil,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-rest-family-selected-v1';W=R/'output/veld-rest-family-station-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
n=json.loads((O/'validation.json').read_text());w=json.loads((W/'validation.json').read_text())
normal_log=(O/'native.log').read_text()
match=re.search(r'VELD REST FAMILY SELECTED: (\d+) checks,0 failures',normal_log)
assert n['returnCode']==0 and match and 'ERROR:' not in normal_log;assert w['returnCode']==0 and '47 checks,0 failures' in (W/'native.log').read_text()
normal_checks=int(match.group(1));package_checks=json.loads((P/'verification.json').read_text())['checks']
index=R/'tests/index.json';data=json.loads(index.read_text())
for key,reason in [('test_veld_rest_family_selected','Normal Veld loader, generic1840ms/reverse snapshots and native cardinal source proof.'),('test_veld_rest_family_station','Actual habitation rotations/east specialised bunk regression need native capture.')]:
    if key not in data['subsystems']['veld-rest']:data['subsystems']['veld-rest'].append(key)
    data['lanes'][key]={'lane':'native','reason':reason}
index.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
note='''

## Veld generic rest family selected - October 1, 2026

Normal grid loader now selects both literal veld-rest-family-v1 manifests after wet death overrides, with paired ACTIVE_ASSETS entries.24states/104refs/48unchanged authored exports,1840ms finite lie/exact reverse rise/held sleep. Veld generic life_stage_seconds and snapshot transition limit now1.84s; selected specialised east bunk retains its own1.84s motion. Shared life offset/head alignment uses actor duration instead of.8; equipped head metadata preferred with legacy bare fallback. Family head offset includes14.592world-pixel draw lift, matching layered renderer convention. Source candidates unchanged; staged family metadata/build/banner/evidence retained under revisions/staged-before-selection-v1.

249selected packaging checks/4deterministic files and634normal-loader checks pass: all source pixels/gears/cardinal roles, native148/82, controlled actual Veld class action clocks, exact interruption reverse at seven phases including boundaries, player paused snapshots and actor snapshot admission. Eight reversal failures at floating boundaries resolved by looking up actual player down slot and choosing retained reverse clock from elapsed/±epsilon to match its reversed texture. Veld rest_interruption_seconds is dispatched by existing service-loss branch; other actors retain prior hook. Fixture first used inactive actor/empty fatigue goal and invalid RefCounted.free, corrected to valid active fatigue stage/reference release; failed intervals retained, hung errored process explicitly stopped. Corrected normal run24.01s engine0. Separate actual default habitation four-rotation47checks/eight captures pass,43.51s engine0, physical approach and optional head-alignment bypass preserved; native bunk rest visually reviewed. This is specialised bunk regression, NOT generic cardinal bed/contact/routing/Continue/death proof. BOTH overall runners FAILED: last_session.json delta among2,931real non-log files in scratch intervals. No attribution/restore/clean-profile claim.

Full goal active/incomplete: actual compatible generic furniture/head contact and shared offset math, actual service-loss/save/fresh-scene generic continuity, already-resting/seated death pose/world offsets, seated/life sources and full-set identity/detail/grade/camera/anatomy/live-motion polish remain. Current habitation exposes specialised east bunk rather than fabricated cardinal generic targets. No commit/export or owner-layout changes. Handoff:character/veld-rest-family-v1/HANDOFF.md.

Lesson: do not add epsilon blindly at half-open reversal boundaries; derive the actual source slot from the same player clock and compare candidate retained clocks against the reversed target. A valid rest checkpoint needs active life state and fatigue goal as well as a long enough timer limit. Separate normal source/controlled actor clock proof from world service-loss/restoration; correct head-center metadata must include renderer draw lift and equipment ownership.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;old=p.read_bytes()
    if note.lstrip().encode() not in old:p.write_bytes(note.lstrip().encode()+old if rel=='docs/CURRENT_STATUS.md' else old+note.encode())
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode() not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode())
html=P/'index.html';s=html.read_text(encoding='utf-8').replace('Staged family:','Selected generic family:').replace('402 actual-player','634 normal-loader/player').replace('Furniture contact, life-stage timing, normal selection and interrupted-rest/death joins remain.','Generic furniture contact, routing, saved interruptions and rest/death joins remain. Existing specialised bunk passes47checks/eight real habitation captures.').replace('/output/veld-rest-family-candidate-v1/','/output/veld-rest-family-selected-v1/')
s=re.sub(r'\b(?:249|265) packaging',f'{package_checks} packaging',s)
s=re.sub(r'\b\d+ normal-loader/player',f'{normal_checks} normal-loader/player',s)
html.write_text(s,encoding='utf-8')
review=P/'integration-review';review.mkdir(exist_ok=True)
shutil.copy2(W/'rotation-0-berth-0-rest.png',review/'selected-bunk-rest.png')
handoff='''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld selected generic cardinal rest

## Objective and acceptance
Full master-matched Veld animation set and whole-set polish active/incomplete. Generic cardinal family normally selected; controlled source/clock proof and selected bunk regression complete, generic furnished/world/owner acceptance unproven.

## Accepted decisions and constraints
24states/104literal paths/48unchanged exports,1840ms finite lowering/exact reverse rise/held sleep. Directional masters/palette/native scale/handed tools preserved. Exact standing/seated hardware or authored depth pitches as recorded. Specialised east bunk unchanged. No commit/export/owner-layout changes.

## Current state
Normal loader and ACTIVE_ASSETS select both family manifests. Veld generic stage duration/snapshot limit1.84s; shared offset/head progress uses actor duration and gear head metadata with legacy fallback. Family anchors include14.592world draw lift. Existing service-loss branch dispatches Veld slot-aware reverse hook, other actors unchanged. New selected/station .gd/.uid/scratch runners/native lanes. Staged metadata revision retained. Pipeline/bible/skill/current status updated.

## Verification
249package checks and634normal-loader/player/controlled Veld clocks/snapshot admission/exact interrupted reversal checks pass. Native148/82 reviewed unchanged frames. Actual default habitation four rotations47checks/eight captures pass, selected bunk physical approach/head bypass preserved and visible. Corrected native24.01s/station43.51s engines0; BOTH strict full owner-profile guards FAILED last_session.json among2,931non-log files under explicit scratchAPPDATA. Failed fixture/boundary intervals retained, one hung errored process explicitly terminated. No attribution/restore/clean-profile claim. Source/controlled reversal is not actual service-loss/Continue/routing/furnished cardinal rest.

## Next action
Prove compatible generic bed/head contact and equipment placement when actual geometry provides it, shared offset math across the1.84s stages, actual service-loss/paused/fresh-scene generic checkpoints. Current habitation provides selected east bunk, not generic cardinal targets. Already-resting/seated deaths need pose/world-offset continuity. Own seated/life sources and full-set cross-animation grade/detail/anatomy/camera/live-motion polish remain. No blocker; keep full goal active.
'''
handoff=handoff.replace('249package',f'{package_checks}package').replace('634normal-loader',f'{normal_checks}normal-loader').replace('Corrected native24.01s',f"Latest native{n['seconds']}s")
handoff+='\n## Registered rest alignment follow-up\n\nEight paired cardinal sleeping anchors independently reconstructed from source registration, opaque head pixels and actual CELL384*.17/H148 plus14.592 draw lift. Controlled real RoomActivity resolver uses retained registered hab_berth_west fixture geometry; five progress samples per lowering/sleep/rise prove1840ms body/head alignment and unchanged physical foot, gear-specific ownership and legacy fallback.1062checks pass; this is alignment math, not installed generic furniture or visual contact/route/Continue proof. Source exports and production scripts unchanged in this follow-up.\n'
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['integration-evidence.json','candidate-evidence.json']]
paths.extend([R/f'scripts/{name}.gd' for name in ['crew_life','veld_npc','bill_npc','grid_canvas']]);paths.extend([R/'character/ACTIVE_ASSETS.json',index])
paths.extend([R/f'tests/test_veld_rest_family_{kind}.gd{suffix}' for kind in ['selected','station'] for suffix in ['', '.uid']]);paths.extend([R/'tools/run_veld_rest_family_selected.py',R/'tools/run_veld_rest_family_station_validation.py'])
paths.extend(p for root in [O,W] for p in root.iterdir() if p.is_file())
e={'normalSelection':True,'packagingChecks':package_checks,'normalPlayerChecks':normal_checks,'actualBunkChecks':47,'normalRunner':n,'stationRunner':w,'scope':'normal source/controlled Veld clock+reverse/snapshot admission/retained registered berth resolver+alignment math/actual default specialised bunk; no generic furnished routing/Continue/death/full-set acceptance','files':{p.relative_to(R).as_posix():sha(p) for p in paths}}
(P/'integration-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8');print(json.dumps({'boundFiles':len(paths),'normalChecks':normal_checks,'bunkChecks':47,'normalSelection':True}))
