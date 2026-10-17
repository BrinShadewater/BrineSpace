from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
source=(p/'release.gd').read_text()
prefix=source[:source.index('\tfor bad in [')]
prefix=prefix.replace('"sortY":slot.item.sort_y if slot!=null else 0,','"pivot":[texture.get_meta("crew_pivot").x,texture.get_meta("crew_pivot").y],"height":texture.get_meta("crew_standing_height"),"gear":"helmet" if npc.helmet_equipped else "bare","sortY":slot.item.sort_y if slot!=null else 0,')
tail='''	var original_rooms:Array=game.placed_rooms.duplicate(true)
	for mode in ["bare","helmet"]:
		for phase in ["before","after"]:
			for hazard in ["gear","death","fire","water","floor","service"]:
				game.occupied.clear();game.powered_room_cells.clear();game.placed_rooms=original_rooms.duplicate(true)
				for room in game.placed_rooms:
					room.fire=0;room.water_level=0;room.erase(FLOOR.FIELD);game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
				view.bind_room(game.occupied[ORIGIN]);view.embedded_case=false;view.sync_case()
				npc=preload("res://character/james-floor-case-west-v1/floor_actor.gd").new()
				game.branforth_npc=npc;npc.preview_player=player;npc.rebuild(game)
				npc.helmet_equipped=mode=="helmet";npc.active=true;npc.dead=false;npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.needs.curiosity=90
				npc.foot=start;npc.direction=facing;npc.path=PackedVector2Array([contact]);npc.movement_medium="dry"
				player.return_plan.clear();player.last_source.clear();player.motion.clear();player.current_key="";player.last_time=-1
				game.visual_time_seconds=100;game.paused=false;var reached:=false;var carry_ticks:=0
				for tick in range(2000):
					npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
					if npc.stage!="workshop_carry":continue
					carry_ticks+=1
					if carry_ticks>=20:reached=true;break
				check(reached,"Actual carry reached "+mode+phase+hazard)
				if not reached:quit(1);return
				game.powered_room_cells.erase(ORIGIN);npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
				var release:float=FLOOR.release_time(player)
				check(not player.return_plan.is_empty() and is_finite(release),"Actual source-bound release plan")
				if failures:quit(1);return
				var plan:Dictionary=player.return_plan.duplicate(true)
				while game.visual_time_seconds<release-.03:
					npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
				if phase=="after":
					game.visual_time_seconds=release+.001;npc.update(game,.02);game.grid_view._get_branforth_frame(game)
				var owned:Dictionary=FLOOR.payload(game.occupied[ORIGIN]).duplicate(true)
				check(owned.is_empty()==(phase=="before"),"Prescribed pre/post release ownership")
				var foot_before:Vector2=npc.foot
				var label:String=mode+"-floor-priority-"+phase+"-"+hazard
				await record_case(view,npc,label+"-initial")
				# Advance beyond cue before dispatch: priorities must supersede actor
				# return before its hook can create any pre-release floor ownership.
				game.visual_time_seconds=release+.04
				match hazard:
					"gear":check(npc.set_helmet_equipped(not npc.helmet_equipped),"Public gear setter")
					"death":npc.die();check(npc.dead,"Public death API")
					"fire":
						game.occupied[ORIGIN].fire=1.0;npc.update(game,.02)
						check(npc.fire_cells.has(ORIGIN) and npc.goal=="fire-retreat","Actual fire refresh/dispatch")
					"water":
						game.occupied[ORIGIN].water_level=.95;npc.breath_oxygen=12;npc.tank_oxygen=12
						preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",.02)
						npc.update(game,.02);check(npc.movement_medium=="flooded","Actual flooding medium selection")
					"floor":
						game.occupied.erase(ORIGIN);game.placed_rooms=game.placed_rooms.filter(func(room):return room.pos!=ORIGIN)
						npc.update(game,.02);check(not npc.can_stand(npc.foot),"Actual topology invalidates contact")
					"service":
						game.powered_room_cells[ORIGIN]=true;npc.foot=contact;npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.path.clear();npc.state="idle"
						npc.arrive();npc.update(game,.02);check(npc.stage=="workshop_inspect","Actual prescribed new RoomActivity")
				check(not npc.cargo_return_active(),"Priority immediately supersedes return")
				game.grid_view._get_branforth_frame(game)
				check(player.return_plan.is_empty() and player.return_texture(game.visual_time_seconds,plan.gear)==null,"No stale source/return plan")
				var actual:Dictionary=FLOOR.payload(game.occupied.get(ORIGIN,{}))
				check(actual==(owned if hazard!="floor" else {}),"Released case persists; unreleased case cannot appear; removed room has none")
				check(not view.embedded_case,"Replacement source cannot hide separate case")
				check(view.case_enabled==(phase=="after" and hazard!="floor"),"Separate floor drawing follows surviving room ownership")
				await record_case(view,npc,label+"-replaced")
				if hazard=="floor":
					check(prop_slot()==null,"Removed room submits no stale floor case")
					var fresh:Dictionary=game.RoomDatabaseScript.get_room("salvage_workshop").duplicate(true)
					fresh.pos=ORIGIN;fresh.rotation=0;fresh.water_level=0;game.occupied[ORIGIN]=fresh;game.placed_rooms.append(fresh)
					view.bind_room(fresh);check(not view.case_enabled and FLOOR.payload(fresh).is_empty(),"New room cannot resurrect old case")
				results.append({"priority":true,"mode":mode,"phase":phase,"hazard":hazard,"goal":npc.goal,"stage":npc.stage,"state":npc.state,"medium":npc.movement_medium,"dead":npc.dead,"displacement":npc.foot.distance_to(foot_before),"ownedAfterPriority":not actual.is_empty(),"returnCleared":player.return_plan.is_empty()})
				print("JAMES FLOOR PRIORITY ",mode," ",phase," ",hazard," failures=",failures)
				if failures:quit(1);return
	if not FileAccess.file_exists(OUT+"priority.gd.uid"):
		var uid:=FileAccess.open(OUT+"priority.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var f:=FileAccess.open(OUT+"priority-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"24actual prescribed power-loss carry returns, bare/helmet, before/after reviewed release. Public gear/death, actual fire/flood dispatch, topology removal/new room and prescribed new RoomActivity.48native before-after source/room pairs. Staged West only; no full natural hazard/refuge/mortality/SaveContinue or normal selection."},"  "))
	print("JAMES FLOOR PRIORITY: ",checks,"checks; ",failures,"failures;24cases;48presentations")
	quit(1 if failures else 0)
'''
(p/'priority.gd').write_text(prefix+tail)
prior=json.loads((p/'release-inputs.json').read_bytes())
paths=[r/k for k in prior if Path(k).name!='release.gd']+[p/'priority.gd',r/'scripts/room_flooding.gd']
(p/'priority-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('24before/after release priority cases prepared;13 targeted inputs frozen.')
