from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_bill_death_ground_contact_family.gd').read_text(encoding='utf-8').replace('bill-death-ground-contact-family-native-v1','bill-death-ground-normal-family-v1')
s=s.replace('player.load_manifest(BASE,true);check(player.load_equipment_manifest("diving-helmet",HELMET),"Compatible paired family equipment loaded")','check(player.frames.has("death-ground-lateral-north") and player.equipment_frames["diving-helmet"].has("death-ground-lateral-south"),"Normal loader selects paired contact options without injection")')
(R/'tests/test_bill_death_ground_normal_family.gd').write_text(s,encoding='utf-8');(R/'tests/test_bill_death_ground_normal_family.gd.uid').write_text('uid://o9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_contact_family_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-contact-family-native-v1','bill-death-ground-normal-family-v1').replace('test_bill_death_ground_contact_family.gd','test_bill_death_ground_normal_family.gd')
(R/'tools/run_bill_death_ground_normal_family_validation.py').write_text(s,encoding='utf-8')
s=(R/'tests/test_bill_death_ground_contact_mortality.gd').read_text(encoding='utf-8').replace('bill-death-ground-contact-mortality-v1','bill-death-ground-normal-mortality-v1')
start=s.index('\tvar grid=game.grid_view;');end=s.index('\tgame.selected_card_id=',start)
s=s[:start]+'''\tvar grid=game.grid_view;var player=grid.human_water_player
\tcheck(player.frames.has("death-ground-lateral-north") and player.equipment_frames["diving-helmet"].has("death-ground-lateral-south"),"Normal loader paired contact family without injection")
'''+s[end:]
s=s.replace('var cases:=0;var restores:=0;var captures:=0','var cases:=0;var restores:=0;var captures:=0;var continue_cases:=[]')
needle='var pixels:PackedByteArray=grid._get_human_frame_source("death-ground",d).get_image().get_data();var phase:float=actor.death_entry_seconds'
assert needle in s
s=s.replace(needle,needle+'''
\t\t\t\t\t\t\t\tif d in ["north","south"]:
\t\t\t\t\t\t\t\t\tvar id:String="%s-%s-%s-%s"%[contact[0],d,"helmet" if gear else "bare","mid" if elapsed<2 else "terminal"]
\t\t\t\t\t\t\t\t\tvar checkpoint:String="user://bill-ground-continue-"+id+".save";var image_path:String="user://bill-ground-continue-"+id+".png"
\t\t\t\t\t\t\t\t\tcheck(Save.write(game,checkpoint)==OK,"Write fresh-process Continue checkpoint")
\t\t\t\t\t\t\t\t\tcheck(grid._get_human_frame_source("death-ground",d).get_image().save_png(image_path)==OK,"Expected Continue pixels")
\t\t\t\t\t\t\t\t\tcontinue_cases.append({"id":id,"checkpoint":checkpoint,"expectedImage":image_path,"direction":d,"helmet":gear,"variant":expected,"entryPhase":phase,"foot":[foot.x,foot.y],"elapsed":elapsed})''')
s=s.replace('await RenderingServer.frame_post_draw;check(root.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")', 'var descriptors:=FileAccess.open(OUT+"continue-cases.json",FileAccess.WRITE);descriptors.store_string(JSON.stringify(continue_cases,"\\t"));descriptors.close()\n\tawait RenderingServer.frame_post_draw;check(root.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")')
s=s.replace('BILL GROUND CONTACT MORTALITY','BILL GROUND NORMAL MORTALITY')
(R/'tests/test_bill_death_ground_normal_mortality.gd').write_text(s,encoding='utf-8');(R/'tests/test_bill_death_ground_normal_mortality.gd.uid').write_text('uid://p9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_contact_mortality_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-contact-mortality-v1','bill-death-ground-normal-mortality-v1').replace('test_bill_death_ground_contact_mortality.gd','test_bill_death_ground_normal_mortality.gd').replace('BILL GROUND CONTACT MORTALITY','BILL GROUND NORMAL MORTALITY')
(R/'tools/run_bill_death_ground_normal_mortality_validation.py').write_text(s,encoding='utf-8')
print('Prepared normal-loader matrix/mortality and16 fresh-process Continue checkpoints; no candidate injection')
