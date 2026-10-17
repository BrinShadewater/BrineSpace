extends "res://character/james-hull-lifecycle-v1/validate.gd"
const RESULT:="res://character/james-hull-cardinal-v1/"
class CardinalJames extends "res://scripts/branforth_npc.gd":
	var available_face:String="north"
	var work_cell:=Vector2i(21,20)
	func can_stand(point:Vector2) -> bool:
		if not super.can_stand(point):return false
		if cell_at(point)!=work_cell:return true
		var local:Vector2=point-(Vector2(work_cell)+Vector2.ONE*.5)*384
		if maxf(absf(local.x),absf(local.y))<80:return true
		var facing:String=("west" if local.x<0 else "east") if absf(local.x)>absf(local.y) else ("north" if local.y<0 else "south")
		return facing==available_face
var cases:Array=[]
func settle_target():
	game.selected_room_cell=Vector2i(21,20);game._refresh_all();game._set_grid_zoom(1.2,true,Vector2(21.5,20.5)/40)
	if not game.hand_collapsed:game._toggle_hand_collapsed()
	for step in range(120):
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_preparing and not game.grid_view.zoom_settling:return
	check(false,"Cardinal scene camera settles")
func observe(facing:String):
	var actor=game.branforth_npc;var key:String=actor.animation_state()+"-"+actor.direction;var source:Texture2D=game.grid_view._get_branforth_frame_source(game);var index:int=game.grid_view.branforth_player.frames[key].find(source)
	var path:String=RESULT+"native/"+facing+"-%04d.png"%records.size()
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(path)==OK,"Cardinal native source capture")
	var canvas:Vector2=actor.foot*game.get_cell_size()/384.0
	var global:Vector2=game.grid_view.get_global_transform_with_canvas()*canvas
	var stretched:Vector2=root.get_stretch_transform()*global
	records.append({"case":facing,"path":path,"key":key,"index":index,"work":actor.timer,"foot":[actor.foot.x,actor.foot.y],"globalFoot":[global.x,global.y],"stretchFoot":[stretched.x,stretched.y],"water":game.occupied[Vector2i(21,20)].get("water_level",0),"sourceHash":source.get_image().get_data().hex_encode().sha256_text(),"sparks":Effects.torch_actors(game).has(actor)})
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(RESULT+"native")
	await start_scene("user://james-hull-cardinal.loop")
	game.branforth_npc=CardinalJames.new();game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;check(actor.active,"Genuine core release through inherited James actor")
	for other in [game.bill_npc,game.veld_npc,game.marsh_npc]:other.active=false
	for other in game.companion_actors.values():other.active=false
	var core:=Vector2i(20,20);var base:Dictionary=game.occupied[core].duplicate(true);var target:=Vector2i(21,20)
	var discovered:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(RESULT+"access-probe-evidence.json"))
	for facing in ["east","south","west"]:
		game.placed_rooms.assign([base.duplicate(true)]);game.occupied.clear();game.occupied[core]=game.placed_rooms[0]
		game.wrecks.erase(target);game.drone_fleet.sites.erase(target);game._place_room("life_support",target,true)
		actor.available_face=facing;actor.signature="";actor.room_cache.clear();actor.rebuild(game);actor.hull_return.clear();actor.hull_resume.clear();actor.finish_hull_animation();actor.helmet_equipped=false;actor.movement_medium="dry"
		var desired:=Vector2.ZERO
		for row in discovered.rows:
			if row.get("id","")=="life_support" and row.get("wanted","")==facing:desired=Vector2(row.point[0],row.point[1])
		var starts:Array=[]
		for node in actor.room_nodes.get(target,[]):
			var point:Vector2=actor.graph.get_point_position(node);var local:Vector2=point-(Vector2(target)+Vector2.ONE*.5)*384
			if maxf(absf(local.x),absf(local.y))<80 and actor.can_stand(point):starts.append(point)
		starts.sort_custom(func(a,b):return a.distance_squared_to(desired)<b.distance_squared_to(desired))
		check(not starts.is_empty(),"Available genuine interior fixture start")
		if starts.is_empty():quit(2);return
		actor.foot=starts[0];actor.goal="";actor.state="idle";actor.stage="";actor.timer=0
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		var room:Dictionary=game.occupied[target];room.hull_crack=.8;room.water_level=0.0
		check(Hull.request(game,target),"Real paid rupture repair")
		var paid:float=game.resources.metal;check(paid==95,"Original five-Metal repair cost")
		await settle_target()
		var contact:=Vector2.INF;var captured:Dictionary={};var states:Dictionary={};var work_steps:=0;var travel_steps:=0
		for step in range(2400):
			game._process(1.0/60.0)
			if not room.has("leak_repair"):break
			if not actor.hull_animation_active():travel_steps+=1;continue
			if not contact.is_finite():contact=actor.foot
			work_steps+=1;var state:String=actor.animation_state();states[state]=true
			check(actor.foot==contact and actor.can_stand(actor.foot),"Actual planted physical worksite")
			check(actor.direction==facing and actor.goal=="hull-repair","Actual ordinary controller chooses available wall facing")
			check(actor.timer==room.leak_repair.progress and actor.hull_animation_duration==14,"Original room-paid clock owns pose")
			check(game.resources.metal==paid,"No extra charge during full lifecycle")
			check(Effects.torch_actors(game).has(actor)==(state=="weld"),"Sparks only during held tool")
			check(actor.valid_branforth_snapshot(actor.snapshot()),"Cardinal ordinary snapshot admitted")
			var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
			check(source.get_meta("crew_pivot")==Vector2(92,172) and source.get_meta("crew_standing_height")==148.0,"Master ruler/pivot retained")
			var key:String=state+"-"+facing;var index:int=game.grid_view.branforth_player.frames[key].find(source);var token:String=key+str(index)
			if not captured.has(token):captured[token]=true;await observe(facing)
		check(not room.has("leak_repair") and room.get("hull_welded",false) and room.hull_crack==0,"Original rupture job completes once")
		check(states.has("torch-draw") and states.has("weld") and states.has("torch-stow"),"All three tool phases selected")
		check(actor.goal.is_empty() and not Effects.torch_actors(game).has(actor),"Completion releases work/effects")
		check(game.resources.metal==paid and work_steps==839,"Fourteen-second paid work preserved")
		await observe(facing)
		cases.append({"direction":facing,"contact":[contact.x,contact.y],"workSteps":work_steps,"travelSteps":travel_steps,"sourceSlots":captured.size(),"metal":paid,"completed":not room.has("leak_repair"),"states":states.keys()})
		print("JAMES CARDINAL CASE ",facing," captures=",captured.size()," completed=",not room.has("leak_repair"))
	var file:=FileAccess.open(RESULT+"native-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"records":records,"scope":"Three actual paid bare rupture jobs in dedicated free-placed life-support fixture; prescribed interior start/available wall band, inherited real floor/prop checks, ordinary Hull.approach/path/move and game updates. Full draw/held/stow/completion; first occurrence of each selected source captured. Not naturally chosen other-wall access in owner layouts, cross-room travel, fresh Continue, interruptions, gear or continuous footage."},"  "));file.close()
	if not FileAccess.file_exists(RESULT+"validate.gd.uid"):
		var uid:=FileAccess.open(RESULT+"validate.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES CARDINAL: ",checks," checks, ",failures," failures, ",records.size()," captures");game.queue_free();quit(1 if failures else 0)
