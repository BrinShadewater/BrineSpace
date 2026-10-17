extends SceneTree
const OUT := "res://character/james-console-water-turn-v1/"
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
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
	var file: String=OUT+"arrival-captures/"+label+".png"
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
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-workstation-routes.meta";game.run_save_path="user://james-workstation-routes.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	var legacy=preload("res://scripts/crew_sprite_player.gd").new()
	legacy.load_manifest("res://character/james-water-turn-family-v1/bare-manifest.json")
	legacy.load_equipment_manifest("diving-helmet","res://character/james-water-turn-family-v1/helmet-manifest.json")
	var old_extents:Dictionary={"bare":legacy.clip_extent("swim-turn-east-north"),"helmet":legacy.clip_extent("swim-turn-east-north","diving-helmet")}
	player.load_manifest(OUT+"bare-manifest.json",true,false);player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json")
	for q in range(4):
		game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
		for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("life_support" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=.95
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.movement_medium="flooded";npc.stage="";npc.path.clear();npc.expedition.clear();npc.goal="maintenance";npc.goal_cell=cell;npc.state="interact";npc.timer=6
		var stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(stations.size()==1,"Console fixture")
		if stations.is_empty():continue
		for pair in ["east-north","north-east"]:
			var source_direction:String=pair.get_slice("-",0);var destination_direction:String=pair.get_slice("-",1)
			for mode in ["bare","helmet"]:
				npc.helmet_equipped=mode=="helmet";var gear:String="" if mode=="bare" else "diving-helmet";var key:String="swim-turn-"+pair
				npc.foot=center+stations[0].point+Vector2(0,6);npc.direction=destination_direction
				var extent:Array=player.clip_extent(key,gear)
				check(npc.swim_segment_clear(npc.foot,npc.foot,destination_direction,source_direction,false,extent),"Whole staged clip plus unchanged incoming/master body fits fine contact")
				check(not npc.swim_segment_clear(npc.foot,npc.foot,destination_direction,source_direction,false,old_extents[mode]),"Previous turn rejected at fine contact")
				check(not npc.swim_segment_clear(center+stations[0].point,center+stations[0].point,destination_direction,source_direction,false,extent),"Original raw contact still rejected")
				player.motion.clear();player.current_key="";player.last_time=-1;player.current_equipment=gear;game.visual_time_seconds=100
				npc.direction=source_direction;var incoming:Texture2D=game.grid_view._get_branforth_frame(game);check(incoming!=null and npc.animation_state()=="swim","Normal incoming master swim")
				npc.direction=destination_direction;var elapsed:=.001;var captures:Array=[]
				for slot in range(6):
					game.visual_time_seconds=100+elapsed+(.001 if slot>0 else 0)
					var texture:Texture2D=game.grid_view._get_branforth_frame(game)
					# First call starts the transition at100.001, subsequent samples account for it.
					var phase:float=0 if slot==0 else elapsed
					var expected:Texture2D=player.frame_at_elapsed(key,phase,gear)
					check(player.motion.get("clip","")==key,"Normal grid uses staged compact turn")
					check(texture.get_image().get_data()==expected.get_image().get_data(),"Selected authored quarter slot")
					var used:Rect2=texture.get_meta("crew_alpha_extent");var slot_extent:Array=[used.position.x,used.position.y,used.end.x,used.end.y]
					check(npc.swim_segment_clear(npc.foot,npc.foot,destination_direction,source_direction,false,slot_extent),"Every native pose fits actual geometry")
					var frozen:Texture2D=game.grid_view._get_branforth_frame(game);check(frozen.get_image().get_data()==texture.get_image().get_data(),"Paused turn holds exact pixels")
					if q==0:captures.append(await capture(pair+"-"+mode+"-"+str(slot).pad_zeros(3),npc))
					elapsed+=float(player.timing[key].durations[slot])/1000
				game.visual_time_seconds=100.001+player.cycle_seconds(key,gear)+.001
				var final:Texture2D=game.grid_view._get_branforth_frame(game)
				check(player.motion.get("clip","")=="" and final.get_image().get_data()==player.frames["swim-"+destination_direction][0].get_image().get_data() if gear.is_empty() else player.motion.get("clip","")=="" and final.get_image().get_data()==player.equipment_frames[gear]["swim-"+destination_direction][0].get_image().get_data(),"Finite turn joins selected north swim master")
				results.append({"rotation":q,"mode":mode,"pair":pair,"point":str(npc.foot-center),"slots":6,"captures":captures})
	var file:=FileAccess.open(OUT+"native-staged-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Staged exact compact quarter through normal grid at fine six-unit-backed console contacts, four rotations and two gear modes; complete selected body/clip geometry, paused pixels and finite endpoint. Candidate manifest appended into scratch player; normal installed selected-clip gate, no clearance injection. Legacy counterfactual reads immutable legacy manifests explicitly. Incoming swim seeded at contact; whole journeys, save and installation have separate evidence; not owner acceptance."},"  "));file.close()
	print("JAMES CONSOLE COMPACT TURN: ",checks," checks; ",failures," failures; ",results.size()," staged contact cases")
	quit(1 if failures else 0)
