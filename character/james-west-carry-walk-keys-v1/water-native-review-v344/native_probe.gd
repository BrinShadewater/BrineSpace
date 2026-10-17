extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/water-native-review-v344/"
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
	game.meta.save_path="user://james-water344.meta";game.run_save_path="user://james-water344.loop"
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
	var old=game.grid_view;var normal=old.branforth_player;var parent=old.get_parent();var index:int=old.get_index()
	var player=Player.new()
	for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides"]:player.set(field,normal.get(field).duplicate(true))
	player.install_bridges()
	var grid=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/staged_grid.gd").new()
	grid.name="GridView";grid.custom_minimum_size=old.custom_minimum_size
	parent.remove_child(old);parent.add_child(grid);parent.move_child(grid,index);game.grid_view=grid;old.queue_free()
	grid.branforth_player=player;grid.fixture_visual_time=-1
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
		if npc.can_stand(at) and npc.swim_segment_clear(at,at,"west","west",false,[union.position.x,union.position.y,union.end.x,union.end.y]):foot=at;break
	check(foot.is_finite(),"Authored workshop contains collision-clear complete reorientation envelope")
	if not foot.is_finite():quit(2);return
	npc.foot=foot
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		npc.helmet_equipped=not gear.is_empty()
		for source in ["west","east","north","south"]:
			for target in ["west","east","north","south"]:
				if source==target:continue
				var label:String=("bare" if gear.is_empty() else "helmet")+"-"+source+"-"+target
				var stop:String="swim-stop-phase-2-"+source
				npc.direction=source;npc.state="idle";npc.path.clear();game.visual_time_seconds=100.65
				player.restore_snapshot({"key":"swim-"+source,"equipment":gear,"phase":0.0,"last_time":99.9,"started":99.0,"last_position":foot/384.0,"motion":{"state":"tread","direction":source,"clip":stop,"started":100.0}})
				check(npc.animation_state()=="tread","Actual actor selects tread in clear flooded room")
				var before:Texture2D=grid._get_branforth_frame_source(game)
				var pre_capture:Dictionary=player.snapshot()
				await capture(label+"-stop",npc)
				npc.direction=target;npc.state="walk"
				var diagnostic:Dictionary={"preCapture":pre_capture,"postCapture":player.snapshot(),"actorScript":npc.get_script().resource_path,"actorState":npc.animation_state(),"actorMedium":npc.movement_medium,"stage":npc.stage,"clock":game.visual_time_seconds,"gridPlayer":grid.branforth_player.get_script().resource_path,"predicted":player.preview_water_transition(npc.animation_state(),target,game.visual_time_seconds,gear),"allowed":grid._water_transition_clear(npc)}
				var entry:Texture2D=grid._get_branforth_frame_source(game)
				diagnostic["afterEntry"]=player.snapshot()
				FileAccess.open(OUT+"entry-diagnostic.json",FileAccess.WRITE).store_string(JSON.stringify(diagnostic,"\t"))
				check(same(before,entry),"Actual main-scene renderer preserves changed-heading restart entry")
				var key:String=player.motion.clip;check(key.begins_with("swim-reorient-"),"Actual renderer selects staged reorientation")
				if not key.begins_with("swim-reorient-"):quit(2);return
				var elapsed:=0.0
				for slot in range(bank[key].size()):
					game.visual_time_seconds=100.65+elapsed+float(clocks[key].durations[slot])/2000.0
					check(same(grid._get_branforth_frame_source(game),bank[key][slot]),"Main-scene renderer samples exact authored pose")
					check(npc.foot==foot,"Visual bridge does not relocate physical actor")
					await capture(label+"-"+str(slot),npc)
					elapsed+=float(clocks[key].durations[slot])/1000.0
				game.visual_time_seconds=100.65+player.cycle_seconds(key,gear)+.001
				check(same(grid._get_branforth_frame_source(game),bank["swim-"+target][0]),"Native renderer returns to destination swimming")
				await capture(label+"-complete",npc)
	if not FileAccess.file_exists(OUT+"native_probe.gd.uid"):FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	FileAccess.open(OUT+"native-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"normalChanged":false,"scope":"Real main scene/actor animation selection/staged Grid subclass/actual rendering in authored flooded workshop. Prescribed stationary pose clocks; not autonomous navigation, exterior, blocked fallback or whole-run Continue."},"\t"))
	print("JAMES NATIVE WATER checks=",checks," failures=",failures," captures=",captures.size());game.queue_free();await process_frame;quit(0 if failures==0 else 1)
