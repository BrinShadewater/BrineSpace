from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'native-audit.gd').read_text()
source=source.replace('for issue in ["power-loss","food-empty","complete"]:','for issue in ["power-loss"]:')
source=source.replace('var credited:=0.0;var left:=false;var after_ticks:=0','var credited:=0.0;var left:=false;var after_ticks:=0;var restored:=false;var contact:Vector2=npc.foot')
marker='\t\t\t\tleft=npc.stage not in ["life_eat","life_drink"]'
extra='''\t\t\t\tif after_ticks==1:
\t\t\t\t\tcheck(npc.meal_return_active() and results[-1].samePixels,"Power loss begins exact current-pose return")
\t\t\t\t\tgame.powered_room_cells[cell]=true
\t\t\t\tif npc.meal_return_active():
\t\t\t\t\tcheck(npc.foot==contact and npc.direction=="north" and npc.stage=="" and npc.goal=="" and not npc.helmet_equipped,"Interrupted return stays fixed and uncommitted despite restored power")
\t\t\t\t\tvar clip:String=npc.animation_state()+"-north"
\t\t\t\t\tcheck(player.frames[clip].has(game.grid_view._get_branforth_frame_source(game)),"Production return uses selected whole source pose")
\t\t\t\tif not restored and npc.meal_return_active() and float(npc.meal_return.elapsed)>=npc.meal_return_seconds(npc.meal_return.source,npc.meal_return.index)*.35:
\t\t\t\t\tgame.paused=true;var before_actor:Dictionary=npc.snapshot();var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data();var clock:float=game.visual_time_seconds
\t\t\t\t\tvar save=preload("res://scripts/run_save.gd");var scratch_path:="user://james-meal-return.loop"
\t\t\t\t\tcheck(save.problem(save.capture(game)).is_empty(),"Meal return checkpoint valid")
\t\t\t\t\tcheck(save.write(game,scratch_path)==OK,"Actual meal return checkpoint writes")
\t\t\t\t\tvar data:Dictionary=save.read(scratch_path)
\t\t\t\t\troot.remove_child(game);game.queue_free();await process_frame
\t\t\t\t\tgame=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
\t\t\t\t\tgame.meta.save_path="user://james-locker.meta";game.run_save_path=scratch_path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
\t\t\t\t\troot.add_child(game);current_scene=game
\t\t\t\t\twhile not game.startup_complete:await process_frame
\t\t\t\t\tgame.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
\t\t\t\t\tcheck(await save.restore_staged(game,data),"Actual fresh-scene mid-return disk Continue")
\t\t\t\t\tgame.run_save_path=scratch_path;game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player
\t\t\t\t\tgame._set_grid_zoom(1.256,true,Vector2(.5125,.5125))
\t\t\t\t\tcheck(npc.snapshot()==before_actor and game.paused and game.visual_time_seconds==clock,"Interrupted meal Continue retains actor/clock/pause")
\t\t\t\t\tcheck(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Interrupted meal Continue retains exact selected pixels")
\t\t\t\t\tgame._process(.5);check(npc.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused return does not advance")
\t\t\t\t\tcheck(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Paused return retains exact pose pixels")
\t\t\t\t\tgame.paused=false;game.set_process(false);restored=true
\t\t\t\tleft=not npc.meal_return_active()
'''
assert marker in source
source=source.replace(marker,extra)
source=source.replace('results[-1]["afterTicks"]=after_ticks','''results[-1]["afterTicks"]=after_ticks;results[-1]["freshSceneRestore"]=restored
\t\t\tcheck(restored and npc.stage=="" and npc.state=="idle" and npc.goal=="" and npc.foot==contact,"Uncredited return reaches empty standing state")
\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\t\tvar image:Image=player.frames["idle-north"][0].get_image()
\t\t\tcheck(texture.get_image().get_region(Rect2i(Vector2i.ZERO,image.get_size())).get_data()==image.get_data(),"Return ends at exact selected idle pixels")
\t\t\tresults[-1].captures.append(await capture(issue+"-"+phase+"-finished",npc))
\t\t\tgame.resources.food=0;npc.needs.curiosity=95;npc.decision_rng.seed=17
\t\t\tvar walking:=false
\t\t\tfor tick in range(2000):
\t\t\t\tvar previous:Vector2=npc.foot;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
\t\t\t\tif npc.foot!=previous and npc.animation_state()=="walk":walking=true;break
\t\t\tcheck(walking,"Normal chooser moves to next available task after return")''')
source=source.replace('native-audit-evidence.json','native-return-evidence.json')
source=source.replace('Thirteen actual default North galley journeys from normal hunger chooser: six power losses, six depleted-food continuations, one normal completion. Audit immediate pose continuity and hunger credit; no abort choreography or Continue proof claimed.','Six actual normal North meal services interrupted mid each of six source clips by power loss. Exact current-pose return, fixed foot/facing, no credit or restart despite restored power, selected whole return frames, six fresh-scene mid-return disk Continues with exact actor/clock/pixels/pause, exact idle completion and normal next task. Hazards/changed furniture remain separate.')
source=source.replace('JAMES MEAL INTERRUPTION AUDIT: ','JAMES MEAL RETURNS: ')
(P/'native-return.gd').write_text(source)
print('Created six actual interruption returns with six fresh-scene Continues')
