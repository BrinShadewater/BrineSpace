"""Prepare normal catalogue North fixture with explicit old-source counterfactual."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-v2/supplemental/north-walk-polish-v1'
a=json.loads((OUT/'admission.json').read_text())
s=(ROOT/'tools/review_marsh_north_walk_world_v1.gd').read_text().replace('north-walk-world-v3-2026-10-03','north-walk-selected-world-v2-2026-10-03')
counter={'pivot':[92,172],'standingHeight':148,'states':[x['state'] for x in a['oldStates'].values()]}
(OUT/'original-counterfactual-manifest.json').write_text(json.dumps(counter,indent=2)+'\n')
lines=[' var original_player=preload("res://scripts/crew_sprite_player.gd").new()',' original_player.load_manifest("res://character/marsh-v2/supplemental/north-walk-polish-v1/original-counterfactual-manifest.json")']
for key in a['oldStates']:lines+=[' normal_rows['+json.dumps(key)+']=original_player.frames['+json.dumps(key)+'].duplicate()']
for key,x in a['newStates'].items():
 slots=list(range(6)) if key=='walk-north' else [0]
 for i in slots:
  lines+=[' check(player.frames['+json.dumps(key)+']['+str(i)+'].get_image().get_data()==source_image('+json.dumps(x['state']['frameFiles'][i])+').get_data(),"normal catalogue submits admitted North source")']
needle=' player.load_manifest("res://character/marsh-north-walk-family-detail-v1/manifest.json",true)';assert needle in s
s=s.replace(needle,'\n'.join(lines))
s=s.replace('staged six-phase override loaded into actual grid player','normal catalogue six-phase family loaded into actual grid player').replace('staged phase-specific stop','normal phase-specific stop').replace('staged six-phase art and six exact stop-entry aliases override only in fixture instance','normal catalogue six-phase art and six exact stop-entry aliases; explicit original-source counterfactual')
s=s.replace('func contact(texture:Texture2D)', 'func source_image(path:String)->Image:\n var decoded:=Image.new()\n var error:=decoded.load_png_from_buffer(FileAccess.get_file_as_bytes(path))\n check(error==OK,"explicit source PNG bytes decode")\n return decoded\nfunc contact(texture:Texture2D)')
(ROOT/'tools/review_marsh_north_walk_selected_v1.gd').write_text(s)
(ROOT/'tools/review_marsh_north_walk_selected_v1.gd.uid').write_text('uid://dmnorthselected1\n')
f=(ROOT/'tools/fingerprint_marsh_north_walk_world_v1.py').read_text();needle='records={p.relative_to(ROOT)'
addition="paths.update(p for p in (ROOT/'character/marsh-v2/supplemental/north-walk-polish-v1').glob('*') if p.is_file())\npaths.update(ROOT/'tools'/n for n in ['install_marsh_north_walk_family_v1.py','prepare_marsh_north_walk_selected_v1.py','review_marsh_north_walk_selected_v1.gd','review_marsh_north_walk_selected_v1.gd.uid','fingerprint_marsh_north_walk_selected_v1.py'])\n"
f=f.replace(needle,addition+needle);(ROOT/'tools/fingerprint_marsh_north_walk_selected_v1.py').write_text(f)
p=(ROOT/'tools/publish_marsh_north_walk_world_v1.py').read_text().replace('north-walk-world-v3-2026-10-03','north-walk-selected-world-v2-2026-10-03').replace('marsh-north-walk-family-detail-v1/world-review','marsh-v2/supplemental/north-walk-polish-v1/world-review').replace("ROOT/'character/marsh-north-walk-family-detail-v1/manifest.json'","ROOT/'character/marsh-v2/supplemental/north-walk-polish-v1/manifest.json'").replace('3816','3840').replace("'normalAdmission':False","'normalAdmission':True")
(ROOT/'tools/publish_marsh_north_walk_selected_v1.py').write_text(p)
print('Prepared actual normal catalogue fixture;Separate original sprite loader;12 selected decodes +12 selected-source assertions:3840 checks expected.')
