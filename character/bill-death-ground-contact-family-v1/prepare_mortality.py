from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
source=(R/'tests/test_bill_death_ground_contact_station.gd').read_text(encoding='utf-8')
head=source.split('\tvar records:=[]')[0].replace('bill-death-ground-contact-station-v1','bill-death-ground-contact-mortality-v1')
head=head.replace('var game','const Save=preload("res://scripts/run_save.gd")\nvar game',1)
body='''\tvar cases:=0;var restores:=0;var captures:=0
\tfor contact in contacts:
\t\tfor d in ["east","west","north","south"]:
\t\t\tfor gear in [false,true]:
\t\t\t\tfor cause in ["air","food"]:
\t\t\t\t\tfor before in ["kneel","repair"]:
\t\t\t\t\t\tactor=game.bill_npc
\t\t\t\t\t\tactor.active=true;actor.dead=false;actor.state=before;actor.stage="";actor.timer=0;actor.path.clear();actor.goal="curiosity";actor.expedition.clear();actor.moonbay_assignment.clear();actor.helmet_equipped=gear;actor.movement_medium="dry";actor.direction=d;actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+contact[1]
\t\t\t\t\t\tawait actor.rebuild(game)
\t\t\t\t\t\tvar foot:Vector2=actor.foot
\t\t\t\t\t\tgame.resources.food=0 if cause=="food" else 100;game.resources.oxygen=0 if cause=="air" else 100
\t\t\t\t\t\tactor.tank_oxygen=.01 if cause=="air" else 60;actor.breath_oxygen=.01 if cause=="air" else 15;actor.starvation=89.99 if cause=="food" else 0
\t\t\t\t\t\tvar expected:String="lateral" if contact[0]=="counter" and d in ["north","south"] else ""
\t\t\t\t\t\tvar key:String="death-ground-"+("lateral-" if expected=="lateral" else "")+d
\t\t\t\t\t\tvar equipment:String="diving-helmet" if gear else ""
\t\t\t\t\t\tgrid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=100
\t\t\t\t\t\tgrid._get_human_frame_source(before,d);game.visual_time_seconds=101;grid._get_human_frame_source(before,d)
\t\t\t\t\t\tFLOOD.step_crew(game,actor,"bill",.02);cases+=1
\t\t\t\t\t\tcheck(actor.dead and actor.state=="death-ground","Actual survival-trigger dry death")
\t\t\t\t\t\tcheck(actor.death_ground_variant==expected,"Actual contact choice: "+contact[0]+d+str(gear)+cause+before)
\t\t\t\t\t\tcheck(actor.foot==foot and actor.path.is_empty() and actor.goal.is_empty(),"Mortality preserves anchor and cancels intent")
\t\t\t\t\t\tcheck(grid._get_human_frame_source("death-ground",d)==player.frame_at_elapsed(key,actor.death_entry_seconds,equipment),"Chosen lowered entry rendered")
\t\t\t\t\t\tgame.visual_time_seconds=104
\t\t\t\t\t\tvar terminal:Texture2D=player.frame_at_elapsed(key,99,equipment)
\t\t\t\t\t\tcheck(grid._get_human_frame_source("death-ground",d)==terminal,"Chosen terminal rendered")
\t\t\t\t\t\tcheck(grid._get_human_frame_source("death-ground",d)==terminal,"Paused terminal stable")
\t\t\t\t\t\tif cause=="food" and before=="repair":
\t\t\t\t\t\t\tfor elapsed in [.65,2.0]:
\t\t\t\t\t\t\t\tgrid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=200
\t\t\t\t\t\t\t\tgrid._get_human_frame_source("death-ground",d);game.visual_time_seconds=200+elapsed
\t\t\t\t\t\t\t\tvar pixels:PackedByteArray=grid._get_human_frame_source("death-ground",d).get_image().get_data();var phase:float=actor.death_entry_seconds
\t\t\t\t\t\t\t\tcheck(Save.write(game,game.run_save_path)==OK,"Write actual death checkpoint: "+Save.last_error)
\t\t\t\t\t\t\t\tvar saved:Dictionary=Save.read(game.run_save_path);check(not saved.is_empty(),"Read actual checkpoint")
\t\t\t\t\t\t\t\tif not saved.is_empty():
\t\t\t\t\t\t\t\t\tcheck(await Save.restore(game,saved),"Production disk restoration")
\t\t\t\t\t\t\t\t\tactor=game.bill_npc
\t\t\t\t\t\t\t\t\tgame.set_process(false);game.tick_timer.stop();game.run_save_path="user://bill-ground-station.loop"
\t\t\t\t\t\t\t\t\tcheck(actor.dead and actor.death_ground_variant==expected and is_equal_approx(actor.death_entry_seconds,phase),"Saved variant and prefix restored")
\t\t\t\t\t\t\t\t\tcheck(actor.direction==d and actor.helmet_equipped==gear and actor.foot==foot,"Dead identity and contact restored")
\t\t\t\t\t\t\t\t\tcheck(grid._get_human_frame_source("death-ground",d).get_image().get_data()==pixels,"Exact chosen mid-fall/terminal pixels restored")
\t\t\t\t\t\t\t\t\trestores+=1
\t\t\t\t\t\t\tgrid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
\t\t\t\t\t\t\tcheck(root.get_texture().get_image().save_png(OUT+"%s-%s-%s-terminal.png"%[contact[0],d,"helmet" if gear else "bare"])==OK,"Actual restored terminal room capture");captures+=1
\t\t\t\t\t\tactor.active=false
\tcheck(cases==64 and restores==32 and captures==16,"Full64 mortality/32 disk-restore/16 capture matrix")
\tawait RenderingServer.frame_post_draw;check(root.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")==OK,"Fresh native proof")
\tprint("BILL GROUND CONTACT MORTALITY: %d checks,%d failures; %d cases,%d restores,%d captures"%[checks,failures,cases,restores,captures]);quit(1 if failures else 0)
'''
(R/'tests/test_bill_death_ground_contact_mortality.gd').write_text(head+body,encoding='utf-8');(R/'tests/test_bill_death_ground_contact_mortality.gd.uid').write_text('uid://l9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_contact_station_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-contact-station-v1','bill-death-ground-contact-mortality-v1').replace('test_bill_death_ground_contact_station.gd','test_bill_death_ground_contact_mortality.gd').replace("'BILL GROUND STATION CANDIDATE'","'BILL GROUND CONTACT MORTALITY'")
(R/'tools/run_bill_death_ground_contact_mortality_validation.py').write_text(s,encoding='utf-8')
print('Prepared actual64 survival-death cases and32 disk restores at real galley contacts')
