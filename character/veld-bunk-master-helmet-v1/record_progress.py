from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld seven-pose bunk helmet and whole-body drift audit - October 1, 2026'
note='''
## Veld seven-pose bunk helmet and whole-body drift audit - October 1, 2026

character/veld-bunk-master-helmet-v1 stages native master East helmet0..3 and
built-in authored reclining shell/gasket4..6. Raw/prompt/result
exec-3ceb331e-e2e1-4f5e-9268-fdacc3feffcb saved. One35/157 reclining ruler and
pooled semantic native-master grade; generated bodies excluded, original body
outside bounded head/collar fit exact.10helmet exports, paired4states/18refs
per gear:entry7/exit7/sleep1/death3, original1840ms live/880ms death clocks.
No normal loader/ACTIVE_ASSETS or production script changes this turn.

22package checks and1302native checks0failures/89.11s engine0. Actual main/default
habitation4rotations/both gears, candidate wrappers injected:112prescribed live
lowering/rising samples/all7poses, fixed physical approach foot and valid live
snapshots;8actual held deaths/32typed actor-file fresh-dead restores at retained
clocks, exact source/bed offset/depth/corpse. All2931owner non-log files unchanged
under scratch APPDATA. Full112unmodified room crops/4boards,7head/source and
standing-master boards reviewed; browser candidate shown. No fresh-scene full
RunSave Continue/natural approach/partial-transition death/owner acceptance.
Evidence hashes after interval, not frozen source/dependency stability.

Source review exposed crop-induced neck gap: extend authored gasket (initial
source crops ended668/721), exclude neighboring chest badge and erase rear bun
separately instead of rectangular clearing through original front neck. Upright
master includes collar; rigid whole-component roll into lying pose can penetrate
mattress. Author reclining shell/gasket perspective while retaining supported
body, then prove actual native bed contact; do not squeeze hardware to fit.

Same148ruler/p128,224 cross-animation standing audit finds older bunk body still
drifted: bare140opaque-height vs selected idle148, candidate helmet146 vs selected
helmet155. Body narrower/offset, blue-gray suit and amber insignia/scanner/hardware
differ from current master. Helmet source/contact repair is useful staged work,
not whole-bunk consistency. Next rebuild entire bunk body from dense current
master with exact idle joins, one source ruler and registered bed/seat anatomy;
refit these helmets, then partial/seated deaths/full-scene Continue/lifecycle/
normal selection. Full Veld set/master/style/perspective/size/grade polish open.

Lesson: run same-ruler whole-figure comparison even when repairing only a helmet.
Nominal standingHeight metadata and exact reuse can conceal inherited stature,
uniform and lateral-anchor drift. Passing native clocks/contact cannot certify
master identity; let contrary visual evidence change the next authoring task.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
changed=0
for i,p in enumerate(targets):
    b=p.read_bytes()
    if title.encode() in b:continue
    n=note.strip().encode()+b'\n\n';p.write_bytes(n+b if i==0 else b+b'\n'+n);changed+=1
files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='evidence.json']
files += [R/'tests/test_veld_bunk_master_helmet.gd',R/'tests/test_veld_bunk_master_helmet.gd.uid',R/'tools/run_veld_bunk_master_helmet.py',R/'scripts/veld_death_motion.gd',R/'scripts/grid_canvas.gd',R/'scripts/veld_npc.gd',R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png',R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png']
for f in json.loads((P/'package-checks.json').read_text())['sourceBindings']:files.append(R/f)
O=R/'output/veld-bunk-master-helmet-v1';files += [O/f for f in ['native.log','validation.json','records.json','profile-before.json','profile-after.json']]
bindings={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(P/'evidence.json').write_text(json.dumps({'bindings':bindings,'scope':'after-run file hashes only; no interval-frozen stability claim','normalSelection':False,'goalStatus':'active/incomplete','next':'whole bunk body/master idle joins and registration before full lifecycle/selection'},indent=2)+'\n')
print(f'{changed}milestone targets updated;{len(bindings)}after-run bindings')
