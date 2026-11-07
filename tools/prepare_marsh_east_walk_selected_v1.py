"""Probe normal selected art and an explicit original-source counterfactual."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-v2/supplemental/east-walk-polish-v1'
a=json.loads((OUT/'admission.json').read_text())
s=(ROOT/'tools/review_marsh_east_walk_world_v1.gd').read_text().replace('east-walk-world-v3-2026-10-03','east-walk-selected-world-v3-2026-10-03')
inventory=json.loads((ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-contact/inventory.json').read_text())
oldpaths=['res://'+r['path'] for r in inventory['states']['walk-east']['frames']];newpaths=a['newState']['state']['frameFiles']
lines=[' normal_rows["walk-east"]=[]',' for original_path in '+json.dumps(oldpaths)+':','  var old_image:=source_image(original_path)','  var old_texture:=ImageTexture.create_from_image(old_image)','  old_texture.set_meta("crew_pivot",Vector2(92,172))','  old_texture.set_meta("crew_standing_height",148)','  normal_rows["walk-east"].append(old_texture)',' var expected_selected='+json.dumps(newpaths),' for slot in range(6):','  check(player.frames["walk-east"][slot].get_image().get_data()==source_image(expected_selected[slot]).get_data(),"normal catalog submits admitted whole pose")']
needle=' player.load_manifest("res://character/marsh-east-walk-family-contact-v1/manifest.json",true)'
assert needle in s;s=s.replace(needle,'\n'.join(lines))
s=s.replace('staged six-phase override loaded into actual grid player','normal selected six-phase family loaded in actual grid player').replace('staged six-phase art override only in fixture instance','normal catalog selected six-phase family; explicit original walk-source counterfactual for same-root depth/pixel comparisons')
s=s.replace('func contact(texture:Texture2D)', 'func source_image(path:String)->Image:\n var decoded:=Image.new()\n var error:=decoded.load_png_from_buffer(FileAccess.get_file_as_bytes(path))\n check(error==OK,"explicit source PNG bytes decode")\n return decoded\nfunc contact(texture:Texture2D)')
(ROOT/'tools/review_marsh_east_walk_selected_v1.gd').write_text(s)
(ROOT/'tools/review_marsh_east_walk_selected_v1.gd.uid').write_text('uid://dmeastselected1\n')
f=(ROOT/'tools/fingerprint_marsh_east_walk_bob_world_v1.py').read_text()
f=f.replace('records={p.relative_to(ROOT)',"paths.update(p for folder in ['character/marsh-east-walk-halfcycle-polish-v1','character/marsh-v2/supplemental/east-walk-polish-v1'] for p in (ROOT/folder).glob('*') if p.is_file())\npaths.update(ROOT/'tools'/n for n in ['prepare_marsh_east_walk_halfcycle_v1.py','review_marsh_east_walk_halfcycle_v1.py','install_marsh_east_walk_halfcycle_v1.py','prepare_marsh_east_walk_selected_v1.py','review_marsh_east_walk_selected_v1.gd','review_marsh_east_walk_selected_v1.gd.uid','fingerprint_marsh_east_walk_selected_v1.py'])\nrecords={p.relative_to(ROOT)")
(ROOT/'tools/fingerprint_marsh_east_walk_selected_v1.py').write_text(f)
p=(ROOT/'tools/publish_marsh_east_walk_bob_world_v1.py').read_text().replace('east-walk-bob-world-v1-2026-10-03','east-walk-selected-world-v3-2026-10-03').replace('marsh-east-walk-bob-contact-v1','marsh-v2/supplemental/east-walk-polish-v1').replace('1653','1671')
p=p.replace("'normalAdmission':False","'normalAdmission':True")
(ROOT/'tools/publish_marsh_east_walk_selected_v1.py').write_text(p)
print('Normal selected native probe prepared; explicit original-source comparison, no candidate manifest override;1671checks expected.')
