from pathlib import Path
P = Path(__file__).resolve().parent
source = (P / 'native-locker.gd').read_text(encoding='utf8')
source = source.replace('OUT+"captures/"', 'OUT+"power-captures/"').replace('OUT+"captures"', 'OUT+"power-captures"')
source = source.replace('var ticks:=0;', 'var interrupted:=false;var power_record:Dictionary={}\n\t\t\tvar ticks:=0;')
needle = '\t\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)'
insertion = '''				if not interrupted and npc.helmet_action_active():
					var elapsed:float=player.cycle_seconds(key)-npc.timer
					var threshold:float=([.2,.4,1.2,2.0][q] if equip else [.2,.8,1.8,2.0][q])
					if elapsed>=threshold:
						var held_gear:bool=npc.helmet_equipped;var held_foot:Vector2=npc.foot;var shelf_before:bool=Service.helmet_on_shelf(game,cell)
						game.powered_room_cells.erase(cell);game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
						check(not npc.helmet_action_active() and npc.helmet_equipped==held_gear,"Power loss cancels without premature gear commit")
						check(npc.path.is_empty() and npc.goal.is_empty() and npc.locker_request.is_empty(),"Offline fitting clears obsolete request/route")
						check(npc.foot==held_foot,"Power cancellation remains at locker")
						check(Service.helmet_on_shelf(game,cell),"Offline reusable shelf helmet returns")
						check(not Service.request(game,"branforth",cell),"Offline UI request refused")
						var idle:Texture2D=game.grid_view._get_branforth_frame_source(game)
						check(idle.get_image().get_data()==player.frame_at_elapsed("idle-east",0,"diving-helmet" if held_gear else "").get_image().get_data(),"Canceled fitting selects unchanged-gear idle master")
						power_record={"elapsed":elapsed,"gear":held_gear,"shelfBefore":shelf_before,"shelfAfter":Service.helmet_on_shelf(game,cell),"visualPolicy":"Immediate unchanged-gear idle on service loss; held-pose return motion is not authored by this guard."}
						if q in [0,1]:await capture("q%d-%s-power-canceled"%[q,action],npc)
						game.powered_room_cells[cell]=true
						check(Service.request(game,"branforth",cell),"Power restoration accepts normal retry")
						interrupted=true;started=false;complete=false;seen.clear();samples.clear();contact=Vector2.INF
'''
assert source.count(needle) == 2
source = source.replace(needle, insertion + needle, 1)
source = source.replace('check(started and complete and not npc.dead,"Normal approach and fitting complete")', 'check(started and complete and not npc.dead,"Normal approach and fitting complete")\n\t\t\tcheck(interrupted,"Live power interruption exercised")')
source = source.replace('"rotation":q,"action":action,', '"rotation":q,"action":action,"powerInterruption":power_record,')
source = source.replace('native-locker-evidence.json', 'native-locker-power-evidence.json').replace('JAMES LOCKER JOURNEYS:', 'JAMES LOCKER POWER:')
old_scope=source.split('"scope":"',1)[1].split('"',1)[0]
source=source.replace(old_scope,'Eight actual room-service power losses during normal fitting/removal. No early gear commit, obsolete request/path cleared, grounded foot, reusable shelf restored and offline request refused. Normal retry completes all twelve slots and next task. Current visual cancellation is immediate unchanged-gear idle; finite held-item return is not verified. Standard rotations/seed17 only.')
(P / 'native-locker-power.gd').write_text(source, encoding='utf8')
print('Created eight normal service power-loss/retry cases')
