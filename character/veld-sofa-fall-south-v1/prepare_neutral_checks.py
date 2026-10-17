"""Retain prior staged evidence and extend paired entrances for empty hands."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
text=(R/'tests/test_veld_sofa_fall_south_staged.gd').read_text(encoding='utf-8')
text=text.replace('veld-sofa-fall-south-staged-v1','veld-sofa-fall-south-neutral-staged-v1')
needle='\treturn game\n'
text=text.replace(needle,'\tgame.grid_view.veld_player.load_manifest("res://character/veld-sofa-fall-south-v1/bare-neutral-manifest.json",true)\n\tcheck(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-sofa-fall-south-v1/helmet-neutral-manifest.json"),"Paired neutral branch")\n'+needle,1)
text=text.replace('[.05,.10,.25,.40,2.40,4.20]','[.05,.10,.25,.40,2.40,4.20,11.95]')
text=text.replace('\t\t\tactor.prepare_death_motion(game);actor.die()','\t\t\tvar expected_clip:String="death-sofa-neutral-south" if reading_sample in [.05,11.95] else "death-sofa-read-south"\n\t\t\tactor.prepare_death_motion(game);actor.die()')
text=text.replace('=="death-sofa-read-south","Actual staged','==expected_clip,"Actual staged')
text=text.replace('frames["death-sofa-read-south"]','frames[expected_clip]').replace('[key]["death-sofa-read-south"]','[key][expected_clip]')
text=text.replace('["first","seat","equipment","slot"]','["first","seat","equipment","slot","branch"]')
text=text.replace('\t\t\t\t\t"slot":bad.veld_water_death.entry_index=14','\t\t\t\t\t"slot":bad.veld_water_death.entry_index=14\n\t\t\t\t\t"branch":bad.veld_water_death.clip="death-sofa-read-south" if expected_clip=="death-sofa-neutral-south" else "death-sofa-neutral-south"')
text=text.replace('interruptions==12 and restores==48','interruptions==14 and restores==56').replace('Twelve distinct incoming poses and48actor restores','Fourteen entrances including both neutral endpoints and56actor restores').replace('VELD SOUTH SOFA FALL STAGED','VELD SOUTH SOFA FALL NEUTRAL STAGED').replace('12 prescribed actor deaths/48 actor-file restores','14 prescribed actor deaths/56 actor-file restores')
(R/'tests/test_veld_sofa_fall_south_neutral_staged.gd').write_text(text,encoding='utf-8')
(R/'tests/test_veld_sofa_fall_south_neutral_staged.gd.uid').write_text('uid://d0evssfntr1\n',encoding='utf-8')
runner=(R/'tools/run_veld_sofa_fall_south_staged.py').read_text(encoding='utf-8')
runner=runner.replace('veld-sofa-fall-south-staged-v1','veld-sofa-fall-south-neutral-staged-v1').replace('test_veld_sofa_fall_south_staged.gd','test_veld_sofa_fall_south_neutral_staged.gd').replace('12 prescribed actor deaths/48 actor-file restores','14 prescribed actor deaths/56 actor-file restores').replace('VELD SOUTH SOFA FALL STAGED','VELD SOUTH SOFA FALL NEUTRAL STAGED')
runner=runner.replace("f'character/veld-sofa-fall-south-v1/{gear}-manifest.json'","f'character/veld-sofa-fall-south-v1/{gear}-manifest.json'")
needle='    frozen_paths=sorted(set(frozen_paths))'
extra='''    for gear in ['bare','helmet']:
        manifest=ROOT/f'character/veld-sofa-fall-south-v1/{gear}-neutral-manifest.json'
        frozen_paths.append(manifest)
        for state in json.loads(manifest.read_text(encoding='utf-8'))['states']:
            frozen_paths.extend(ROOT/f.removeprefix('res://') for f in state['frameFiles'])
    frozen_paths.append(ROOT/'character/veld-sofa-fall-south-v1/build_neutral.py')
'''
runner=runner.replace(needle,extra+needle)
(R/'tools/run_veld_sofa_fall_south_neutral_staged.py').write_text(runner,encoding='utf-8')
execution={'tool':'built-in imagegen','outputs':[{'raw':'edit-v1.png','defaultOutput':'exec-6ddc49e4-a303-42db-9e75-25fceed56985.png','prompt':'prompt-v1.txt','decision':'rejected: top-right tablet retained behind relaxed gloves; global shading drift'},{'raw':'edit-v2.png','defaultOutput':'exec-82424637-50fb-4da4-b00c-8f69d62e975a.png','prompt':'prompt-v2.txt','decision':'only bounded forearm/waist patches used; other source changes rejected'}]}
for row in execution['outputs']:
    for key in ['raw','prompt']:row[key+'SHA256']=hashlib.sha256((P/'sources/neutral-branch'/row[key]).read_bytes()).hexdigest()
(P/'sources/neutral-branch/execution.json').write_text(json.dumps(execution,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'newNativeTest':True,'priorTestRetained':True,'worldScope':'actor API only; ordinary world save/future still pending'}))
