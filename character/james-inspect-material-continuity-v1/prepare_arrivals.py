from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'character/james-arrival-facing-polish-v1/native-installed.gd').read_text(encoding='utf-8')
s=s.replace('res://character/james-arrival-facing-polish-v1/','res://character/james-inspect-material-continuity-v1/')
s=s.replace('for medium in ["dry","flooded"]:','for medium in ["dry"]:')
s=s.replace('npc.breath_oxygen=100;npc.tank_oxygen=100','npc.breath_oxygen=15;npc.tank_oxygen=60')
s=s.replace('game.architect_run.clear();game.occupied.clear();','game.running=true;game.paused=false;game.Architects.advance_core(game,10)\n\tcheck(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Actual core release supplies valid roster")\n\tgame.occupied.clear();')
s=s.replace('game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":ORIGIN}])','check(not game.recovered_crew.is_empty(),"Normal recovered roster retained")')
s=s.replace('game.wrecks.clear()','pass # Preserve normal architect/wreck registry for valid disk saves.')
s=s.replace('game.run_save_path="user://james-water-cargo-turn-routes.loop"','game.run_save_path="user://james-tablet-arrival.loop"')
s=s.replace('game.meta.save_path="user://james-water-cargo-turn-routes.meta"','game.meta.save_path="user://james-tablet-arrival.meta"')
s=s.replace('game=load("res://scenes/main.tscn").instantiate();','game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);',1)
needle='\t\t\t\t\t\t\tdiagnostic_elapsed+=float(diagnostic_durations[i])/1000.0'
insert='''							if i==int(frames[diagnostic_key].size()/2):
								game.paused=true
								var before_actor:Dictionary=npc.snapshot()
								var before_pixels:PackedByteArray=tex.get_image().get_data()
								var before_playback:Dictionary=player.snapshot()
								var clock:float=game.visual_time_seconds
								var save=preload("res://scripts/run_save.gd")
								var scratch_path:="user://james-tablet-arrival.loop"
								var data:Dictionary=save.capture(game)
								var problem:String=save.problem(data)
								check(problem.is_empty(),"Mid-diagnostic checkpoint valid: "+problem)
								if not problem.is_empty():quit(2);return
								check(save.write(game,scratch_path)==OK,"Actual diagnostic checkpoint writes")
								data=save.read(scratch_path)
								root.remove_child(game);game.queue_free();await process_frame
								game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
								game.meta.save_path="user://james-tablet-arrival.meta";game.run_save_path=scratch_path
								game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
								root.add_child(game);current_scene=game
								while not game.startup_complete:await process_frame
								game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
								check(await save.restore_staged(game,data),"Actual fresh-scene diagnostic disk Continue")
								game.run_save_path=scratch_path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
								npc=game.branforth_npc;player=game.grid_view.branforth_player
								frames=player.frames if gear.is_empty() else player.equipment_frames[gear]
								check(npc.snapshot()==before_actor,"Continue exact actor snapshot")
								check(game.paused and game.visual_time_seconds==clock,"Continue clock/pause exact")
								check(player.snapshot()==before_playback,"Continue playback snapshot exact")
								check(game.grid_view._get_branforth_frame(game).get_image().get_data()==before_pixels,"Continue selected pose pixels exact")
								game._process(.5)
								check(npc.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused Continue does not advance")
								check(game.grid_view._get_branforth_frame(game).get_image().get_data()==before_pixels,"Paused Continue pixels exact")
								game.paused=false;game.set_process(false)
'''
assert needle in s;s=s.replace(needle,insert+needle)
s=s.replace('"captures":captures})','"captures":captures,"freshSceneMidpointContinue":true})')
s=s.replace('check(npc.state=="interact" and npc.goal=="curiosity","Diagnostics still active through complete authored cycle")','check(npc.state=="interact" and npc.goal=="curiosity","Diagnostics still active through complete authored cycle")\n\t\t\t\t\t\t\tcheck(npc.foot==destination and npc.direction==facing and npc.helmet_equipped==(mode=="helmet"),"Fixed contact/facing/gear throughout cycle and Continue")')
s=s.replace('\tcheck(mismatches==(12 if baseline else 0),','\tcheck(results.size()==8,"Complete eight-direction/mode approach and Continue scope")\n\tcheck(mismatches==(12 if baseline else 0),')
s=s.replace('\t\t\t\tresults.append({"mode":mode,"medium":medium,"incoming":facing,"arrived":arrived_direction,"actualMove":true,"captures":captures,"freshSceneMidpointContinue":true})','\t\t\t\tresults.append({"mode":mode,"medium":medium,"incoming":facing,"arrived":arrived_direction,"actualMove":true,"captures":captures,"freshSceneMidpointContinue":true})\n\t\t\t\tprint("JAMES TABLET JOURNEY COMPLETE: ",mode," ",facing,"; checks ",checks,"; failures ",failures)')
s=s.replace('installed-evidence.json','native-arrival-continue-evidence.json')
s=s.replace('JAMES ARRIVAL FACING:','JAMES TABLET ARRIVAL CONTINUE:')
old='16 explicit collision-checked generic maintenance-room arrival paths through real James move/arrive and normal grid; dry/flooded, four incoming directions, bare/helmet. Full six-slot same-facing swim stops; all dry tablet slots through actual NPC.update, six-second completion/need relief. Not pathfinder, workstation-specific rotation or exterior journey proof.'
new='Eight explicit collision-checked dry generic maintenance-room arrival paths through real James move/arrive and normal grid; four incoming directions, bare/helmet. All1130 dry tablet slots through actual NPC.update; eight actual fresh-scene midpoint disk Continues with exact actor/playback/clock/pause/pixels, six-second completion and normal need relief. Not autonomous pathfinder, actual locker/equipment changes, workstation-specific rotation or exterior journey proof.'
assert old in s;s=s.replace(old,new)
s=s.replace('func _init() -> void:call_deferred("run")','func _init() -> void:\n\tprint("JAMES TABLET ARRIVAL CONTINUE BOOT")\n\tcall_deferred("run")')
s=s.replace('\tquit(1 if failures else 0)','\tif not FileAccess.file_exists(OUT+"native-arrival-continue.gd.uid"):\n\t\tvar uid_file:=FileAccess.open(OUT+"native-arrival-continue.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))\n\tquit(1 if failures else 0)')
(P/'native-arrival-continue.gd').write_text(s,encoding='utf-8')
print('Eight dry actual approaches/full cycles/midpoint disk Continue fixture prepared.')
