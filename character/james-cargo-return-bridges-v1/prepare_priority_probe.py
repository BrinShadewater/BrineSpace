from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
prefix=(p/'actor-return.gd').read_text().split('\n\tfor mode in ["bare","helmet"]:')[0]
body='''
	var original_rooms:Array=game.placed_rooms.duplicate(true)
	for mode in ["bare","helmet"]:
		for hazard in ["gear","death","fire","water","floor","service"]:
			game.occupied.clear();game.powered_room_cells.clear();game.placed_rooms=original_rooms.duplicate(true)
			for room in game.placed_rooms:room.fire=0;room.water_level=0;game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
			npc=preload("res://character/james-cargo-return-bridges-v1/return_actor.gd").new();game.branforth_npc=npc;npc.preview_player=player;npc.rebuild(game)
			npc.helmet_equipped=mode=="helmet";npc.active=true;npc.dead=false;npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.needs.curiosity=90
			npc.foot=start;npc.direction=facing;npc.path=PackedVector2Array([contact]);npc.movement_medium="dry"
			player.return_plan.clear();player.last_source.clear();player.motion.clear();player.current_key="";player.last_time=-1
			game.visual_time_seconds=100;game.paused=false;var reached:=false;var carry_ticks:=0
			for tick in range(2000):
				npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
				if npc.stage!="workshop_carry":continue
				carry_ticks+=1
				if carry_ticks<20:continue
				reached=true;break
			check(reached,"Actual carry reached "+mode+hazard)
			if not reached:continue
			game.powered_room_cells.erase(ORIGIN);npc.update(game,.02);game.visual_time_seconds+=.02
			check(npc.cargo_return_active(),"Actual power-loss return admitted "+mode+hazard)
			if player.return_plan.is_empty():continue
			var plan:Dictionary=player.return_plan.duplicate(true);var foot_before:Vector2=npc.foot
			var before:Texture2D=game.grid_view._get_branforth_frame(game);var label:String="priority-"+mode+"-"+hazard
			before.get_image().save_png(OUT+"arrival-captures/"+label+"-before-source.png")
			var world_before:String=await capture(label+"-before-000",npc)
			match hazard:
				"gear":check(npc.set_helmet_equipped(not npc.helmet_equipped),"Public gear setter accepted")
				"death":npc.die();check(npc.dead,"Public death API applied")
				"fire":
					game.occupied[ORIGIN].fire=1.0;npc.update(game,.02);game.visual_time_seconds+=.02
					check(npc.fire_cells.has(ORIGIN) and npc.goal=="fire-retreat","Actual fire refresh/retreat dispatch")
				"water":
					game.occupied[ORIGIN].water_level=.95;npc.breath_oxygen=12;npc.tank_oxygen=12
					preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",.02)
					npc.update(game,.02);game.visual_time_seconds+=.02
					check(npc.movement_medium=="flooded","Actual RoomFlooding water/air selection")
				"floor":
					game.occupied.erase(ORIGIN);game.placed_rooms=game.placed_rooms.filter(func(room):return room.pos!=ORIGIN)
					npc.update(game,.02);game.visual_time_seconds+=.02
					check(not npc.can_stand(npc.foot),"Actual topology removal invalidates contact")
				"service":
					game.powered_room_cells[ORIGIN]=true;npc.foot=contact;npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.path.clear();npc.state="idle"
					npc.arrive();npc.update(game,.02);game.visual_time_seconds+=.02
					check(npc.stage=="workshop_inspect","Actual prescribed new RoomActivity arrival")
			check(not npc.cargo_return_active(),"Priority removes actor return immediately "+label)
			var after:Texture2D=game.grid_view._get_branforth_frame(game)
			check(player.return_plan.is_empty(),"Priority clears display return "+label)
			check(after!=null,"Priority has native replacement source")
			check(player.return_texture(game.visual_time_seconds,plan.gear)==null,"No stale return source after priority")
			after.get_image().save_png(OUT+"arrival-captures/"+label+"-after-source.png")
			var world_after:String=await capture(label+"-after",npc)
			results.append({"mode":mode,"hazard":hazard,"goal":npc.goal,"stage":npc.stage,"state":npc.state,"medium":npc.movement_medium,"dead":npc.dead,"pathSize":npc.path.size(),"displacement":npc.foot.distance_to(foot_before),"reason":npc.return_reason,"actorReturnActive":npc.cargo_return_active(),"displayReturnEmpty":player.return_plan.is_empty(),"sources":[OUT+"arrival-captures/"+label+"-before-source.png",OUT+"arrival-captures/"+label+"-after-source.png"],"world":[world_before,world_after]})
	var f:=FileAccess.open(OUT+"priority-evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"12prescribed actual carry/power-loss return admissions; public gear/death APIs, actual fire field dispatch, RoomFlooding wet/air selection, topology floor removal and prescribed new RoomActivity arrival. Native before/after sources and room captures. No full natural hazard/refuge/route, mortality bookkeeping or save/restore acceptance."},"  "))
	if not FileAccess.file_exists(OUT+"priority.gd.uid"):
		var uid:=FileAccess.open(OUT+"priority.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES CARGO RETURN PRIORITY: ",checks,"checks; ",failures,"failures; ",results.size(),"cases")
	quit(1 if failures else 0)
'''
(p/'priority.gd').write_text(prefix+body)
paths=['scripts/bill_npc.gd','scripts/branforth_npc.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/fire_safety.gd','scripts/flood_safety.gd','scripts/room_flooding.gd','character/james-east-cargo-heads-v3/return_plan.gd']
paths += [str(x.relative_to(r)) for x in [p/'return_actor.gd',p/'return_player.gd',p/'priority.gd',p/'bare-joined-manifest-v4.json',p/'helmet-joined-manifest-v4.json']]
(p/'priority-inputs.json').write_text(json.dumps({path:hashlib.sha256((r/path).read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Prepared12actual admitted-return priority cases;13targeted inputs frozen before launch.')
