extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-air-family-v1/"
const ORIGIN := Vector2i(20,20)
var game
var failures:=0
var checks:=0
var results: Array=[]
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func endpoint(npc,desired: Vector2,cell: Vector2i,d: String) -> int:
	var best: int=-1;var distance: float=INF
	for node in npc.room_nodes.get(cell,[]):
		var at: Vector2=npc.graph.get_point_position(node)
		if not npc.swim_segment_clear(at,at,d,d,true):continue
		if not npc.swim_segment_clear(at,at,d,d,false,npc.action_clearance["helmet" if npc.helmet_equipped else "bare"]["transition-"+d]):continue
		if at.distance_squared_to(desired)<distance:best=node;distance=at.distance_squared_to(desired)
	return best
func capture(label: String,npc) -> String:
	var center: Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var screenshot:=root.get_texture().get_image()
	var cell_size: float=game.get_cell_size()
	var world: Rect2=Rect2(npc.foot/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var file: String=OUT+"installed-behaviour-captures/"+label+".png"
	check(crop.get_width()>0 and crop.get_height()>0,"Visible route capture "+label)
	check(crop.save_png(file)==OK,"Save route capture")
	if label.ends_with("-000"):
		var texture: Texture2D=game.grid_view._get_branforth_frame(game)
		var used: Rect2i=texture.get_image().get_used_rect();var sc: float=cell_size*.17/float(texture.get_meta("crew_standing_height"));var pivot: Vector2=texture.get_meta("crew_pivot")
		var actor_world:=Rect2(center+(Vector2(used.position)-pivot)*sc,Vector2(used.size)*sc).grow(3)
		var actor_screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*actor_world
		var roi:=Rect2i(actor_screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size())))
		var before: PackedByteArray=screenshot.get_region(roi).get_data()
		npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var after: PackedByteArray=root.get_texture().get_image().get_region(roi).get_data();var differences:=0
		for i in range(mini(before.size(),after.size())):
			if absi(int(before[i])-int(after[i]))>=5:differences+=1
		check(differences>25,"Actor on/off render difference "+label)
		npc.active=true;game.grid_view.queue_redraw();await process_frame
	return file
