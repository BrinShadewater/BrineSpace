extends SceneTree
## Actual FloodSafety routes and main crew ticks, with candidate pixels and real air drain.
const Safety=preload("res://scripts/flood_safety.gd")
const Flood=preload("res://scripts/room_flooding.gd")
const PACKS={"bare":"res://character/veld-swim-distress-family-coherent-v1/bare-manifest.json","helmet":"res://character/veld-swim-distress-family-coherent-v1/helmet-manifest.json"}
const REPORT="res://output/veld-distress-escape-v1/journey-checks.json"
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func rotate_cell(v:Vector2i,q:int)->Vector2i:
	for i in q:v=Vector2i(-v.y,v.x)
	return v
func explain_edge(actor,a:Vector2,b:Vector2,heading:String,gear:String)->Dictionary:
	var e:Array=actor.swim_clearance[gear][heading]
	var footprint:=Rect2(Vector2(e[0],e[1]),Vector2(e[2]-e[0],e[3]-e[1]))
	for cell in actor.geometry:
		var data:Dictionary=actor.geometry[cell];var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
		for blocker in data.get("swim_blockers",data.get("blockers",[])):
			var obstacle:Rect2=blocker.grow(-maxf(0,float(data.get("blocker_padding",0))-2))
			var expanded:=Rect2(obstacle.position+center-footprint.end,obstacle.size+footprint.size)
			if actor.segment_hits_rect(a,b,expanded):return {"cause":"exact_blocker_sweep","cell":[cell.x,cell.y],"obstacle":str(obstacle)}
	var columns:=maxi(1,ceili(footprint.size.x/8));var rows:=maxi(1,ceili(footprint.size.y/8))
	for y in range(rows+1):
		for x in range(columns+1):
			var offset:=footprint.position+footprint.size*Vector2(float(x)/columns,float(y)/rows)
			if actor._swim_floor_clear(a+offset,b+offset):continue
			for i in range(9):
				var point:Vector2=(a+offset).lerp(b+offset,float(i)/8);var cell:Vector2i=actor.cell_at(point)
				if not actor.geometry.has(cell):return {"cause":"missing_floor"}
				var data:Dictionary=actor.geometry[cell];var local:Vector2=point-(Vector2(cell)+Vector2.ONE*.5)*384
				if data.get("corridor",false) and not actor.can_stand(point):
					return {"cause":"corridor_floor_sample","point":[point.x,point.y],"local":[local.x,local.y],"radius10":preload("res://rooms/underwater/corridor_geometry.gd").contains_foot(data.room,local,10),"radius2":preload("res://rooms/underwater/corridor_geometry.gd").contains_foot(data.room,local,2)}
	return {"cause":"other_floor_gate"}
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://veld-distress-escape.meta";game.run_save_path="user://veld-distress-escape.loop";game.Preferences.save_path="user://veld-distress-escape.cfg"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	var grid=game.grid_view;var player=grid.veld_player;player.load_manifest(PACKS.bare,true)
	check(player.load_equipment_manifest("diving-helmet",PACKS.helmet),"Candidate helmet injection")
	game.hardware.doors=false;game.hardware.pumps=false;game.running=true;game.paused=false
	game.resources.food=100;game.resources.oxygen=100
	game.recovered_crew=[{"architect_id":"veld","alive":true}]
	for peer in [game.bill_npc,game.branforth_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1);game.drone_fleet.orders.clear();game.drone_fleet.sites.clear()
	var cases:=[];var samples:=[];var diagnostics:=[];var review_rows:=[]
	for q in 4:
		for gear in ["bare","helmet"]:
			game.running=true;game.paused=false;game.crew_count=1;game.recovered_crew=[{"architect_id":"veld","alive":true}]
			game.placed_rooms.clear();game.occupied.clear();game.powered_room_cells.clear()
			var origin:=Vector2i(20,20);var wet:=origin+rotate_cell(Vector2i.RIGHT,q)
			for x in range(-1,3):
				var name:String="airlock" if x==-1 else "corridor" if x==1 else "storage_bay"
				var room:Dictionary=game.RoomDatabaseScript.get_room(name).duplicate(true)
				room.pos=origin+rotate_cell(Vector2i(x,0),q);room.rotation=(3+q)%4 if x==-1 else (1+q)%4 if x==1 else q;room.water_level=.95 if x==1 else 0
				game.placed_rooms.append(room);game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
			var actor=game.veld_npc;actor.dead=false;actor.active=true;actor.helmet_equipped=gear=="helmet";actor.direction=["west","north","east","south"][q];actor.state="idle";actor.goal="";actor.stage="";actor.path.clear();actor.expedition.clear();actor.locker_request.clear();actor.moonbay_assignment.clear();actor.cancel_helmet_action()
			await actor.rebuild(game);actor.movement_medium="flooded";actor.air_was_low=false;actor.air_recovery=0;actor.tank_oxygen=4.9;actor.breath_oxygen=4.9
			actor.set_meta("flood_safety_wait",0.0);actor.set_meta("flood_retreat_check",0.0);actor.set_meta("flood_blocked_warning",false)
			actor.active=false;game.paused=false;Flood.advance(game,.001);actor.active=true
			var desired:Vector2=(Vector2(wet)+Vector2.ONE*.5)*384+Vector2(rotate_cell(Vector2i(-140,0),q));var best:=INF;var start:Variant=null;var minimum_route:=INF;var clear_points:=0;var route_points:=0
			for id in actor.room_nodes.get(wet,[]):
				var point:Vector2=actor.graph.get_point_position(id)
				actor.foot=point
				if preload("res://scripts/crew_life.gd").clear(actor,"swim-distress") and point.distance_to(desired)<best:
					clear_points+=1
					var viable:Dictionary=Safety.escape_route(game,actor)
					if not viable.is_empty():minimum_route=minf(minimum_route,float(viable.seconds));route_points+=1
					if not viable.is_empty() and viable.seconds<4.4:best=point.distance_to(desired);start=point
			var edges:=[];var allowed_edges:=0
			for node in actor.room_nodes.get(wet,[]):
				for other in actor.graph.get_point_connections(node):
					var a:Vector2=actor.graph.get_point_position(node);var b:Vector2=actor.graph.get_point_position(other)
					if actor.cell_at(b)==wet:continue
					var heading:String=actor.travel_heading(a,b,actor.direction)
					var allowed:bool=actor.swim_segment_clear(a,b,heading,heading)
					if allowed:
						allowed_edges+=1
						var sideways:Vector2=Vector2(-(b-a).y,(b-a).x).normalized()*24
						check(not actor.swim_segment_clear(a+sideways,b+sideways,heading,heading),"Offset silhouette remains blocked by actual wall")
						actor.hardware_doors_locked=true
						check(not actor.swim_segment_clear(a,b,heading,heading),"Global door lock blocks silhouette sweep")
						actor.hardware_doors_locked=false
						actor.locked_room_cells[wet]=true
						check(not actor.swim_segment_clear(a,b,heading,heading),"Local door lock blocks silhouette sweep")
						actor.locked_room_cells.erase(wet)
						var prior_fire:Dictionary=actor.fire_cells.duplicate();actor.foot=a;actor.fire_cells[actor.cell_at(b)]=true
						check(not actor.swim_segment_clear(a,b,heading,heading),"Fire refuge entry remains blocked")
						actor.fire_cells=prior_fire
					edges.append({"from":[a.x,a.y],"to":[b.x,b.y],"heading":heading,"baseSwimAllowed":allowed,"explanation":{} if allowed else explain_edge(actor,a,b,heading,gear)})
			diagnostics.append({"rotation":q,"gear":gear,"clearTestedPoints":clear_points,"routeTestedPoints":route_points,"crossRoomEdges":edges,"allowedCrossRoomEdges":allowed_edges,"selectedSwimProfile":actor.swim_clearance[gear],"wetGeometry":str(actor.geometry[wet])})
			print("VELD GRAPH q",q," ",gear," crossEdges=",edges.size()," baseAllowed=",allowed_edges)
			print("VELD EXIT PROBE q",q," ",gear," clear=",clear_points," routes=",route_points," minimumSeconds=",minimum_route," ports=",game.get_room_doors(game.occupied[wet]))
			check(start!=null,"Real exit point q%d %s"%[q,gear])
			if start==null:continue
			actor.foot=start
			Flood.step_crew(game,actor,"veld",.02)
			check(actor.animation_state()=="swim-distress" and actor.air_was_low,"Real low-air presentation before retreat")
			game.visual_time_seconds+=.05
			var entry_frames:Array=player.frames["swim-distress-"+actor.direction] if gear=="bare" else player.equipment_frames["diving-helmet"]["swim-distress-"+actor.direction]
			check(grid._get_veld_frame(game)==entry_frames[0],"Actual physical-route distress entry pixels")
			var case_textures:Array=[entry_frames[0]];var captured_keys:Dictionary={"swim-distress-"+actor.direction+"/0":true}
			check(Safety.advance(game,actor,.01) and actor.goal=="flood-retreat" and not actor.path.is_empty(),"Actual safety chooses physical route")
			var initial_air:float=actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen;var starting_foot:Vector2=actor.foot;var slots:={0:true};var crossed:=false;var last_air:=initial_air;var minimum_air:=initial_air;var recovered:=false;var ticks:=0;var trace:=[]
			for tick in 200:
				# Acknowledge the real warning pause as Continue; do not disable air drain.
				game.paused=false;game.crew_comms.panel.hide();game.visual_time_seconds+=.05;game._update_test_walker(.05);ticks=tick+1
				var texture:Texture2D=grid._get_veld_frame(game)
				check(texture!=null and not actor.dead,"Live route renders without death")
				if actor.animation_state()=="swim-distress":
					var row:Array=player.frames["swim-distress-"+actor.direction] if gear=="bare" else player.equipment_frames["diving-helmet"]["swim-distress-"+actor.direction]
					var slot:int=row.find(texture);check(slot>=0,"Actual route selects candidate distress pixels");slots[slot]=true
					var sample_key:String="swim-distress-"+actor.direction+"/"+str(slot)
					if not captured_keys.has(sample_key) and case_textures.size()<7:case_textures.append(texture);captured_keys[sample_key]=true
				last_air=actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen
				minimum_air=minf(minimum_air,last_air);recovered=recovered or actor.air_recovery>0
				trace.append({"tick":tick,"foot":[actor.foot.x,actor.foot.y],"medium":actor.movement_medium,"pose":actor.animation_state(),"air":last_air,"water":game.occupied.get(actor.cell_at(actor.foot),{}).get("water_level",0),"goal":actor.goal,"pathPoints":actor.path.size(),"recovery":actor.air_recovery})
				if actor.cell_at(actor.foot)!=wet and actor.movement_medium=="dry":crossed=true;break
			check(crossed and not actor.dead and actor.foot.distance_to(starting_foot)>20,"Physical doorway crossing before exhaustion")
			check(not slots.is_empty() and minimum_air<initial_air-.05,"Distress advances while real oxygen is consumed")
			check(recovered and not actor.air_was_low and actor.animation_state()!="swim-distress","Real safe-air crossing starts recovery/exits wet pose")
			review_rows.append({"rotation":q,"gear":gear,"textures":case_textures,"sampleKeys":captured_keys.keys()})
			cases.append({"rotation":q,"gear":gear,"start":[starting_foot.x,starting_foot.y],"finish":[actor.foot.x,actor.foot.y],"ticks":ticks,"distressSlots":slots.keys(),"initialAir":initial_air,"remainingAir":last_air,"minimumAir":minimum_air,"recovery":actor.air_recovery,"safeRecoveryObserved":recovered,"trace":trace,"crossedDryAlive":crossed and not actor.dead})
	check(cases.size()==8,"Four physical route rotations in both gear states")
	var view:=SubViewport.new();view.size=Vector2i(994,8*165);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
	var bg:=ColorRect.new();bg.size=Vector2(view.size);bg.color=Color("202a30");view.add_child(bg)
	for row_index in review_rows.size():
		var row:Dictionary=review_rows[row_index]
		var label:=Label.new();label.text="q%d %s actual route samples"%[row.rotation,row.gear];label.position=Vector2(5,row_index*165);view.add_child(label)
		for i in row.textures.size():
			var sprite:=Sprite2D.new();sprite.texture=row.textures[i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2(i*142,row_index*165+20);view.add_child(sprite)
	await RenderingServer.frame_post_draw
	check(view.get_texture().get_image().save_png("res://output/veld-distress-escape-v1/native-contact.png")==OK,"Actual escape sample contact")
	var report:=FileAccess.open(REPORT,FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"geometryDiagnostics":diagnostics,"reviewSamples":review_rows.map(func(r):return {"rotation":r.rotation,"gear":r.gear,"sampleKeys":r.sampleKeys}),"scope":"Actual main crew/FloodSafety ticks,room flow/oxygen and physical escape to dry air; candidate injection. Warning pauses acknowledged. No crowd/exterior/locker completion or selected-loader proof."},"\t"));report.close()
	for child in root.get_children():child.process_mode=Node.PROCESS_MODE_DISABLED
	preload("res://scripts/audio_shutdown.gd").stop_audio(root);await create_timer(.2,true,false,true).timeout;game.free()
	print("VELD DISTRESS ESCAPE: %d checks,%d failures; %d routes"%[checks,failures,cases.size()]);quit(1 if failures else 0)
