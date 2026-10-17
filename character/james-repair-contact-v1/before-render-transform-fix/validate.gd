extends SceneTree
const OUT := "res://character/james-repair-contact-v1/"
const Effects = preload("res://scripts/station_effects.gd")
const Hull = preload("res://scripts/hull_repair.gd")
var checks := 0
var failures := 0
var game
var records: Array = []
func _init(): call_deferred("run")
func check(ok: bool, why: String):
	checks += 1
	if not ok: failures += 1; push_error(why)
class Board extends Node2D:
	var game
	var source: Texture2D
	var before := false
	func _draw():
		draw_rect(Rect2(0,0,1000,420),Color("303b40"))
		var actor = game.branforth_npc
		var original: Vector2 = actor.foot
		var corrected: Dictionary = Effects._james_torch_tips.duplicate()
		if before: Effects._james_torch_tips = {"north":[16,-127],"east":[37,-75],"south":[0,-59],"west":[-35,-75]}
		for column in range(4):
			var height: float = [148.0,82.0,54.0,27.0][column]
			var size: float = height / .17
			var unit: float = size / 384.0
			var at := Vector2(125+column*245,350)
			actor.foot = at/unit
			var scale: float = size*.17/148.0
			draw_texture_rect(source,Rect2(at+Vector2(0,size*.038)-Vector2(92,172)*scale,source.get_size()*scale),false)
			Effects.draw_torch_sparks(self,game,size)
			draw_string(ThemeDB.fallback_font,Vector2(column*245+18,400),str(int(height))+"px",HORIZONTAL_ALIGNMENT_LEFT,-1,16)
		actor.foot = original
		Effects._james_torch_tips = corrected
		draw_string(ThemeDB.fallback_font,Vector2(12,24),("BEFORE" if before else "CORRECTED")+" / prescribed held source / "+actor.direction+" / "+("helmet" if actor.helmet_equipped else "bare"),HORIZONTAL_ALIGNMENT_LEFT,-1,18)
