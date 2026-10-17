extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/water-journey-review-v345/"
const ORIGIN=Vector2i(20,20)
const Player=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/reorient_player.gd")
var game
var checks:=0
var failures:=0
var captures:Array=[]
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func same(a:Texture2D,b:Texture2D)->bool:
	if a==null or b==null:return false
	var aa:Texture2D=a.diffuse_texture if a is CanvasTexture else a
	var bb:Texture2D=b.diffuse_texture if b is CanvasTexture else b
	return aa.get_image().get_data()==bb.get_image().get_data()
func _init()->void:call_deferred("run")
func capture(label:String,npc)->void:
	game.hand_panel.hide();game.card_drag.hide()
	var center:Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var screenshot:Image=root.get_texture().get_image()
	var world:=Rect2(center-Vector2.ONE*game.get_cell_size()*.4,Vector2.ONE*game.get_cell_size()*.8)
	var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:Image=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	check(crop.get_width()>0 and crop.get_height()>0,"Visible native crop")
	check(crop.save_png(OUT+label+".png")==OK,"Save native pose crop")
	captures.append({"file":label+".png","time":game.visual_time_seconds,"motion":game.grid_view.branforth_player.motion.duplicate(true),"foot":[npc.foot.x,npc.foot.y]})
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Isolated APPDATA")
	if failures:quit(2);return
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://james-water345.meta";game.run_save_path="user://james-water345.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	game.running=true;game.Architects.advance_core(game,10)
	game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
	for delta in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room:Dictionary=game.RoomDatabaseScript.get_room("salvage_workshop" if delta==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=ORIGIN+delta;room.rotation=0;room.water_level=.95
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	install_player()
	var player=game.grid_view.branforth_player
	var npc=game.branforth_npc;npc.rebuild(game);npc.active=true;npc.dead=false;npc.state="idle";npc.stage="";npc.goal="";npc.path.clear();npc.expedition.clear();npc.movement_medium="flooded"
	var union:=Rect2();var first:=true
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		for key in bank:
			if not str(key).begins_with("swim-reorient-"):continue
			var extent:Array=player.clip_extent(key,gear);var rect:=Rect2(Vector2(extent[0],extent[1]),Vector2(extent[2]-extent[0],extent[3]-extent[1]))
			union=rect if first else union.merge(rect);first=false
	var foot:=Vector2.INF
	for node in npc.room_nodes.get(ORIGIN,[]):
		var at:Vector2=npc.graph.get_point_position(node)
		if npc.can_stand(at) and npc.swim_segment_clear(at,at+Vector2(0,-24),"north","west",false,[union.position.x,union.position.y,union.end.x,union.end.y]):foot=at;break
	check(foot.is_finite(),"Authored workshop contains collision-clear complete reorientation envelope")
	if not foot.is_finite():quit(2);return
	npc.foot=foot
	for gear in ["","diving-helmet"]:
		var mode:String="bare" if gear.is_empty() else "helmet"
		npc=game.branforth_npc;npc.foot=foot;npc.helmet_equipped=not gear.is_empty();npc.movement_medium="flooded"
		npc.direction="west";npc.state="idle";npc.stage="";npc.goal="";npc.path.clear();npc.expedition.clear()
		player=game.grid_view.branforth_player;game.visual_time_seconds=100.65;game.paused=true
		player.restore_snapshot({"key":"swim-west","equipment":gear,"phase":0.0,"last_time":99.9,"started":99.0,"last_position":foot/384.0,"motion":{"state":"tread","direction":"west","clip":"swim-stop-phase-2-west","started":100.0}})
		var before:Texture2D=game.grid_view._get_branforth_frame_source(game)
		npc.direction="north";npc.state="walk"
		var entry:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(same(before,entry),"Restart preserves moving route entry")
		var key:String=player.motion.clip
		check(key.begins_with("swim-reorient-"),"Moving route starts authored bridge")
		if not key.begins_with("swim-reorient-"):quit(2);return
		var destination:Vector2=foot+Vector2(0,-24)
		var extent:Array=player.clip_extent(key,gear)
		check(npc.swim_segment_clear(foot,destination,"north","west",false,extent),"Complete prescribed segment fits full active bridge envelope")
		if failures:quit(2);return
		npc.path=PackedVector2Array([destination]);npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		await capture(mode+"-entry",npc)
		var resumed:=false;var ticks:=0;var travelled:=0.0
		while ticks<160:
			var previous:Vector2=npc.foot
			if not npc.path.is_empty():npc.move(.01)
			game.visual_time_seconds+=.01;ticks+=1
			travelled+=npc.foot.distance_to(previous)
			var tex:Texture2D=game.grid_view._get_branforth_frame_source(game)
			if not resumed and ticks==15:
				await capture(mode+"-before-resume",npc)
				var actor_before:Dictionary=npc.snapshot();var playback_before:Dictionary=player.snapshot();var pixels:PackedByteArray=tex.get_image().get_data();var visual:float=game.visual_time_seconds
				var save=preload("res://scripts/run_save.gd");var path:String="user://water345-"+mode+".loop"
				var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
				check(problem.is_empty(),"Full swimming checkpoint admitted: "+problem)
				if not problem.is_empty():quit(2);return
				check(save.write(game,path)==OK,"Actual disk checkpoint write");data=save.read(path)
				root.remove_child(game);game.queue_free();await process_frame
				game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://water345.meta";game.run_save_path=path
				root.add_child(game);current_scene=game
				while not game.startup_complete:await process_frame
				game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
				install_player()
				check(await save.restore_staged(game,data),"Fresh scene restores disk checkpoint with staged bank installed first")
				game.run_save_path=path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
				npc=game.branforth_npc;player=game.grid_view.branforth_player
				check(npc.snapshot()==actor_before,"Full swimming actor exact after disk restore")
				check(player.snapshot()==playback_before,"Swimming playback exact after disk restore")
				check(game.paused and game.visual_time_seconds==visual,"Pause/clock preserved")
				check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Exact swimming pixels after fresh scene restore")
				game._process(.5);check(npc.snapshot()==actor_before and game.visual_time_seconds==visual,"Paused restored swimmer does not advance")
				await capture(mode+"-after-resume",npc);resumed=true
			if ticks==45:await capture(mode+"-moving",npc)
		check(resumed,"Whole-run fresh scene checkpoint exercised")
		check(travelled>23.9 and npc.foot.distance_to(destination)<.01,"Actual movement reaches prescribed flooded route endpoint")
		check(not str(player.motion.get("clip","")).begins_with("swim-reorient-"),"Finite bridge releases after movement and disk resume")
		await capture(mode+"-complete",npc)
	FileAccess.open(OUT+"journey-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"Two prescribed 24-unit actual move() flooded routes; full bridge segment clearance; two fresh main-scene whole-run disk restores with staged bank installed before restoration. Not autonomous update()/goal dispatch, normal selection, exterior, blocked fallback or title UI Continue."},"\t"))
	print("JAMES WATER JOURNEY checks=",checks," failures=",failures," captures=",captures.size());game.queue_free();await process_frame;quit(0 if failures==0 else 1)
func install_player()->void:
	var old=game.grid_view;var normal=old.branforth_player;var parent=old.get_parent();var index:int=old.get_index()
	var player=Player.new()
	for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides"]:player.set(field,normal.get(field).duplicate(true))
	player.install_bridges()
	var grid=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/staged_grid.gd").new()
	grid.name="GridView";grid.custom_minimum_size=old.custom_minimum_size
	parent.remove_child(old);parent.add_child(grid);parent.move_child(grid,index);game.grid_view=grid;old.queue_free()
	grid.branforth_player=player;grid.fixture_visual_time=-1
