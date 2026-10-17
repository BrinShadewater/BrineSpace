extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-west-water-death-material-v2/"
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
	var file: String=OUT+"restore-captures/"+label+".png"
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
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	root.size=Vector2i(1600,900)
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	var stem:String="user://james-death-restore-"+str(OS.get_process_id())
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game.Architects.advance_core(game,10)
	var hab:=Vector2i(20,22);game.wrecks.erase(hab)
	game._place_room("corridor",Vector2i(20,21),true);game._place_room("maintenance_bay",hab,true);game.powered_room_cells[hab]=true
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1);game.resources.oxygen=100;game.resources.food=100
	game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9);await process_frame
	DirAccess.make_dir_recursive_absolute(OUT+"restore-captures")
	var evidence:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance-evidence.json"))
	var save=preload("res://scripts/run_save.gd")
	for mode in ["bare","helmet"]:
		var gear:String="" if mode=="bare" else "diving-helmet"
		for d in ["west"]:
			for medium in ["flooded"]:
				var npc=game.branforth_npc;npc.dead=false;npc.active=true;npc.state="idle";npc.stage="";npc.goal="";npc.direction=d;npc.helmet_equipped=mode=="helmet";npc.movement_medium=medium;npc.path.clear();npc.expedition.clear();npc.air_recovery=0;npc.air_was_low=false;npc.rebuild(game)
				var action:String="death-ground" if medium=="dry" else "death-water";var key:String=action+"-"+d
				for room in game.placed_rooms:room.water_level=0.0 if medium=="dry" else .95
				var point:=Vector2.INF
				for node in npc.room_nodes.get(hab,[]):
					var at:Vector2=npc.graph.get_point_position(node)
					if npc.swim_segment_clear(at,at,d,d,false,evidence.bounds[mode][key]):point=at;break
				check(point.is_finite(),"Restored death fixture clear node "+mode+key)
				if not point.is_finite():continue
				npc.foot=point;npc.die()
				var player=game.grid_view.branforth_player;var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear];var timing:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
				player.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0;game.visual_time_seconds=100.0
				game.grid_view._get_branforth_frame(game)
				var middle:=0.0
				for i in range(3):middle+=float(timing[key].durations[i])/1000.0
				middle+=float(timing[key].durations[3])/2000.0
				for sample in [middle,player.cycle_seconds(key,gear)+30.0]:
					game.visual_time_seconds=100.0+sample
					var expected_index:int=3 if sample==middle else 5
					var texture:Texture2D=game.grid_view._get_branforth_frame(game);var pixels:=texture.get_image().get_data()
					check(texture==frames[key][expected_index],"Selected pre-save phase "+mode+key+str(expected_index))
					var clock:float=game.visual_time_seconds;var playback:Dictionary=player.snapshot()
					var reason:String=save.problem(save.capture(game));check(reason.is_empty(),"Valid actual checkpoint: "+reason)
					if not reason.is_empty():quit(1);return
					check(save.write(game,game.run_save_path)==OK,"Death checkpoint writes "+mode+key)
					var checkpoint:Dictionary=save.read(game.run_save_path);check(not checkpoint.is_empty(),"Death checkpoint reads "+mode+key)
					if checkpoint.is_empty():quit(1);return
					check(await save.restore_staged(game,checkpoint),"Death checkpoint restores "+mode+key+save.last_error)
					game.run_save_path=stem+".loop";game.tick_timer.stop();game.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player
					check(npc.dead and npc.animation_state()==action and npc.direction==d,"Restore preserves death identity/facing "+mode+key)
					check(game.paused and game.visual_time_seconds==clock,"Restore paused visual clock "+mode+key)
					check(player.snapshot()==playback,"Restore exact independent sprite phase "+mode+key)
					check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Restore exact pose pixels "+mode+key)
					game._process(.5)
					check(game.visual_time_seconds==clock and game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Pause does not restart/advance dead pose "+mode+key)
					if expected_index==5:
						game.visual_time_seconds+=10.0
						check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Resumed corpse remains terminal "+mode+key)
						var target:Vector2=npc.foot/384.0/float(game.GRID_SIZE)
						game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9,true,target)
						await process_frame
						for attempt in range(30):
							if game._grid_view_center_ratio().distance_to(target)<.004:break
							await process_frame
						check(game._grid_view_center_ratio().distance_to(target)<.004,"Restored camera visibly centers corpse "+mode+key)
						await capture(mode+"-"+action.trim_prefix("death-")+"-"+d+"-terminal",npc)
					results.append({"mode":mode,"key":key,"index":expected_index,"actualDiskRestore":true})
	var file:=FileAccess.open(OUT+"restore-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"4 actual scratch RunSave writes/reads/staged restores,mid-collapse and terminal,2 selected West-water gear cases; exact pixels/clock/phase/pause/resumed terminal and2 native terminal captures. Does not prove actual oxygen journey or legacy saves lacking playback."},"  "));file.close()
	print("JAMES WEST WATER DEATH DISK RESTORE: ",checks," checks; ",failures," failures;4 actual checkpoint phases")
	if not FileAccess.file_exists(get_script().resource_path+".uid"):
		var uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	quit(1 if failures else 0)
