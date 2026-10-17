extends SceneTree
const OUT := "res://character/james-workstation-arrival-polish-v1/"
var checks:=0
var failures:=0
var results:Array=[]
var service_nodes:Array=[]
var game
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch user directory")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-workstation.meta";game.run_save_path="user://james-workstation.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player
	var samples:Array=[]
	for id in ["life_support","pressure_control","listening_post"]:
		for q in range(4):
			game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
			game.selected_rotation=q;game._place_room(id,cell,true);game.occupied[cell].rotation=q;game.occupied[cell].water_level=.95;game.powered_room_cells[cell]=true
			npc.rebuild(game);npc.active=true;npc.dead=false;npc.movement_medium="flooded";npc.swim_clearance.clear();npc.tread_clearance.clear();npc.action_clearance.clear()
			var stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);var chosen:Dictionary={}
			for station in stations:
				if station.get("mode","") in ["console","interact"] or id in ["pressure_control","listening_post"]:chosen=station;break
			if chosen.is_empty():
				results.append({"room":id,"rotation":q,"stationUnavailable":true});continue
			for mode in ["bare","helmet"]:
				var gear:String="" if mode=="bare" else "diving-helmet"
				npc.helmet_equipped=mode=="helmet";npc.direction=chosen.facing;npc.movement_medium="flooded";npc.state="idle";npc.stage="";npc.path.clear()
				var candidates:Array=[]
				for node in npc.room_nodes.get(cell,[]):
					var at:Vector2=npc.graph.get_point_position(node);var station:Dictionary=npc.RoomActivity.at(npc.geometry[cell],at-center)
					if station.is_empty() or not npc.spawn_clear(at):continue
					npc.foot=at;npc.direction=station.facing
					candidates.append({"point":str(at-center),"facing":station.facing,"stationDistance":(at-center).distance_to(station.point),"stopAllowed":game.grid_view._water_transition_clear(npc),"stationaryState":npc.animation_state()})
				service_nodes.append({"room":id,"rotation":q,"mode":mode,"candidates":candidates})
				for incoming in ["east","south","west","north"]:
					npc.foot=center+chosen.point;npc.helmet_equipped=mode=="helmet";npc.movement_medium="flooded";npc.dead=false;npc.active=true;npc.goal="curiosity";npc.goal_cell=cell;npc.stage="";npc.state="walk";npc.direction=incoming;npc.path=PackedVector2Array([npc.foot+Vector2(1,0)]);npc.expedition.clear()
					player.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0;game.visual_time_seconds=100
					var source_state:String=npc.animation_state();var source:Texture2D=game.grid_view._get_branforth_frame(game);check(source!=null,"Actual incoming grid frame")
					npc.path.clear();npc.arrive()
					var desired:String=npc.direction;var allowed:bool=game.grid_view._water_transition_clear(npc)
					var after:Texture2D=game.grid_view._get_branforth_frame(game);check(after!=null,"Actual station arrival grid frame")
					if source==null or after==null:continue
					check(desired==str(chosen.facing),"Station authored facing selected")
					var shown:String=str(after.get_meta("crew_water_facing",""))
					var changed:bool=incoming!=desired
					results.append({"room":id,"rotation":q,"mode":mode,"incoming":incoming,"sourceState":source_state,"desired":desired,"shown":shown,"changedFacing":changed,"snap":changed and shown==desired,"transitionAllowed":allowed,"selectedClip":player.motion.get("clip",""),"point":str(chosen.point),"state":npc.animation_state(),"stationMode":chosen.get("mode","")})
					if q==0 and changed and samples.size()<12:samples.append({"label":id+" "+mode+" "+incoming+"->"+desired+" allow="+str(allowed),"source":source,"after":after})
	var snap_count:=0;var constrained:=0;var cases:=0
	for item in results:
		if item.get("stationUnavailable",false):continue
		cases+=1
		if item.snap:snap_count+=1
		if item.changedFacing and not item.transitionAllowed:constrained+=1
	if DisplayServer.get_name()!="headless":
		var viewport:=SubViewport.new();viewport.size=Vector2i(800,maxi(1,samples.size())*125);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
		var bg:=ColorRect.new();bg.size=Vector2(viewport.size);bg.color=Color("303b40");viewport.add_child(bg)
		for i in range(samples.size()):
			var title:=Label.new();title.text=samples[i].label;title.position=Vector2(6,i*125);viewport.add_child(title)
			for column in range(2):
				var tex:Texture2D=samples[i].source if column==0 else samples[i].after;var sprite:=Sprite2D.new();sprite.texture=tex;sprite.centered=false;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*82.0/148.0;sprite.position=Vector2(120+column*380,i*125+80)-tex.get_meta("crew_pivot")*82.0/148.0;viewport.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(viewport.get_texture().get_image().save_png(OUT+"native-baseline-contact.png")==OK,"Save actual-selected82px source/arrival pairs")
	var file:=FileAccess.open(OUT+"baseline-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"facingSnaps":snap_count,"constrainedFacingChanges":constrained,"results":results,"resolvedServiceNodes":service_nodes,"scope":"Controlled actual NPC.arrive at authored fixture workstation points in3rooms x4rotations x2gear x4incoming directions; normal grid selection. Incoming swim seeded at endpoint,not a traversed/autonomous route. Actual valid service graph nodes scanned separately; clearance recorded,not changed."},"  "));file.close()
	print("JAMES WORKSTATION BASELINE: ",checks," checks; ",failures," failures; ",cases," cases; ",snap_count," facing snaps; ",constrained," constrained changes")
	quit(1 if failures else 0)
