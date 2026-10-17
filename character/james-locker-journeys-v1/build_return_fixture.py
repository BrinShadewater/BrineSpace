from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'native-locker.gd').read_text(encoding='utf8')
source=source.replace('OUT+"captures/"','OUT+"return-captures/"').replace('OUT+"captures"','OUT+"return-captures"')
source=source.replace('game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])','game.running=true;game.paused=false;game.Architects.advance_core(game,10)\n\tcheck(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")')
source=source.replace('game.wrecks.clear()','# Retain real pod records for checkpoints.')
source=source.replace('var ticks:=0;','var interrupted:=false;var return_record:Dictionary={}\n\t\t\tvar ticks:=0;')
needle='\t\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)'
insertion='''				if not interrupted and npc.helmet_action_active():
					var elapsed:float=player.cycle_seconds(key)-npc.timer
					var threshold:float=([.2,.4,1.2,2.0][q] if equip else [.2,.8,1.8,2.0][q])
					if elapsed>=threshold:
						var held_gear:bool=npc.helmet_equipped;var held_foot:Vector2=npc.foot;var total:float=player.cycle_seconds(key)
						var first_elapsed:=elapsed;var return_ticks:=0;var restored:=false;var seen_return:Array=[];var return_captures:Array=[]
						game.powered_room_cells.erase(cell)
						Service.check_service(game,npc)
						check(npc.helmet_return_active(),"Service loss starts reverse held-pose return")
						check(not Service.request(game,"branforth",cell),"Offline UI request refused during return")
						var first:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
						check(first==player.frame_at_elapsed(key,elapsed).get_image().get_data(),"Interruption begins on exact held pose without jump")
						while npc.helmet_return_active() and return_ticks<1000:
							var before_elapsed:float=total-npc.timer
							game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;return_ticks+=1
							check(npc.foot==held_foot and npc.helmet_equipped==held_gear,"Return keeps fixed contact and uncommitted gear")
							if npc.helmet_return_active():
								var reverse_elapsed:float=total-npc.timer
								check(reverse_elapsed<=before_elapsed and reverse_elapsed>=0,"Return clock decreases monotonically")
								var expected:Texture2D=player.frame_at_elapsed(key,reverse_elapsed)
								check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==expected.get_image().get_data(),"Reverse clock draws exact authored source pose")
								check(Service.helmet_on_shelf(game,cell)==(reverse_elapsed<float(row.events[0].timeMs)/1000 if equip else reverse_elapsed>=float(row.events[0].timeMs)/1000),"Reverse shelf marker follows returned held item")
								var slot:int=player.frames[key].find(expected)
								if slot not in seen_return:
									seen_return.append(slot)
									if q==2:return_captures.append(await capture("q2-%s-return-%02d"%[action,slot],npc))
								if not restored and reverse_elapsed<=first_elapsed*.5:
									game.paused=true;var before_actor:Dictionary=npc.snapshot();var clock:float=game.visual_time_seconds;var pixels:PackedByteArray=expected.get_image().get_data();var shelf:bool=Service.helmet_on_shelf(game,cell)
									check(preload("res://scripts/branforth_npc.gd").valid_branforth_snapshot(before_actor),"Returning snapshot valid")
									var invalid:Dictionary=before_actor.duplicate(true);invalid.branforth_helmet_return="invalid";check(not preload("res://scripts/branforth_npc.gd").valid_branforth_snapshot(invalid),"Malformed return flag rejected")
									invalid=before_actor.duplicate(true);invalid.timer=total+1;check(not preload("res://scripts/branforth_npc.gd").valid_branforth_snapshot(invalid),"Return clock outside authored duration rejected")
									var save=preload("res://scripts/run_save.gd");var reason:String=save.problem(save.capture(game));check(reason.is_empty(),"Returning checkpoint valid: "+reason)
									if not reason.is_empty():quit(1);return
									var scratch_path:="user://james-returning-helmet.loop"
									check(save.write(game,scratch_path)==OK,"Returning checkpoint writes")
									var data:Dictionary=save.read(scratch_path);check(not data.is_empty(),"Returning checkpoint reads")
									check(await save.restore_staged(game,data),"Actual returning Continue restore: "+save.last_error)
									game.run_save_path=scratch_path;game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player
									check(npc.snapshot()==before_actor and npc.helmet_return_active(),"Continue keeps reverse mode and exact actor timer")
									check(game.paused and game.visual_time_seconds==clock and game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Continue keeps paused reverse pose/clock")
									check(Service.helmet_on_shelf(game,cell)==shelf,"Continue keeps reverse shelf state")
									game._process(.5);check(game.visual_time_seconds==clock and game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Paused returning Continue does not advance")
									game.set_process(false);game.paused=false;restored=true
									game.powered_room_cells[cell]=true
									check(not Service.request(game,"branforth",cell),"Restored power cannot restart an unfinished return")
						check(restored and not npc.helmet_action_active() and not npc.helmet_return_active(),"Reverse return completes finite duration after Continue")
						check(npc.helmet_equipped==held_gear and npc.path.is_empty() and npc.locker_request.is_empty(),"Abort completion leaves original equipment without obsolete work")
						check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==player.frame_at_elapsed("idle-east",0,"diving-helmet" if held_gear else "").get_image().get_data(),"Return joins exact original idle master")
						return_record={"startedElapsed":first_elapsed,"returnTicks":return_ticks,"restored":restored,"slots":seen_return,"captures":return_captures}
						game.powered_room_cells[cell]=true;check(Service.request(game,"branforth",cell),"Normal retry accepted after finite return")
						interrupted=true;started=false;complete=false;seen.clear();samples.clear();contact=Vector2.INF
'''
assert source.count(needle)==2
source=source.replace(needle,insertion+needle,1)
source=source.replace('"rotation":q,"action":action,','"rotation":q,"action":action,"return":return_record,')
source=source.replace('native-locker-evidence.json','native-locker-return-evidence.json').replace('JAMES LOCKER JOURNEYS:','JAMES LOCKER RETURN:')
old_scope=source.split('"scope":"',1)[1].split('"',1)[0]
source=source.replace(old_scope,'Eight actual service-loss reversals from sampled forward poses; existing selected source, decreasing simulation clock, fixed contact, uncommitted gear, reverse shelf markers, eight actual midpoint Continue restores, paused pixels and no premature restart when power returns. Normal retry and next task afterward. Standard four rotations and seed17; other safety cancellations remain immediate.')
(P/'native-locker-return.gd').write_text(source,encoding='utf8')
print('Created eight finite reversal and actual midpoint Continue cases')
