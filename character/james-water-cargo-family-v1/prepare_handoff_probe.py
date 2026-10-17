from pathlib import Path
P=Path(__file__).resolve().parent
source=(P.parent/'james-water-turn-family-v1/native-routes.gd').read_text()
prefix=source[:source.index('\tvar clearance: Dictionary=')].replace('james-water-turn-family-v1','james-water-cargo-family-v1').replace('james-water-turn-routes','james-water-cargo-phases')
body='''
	var home:=Vector2i(20,18)
	var room:Dictionary=game.RoomDatabaseScript.get_room("airlock").duplicate(true);room.pos=home;room.rotation=0
	game.occupied[home]=room;game.placed_rooms.append(room);game.powered_room_cells[home]=true
	var player=game.grid_view.branforth_player
	player.load_manifest("res://character/james-water-cargo-family-v1/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/james-water-cargo-family-v1/helmet-manifest.json"),"Candidate helmets")
	game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
	await process_frame
	game._center_grid_on_station_now();await process_frame
	DirAccess.make_dir_recursive_absolute("res://character/james-water-cargo-family-v1/route-captures")
	var trips=preload("res://scripts/crew_expedition.gd")
	var sites=preload("res://scripts/harvest_sites.gd")
	var target:=Vector2i(24,20)
	var center:Vector2=(Vector2(Vector2i(23,20))+Vector2.ONE*.5)*384.0
	var deltas:Dictionary={"east":Vector2.RIGHT,"south":Vector2.DOWN,"west":Vector2.LEFT,"north":Vector2.UP}
	for mode in ["helmet"]:
		var gear:String="" if mode=="bare" else "diving-helmet"
		npc.helmet_equipped=mode=="helmet";npc.set_movement_medium("exterior");npc.tank_oxygen=60
		var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		for d in ["east","south","west","north"]:
			var site:Dictionary=sites.make_site("salvage",3);site.discovered=false;game.drone_fleet.sites={target:site}
			npc.foot=center;npc.direction=d;npc.state="idle"
			npc.expedition={"kind":"salvage","phase":"salvage","home":home,"target":target,"route":PackedVector2Array(),"sea_route":PackedVector2Array([center-deltas[d]*200,center]),"elapsed":0.0,"cargo":{},"recall":false}
			var resources:Dictionary=game.resources.duplicate()
			player.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0;game.visual_clock=0
			var texture:Texture2D=game.grid_view._get_branforth_frame(game)
			check(texture==frames["salvage-"+d][0],"Selected salvage pose "+d+mode)
			await capture(mode+"-salvage-"+d+"-000",npc)
			trips.advance(game,npc,5.48)
			check(npc.expedition.phase=="pickup" and npc.expedition.elapsed==0.0,"Actual salvage to pickup "+d)
			check(npc.animation_state()=="swim-pickup" and npc.action_elapsed()==0.0,"Simulation sampler selected "+d)
			var elapsed:=0.0
			var durations:Array=[70,80,90,100,100,80]
			for i in range(6):
				var sample:float=elapsed+float(durations[i])/2000.0
				trips.advance(game,npc,sample-float(npc.expedition.elapsed))
				game.visual_clock+=.3
				texture=game.grid_view._get_branforth_frame(game)
				check(texture==frames["swim-pickup-"+d][i],"Actual pickup slot "+d+mode+str(i))
				check(site.units==3 and npc.expedition.cargo.is_empty(),"No premature resource commitment "+d+str(i))
				var paused_elapsed:float=npc.expedition.elapsed
				game.visual_clock+=1.0
				check(game.grid_view._get_branforth_frame(game)==texture and npc.expedition.elapsed==paused_elapsed,"Cosmetic time cannot advance pickup "+d+str(i))
				await capture(mode+"-pickup-"+d+"-"+str(i).pad_zeros(3),npc)
				elapsed+=float(durations[i])/1000.0
			trips.advance(game,npc,.52-float(npc.expedition.elapsed)+.000001)
			check(npc.expedition.phase=="return" and site.units==2 and npc.expedition.cargo==sites.LOADS.salvage,"Commit one load at completion "+d)
			check(game.resources==resources,"Cargo not delivered before safe return "+d)
			texture=game.grid_view._get_branforth_frame(game)
			check(texture==frames["swim-carry-"+d][0],"Actual pickup to carry endpoint "+d+mode)
			await capture(mode+"-carry-"+d+"-000",npc)
			var old_foot:Vector2=npc.foot
			trips.advance(game,npc,.1)
			check(npc.foot!=old_foot and npc.animation_state()=="swim-carry" and not npc.expedition.cargo.is_empty(),"Actual exterior movement retains cargo "+d)
			# Recall interruption from a fresh pickup must not consume the deposit.
			site.units=3;npc.expedition.phase="pickup";npc.expedition.elapsed=.23;npc.expedition.cargo={};npc.expedition.recall=true
			trips.advance(game,npc,.01)
			check(npc.expedition.phase=="return" and site.units==3 and npc.expedition.cargo.is_empty(),"Recall cancels uncommitted pickup "+d)
			results.append({"direction":d,"mode":mode,"pickupSlots":6,"phaseCommit":true,"recall":true})
	var file=FileAccess.open("res://character/james-water-cargo-family-v1/phase-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Four helmet-equipped controlled injected exterior salvage/pickup states, actual expedition advancement, actual NPC action selection and normal grid drawing with candidate manifest injected. Pickup pause and resource/recall handoffs, short exterior move; not dispatch, full airlock journey, turn clearance or installed selection proof. Bare exterior presentation is only covered by the standalone sprite player because set_movement_medium correctly requires breathing gear."},"  "))
	print("JAMES WATER CARGO PHASES: ",checks," checks; ",failures," failures; controlled phase fixture only")
	quit(1 if failures else 0)
'''
(P/'native-phases.gd').write_text((prefix+body).replace('visual_clock=0','visual_time_seconds=0.0').replace('visual_clock','visual_time_seconds'))
print('Prepared controlled actual expedition phase and candidate grid fixture')
