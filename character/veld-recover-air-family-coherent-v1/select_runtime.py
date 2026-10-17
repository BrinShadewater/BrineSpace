from pathlib import Path
import json,shutil,os
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
archive=P/'revisions/before-runtime-selection-v1';archive.mkdir(parents=True,exist_ok=True)
for f in [ROOT/'scripts/grid_canvas.gd',ROOT/'character/ACTIVE_ASSETS.json',P/'bare-manifest.json',P/'helmet-manifest.json']:
 target=archive/f.name
 if not target.exists():shutil.copy2(f,target)
registry_path=ROOT/'character/ACTIVE_ASSETS.json';registry=json.loads(registry_path.read_text())
key='veld-dry-recovery-family'
for gear,section in [('bare','actionOverrides'),('helmet','equipmentActionOverrides')]:
 path=f'character/{P.name}/{gear}-manifest.json';registry[section][key]=path
 binding={'script':'scripts/grid_canvas.gd','contains':'res://'+path}
 if binding not in registry['bindings']:registry['bindings'].append(binding)
temporary=registry_path.with_name('ACTIVE_ASSETS.veld-recovery.tmp');temporary.write_text(json.dumps(registry,indent=2)+'\n',encoding='utf-8');os.replace(temporary,registry_path)
s=(ROOT/'tests/test_veld_recover_air_family_candidates.gd').read_text()
s=s.replace('Candidate injection, genuine','Normal selection, genuine').replace('candidate-native-v1','selected-native-v1').replace('VELD RECOVERY CANDIDATE','VELD RECOVERY SELECTED').replace('Injected candidate pixels','Normal loader pixels')
lines='\tplayer.load_manifest(PACKS["bare"],true)\n\tcheck(player.load_equipment_manifest("diving-helmet",PACKS["helmet"]),"Candidate injection")\n'
assert lines in s;s=s.replace(lines,'')
(ROOT/'tests/test_veld_recover_air_family_selected.gd').write_text(s)
(ROOT/'tests/test_veld_recover_air_family_selected.gd.uid').write_text('uid://bd5w8p2m4k913\n')
s=(ROOT/'tools/run_veld_recover_air_family_candidate_validation.py').read_text().replace('candidate-native-v1','selected-native-v1').replace('test_veld_recover_air_family_candidates.gd','test_veld_recover_air_family_selected.gd').replace('Veld candidate dry recovery family','Veld selected dry recovery family')
(ROOT/'tools/run_veld_recover_air_family_selected_validation.py').write_text(s)
print('Selected recovery registry bindings and prepared normal-loader validation;backup retained')
