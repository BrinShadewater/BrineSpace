from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_veld_rest_family_candidate.gd').read_text(encoding='utf-8').replace('test_veld_rest_family_candidate','test_veld_rest_family_selected').replace('VELD REST FAMILY CANDIDATE','VELD REST FAMILY SELECTED').replace('veld-rest-family-candidate-v1','veld-rest-family-selected-v1')
a=s.index('\tvar p=Player.new()');b=s.index('\tfor direction',a)
s=s[:a]+'''\tvar grid=load("res://scripts/grid_canvas.gd").new()
\tgrid._load_replacement_crew_animations()
\tvar p=grid.veld_player
\tvar actor=load("res://scripts/veld_npc.gd").new()
\tactor.active=false;actor.dead=false;actor.state="idle";actor.movement_medium="dry"
\tcheck(p.frames.size()>12,"Normal loader preserves existing Veld states")
'''+s[b:]
a=s.index('\t\tif DisplayServer');s=s[:a]+'''\t\tfor equipped in [false,true]:
\t\t\tactor.direction=direction;actor.helmet_equipped=equipped;actor.bunk_motion.clear()
\t\t\tvar gear:String="diving-helmet" if equipped else ""
\t\t\tfor elapsed in [0.0,.24,.50,.82,1.18,1.54,1.839]:
\t\t\t\tactor.stage="life_lie";actor.timer=1.84-elapsed
\t\t\t\tcheck(is_equal_approx(actor.action_elapsed(),elapsed),"Actual Veld generic lowering uses1840ms")
\t\t\t\tvar before:Texture2D=grid._get_veld_live_frame_source(ActorContext.new(actor))
\t\t\t\tcheck(actor.valid_veld_snapshot(actor.snapshot()),"Generic longer rest snapshot validates")
\t\t\t\tvar reverse:float=actor.interrupted_life_rise_seconds()
\t\t\t\tactor.stage="life_get_up";actor.timer=reverse
\t\t\t\tcheck(grid._get_veld_live_frame_source(ActorContext.new(actor)).get_image().get_data()==before.get_image().get_data(),"Phase-aware reversed interruption exact pixels")
\t\t\t\tcheck(actor.valid_veld_snapshot(actor.snapshot()),"Interrupted rise snapshot validates")
\t\t\tactor.stage="life_sleep";actor.timer=10.4
\t\t\tvar pool:Dictionary=p.equipment_frames[gear] if equipped else p.frames
\t\t\tcheck(pool["sleep-"+direction][0].has_meta("crew_rest_head_offset"),"Selected sleeping anchor available")
'''+s[a:]
s=s.replace('\tprint("VELD REST FAMILY SELECTED','\tactor.free();grid.free()\n\tprint("VELD REST FAMILY SELECTED')
s+='''
class ActorContext extends RefCounted:
\tvar veld_npc
\tfunc _init(actor):veld_npc=actor
\tfunc get_visual_time_seconds():return 42.0
\tfunc get_dr_veld_position():return veld_npc.foot
'''
(R/'tests/test_veld_rest_family_selected.gd').write_text(s,encoding='utf-8')
s=(R/'tools/run_veld_rest_family_candidate.py').read_text(encoding='utf-8').replace('candidate','selected').replace('CANDIDATE','SELECTED').replace("'normalLoader':False","'normalLoader':True")
(R/'tools/run_veld_rest_family_selected.py').write_text(s,encoding='utf-8')
s=(R/'tests/test_bill_rest_family_station.gd').read_text(encoding='utf-8').replace('bill-rest-family-station-v1','veld-rest-family-station-v1').replace('bill-rest-station','veld-rest-station').replace('game.bill_npc;var grid','game.veld_npc;var grid').replace('grid.human_water_player','grid.veld_player').replace('grid.human_animation_key="";grid.human_animation_last_time=-1','player.current_key="";player.last_time=-1').replace('grid._get_human_frame_source(npc.animation_state(),npc.direction)','grid._get_veld_live_frame_source(game)').replace('BILL REST FAMILY STATION','VELD REST FAMILY STATION')
s=s.replace('func _init():call_deferred("run")','''func _init():
\tvar uid_path="res://tests/test_veld_rest_family_station.gd.uid"
\tif not FileAccess.file_exists(uid_path):
\t\tvar uid=FileAccess.open(uid_path,FileAccess.WRITE);uid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")
\tcall_deferred("run")''')
(R/'tests/test_veld_rest_family_station.gd').write_text(s,encoding='utf-8')
s=(R/'tools/run_bill_rest_family_station_validation.py').read_text(encoding='utf-8').replace('bill','veld').replace('BILL','VELD')
(R/'tools/run_veld_rest_family_station_validation.py').write_text(s,encoding='utf-8');print('Normal loader/generic clocks/exact reverse and actual bunk regression fixtures prepared.')
