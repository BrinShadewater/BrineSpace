from pathlib import Path
P = Path(__file__).resolve().parent
source = (P / 'native-locker.gd').read_text(encoding='utf8')
source = source.replace('OUT+"captures/"', 'OUT+"restore-captures/"').replace('OUT+"captures"', 'OUT+"restore-captures"')
source = source.replace('game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])', 'game.running=true;game.paused=false;game.Architects.advance_core(game,10)\n\tcheck(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core release supplies checkpoint roster")')
source = source.replace('game.wrecks.clear()', '# Retain real unrecovered pod/roster records for checkpoint validation.')
source = source.replace('var ticks:=0;', 'var restored:=false;var restore_record:Dictionary={}\n\t\t\tvar ticks:=0;')
needle = '\t\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)'
insertion = '''				var restore_due:=false
				if not restored:
					if q==3 and not npc.path.is_empty() and npc.foot.distance_to(before)>0 and ticks>=30:restore_due=true
					elif q<3 and npc.helmet_action_active():
						var elapsed:float=player.cycle_seconds(key)-npc.timer
						var threshold:float=([.2,.4,1.2][q] if equip else [1.8,2.0,.8][q])
						restore_due=elapsed>=threshold
				if restore_due:
					game.paused=true
					var saved_actor:Dictionary=npc.snapshot();var saved_clock:float=game.visual_time_seconds
					var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
					var shelf:bool=Service.helmet_on_shelf(game,cell)
					var save=preload("res://scripts/run_save.gd");var reason:String=save.problem(save.capture(game))
					check(reason.is_empty(),"Fitting checkpoint validates real roster/actor: "+reason)
					if not reason.is_empty():quit(1);return
					var scratch_path:="user://james-fitting-restore.loop"
					check(save.write(game,scratch_path)==OK,"Fitting checkpoint writes actual disk")
					var checkpoint:Dictionary=save.read(scratch_path);check(not checkpoint.is_empty(),"Fitting checkpoint reads")
					if checkpoint.is_empty():quit(1);return
					check(await save.restore_staged(game,checkpoint),"Actual staged Continue fitting restore: "+save.last_error)
					game.run_save_path=scratch_path;game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false)
					npc=game.branforth_npc;player=game.grid_view.branforth_player
					check(npc.snapshot()==saved_actor,"Continue preserves fitting actor/timer/path")
					check(game.visual_time_seconds==saved_clock and game.paused,"Continue preserves paused simulation clock")
					check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Continue preserves exact fitting/walk pixels")
					check(Service.helmet_on_shelf(game,cell)==shelf,"Continue preserves shelf handoff")
					game._process(.5)
					check(game.visual_time_seconds==saved_clock and game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Paused Continue holds fitting pixels")
					game.set_process(false);game.paused=false;restored=true
					restore_record={"state":saved_actor.state,"timer":saved_actor.timer,"shelf":shelf,"clock":saved_clock,"file":scratch_path}
'''
assert source.count(needle) == 2
source = source.replace(needle, insertion + needle, 1)
source = source.replace('check(started and complete and not npc.dead,"Normal approach and fitting complete")', 'check(started and complete and not npc.dead,"Normal approach and fitting complete")\n\t\t\tcheck(restored,"Actual fitting/approach checkpoint restored")')
source = source.replace('"rotation":q,"action":action,', '"rotation":q,"action":action,"restore":restore_record,')
source = source.replace('native-locker-evidence.json', 'native-locker-restore-evidence.json').replace('JAMES LOCKER JOURNEYS:', 'JAMES LOCKER RESTORE:')
old_scope=source.split('"scope":"',1)[1].split('"',1)[0]
source=source.replace(old_scope,'Eight real disk write/read/staged Continue cases: fitting before/after shelf markers, mid-held poses and pending approaches. Exact actor/path/timer, pixels, shelf, paused clock and normal resume asserted. Actual core-release roster and unrecovered pod records retained; standard four rotations and seed17 only.')
(P / 'native-locker-restore.gd').write_text(source, encoding='utf8')
print('Created eight actual fitting/approach Continue cases')
