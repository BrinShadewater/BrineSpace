from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_sofa_partial_south_continue.gd').read_text(encoding='utf-8')
lines=s.splitlines()
lines=[line for line in lines if not ('veld-sofa-partial-fall-south-v1/' in line and ('load_manifest' in line or 'load_equipment_manifest' in line))]
s='\n'.join(lines)+'\n'
s=s.replace('veld-sofa-partial-south-continue-v1','veld-sofa-partial-south-normal-continue-v1').replace('SOFA PARTIAL CONTINUE','SOFA PARTIAL NORMAL CONTINUE').replace('Fresh staged scene Continue','Fresh normal scene Continue')
needle='\treturn game\n'
extra='''\tfor gear in ["bare","helmet"]:
\t\tvar path:String="res://character/veld-sofa-partial-fall-south-selected-v1/bare-manifest.json" if gear=="bare" else "res://character/veld-sofa-partial-fall-south-selected-v1/helmet-manifest.json"
\t\tvar manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
\t\tvar pool:Dictionary=game.grid_view.veld_player.frames if gear=="bare" else game.grid_view.veld_player.equipment_frames["diving-helmet"]
\t\tcheck(manifest.states.size()==6,"Normal partial six-state pair")
\t\tfor state in manifest.states:
\t\t\tcheck(pool.has(state.id) and pool[state.id].size()==6,"Normal loader partial slots")
\t\t\tif not pool.has(state.id):continue
\t\t\tfor index in 6:
\t\t\t\tvar image:=Image.new();check(image.load(state.frameFiles[index])==OK,"Literal normal partial source image")
\t\t\t\tcheck(pool[state.id][index].get_image().get_data()==image.get_data(),"Normal partial source pixels, no injection")
\t\t\t\tcheck(pool[state.id][index].get_meta("crew_sofa_partial_floor_fall",false),"Normal opt-in marker")
'''
assert s.count(needle)==1;s=s.replace(needle,extra+needle)
assert 'load_manifest(' not in s and 'load_equipment_manifest(' not in s,'No fixture injection'
(R/'tests/test_veld_sofa_partial_south_normal_continue.gd').write_text(s,encoding='utf-8')
(R/'tests/test_veld_sofa_partial_south_normal_continue.gd.uid').write_text('uid://d0evssfprtn1\n',encoding='utf-8')
r=(R/'tools/run_veld_sofa_partial_south_continue.py').read_text(encoding='utf-8')
r=r.replace('veld-sofa-partial-south-continue-v1','veld-sofa-partial-south-normal-continue-v1').replace('test_veld_sofa_partial_south_continue.gd','test_veld_sofa_partial_south_normal_continue.gd').replace('SOFA PARTIAL CONTINUE','SOFA PARTIAL NORMAL CONTINUE')
r=r.replace("'veld-sofa-partial-fall-south-v1']","'veld-sofa-partial-fall-south-v1','veld-sofa-partial-fall-south-selected-v1']")
(R/'tools/run_veld_sofa_partial_south_normal_continue.py').write_text(r,encoding='utf-8')
print('Normal-only24world disk/fresh restores;72source slots checked every fresh load')
