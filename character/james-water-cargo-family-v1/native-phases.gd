extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-water-cargo-family-v1/"
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
	var file: String=OUT+"route-captures/"+label+".png"
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
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-water-cargo-phases.meta";game.run_save_path="user://james-water-cargo-phases.loop"
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
			player.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0;game.visual_time_seconds=0.0
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
				game.visual_time_seconds+=.3
				texture=game.grid_view._get_branforth_frame(game)
				check(texture==frames["swim-pickup-"+d][i],"Actual pickup slot "+d+mode+str(i))
				check(site.units==3 and npc.expedition.cargo.is_empty(),"No premature resource commitment "+d+str(i))
				var paused_elapsed:float=npc.expedition.elapsed
				game.visual_time_seconds+=1.0
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
