"""Capture continuous finite motion through normal renderer, without save changes."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_sofa_selected_continue.gd').read_text(encoding='utf-8');helpers=s[:s.index('func run():')]
helpers=helpers.replace('veld-sofa-selected-continue-v1','veld-sofa-normal-motion-v1').replace('test_veld_sofa_selected_continue.gd.uid','test_veld_sofa_normal_motion.gd.uid')
run='''func run():
\tcheck(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA")
\tDirAccess.make_dir_recursive_absolute(OUT)
\tvar game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
\tgame.selected_rotation=0;game._place_room("observation_room",CELL,true);game.powered_room_cells[CELL]=true
\tawait recover_survivor(game);await game.veld_npc.rebuild(game)
\tvar station:Dictionary={}
\tfor candidate in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
\t\tif candidate.get("mode","")=="read" and candidate.facing=="south":station=candidate;break
\tcheck(not station.is_empty(),"Actual South sofa for native motion")
\tvar baseline:Dictionary=SAVE.capture(game);check(SAVE.problem(baseline).is_empty(),"Real baseline normal eligibility")
\tif failures:quit(1);return
\tvar records:Array=[]
\tfor equipped in [false,true]:
\t\tfor target in [.05,.40]:
\t\t\tcheck(await SAVE.restore_staged(game,baseline),"Baseline world restore before motion case")
\t\t\tvar actor=game.veld_npc;prepare(actor,station,equipped);game.visual_time_seconds=400
\t\t\tvar player=game.grid_view.veld_player;player.current_key="";player.motion.clear();player.last_time=-1
\t\t\tfor tick in 1600:
\t\t\t\tgame.grid_view._get_veld_live_frame_source(game)
\t\t\t\tif actor.stage=="observation_read" and 12-actor.timer>=target:break
\t\t\t\tactor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
\t\t\tgame.grid_view._get_veld_frame_source(game)
\t\t\tvar foot:Vector2=actor.foot;FLOOD.kill(game,actor,"veld","South sofa native motion fixture")
\t\t\tvar started:float=actor.water_death_motion.started
\t\t\tvar name:String=("helmet" if equipped else "bare")+"-"+("neutral" if target==.05 else "tablet")
\t\t\tcheck(actor.dead and actor.valid_veld_snapshot(actor.snapshot()),"Actual admitted world death for motion")
\t\t\tfor tick in 49:
\t\t\t\tif tick>0:actor.update(game,1.0/30)
\t\t\t\tgame.visual_time_seconds=started+tick/30.0
\t\t\t\tvar source:Texture2D=game.grid_view._get_veld_frame_source(game)
\t\t\t\tvar rendered=await capture_bunk(game,CELL,name+"-tick-%02d"%tick,source)
\t\t\t\tcheck(actor.foot==foot,"Physical foot fixed through every native motion presentation")
\t\t\t\trecords.append({"name":name,"tick":tick,"elapsed":tick/30.0,"pixels":pixels_hash(source),"rendered":rendered})
\tcheck(records.size()==196,"Four paired prop/gear native motion sequences")
\tvar f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\\t"));f.close()
\tprint("VELD SOFA NORMAL MOTION: %d checks,%d failures;196 native motion captures"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_veld_sofa_normal_motion.gd').write_text(helpers+run,encoding='utf-8');(R/'tests/test_veld_sofa_normal_motion.gd.uid').write_text('uid://d0evssfmtn1\n',encoding='utf-8')
r=(R/'tools/run_veld_sofa_selected_continue.py').read_text(encoding='utf-8').replace('veld-sofa-selected-continue-v1','veld-sofa-normal-motion-v1').replace('test_veld_sofa_selected_continue.gd','test_veld_sofa_normal_motion.gd').replace('helmet-2.4-suspended-after-room.png','helmet-tablet-tick-48-room.png').replace('0 failures;20 fresh disk restores','0 failures;196 native motion captures').replace("['SOFA WORLD CONTINUE','VELD SOFA WORLD CONTINUE'","['VELD SOFA NORMAL MOTION'")
(R/'tools/run_veld_sofa_normal_motion.py').write_text(r,encoding='utf-8')
print('Normal renderer motion fixture prepared; four gear/prop sequences')