func run() -> void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch user directory")
	if failures:quit(2);return
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-air-behaviour.meta";game.run_save_path="user://james-air-behaviour.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
	for delta in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room: Dictionary=game.RoomDatabaseScript.get_room("maintenance_bay" if delta==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=ORIGIN+delta;room.rotation=0;room.water_level=.95
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1) # Disable the idle fallback demonstrator too.
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":ORIGIN}])
	var npc=game.branforth_npc;npc.rebuild(game);npc.active=true;npc.dead=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF

	var clearance:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance.json"))
	var evidence:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance-evidence.json"))
	preload("res://scripts/crew_life.gd").clearance.clear()
	preload("res://scripts/crew_life.gd").clear(npc,"swim-distress")
	check(preload("res://scripts/crew_life.gd").clearance["branforth"]==clearance.life,"Actual lazy selected life clearance")
	var player=game.grid_view.branforth_player
	game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
	await process_frame;game._center_grid_on_station_now();await process_frame
	DirAccess.make_dir_recursive_absolute(OUT+"installed-behaviour-captures")
	game.resources.oxygen=100;game.resources.food=100
	var flood=preload("res://scripts/room_flooding.gd")
	for mode in ["bare","helmet"]:
		var gear:String="" if mode=="bare" else "diving-helmet"
		var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		for d in ["east","south","west","north"]:
			npc.helmet_equipped=mode=="helmet";npc.dead=false;npc.state="idle";npc.stage="";npc.direction=d;npc.expedition.clear();npc.path.clear();npc.air_recovery=0;npc.air_was_low=false;npc.tank_oxygen=10;npc.breath_oxygen=4;npc.starvation=0;npc.movement_medium="flooded"
			var point:=Vector2.INF
			for node in npc.graph.get_point_ids():
				var at:Vector2=npc.graph.get_point_position(node)
				if not game.occupied.has(npc.cell_at(at)):continue
				if not npc.swim_segment_clear(at,at,d,d,false,clearance.life[mode]["swim-distress-"+d]):continue
				if not npc.swim_segment_clear(at,at,d,d,false,evidence.bounds[mode]["recover-air-"+d]):continue
				point=at;break
			check(point.is_finite(),"Both action envelopes clear at actual room node "+mode+d)
			if not point.is_finite():continue
			npc.foot=point
			for room in game.placed_rooms:room.water_level=.95
			flood.step_crew(game,npc,"branforth",.01)
			check(npc.air_was_low and npc.movement_medium=="flooded" and not npc.dead,"Actual unsafe-air low flag "+mode+d)
			check(npc.animation_state()=="swim-distress" and npc.action_elapsed()<0,"Actual low-air distress chooser "+mode+d)
			player.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0;game.visual_time_seconds=100.0
			game.grid_view._get_branforth_frame(game)
			for i in range(6):
				game.visual_time_seconds=100.0+i*.16+.08
				var texture:Texture2D=game.grid_view._get_branforth_frame(game)
				check(texture==frames["swim-distress-"+d][i],"Normal grid distress slot "+mode+d+str(i))
				check(game.grid_view._get_branforth_frame(game)==texture,"Paused distress cosmetic clock "+mode+d+str(i))
				await capture(mode+"-distress-"+d+"-"+str(i).pad_zeros(3),npc)
			for room in game.placed_rooms:room.water_level=0.0
			flood.step_crew(game,npc,"branforth",.01)
			check(npc.air_recovery==3.0 and not npc.air_was_low and npc.movement_medium=="dry","Safe air starts actual3sec recovery "+mode+d)
			check(npc.animation_state()=="recover-air" and npc.action_elapsed()==0.0,"Recovery simulation sampler "+mode+d)
			for i in range(6):
				var sample:float=i*.5+.25
				flood.step_crew(game,npc,"branforth",sample-(3.0-npc.air_recovery))
				var texture:Texture2D=game.grid_view._get_branforth_frame(game)
				check(texture==frames["recover-air-"+d][i],"Actual simulation recovery slot "+mode+d+str(i))
				var remaining:float=npc.air_recovery;game.visual_time_seconds+=1.0
				check(game.grid_view._get_branforth_frame(game)==texture and npc.air_recovery==remaining,"Cosmetic time cannot advance recovery "+mode+d+str(i))
				await capture(mode+"-recovery-"+d+"-"+str(i).pad_zeros(3),npc)
			flood.step_crew(game,npc,"branforth",npc.air_recovery+.000001)
			check(npc.air_recovery==0.0 and npc.animation_state()=="idle","Actual recovery completion returns idle "+mode+d)
			var idle_texture:Texture2D=game.grid_view._get_branforth_frame(game)
			var idle_image:=Image.create(256,360,false,Image.FORMAT_RGBA8)
			var idle_pivot:Vector2=idle_texture.get_meta("crew_pivot")
			idle_image.blit_rect(idle_texture.get_image(),Rect2i(Vector2i.ZERO,idle_texture.get_size()),Vector2i(Vector2(128,224)-idle_pivot))
			check(idle_image.get_data()==frames["recover-air-"+d].back().get_image().get_data(),"Actual idle handoff preserves world-registered pixels "+mode+d)
			var before:Dictionary=npc.snapshot()
			npc.direction=d;npc.air_recovery=1.5;npc.state="walk"
			check(npc.animation_state()!="recover-air" and npc.action_elapsed()<0,"Movement interrupts idle-only recovery art "+mode+d)
			npc.state="idle";npc.air_recovery=0.0
			results.append({"mode":mode,"direction":d,"distressSlots":6,"recoverySlots":6,"actualLowAir":true,"actualRecovery":true,"point":str(point)})
	var file:=FileAccess.open(OUT+"installed-behaviour-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Controlled actual RoomFlooding.step_crew low-air and safe-room recovery at eight collision-checked room nodes, both modes/four directions, normal grid actual installed manifests and lazy life clearance; pause/completion/idle-only interruption. Room water changed by fixture, not actual dewatering or travel proof."},"  "));file.close()
	print("JAMES AIR INSTALLED BEHAVIOUR: ",checks," checks; ",failures," failures; controlled low-air/safe-room fixture")
	quit(1 if failures else 0)
