"""Idempotent, byte-preserving milestone notes and after-run evidence bindings."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld supported held-bunk death candidate - October 1, 2026'
note='''
## Veld supported held-bunk death candidate - October 1, 2026

character/veld-bunk-death-east-v1 stages paired finite880ms supported relaxation
from exact selected specialised East sleeper256/p128,224/H148. Built-in raw
exec-b32d13ce-f1c9-437f-8f17-6d45bddbd0d2/prompt saved. One130/586 source ruler;
near forearm/glove inserts only, original head/hair/helmet/shoulder badge/torso
hardware/waist panel/legs/contact exact. Raw whole-body/knee drift rejected.
18package checks pass. No new normal loader or ACTIVE_ASSETS selection.

veld_death_motion.gd opts into death-bunk-east only from held bunk-sleep-east,
same gear, entrance0/first1 and mandatory typed bed offset/depth. Contact persists
through finite interiors and corpse instead of releasing at180ms. Existing
live/water/legacy/other dry routes retained. Partial enter/exit not substituted.

Eight actual mortality cases/default habitation4rotations/both gears:630native
checks0failures,55.05s engine0;32source/native samples and32typed actor-file fresh
dead restores at retained world clocks, exact source/bed position/depth without
navigation graph.56invalid payload and16partial route guards. All2931owner non-log
files unchanged under scratch APPDATA. First70.52s fixture failed on void loader
return asserted as bool; errored process128912 precisely stopped, logs/guards
archived, no owner changes. Water regression1954checks0fail/64oxygen deaths,
39.06s engine0,2931owner files unchanged. No full RunSave/fresh-scene Continue.
Source/GIF/native32room crops/all8cases and same-ruler helmet audit reviewed;
browser candidate shown. Evidence hashes after run; interval stability unmeasured.

Remaining: inherited bunk helmet shell/visor/hardware drift is visible against
current master-fitted generic rest/upright references. Fit all7bunk poses with
proper pitch/contact; complete partial enter/exit and seated deaths, full-scene
Continue/lifecycle/furniture loss, then normal selection. Full set/polish goal open.

Lesson: lying death must retain furniture contact through the entire motion and
corpse, not just exact live entrance. Save presentation selectors/contact so dead
restore does not depend on cleared navigation geometry. Exact reuse of a selected
source prevents new drift but does not certify inherited master fidelity; audit
construction at one native ruler and keep identity repair visible as remaining.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
count=0
for i,p in enumerate(targets):
    b=p.read_bytes()
    if title.encode() in b:continue
    n=note.strip().encode()+b'\n\n'
    p.write_bytes(n+b if i==0 else b+b'\n'+n);count+=1
paths=[R/'scripts/veld_death_motion.gd',R/'scripts/veld_death_motion.gd.uid',R/'scripts/grid_canvas.gd',R/'scripts/veld_npc.gd',R/'tests/test_veld_bunk_death.gd',R/'tests/test_veld_bunk_death.gd.uid',R/'tools/run_veld_bunk_death.py',R/'character/dr-veld-v2/supplemental/bunk-east/bare/006.png',R/'character/dr-veld-v2/supplemental/bunk-east/helmet/006.png',R/'character/veld-rest-east-coherent-v1/frames/helmet/lie-down-east/005.png',R/'character/veld-unified-turn-helmet-v1/master-east.png']
paths += [p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='evidence.json']
O=R/'output/veld-bunk-death-east-v1';paths += [O/f for f in ['native.log','validation.json','records.json','profile-before.json','profile-after.json']]
W=R/'output/veld-water-death-entry-v1';paths += [W/f for f in ['native.log','validation.json','profile-before.json','profile-after.json']]
bindings={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(P/'evidence.json').write_text(json.dumps({'bindings':bindings,'hashScope':'after-run evidence only; not interval-stable dependency claim','normalSelection':False,'remaining':'seven-pose bunk master helmet fit, partial entering/exiting and seated deaths, full-scene Continue/lifecycle, broader full-set polish'},indent=2)+'\n')
print(f'{count} milestone notes updated;{len(bindings)} after-run evidence bindings')
