extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/release-death-review-v349/"
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
	game.meta.save_path="user://james-death349.meta";game.run_save_path="user://james-death349.loop"
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
	var player=game.grid_view.branforth_player
	check(player.get_script().resource_path=="res://scripts/james_water_player.gd","Normal runtime water player selected")
	var npc=game.branforth_npc;npc.rebuild(game);npc.active=true;npc.dead=false;npc.state="idle";npc.stage="";npc.goal="";npc.path.clear();npc.expedition.clear();npc.movement_medium="flooded"
	var foot:=Vector2.INF
	for node in npc.room_nodes.get(ORIGIN,[]):
		var at:Vector2=npc.graph.get_point_position(node)
		if npc.can_stand(at) and npc.swim_segment_clear(at,at,"north","north",true):foot=at;break
	check(foot.is_finite(),"Actual workshop supports native terminal pose fixture")
	if not foot.is_finite():quit(2);return
	var cases:=0
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		for direction in ["west","east","north","south"]:
			for medium in ["dry","flooded"]:
				for room in game.placed_rooms:room.water_level=0.0 if medium=="dry" else .95
				npc.foot=foot;npc.active=true;npc.dead=false;npc.direction=direction;npc.movement_medium=medium;npc.state="idle";npc.stage="";npc.goal="";npc.expedition.clear();npc.path=PackedVector2Array([foot+Vector2(12,0)])
				player.current_key="";player.motion.clear();player.current_equipment=gear;player.last_time=-1;player.phase=0.0;game.visual_time_seconds=100.0;npc.helmet_equipped=not gear.is_empty()
				npc.die()
				var state:String="death-ground" if medium=="dry" else "death-water"
				check(npc.dead and npc.animation_state()==state and npc.path.is_empty() and npc.goal.is_empty(),"Actual death dispatcher clears route/work and selects correct medium")
				var key:String=state+"-"+direction;var elapsed:=0.0
				game.grid_view._get_branforth_frame_source(game)
				for slot in range(bank[key].size()):
					game.visual_time_seconds=100.0+elapsed+float(clocks[key].durations[slot])/2000.0
					var tex:Texture2D=game.grid_view._get_branforth_frame_source(game)
					check(same(tex,bank[key][slot]),"Actual selected death source/clock sampled")
					await capture(("bare" if gear.is_empty() else "helmet")+"-"+key+"-"+str(slot),npc)
					check(npc.foot==foot and npc.dead and npc.path.is_empty(),"Native death remains stationary and terminal")
					elapsed+=float(clocks[key].durations[slot])/1000.0
				game.visual_time_seconds=100.0+elapsed+2.0
				check(same(game.grid_view._get_branforth_frame_source(game),bank[key][-1]),"Terminal death source remains held")
				cases+=1
	if not FileAccess.file_exists(OUT+"native_probe.gd.uid"):FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	FileAccess.open(OUT+"native-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"scope":"Actual James die() dispatch and normal selected renderer for all four directions, both gears and dry/flooded media; every six-pose death clock sampled and terminal held. Prescribed renderer times, not autonomous oxygen/starvation dispatch or continuous motion observation."},"\t"))
	print("JAMES NATIVE DEATH checks=",checks," failures=",failures," cases=",cases," captures=",captures.size());game.queue_free();await process_frame;quit(0 if failures==0 else 1)
