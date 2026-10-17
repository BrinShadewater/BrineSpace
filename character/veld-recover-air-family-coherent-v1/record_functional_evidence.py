from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
survival=ROOT/'output/veld-recover-air-family-candidate-native-v1';world=ROOT/'output/veld-recovery-furnished-v1'
a=json.loads((survival/'validation.json').read_text());b=json.loads((world/'validation.json').read_text());w=json.loads((world/'furnished-checks.json').read_text())
assert a['passed'] and b['passed'] and w['failures']==0
assert '1923 checks,0 failures' in (survival/'native.log').read_text()
binding=json.loads((P/'source-bindings.json').read_text());assert len(binding)==48
assert all(sha(ROOT/f)==h for f,h in binding.items())
captures={r['capture']:sha(ROOT/r['capture'].removeprefix('res://')) for r in w['results']}
report={'states':8,'references':48,'candidateExplicitlyInjected':True,'runtimeChanged':False,'survivalChecks':1923,'lowAirSafeAirCases':64,'actualDiskRestores':24,'interruptionCases':32,'interruptions':['walking pose override/resumed performed clock','task stage pose override/resumed clock','renewed flooded-low-air episode','actual die plus normal survival dispatch excluding dead actors'],'survivalValidation':a,'furnishedValidation':b,'furnishedReport':w,'sourceBindingsSha256':sha(P/'source-bindings.json'),'sourceBindings':binding,'captureHashes':captures,'clearanceAuditSha256':sha(P/'clearance-audit.json'),'evidenceHashes':{str(f.relative_to(ROOT)):sha(f) for f in [survival/'native.log',survival/'validation.json',world/'native.log',world/'validation.json',world/'furnished-checks.json',ROOT/'tests/test_veld_recover_air_family_candidates.gd',ROOT/'tools/review_veld_recovery_furnished_v1.gd']},'visualReview':'native82family contact;furnished deepest east/west bare,north/south helmet screenshots reviewed. Projected overlap counts do not establish3D collision/universal safety;continuous motion and front helmet pitch polish pending.'}
(P/'functional-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
lesson='''

## Veld actual dry recovery transitions/restores — September 30, 2026

Candidate family passes1923actual Veld actor/renderer checks:64low-air/safe-air
cases,24disk restores and32state interruption cases.114furnished checks exercise
all48poses at8clear points in5authored rooms/1625graph nodes;native family and
four contextual deep-bend views inspected,profiles unchanged. Dry recovery has
no consumed pose-clearance profile gate: measure its real visual envelope and
compare new furniture overlaps with selected idle/prior art;do not add unread
clearance entries or call projected screen overlaps3D collision proof.
Use actual die() and normal Flood.advance dispatch for death interruption.
Directly flipping dead does not enter death state;direct step_crew can bypass the
dispatch's dead-actor exclusion. Preserve failed fixtures and source contracts;
do not change production to satisfy an invented timer-zero expectation.
Runtime remains unchanged;geometry/pitch/continuous-motion follow-up precedes
selection. Evidence:character/veld-recover-air-family-coherent-v1/functional-evidence.json.
'''
for name in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else ROOT/name
 with f.open('a',encoding='utf-8') as stream:stream.write(lesson)
f=ROOT/'docs/CURRENT_STATUS.md';text=f.read_text(encoding='utf-8');f.write_text('''## Veld recovery physiology/checkpoints and furnished review — September 30, 2026

Staged8gear states/48refs pass1923actual actor/renderer checks:64genuine low-air
transitions,24disk restores,32walking/task/flooding/death interruption cases.
114furnished checks exercise all48poses at8clear points across5rooms/1625nodes;
native82family and4contextual deep-bend views reviewed. Engine errors0,2914real
non-logfiles unchanged. Fixtures corrected to actual die()/normal survival
dispatch and uppercase Preferences;failed intervals retained. Dry recovery lacks
a pose-clearance gate;new projected envelope overlaps are diagnostic and still
need geometry/pitch/continuous-motion follow-up before selection. Runtime
unchanged;full remaining life/rest/distress/death and polish goal active.
[Evidence/handoff](../character/veld-recover-air-family-coherent-v1/HANDOFF.md).

'''+text,encoding='utf-8')
print('Recorded recovery transitions,restores,interruptions and furnished evidence;runtime unchanged')