func run():
	if DisplayServer.get_name()=="headless": quit(2); return
	var expected := OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(OUT+"native")
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-repair-contact.meta";game.run_save_path="user://james-repair-contact.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.running=true;game.paused=false;game.crew_comms.dismiss();game.crew_comms.set_process(false)
	game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;check(actor.active,"Genuine core release")
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	for peer in game.companion_actors.values():peer.active=false
	var initial: Vector2=actor.foot
	var player=game.grid_view.branforth_player
	var evidence: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"source-evidence.json"))
	var offsets: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"torch-tip-offsets.json"))
	for row in evidence.rows:
		actor.direction=row.direction
		var tex: Texture2D=(player.frames if row.gear=="bare" else player.equipment_frames["diving-helmet"])["weld-"+row.direction][int(row.index)]
		check(tex.get_image().get_data()==Image.load_from_file(row.path).get_data(),"Selected immutable whole source")
		check(tex.get_meta("crew_pivot")==Vector2(92,172) and tex.get_meta("crew_standing_height")==148.0,"Selected source ruler")
		var tip: Vector2=Effects.torch_tip_offset(game,actor)
		var point:=Vector2(row.worldPoint[0],row.worldPoint[1])
		check(tip.distance_to(point)<.8,"Corrected normal effect near selected flame")
		for size in [384.0,82.0/.17,54.0/.17,27.0/.17]:
			var pixel_scale:float=size*.17/148.0
			var rendered:Vector2=(Vector2(row.sourcePoint[0],row.sourcePoint[1])-Vector2(92,172))*pixel_scale+Vector2(0,size*.038)
			check(rendered.distance_to(tip*size/384.0)<1.01,"Flame/contact common rendering units")
	# One ordinary paid hull request; controller chooses its worksite and facing.
	actor.foot=initial;actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.helmet_equipped=false;actor.construction_motion.clear()
	game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
	var core:=Vector2i(20,20);var room:Dictionary=game.occupied[core]
	room.hull_crack=.8;room.water_level=0.0;room.erase("leak_repair")
	check(Hull.request(game,core),"Real paid hull repair queued")
	var metal:float=game.resources.metal
	game.selected_room_cell=core;game._refresh_all();game._set_grid_zoom(1.2,true,(Vector2(core)+Vector2.ONE*.5)/40.0)
	if not game.hand_collapsed:game._toggle_hand_collapsed()
	for step in range(120):
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_preparing and not game.grid_view.zoom_settling:break
	var seen: Dictionary={};var working:=false;var foot:=Vector2.ZERO
	for step in range(3000):
		game._process(1.0/60.0)
		var tex: Texture2D=game.grid_view._get_branforth_frame_source(game)
		if actor.goal=="hull-repair" and actor.state=="weld":
			if not working:working=true;foot=actor.foot
			check(actor.foot==foot and actor.path.is_empty(),"Actual repair contact stays fixed")
			check(Effects.torch_actors(game).has(actor),"Actual repair has torch effects")
			check(not Effects.construction_door(game,actor).is_finite(),"Repair uses flame rather than construction doorway")
			var key:String="weld-"+actor.direction
			var index:int=player.frames[key].find(tex)
			check(index>=0,"Normal actual repair selects whole held source")
			if not seen.has(index):
				seen[index]=true
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var name:String="actual-%s-%03d.png"%[actor.direction,index]
				check(root.get_texture().get_image().save_png(OUT+"native/"+name)==OK,"Actual paid repair native capture")
				var p:Vector2=game.grid_view.get_global_transform_with_canvas()*(game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038))
				records.append({"path":name,"direction":actor.direction,"index":index,"footViewport":[p.x,p.y],"progress":room.leak_repair.progress})
		if working and not room.has("leak_repair"):break
	check(working and room.get("hull_crack",1)==0 and not room.has("leak_repair"),"Ordinary paid hull repair completes")
	check(game.resources.metal==metal,"No second repair charge")
	# Construction contact still uses the exact same shared doorway helper.
	actor.goal="construction"
	game.drone_fleet.orders.append({"builder":"branforth","work_cell":core,"pos":core+Vector2i.UP})
	check(Effects.construction_door(game,actor)==(Vector2(core)+Vector2(.5,0))*384-Vector2(0,34),"Construction doorway geometry retained")
	game.drone_fleet.orders.clear()
	# Prescribed sources: helmet weld is not claimed as natural hull eligibility.
	game.visible=false;root.size=Vector2i(1000,420);root.content_scale_size=Vector2i.ZERO
	var board:=Board.new();board.game=game;root.add_child(board)
	actor.goal="hull-repair";actor.state="weld";actor.stage="";actor.path.clear();actor.timer=2.0
	for gear in ["bare","helmet"]:
		actor.helmet_equipped=gear=="helmet"
		for direction in ["north","east","south","west"]:
			actor.direction=direction
			board.source=(player.frames if gear=="bare" else player.equipment_frames["diving-helmet"])["weld-"+direction][0]
			for before in [true,false]:
				board.before=before;board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				check(root.get_texture().get_image().save_png(OUT+"native/"+gear+"-"+direction+("-before" if before else "-corrected")+".png")==OK,"Native effects comparison")
	var report:Dictionary={"checks":checks,"failures":failures,"actualCaptures":records,"actualPaidComplete":working and room.get("hull_crack",1)==0,"prescribedComparisons":16,"scope":"448 selected whole-source/ruler/effect checks at four render sizes. One ordinary paid hull request, natural controller worksite/facing, unique source captures and completion once. Prescribed four-direction/both-gear effects boards; helmet weld not actual repair eligibility. No draw/stow/interrupt/Continue or natural other-facing claim."}
	var file:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify(report,"  "));file.close()
	print("JAMES REPAIR CONTACT: ",checks," checks, ",failures," failures, ",records.size()," actual captures")
	board.queue_free();game.queue_free();quit(1 if failures else 0)
