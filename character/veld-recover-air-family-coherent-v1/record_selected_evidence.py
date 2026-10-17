from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
native=ROOT/'output/veld-recover-air-family-selected-native-v1';overlap=ROOT/'output/veld-recovery-overlap-v1'
n=json.loads((native/'validation.json').read_text());o=json.loads((overlap/'validation.json').read_text());r=json.loads((P/'selected-rebuild-checks.json').read_text())
assert n['passed'] and o['passed'] and r['passed']
assert '1922 checks,0 failures' in (native/'native.log').read_text()
assert '66 checks,0 failures' in (overlap/'native.log').read_text()
test=ROOT/'tests/test_veld_recover_air_family_selected.gd';s=test.read_text();assert 'player.load_manifest(' not in s and 'player.load_equipment_manifest(' not in s
manifests=[P/'bare-manifest.json',P/'helmet-manifest.json']
for f in manifests:assert json.loads(f.read_text())['status'].startswith('installed')
bindings=json.loads((P/'source-bindings.json').read_text());assert len(bindings)==48 and all(sha(ROOT/f)==h for f,h in bindings.items())
files=[ROOT/'scripts/grid_canvas.gd',ROOT/'character/ACTIVE_ASSETS.json',test,ROOT/'tools/run_veld_recover_air_family_selected_validation.py',native/'native.log',native/'validation.json',native/'loaded-water-carry.png',overlap/'native.log',overlap/'validation.json',ROOT/'tools/review_veld_recovery_overlap_v1.gd',P/'selected-rebuild-checks.json']+manifests
for gear in ['bare','helmet']:
 for direction in ['east','west']:files.append(overlap/f'recover-air-{direction}-{gear}.png')
(P/'selected-evidence.json').write_text(json.dumps({'installedLocally':True,'states':8,'references':48,'candidateInjection':False,'normalLoaderChecks':1922,'lowAirTransitions':64,'diskRestores':24,'interruptionCases':32,'normalLoaderValidation':n,'overlapComparisonChecks':66,'overlapValidation':o,'rebuild':r,'sourceBindings':bindings,'evidenceHashes':{str(f.relative_to(ROOT)):sha(f) for f in files},'visualScope':'All current native82 recovery/return views inspected;4same-foot/camera idle/prior/new overlap comparisons inspected. No visible clipping at sampled points;rectangle overlap alone did not justify a movement guard. Not all possible geometry/traffic or owner/full-set acceptance. Front helmet pitch/complete motion and cross-family polish remain.'},indent=2)+'\n')
lesson='''

## Veld dry recovery selected — September 30, 2026

Normal loader selects8gear states/48refs;1922checks pass with candidate loads
removed,including64low-air transitions,24disk restores and32interruptions.
Actual family rebuild preserves2manifests/48frames byte-exact.66same-foot/camera
native comparisons show idle/prior/new at4extra projected-overlap points;no
visible clipping found at those samples. Do not turn projected bounding-box
overlap counts into a new dry movement restriction without visual/contextual
evidence. Historical textures need the room-renderer's crew_frame_92 metadata
flag;reaching the frame selector alone does not prove the comparison was drawn.
Initial missing-flag comparison was rejected and retained;corrected captures
reviewed. Source art unchanged,owner profile unchanged,engine errors0. Local
selection is not full-set/owner acceptance;front pitch/continuous motion and
remaining life/rest/distress/death/cross-family polish remain. Evidence:
character/veld-recover-air-family-coherent-v1/selected-evidence.json.
'''
for name in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else ROOT/name
 with f.open('a',encoding='utf-8') as stream:stream.write(lesson)
f=ROOT/'docs/CURRENT_STATUS.md';t=f.read_text(encoding='utf-8');f.write_text('''## Veld dry recovery family selected — September 30, 2026

Eightgear states/48refs installed locally through literal loader overrides and
registry.1922normal-loader checks PASS33.75s,64low-air transitions,24disk restores,
32interruptions;no candidate loads.66corrected native idle/prior/new comparisons
reviewed at4projected-overlap points;no visible clipping in these samples,so no
new movement guard.2manifest/48frame actual rebuild byte-exact. Native82family
reviewed,engine errors0,2914real non-logfiles unchanged. Historical metadata-flag
review failure retained. Front helmet pitch/continuous motion andremaining
life/rest/distress/death/cross-family polish remain;full goal active.
[Handoff](../character/veld-recover-air-family-coherent-v1/INSTALL_HANDOFF.md).

'''+t,encoding='utf-8')
print('Recorded current selected recovery evidence and workflow lessons')
