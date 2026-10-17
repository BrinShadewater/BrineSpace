from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'validate.gd').read_text()
s=s.replace('game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":Vector2i(20,20)}])','game.running=true;game.paused=false;game.Architects.advance_core(game,10)\n\tcheck(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Normal core release roster")')
s=s.replace('for id in ["crew_lounge","observation_room"]:', 'for id in ["observation_room"]:')
s=s.replace('for sample_mode in range(2):','for test_case in range(6):\n\t\t\tvar sample_mode:int=test_case/3\n\t\t\tvar trigger_stage:String="observation_read_enter" if test_case%3==0 else "observation_read"\n\t\t\tvar trigger_elapsed:float=.21 if test_case%3==0 else .75')
s=s.replace('game.wrecks.clear()', 'game.powered_room_cells.clear()')
s=s.replace('controller-native/', 'continue-native/')
s=s.replace('var began_foot:Vector2=actor.foot;', 'var resumed:=false;var began_foot:Vector2=actor.foot;')
s=s.replace('var frame:Texture2D=game.grid_view._get_branforth_frame(game)', '''var trigger_clock:float=11.04-actor.timer if actor.stage=="observation_read" else actor.action_elapsed()
				if not resumed and actor.stage==trigger_stage and trigger_clock>=trigger_elapsed:
					if test_case%3==2:
						game.powered_room_cells.erase(cell);actor.update(game,1.0/60.0)
						check(actor.stage=="observation_read_exit" and actor.tablet_exit_pose>=0,"Checkpoint dynamic held-to-stow source")
					game.paused=true
					var before_actor:Dictionary=actor.snapshot()
					var before_pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
					var before_playback:Dictionary=player.snapshot()
					var clock:float=game.visual_time_seconds
					var save=preload("res://scripts/run_save.gd")
					var scratch_path:String="user://james-seated-continue-case%d.loop"%test_case
					var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
					check(problem.is_empty(),"Current seated checkpoint valid: "+problem)
					if not problem.is_empty():quit(2);return
					check(save.write(game,scratch_path)==OK,"Actual seated checkpoint writes")
					data=save.read(scratch_path)
					root.remove_child(game);game.queue_free();await process_frame
					game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://branforth_seated.meta";game.run_save_path=scratch_path
					game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
					root.add_child(game);current_scene=game
					while not game.startup_complete:await process_frame
					game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
					check(await save.restore_staged(game,data),"Actual fresh-scene seated disk Continue")
					game.run_save_path=scratch_path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
					actor=game.branforth_npc;player=game.grid_view.branforth_player
					check(actor.snapshot()==before_actor,"Continue actor exact")
					check(game.paused and game.visual_time_seconds==clock,"Continue clock and pause exact")
					check(player.snapshot()==before_playback,"Continue playback exact")
					check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==before_pixels,"Continue source RGBA exact")
					game._process(.5)
					check(actor.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused Continue does not advance")
					check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==before_pixels,"Paused Continue source exact")
					game.selected_room_cell=cell;game._refresh_all();game._set_grid_zoom(1.6,true,(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE))
					game.grid_view.queue_redraw()
					for attempt in range(120):
						await process_frame;await RenderingServer.frame_post_draw
						if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game.grid_view.visible_draw_rooms.size()==1:break
					game.paused=false;resumed=true;previous=""
				var frame:Texture2D=game.grid_view._get_branforth_frame(game)''')
s=s.replace('"%s-mode%d-change%03d.png"%[id,sample_mode,captures]', '"case%02d-mode%d-change%03d.png"%[test_case,sample_mode,captures]')
s=s.replace('"room":id,"mode":sample_mode,','"room":id,"mode":sample_mode,"case":test_case,"resumed":resumed,"sourceHash":game.grid_view._get_branforth_frame_source(game).get_image().get_data().hex_encode().sha256_text(),"tabletExitPose":actor.tablet_exit_pose,')
s=s.replace('check(seen_rise,"Controller completes seated held activity and rises")','check(resumed and seen_rise,"Fresh Continue completes stow and rise")')
s=s.replace('validate-evidence.json','continue-evidence.json').replace('validate.gd.uid','continue.gd.uid')
s=s.replace('Actual normal NPC update timers after reachable q0 furniture station arrival, held activity/rise and source-change native captures, both gears. Fixed60Hz fixture steps and controlled topology; no autonomous incoming/outgoing travel, interruption, fresh Continue or all-rotation claim.','Six actual disk checkpoints restored into fresh main scenes at partial draw, held reading and interrupted dynamic-held stow, both gears, reachable q0 South sofa. Actor/playback/clock/pause/source exact, normal update to rise. No autonomous travel or other cardinal/rotation claim.')
s=s.replace('JAMES SEATED TABLET PHASES:', 'JAMES SEATED FRESH CONTINUE:')
(P/'continue.gd').write_text(s)
for mode,label in enumerate(['bare','helmet']):
    t=s.replace('range(6):',f'range({mode*3},{mode*3+3}):').replace('continue-native/',f'continue-{label}-native/').replace('continue-evidence.json',f'continue-{label}-evidence.json').replace('continue.gd.uid',f'continue-{label}.gd.uid')
    (P/f'continue-{label}.gd').write_text(t)
print('Created six-case fresh scene disk Continue fixture plus bounded three-case gear lanes.')
