from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'key-chain-study-v1';N=R/'output/veld-east-key-chain-v1'
expected=json.loads((N/'inputs-after.json').read_text(encoding='utf-8'))
changed=[name for name,sha in expected.items() if hashlib.sha256((R/name).read_bytes()).hexdigest()!=sha];assert not changed,changed
(S/'carry-forward.json').write_text(json.dumps({'checkedInputs':len(expected),'changed':changed,'scope':'Native interval runtime inputs unchanged after read-only replay/material diagnostic.'},indent=2)+'\n',encoding='utf-8')
title='## Veld East sparse key-chain contact diagnosis — October 3, 2026'
note=title+'''\n\nkey-chain-study-v1 references exact original held/lift/contact whole sprites,
both gears,3distinct poses with prescribed180ms diagnostic holds. No source edits,
reconstructed limbs, invented tween artwork or final motion admission. Native
actual crew_sprite_player source clock plus prescribed8nativepx/sec root exercises
37times per gear,including before/after .18/.36s joins at47/93/148.155checks0,
74presentations/6.09s/engine0/16inputs stable/2931owner files unchanged/scratch
APPDATA.148exact native replay pixel/duration checks0. Both whole chronological
boards and native three-scale contact key viewed. Initial helmet chronology crop
clipped its top3px; corrected review crop395..570 and full helmet board inspected.

Technical success is NOT moving-contact success. Independent warm near-boot
material registration on native captures finds held->lift jump -4px at148 and
-3px at93 in both gears. Whole trial spans4/3px; minimum NCC .687/.662, contact
boot shape changed and correspondence weakens. Material-translation proxy, not
rigid sole proof. Visual chronology also shows case/sleeve contour and brightness
change, especially contact pose. Source-key count is not continuous motion.
Do not select this sparse chain as finished animation or hide joins through root
teleports/per-frame artwork moves. Root velocity is diagnostic, not final stride.

Next original-only tiny heel-peel/prelift source, dense faithful intermediates,
full upper-body/material consistency and actual contact/root start-stop proof.
East full cycle/near-far identity, North gait, full original action-direction,
furniture/ordinary controller/save/Continue and final library polish remain.
Goal active/incomplete. Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Sparse key-chain contact failure and next source requirements recorded; frozen native inputs intact.')
