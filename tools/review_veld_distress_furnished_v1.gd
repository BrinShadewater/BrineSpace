extends SceneTree
## Real authored flooded furniture geometry and disk restore; explicit candidate art.
const Life=preload("res://scripts/crew_life.gd")
const Flood=preload("res://scripts/room_flooding.gd")
const Save=preload("res://scripts/run_save.gd")
const PACKS={"bare":"res://character/veld-swim-distress-family-coherent-v1/bare-manifest.json","helmet":"res://character/veld-swim-distress-family-coherent-v1/helmet-manifest.json"}
const REPORT="res://output/veld-distress-furnished-v1/furnished-checks.json"
const CAPTURES={"east-bare":"res://output/veld-distress-furnished-v1/east-bare.png","west-bare":"res://output/veld-distress-furnished-v1/west-bare.png","north-bare":"res://output/veld-distress-furnished-v1/north-bare.png","south-bare":"res://output/veld-distress-furnished-v1/south-bare.png","east-helmet":"res://output/veld-distress-furnished-v1/east-helmet.png","west-helmet":"res://output/veld-distress-furnished-v1/west-helmet.png","north-helmet":"res://output/veld-distress-furnished-v1/north-helmet.png","south-helmet":"res://output/veld-distress-furnished-v1/south-helmet.png"}
var checks:=0
var failures:=0
var restores:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(1);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://veld-distress-furnished.meta";game.run_save_path="user://veld-distress-furnished.loop";game.Preferences.save_path="user://veld-distress-furnished.cfg"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	var grid=game.grid_view;var player=grid.veld_player
	player.load_manifest(PACKS.bare,true);check(player.load_equipment_manifest("diving-helmet",PACKS.helmet),"Candidate equipment")
	game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
	var origin:=Vector2i(20,20)
	for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room:Dictionary=game.RoomDatabaseScript.get_room("maintenance_bay" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=origin+offset;room.rotation=0;room.water_level=1;game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	for peer in [game.bill_npc,game.branforth_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1);game.bill_npc.expedition.clear()
	root.mode=Window.MODE_WINDOWED;root.size=Vector2i(1600,900);game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.65)
	var rows:=[]
	for rotation in 4:
		for room in game.placed_rooms:room.rotation=rotation
		var actor=game.veld_npc;await actor.rebuild(game)
		check(not actor.geometry.is_empty() and actor.graph.get_point_count()>0,"Actual authored room geometry")
		for direction in ["east","west","north","south"]:
			for gear in ["bare","helmet"]:
				actor=game.veld_npc;actor.dead=false;actor.active=true;actor.direction=direction;actor.helmet_equipped=gear=="helmet";actor.state="idle";actor.stage="";actor.goal="";actor.path.clear();actor.expedition.clear();actor.locker_request.clear();actor.moonbay_assignment.clear();actor.set_movement_medium("flooded");actor.tank_oxygen=11;actor.breath_oxygen=4
				var found:Variant=null;var accepted:=0;var rejected:=0;var blocked_example:Variant=null
				for id in actor.graph.get_point_ids():
					actor.foot=actor.graph.get_point_position(id)
					if Life.clear(actor,"swim-distress"):
						accepted+=1
						if found==null and actor.cell_at(actor.foot)==origin:found=actor.foot
					else:rejected+=1;blocked_example=actor.foot
				check(found!=null,"Furnished clear point q%d %s %s"%[rotation,direction,gear])
				if found==null:continue
				if blocked_example!=null:
					actor.foot=blocked_example
					check(actor.animation_state()!="swim-distress","Real furniture excludes unsafe distress")
				actor.foot=found;actor.air_was_low=false;actor.air_recovery=0;actor.tank_oxygen=12.01;actor.breath_oxygen=5.01
				game.resources.oxygen=100;game.resources.food=100
				grid._get_veld_frame(game);Flood.step_crew(game,actor,"veld",.02);Flood.step_crew(game,actor,"veld",.02)
				check(actor.animation_state()=="swim-distress" and actor.air_was_low and actor.movement_medium=="flooded","Actual flooded threshold/history")
				var key:String="swim-distress-"+direction
				var frames:Array=player.frames[key] if gear=="bare" else player.equipment_frames["diving-helmet"][key]
				var entry:float=game.visual_time_seconds
				check(grid._get_veld_frame(game)==frames[0],"Furnished distress entry zero")
				for slot in 6:
					game.visual_time_seconds=entry+slot*.16+.001
					check(grid._get_veld_frame(game)==frames[slot] and Life.clear(actor,"swim-distress"),"Furnished actual renderer slot")
					if slot in [1,3,5]:
						var expected:PackedByteArray=grid._get_veld_frame(game).get_image().get_data()
						var clock:float=game.visual_time_seconds;var oxygen:float=actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen
						check(Save.write(game,game.run_save_path)==OK,"Current wet disk write: "+Save.last_error)
						var disk:Dictionary=Save.read(game.run_save_path)
						check(not disk.is_empty() and not disk.get("_recovered_backup",false),"Current wet disk read")
						if disk.is_empty():continue
						check(await Save.restore(game,disk),"Actual wet disk restoration: "+Save.last_error)
						game.set_process(false);game.tick_timer.stop();game.run_save_path="user://veld-distress-furnished.loop";actor=game.veld_npc
						check(actor.direction==direction and actor.helmet_equipped==(gear=="helmet") and actor.movement_medium=="flooded" and actor.air_was_low,"Restored wet identity/history")
						check(is_equal_approx(game.visual_time_seconds,clock) and is_equal_approx(actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen,oxygen),"Restored visual clock/oxygen")
						check(actor.foot.is_equal_approx(found) and actor.animation_state()=="swim-distress","Restored actual furnished gate")
						check(grid._get_veld_frame(game).get_image().get_data()==expected,"Exact candidate pixels after disk restore")
						restores+=1
					if rotation==0 and slot==3:
						game._refresh_all();await process_frame;game._center_grid_on_station_now();await process_frame;grid.queue_redraw();await RenderingServer.frame_post_draw
						var image:=root.get_texture().get_image();var size:float=game.get_cell_size();var rect:=Rect2(Vector2(origin)*size,Vector2.ONE*size)
						var screen:Rect2=root.get_stretch_transform()*grid.get_global_transform_with_canvas()*rect
						check(image.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,image.get_size())))).save_png(CAPTURES[direction+"-"+gear])==OK,"Fresh furnished distress capture")
				rows.append({"rotation":rotation,"direction":direction,"gear":gear,"foot":[found.x,found.y],"acceptedGraphNodes":accepted,"rejectedGraphNodes":rejected,"frames":6,"diskRestores":3})
	check(rows.size()==32 and restores==96,"All rotations/directions/gears and96 disk restores")
	var report:=FileAccess.open(REPORT,FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":rows,"diskRestores":restores,"scope":"Five actual authored flooded rooms/four rotations,original clearance,candidate explicitly loaded; graph gate scan and48poses at32clear points,96disk restores. No actual escape journey,crowd certification,normal selection or continuous motion acceptance."},"\t"));report.close()
	for child in root.get_children():child.process_mode=Node.PROCESS_MODE_DISABLED
	preload("res://scripts/audio_shutdown.gd").stop_audio(root);await create_timer(.2,true,false,true).timeout;game.free()
	print("VELD DISTRESS FURNISHED: %d checks,%d failures; %d restores"%[checks,failures,restores]);quit(1 if failures else 0)
