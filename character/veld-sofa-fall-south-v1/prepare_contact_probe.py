from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_sofa_selected_continue.gd').read_text(encoding='utf-8')
s=s.replace('veld-sofa-selected-continue-v1','veld-sofa-contact-probe-v1')
s=s.replace('for equipped in [false,true]:\n\t\tfor case in cases:','for equipped in [false]:\n\t\tfor case in [[.05,"power"]]:')
s=s.replace('check(records.size()==20','check(records.size()==1')
needle='\tcheck(ready,"Actual bunk source submitted at centered native camera")'
probe='''\tif not ready:
\t\tvar diagnostic:Array=[]
\t\tif game.grid_view.content_canvases.has(cell):
\t\t\tfor slot in game.grid_view.content_canvases[cell].slots:
\t\t\t\tif slot.visible and slot.item.get("kind","")=="crew":
\t\t\t\t\tvar actual:Texture2D=slot.item.member.texture
\t\t\t\t\tdiagnostic.append({"sameTexture":actual==source,"samePixels":actual.get_image().get_data()==source.get_image().get_data(),"actualSize":actual.get_size(),"targetSize":source.get_size(),"position":slot.item.member.position,"stage":game.veld_npc.stage})
\t\tvar center:Vector2=game.grid_view.get_global_transform()*((Vector2(cell)+Vector2.ONE*.5)*game.get_cell_size())
\t\tprint("SOFA CONTACT REAL STATE ",JSON.stringify({"name":name,"sourceIdentity":source.get_instance_id(),"centerDistance":center.distance_to(game.grid_scroll.get_global_rect().get_center()),"submittedCrew":diagnostic}))
'''
assert needle in s;s=s.replace(needle,probe+needle)
(R/'tests/test_veld_sofa_contact_probe.gd').write_text(s,encoding='utf-8')
(R/'tests/test_veld_sofa_contact_probe.gd.uid').write_text('uid://d0evssfprb1\n',encoding='utf-8')
r=(R/'tools/run_veld_sofa_selected_continue.py').read_text(encoding='utf-8').replace('veld-sofa-selected-continue-v1','veld-sofa-contact-probe-v1').replace('test_veld_sofa_selected_continue.gd','test_veld_sofa_contact_probe.gd')
r=r.replace("['SOFA WORLD CONTINUE','VELD SOFA WORLD CONTINUE'","['SOFA CONTACT REAL STATE','SOFA WORLD CONTINUE','VELD SOFA WORLD CONTINUE'")
(R/'tools/run_veld_sofa_contact_probe.py').write_text(r,encoding='utf-8')
print('Retained main interval; separate one-context submission diagnostic')
