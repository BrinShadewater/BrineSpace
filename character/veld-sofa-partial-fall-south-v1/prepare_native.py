from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_sofa_selected_continue.gd').read_text(encoding='utf-8');helpers=s[:s.index('func run():')]
helpers=helpers.replace('veld-sofa-selected-continue-v1','veld-sofa-partial-south-staged-v1').replace('test_veld_sofa_selected_continue.gd.uid','test_veld_sofa_partial_south_staged.gd.uid')
needle='\treturn game\n'
helpers=helpers.replace(needle,'\tgame.grid_view.veld_player.load_manifest("res://character/veld-sofa-partial-fall-south-v1/bare-manifest.json",true)\n\tcheck(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-sofa-partial-fall-south-v1/helmet-manifest.json"),"Staged paired partial sofa clips only")\n'+needle,1)
run='''func run():
\tcheck(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA")
\tDirAccess.make_dir_recursive_absolute(OUT)
\tvar game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
\tgame.selected_rotation=0;game._place_room("observation_room",CELL,true);game.powered_room_cells[CELL]=true
\tawait recover_survivor(game);await game.veld_npc.rebuild(game)
\tvar station:Dictionary={}
\tfor candidate in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
\t\tif candidate.get("mode","")=="read" and candidate.facing=="south":station=candidate;break
\tcheck(not station.is_empty(),"Actual South sofa")
\tvar baseline:Dictionary=SAVE.capture(game);check(SAVE.problem(baseline).is_empty(),"Real living baseline valid")
\tif failures:quit(1);return
\tvar records:Array=[];var deaths:=0;var restores:=0;var guards:=0
\tfor equipped in [false,true]:
\t\tfor movement in ["sit","rise"]:
\t\t\tfor pose in 6:
\t\t\t\tcheck(await SAVE.restore_staged(game,baseline),"Actual baseline roster restore before each death")
\t\t\t\tvar actor=game.veld_npc;prepare(actor,station,equipped);game.visual_time_seconds=400
\t\t\t\tvar player=game.grid_view.veld_player;player.current_key="";player.motion.clear();player.last_time=-1
\t\t\t\tvar target:float=[.04,.13,.25,.40,.56,.72][pose] if movement=="sit" else [.76,.67,.55,.40,.24,.08][pose]
\t\t\t\tvar target_stage:String="observation_sit" if movement=="sit" else "observation_rise"
\t\t\t\tfor tick in 6000:
\t\t\t\t\tgame.grid_view._get_veld_live_frame_source(game)
\t\t\t\t\tif actor.stage==target_stage and actor.Life.elapsed(actor)>=target:break
\t\t\t\t\tactor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
\t\t\t\tcheck(actor.stage==target_stage,"Actual timed partial sit/rise stage")
\t\t\t\tvar living:Texture2D=game.grid_view._get_veld_frame_source(game)
\t\t\t\tvar pool:Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
\t\t\t\tvar key:String="sit-down-south" if movement=="sit" else "sit-rise-south"
\t\t\t\tvar index:int=pose if movement=="sit" else 5-pose
\t\t\t\tcheck(living==pool[key][index],"Actual selected partial source: "+str(pose))
\t\t\t\tvar name:String=("helmet" if equipped else "bare")+"-"+movement+"-pose"+str(pose)
\t\t\t\tvar living_rendered=await capture_bunk(game,CELL,name+"-living",living)
\t\t\t\tvar crew_before:int=game.crew_count;FLOOD.kill(game,actor,"veld","South partial sofa fixture")
\t\t\t\tvar clip:String="death-sofa-pose%d-south"%pose
\t\t\t\tcheck(actor.dead and actor.water_death_motion.get("clip","")==clip,"Actual world partial recipe selected")
\t\t\t\tcheck(actor.valid_veld_snapshot(actor.snapshot()),"Strict partial snapshot admitted")
\t\t\t\tcheck(game.crew_count==crew_before-1 and game.Architects.present(game,"bill") and not game.Architects.present(game,"veld"),"World roster death with real paid survivor")
\t\t\t\tif failures:quit(1);return
\t\t\t\tvar started:float=actor.water_death_motion.started;var original_foot:Vector2=actor.foot
\t\t\t\tvar samples:Array=[0.0,.179,.181,.225,.30,.341,.361,.45,.521,.561,.66,.701,.781,.921,1.021,1.60]
\t\t\t\tvar presentations:Array=[]
\t\t\t\tfor ordinal in samples.size():
\t\t\t\t\tvar elapsed:float=samples[ordinal];game.visual_time_seconds=started+elapsed
\t\t\t\t\tvar shown:Texture2D=game.grid_view._get_veld_frame_source(game)
\t\t\t\t\tvar slot:int=0
\t\t\t\t\tif pose<2:slot=0 if elapsed<.18 else (1 if elapsed<.34 else (2 if elapsed<.52 else (3 if elapsed<.70 else (4 if elapsed<.92 else 5))))
\t\t\t\t\telse:slot=0 if elapsed<.18 else (1 if elapsed<.36 else (2 if elapsed<.56 else (3 if elapsed<.78 else (4 if elapsed<1.02 else 5))))
\t\t\t\t\tvar expected:Texture2D=living if slot==0 else pool[clip][slot]
\t\t\t\t\tcheck(shown.get_image().get_data()==expected.get_image().get_data(),"Independent partial six-source clock")
\t\t\t\t\tvar start:float=.18 if pose<2 else .36;var duration:float=.16 if pose<2 else .42
\t\t\t\t\tvar offset:Vector2=actor.water_death_motion.entry_position_offset*(1-clampf((elapsed-start)/duration,0,1))
\t\t\t\t\tvar sample=motion_sample(game);var local:Vector2=actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384
\t\t\t\t\tcheck(sample.offset.distance_to(offset)<.00001 and actor.foot==original_foot,"Independent saved fractional contact/fixed navigation foot")
\t\t\t\t\tvar depth:float=maxf(local.y+offset.y,float(actor.water_death_motion.entry_sort_depth)) if elapsed<start+duration else local.y
\t\t\t\t\tcheck(is_equal_approx(sample.depth,depth),"Independent partial seat/floor depth")
\t\t\t\t\tvar label:String=name+"-sample-%02d"%ordinal;var rendered=await capture_bunk(game,CELL,label,shown)
\t\t\t\t\tpresentations.append({"label":label,"elapsed":elapsed,"sourceSlot":slot,"offset":offset,"depth":sample.depth,"rendered":rendered})
\t\t\t\t\tif ordinal in [1,5,12,15]:
\t\t\t\t\t\tvar file=FileAccess.open("user://partial-sofa-actor.snapshot",FileAccess.WRITE);file.store_var(actor.snapshot());file.close()
\t\t\t\t\t\tfile=FileAccess.open("user://partial-sofa-actor.snapshot",FileAccess.READ);var disk:Dictionary=file.get_var();file.close()
\t\t\t\t\t\tvar restored=actor.get_script().new();await restored.restore_snapshot(game,disk,true);game.veld_npc=restored
\t\t\t\t\t\tcheck(restored.dead and restored.geometry.is_empty() and restored.foot==original_foot,"Actor-file dead geometry/foot retained")
\t\t\t\t\t\tvar restored_sample=motion_sample(game)
\t\t\t\t\t\tcheck(restored_sample.pixels==sample.pixels and restored_sample.offset==sample.offset and is_equal_approx(restored_sample.depth,sample.depth),"Same-clock file/source/contact restore")
\t\t\t\t\t\tgame.veld_npc=actor;restores+=1
\t\t\t\tfor invalid in ["first","slot","gear","amount","seat","offset","clip"]:
\t\t\t\t\tvar bad:Dictionary=actor.snapshot().duplicate(true);var recipe:Dictionary=bad.veld_water_death
\t\t\t\t\tmatch invalid:
\t\t\t\t\t\t"first":recipe.first=2
\t\t\t\t\t\t"slot":recipe.entry_index=6
\t\t\t\t\t\t"gear":recipe.entry_equipment="" if equipped else "diving-helmet"
\t\t\t\t\t\t"amount":recipe.sofa_motion.amount=.9 if pose<5 else .4
\t\t\t\t\t\t"seat":recipe.sofa_motion.seat+=Vector2(0,10)
\t\t\t\t\t\t"offset":recipe.entry_position_offset+=Vector2(0,10)
\t\t\t\t\t\t"clip":recipe.clip="death-sofa-pose%d-south"%((pose+1)%6)
\t\t\t\t\tcheck(not actor.valid_veld_snapshot(bad),"Malformed partial saved source/contact rejected: "+invalid);guards+=1
\t\t\t\tdeaths+=1;records.append({"name":name,"movement":movement,"pose":pose,"recipe":actor.water_death_motion,"living":living_rendered,"presentations":presentations})
\t\t\t\tprint("SOFA PARTIAL STAGED ",name," deaths=",deaths," failures=",failures)
\tcheck(deaths==24 and restores==96 and guards==168,"All6partial poses,both movements/gear,96file restores/168guards")
\tvar f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\\t"));f.close()
\tprint("VELD SOFA PARTIAL STAGED: %d checks,%d failures;24 world deaths/96 actor-file restores"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_veld_sofa_partial_south_staged.gd').write_text(helpers+run,encoding='utf-8');(R/'tests/test_veld_sofa_partial_south_staged.gd.uid').write_text('uid://d0evssfprt1\n',encoding='utf-8')
r=(R/'tools/run_veld_sofa_selected_continue.py').read_text(encoding='utf-8').replace('veld-sofa-selected-continue-v1','veld-sofa-partial-south-staged-v1').replace('test_veld_sofa_selected_continue.gd','test_veld_sofa_partial_south_staged.gd').replace('helmet-2.4-suspended-after-room.png','helmet-rise-pose5-sample-15-room.png').replace('0 failures;20 fresh disk restores','0 failures;24 world deaths/96 actor-file restores').replace("['SOFA WORLD CONTINUE','VELD SOFA WORLD CONTINUE'","['SOFA PARTIAL STAGED','VELD SOFA PARTIAL STAGED'")
r=r.replace("['veld-sofa-fall-south-selected-v1','veld-seated-south-selected-v1']","['veld-sofa-fall-south-selected-v1','veld-seated-south-selected-v1','veld-sofa-partial-fall-south-v1']")
(R/'tools/run_veld_sofa_partial_south_staged.py').write_text(r,encoding='utf-8');print('Paired24actual world deaths/96actor restores staged fixture prepared')
