from pathlib import Path
P = Path(__file__).resolve().parent
source = (P / 'native-next-goal.gd').read_text(encoding='utf8')
source = source.replace('game=load("res://scenes/main.tscn").instantiate();', 'game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);')
source = source.replace('game.architect_run.clear();', 'check(not game.architect_run.is_empty(),"Use current recovered-roster presence rules");game.test_walker_cell=Vector2i(-1,-1);')
source = source.replace('native-next-goal-evidence.json', 'native-traffic-evidence.json')
source = source.replace('var npc=game.branforth_npc;', 'game.hardware.pumps=false\n\tvar peer=game.bill_npc\n\tvar npc=game.branforth_npc;')
source = source.replace('game.recovered_crew.assign([{', 'game.recovered_crew.assign([{ "architect_id":"bill","alive":true,"id":"architect_bill","name":"Bill","origin":cell },{')
source = source.replace('npc.rebuild(game);npc.active=true;', 'peer.active=false;peer.rebuild(game)\n\t\t\tnpc.rebuild(game);npc.active=true;')
source = source.replace('preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",1.0/120);npc.update(game,1.0/120);', 'game._update_test_walker(1.0/120);')
source = source.replace('var next_ticks:=0;', 'var introduced:=false;var encounters:Array=[];var max_wait:=0.0;var detours:=0\n\t\t\tvar next_ticks:=0;')
source = source.replace('var previous:String=npc.direction;var before:Vector2=npc.foot;var old_goal:String=npc.goal', '''var previous:String=npc.direction;var before:Vector2=npc.foot;var old_goal:String=npc.goal
				var before_path:PackedVector2Array=npc.path.duplicate()
				if started and not introduced and npc.cell_at(npc.foot)!=cell and not npc.path.is_empty():
					var forward:Vector2=npc.path[0]-npc.foot
					if forward.length()>64:
						var candidate:Vector2=npc.foot+forward.normalized()*48
						peer.helmet_equipped=mode=="helmet";peer.movement_medium="flooded"
						if peer.can_stand(candidate) and peer.swim_segment_clear(candidate,candidate,"north","north",true):
							peer.foot=candidate;peer.active=true;peer.dead=false;peer.stage="";peer.expedition.clear();peer.path.clear();peer.state="idle";peer.direction="north";peer.goal="curiosity";peer.goal_cell=peer.cell_at(candidate);peer.timer=30
							peer.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0};peer.tank_oxygen=60;peer.breath_oxygen=15;peer.starvation=0;peer.activity="looking around"
							introduced=true;encounters.append({"kind":"peer introduced","james":str(npc.foot-center),"peer":str(peer.foot-center)})
							if q==0:captures.append(await capture("traffic-"+mode+"-introduced",npc))''')
source = source.replace('if not started and not npc.path.is_empty():', '''if introduced:
					check(npc.foot.distance_to(peer.foot)>=npc.CREW_CLEARANCE-.02,"Actual crew keep foot separation")
					max_wait=maxf(max_wait,npc.traffic_wait)
					if npc.foot==before and not npc.path.is_empty() and before_path!=npc.path:
						detours+=1;encounters.append({"kind":"normal detour","james":str(npc.foot-center),"peer":str(peer.foot-center)})
				if not started and not npc.path.is_empty():''')
source = source.replace('check(interrupted.is_empty(),"Every next-route turn finishes its finite clock")', 'check(introduced,"Actual peer intercepts normal chosen route")')
source = source.replace('check(started and arrived and not npc.dead,"Normal next goal completes after egress")', 'check(started and arrived and not npc.dead,"Normal next goal completes after egress")\n\t\t\tcheck(not game.veld_npc.active and not game.marsh_npc.active,"No unintended legacy crew spawn")\n\t\t\tcheck(interrupted.is_empty(),"Actual ordinary turns finish during traffic")')
source = source.replace('"rotation":q,"mode":mode,', '"rotation":q,"mode":mode,"introduced":introduced,"encounters":encounters,"maxWait":max_wait,"detours":detours,')
source = source.replace('JAMES CONSOLE NEXT GOAL:', 'JAMES TRAFFIC JOURNEYS:')
source = source.replace('var prior_clip:String=player.motion.get("clip","");', 'var prior_state:String=player.motion.get("state","");var prior_clip:String=player.motion.get("clip","");')
source = source.replace('if previous!=npc.direction and not npc.path.is_empty():', 'if previous!=npc.direction and not npc.path.is_empty() and prior_state=="swim" and npc.animation_state()=="swim":')
source = source.replace('max_wait=maxf(max_wait,npc.traffic_wait)', '''max_wait=maxf(max_wait,npc.traffic_wait)
					if q==0 and npc.traffic_wait>=.245 and npc.traffic_wait<.255:captures.append(await capture("traffic-"+mode+"-waiting",npc))''')
source = source.replace('false,extent),"Selected pose', 'npc.animation_state()=="tread" and game.grid_view.branforth_player.motion.get("clip","").is_empty(),extent),"Selected pose')
source = source.replace('Skipped starts and unfinished finite turns fail validation.', 'Skipped ordinary-turn starts and unfinished ordinary turns fail validation; state changes from treading are restarts, not ordinary turns.')
source = source.replace('"Selected pose and full body clear actual geometry"', '"Selected pose and full body clear actual geometry: foot=%s direction=%s key=%s phase=%s state=%s extent=%s"%[str(npc.foot),npc.direction,player_key(npc),str(npc.console_motion),npc.animation_state(),str(extent)]')
source += '\nfunc player_key(npc)->String:\n\treturn str(game.grid_view.branforth_player.motion)+" actor "+npc.animation_state()+"-"+npc.direction\n'
source = source.replace('No fixed next path or facing injection.', 'No fixed James next path or facing injection. Native main crew update and passage module run; pumps disabled in fixture, equal initial water levels. A fixture recovered Bill is introduced48 units ahead in a clear adjacent-room lane and may yield normally. Current recovered-roster rules exclude unintended legacy crew.')
source = source.replace('Traffic, high-water bare survival and other seeds/destinations separate.', 'Other traffic patterns, high-water bare survival and other seeds/destinations remain separate.')
(P / 'native-traffic.gd').write_text(source, encoding='utf8')
print('Created normal main-update traffic fixture')
