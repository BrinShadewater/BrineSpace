extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
var OUTPUT:String="res://output/marsh-work-2026-10-14/"+("before-native/" if "--before" in OS.get_cmdline_user_args() else "after-native/")
var game
var checks := 0
var failures := 0
var captures: Array = []
var samples: Array = []
var checkpoints:Array=[]
var marker: ColorRect
var marker_layer: CanvasLayer
const Save=preload("res://scripts/run_save.gd")

func _init(): call_deferred("run")
func check(ok: bool, message: String):
	checks += 1
	if not ok: failures += 1; push_error(message)

func settle_camera(camera: Vector2) -> bool:
	game._set_grid_zoom(.8, true, camera)
	for unused in range(180):
		await process_frame
		await RenderingServer.frame_post_draw
		game._restore_grid_view_center(camera)
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera) < .002: return true
	return false

func capture(label: String, slot: int):
	var actor = game.marsh_npc
	var texture: Texture2D = game.grid_view._get_marsh_frame(game)
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	check(game.grid_view._get_marsh_frame(game).get_image().get_data() == texture.get_image().get_data(), "submitted source remains frozen during rendering")
	var index := captures.size()
	var native := "world-%03d.png" % index
	var source := "source-%03d.png" % index
	check(root.get_texture().get_image().save_png(OUTPUT + native) == OK and texture.get_image().save_png(OUTPUT + source) == OK, "native actor/source pair saved")
	var position: Vector2 = game.get_marsh_position()
	var canvas_position: Vector2 = root.get_final_transform() * game.grid_view.get_global_transform_with_canvas() * (position + Vector2(0, game.get_cell_size() * .038))
	captures.append({"file":native,"sourceFile":source,"label":label,"slot":slot,"visualTime":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"position":[position.x,position.y],"canvasPosition":[canvas_position.x,canvas_position.y],"imageSize":[root.get_texture().get_width(),root.get_texture().get_height()]})


func quiet():
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()

func clear_loading() -> bool:
	var overlay=null
	for child in root.get_children():
		if child.get_script()==Loading:overlay=child;break
	if overlay==null:return false
	var deadline=Time.get_ticks_msec()+20000
	while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
	if overlay.continue_button.disabled:return false
	overlay.continue_button.pressed.emit()
	while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
	return not is_instance_valid(overlay)

func run():
	seed(20261014)
	if not OS.get_environment("APPDATA").contains("marsh-work-2026-10-14"):
		push_error("Explicit isolated APPDATA required");quit(1);return
	if DisplayServer.get_name() == "headless": quit(2); return
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	preload("res://scripts/title_settings.gd").reduced_motion = true
	var store = preload("res://scripts/room_layout_store.gd")
	store.loaded = true; store.data = {}
	game = load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture", true)
	game.meta.save_path = "user://run-study.meta"
	game.run_save_path = "user://run-study.loop"
	game.meta.unlocked_architect_ids = {"bill":true,"marsh":true}
	game.meta.selected_architect = "marsh"
	root.add_child(game); current_scene = game
	var deadline := Time.get_ticks_msec() + 120000
	while not game.startup_complete and Time.get_ticks_msec() < deadline: await process_frame
	check(game.startup_complete, "observable normal main startup")
	if not game.startup_complete: quit(1); return
	game.set_process(false); game.tick_timer.stop(); game.crew_comms.set_process(false); game.crew_comms.dismiss()
	var overlay = null
	for child in root.get_children():
		if child.get_script() == Loading: overlay = child; break
	if overlay != null:
		deadline = Time.get_ticks_msec() + 20000
		while overlay.continue_button.disabled and Time.get_ticks_msec() < deadline: await process_frame
		check(not overlay.continue_button.disabled, "actual Continue enabled")
		overlay.continue_button.pressed.emit()
		while is_instance_valid(overlay) and Time.get_ticks_msec() < deadline: await process_frame
		check(not is_instance_valid(overlay), "loading overlay gone before capture")
	game._confirm_doctrines(); game.tick_timer.stop(); game.set_process(false)
	check(game.running and not game.testing_free_build and not game.testing_disable_failures, "normal economy/failure flags unchanged")
	game.marsh_npc = Normal.new()
	var actor = game.marsh_npc
	actor.rebuild(game); actor.active = true; actor.battery = 100
	game.paused = false; game.Architects.advance_core(game, 10)
	var cell := Vector2i(-1,-1)
	for y in range(20,28):
		for x in range(20,28):
			var candidate := Vector2i(x,y)
			if not game.occupied.has(candidate) and not game.wrecks.has(candidate): cell = candidate; break
		if cell.x >= 0: break
	check(cell.x >= 0, "unoccupied furnished room site")
	if cell.x < 0: quit(1); return
	game._place_room("cold_store", cell, true); game.powered_room_cells[cell] = true
	actor.signature = ""; actor.rebuild(game)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]: peer.active = false
	var starts:Dictionary={}
	var routes:Dictionary={"east":Vector2(96,0)}
	var desired:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384.0
	for facing in routes:
		var chosen:=Vector2.INF
		var best:=INF
		for id in actor.room_nodes.get(cell,[]):
			var point:Vector2=actor.graph.get_point_position(id)
			var target:Vector2=point+routes[facing]
			if actor.can_stand(point) and actor.can_stand(target) and actor.segment_clear(point,target) and point.distance_squared_to(desired)<best:
				chosen=point;best=point.distance_squared_to(desired)
		check(chosen.is_finite(),"actual clear furnished-room route "+facing)
		if not chosen.is_finite():quit(1);return
		starts[facing]=chosen
	var start:Vector2=starts["east"]
	actor.foot = start; actor.direction = "east"; actor.state = "idle"; actor.goal = ""; actor.stage = ""; actor.timer = 10
	actor.path = PackedVector2Array()
	actor.needs = {"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.selected_room_cell = cell; game.paused = true; game._refresh_all(); game.hand_panel.hide()
	var camera: Vector2 = (Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera), "camera and room layers observably settled")
	var player=game.grid_view.marsh_player

	marker_layer=CanvasLayer.new();marker_layer.layer=1000;root.add_child(marker_layer)
	marker=ColorRect.new();marker.size=Vector2(8,8);marker_layer.add_child(marker)
	var before:bool="--before" in OS.get_cmdline_user_args()
	if before:
		# Reconstruct the exact pre-repair ordered selection for comparison only.
		player=preload("res://scripts/crew_sprite_player.gd").new()
		var catalog_path="res://character/marsh-v2/catalog.json"
		var catalog=JSON.parse_string(FileAccess.get_file_as_string(catalog_path))
		for relative in catalog.body:
			if str(relative)!="../marsh-work-joins-v1/manifest.json":player.load_manifest(catalog_path.get_base_dir().path_join(str(relative)),true)
		game.grid_view.marsh_player=player
		# Comparison control reproduces the old shared world-unit anchors.
		var effects=preload("res://scripts/station_effects.gd")
		for direction in effects.DIRECTIONS:
			var points:Array=[]
			for i in range(6):points.append([effects.TORCH_TIPS[direction].x,effects.TORCH_TIPS[direction].y])
			effects._marsh_torch_tips[direction]=points
	var directions:Array=["south"] if before else ["east","west","north","south"]
	game.grid_view._get_marsh_frame(game);game.grid_view.queue_redraw()
	await process_frame;await RenderingServer.frame_post_draw
	check(await settle_camera(camera),"final layout camera settled before cropping")
	var center:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*(game.get_marsh_position()+Vector2(0,game.get_cell_size()*.038))
	var region:=Rect2i(Vector2i(center)-Vector2i(200,220),Vector2i(400,400))
	for facing in directions:
		game.visual_time_seconds=100.0
		player.current_key="";player.motion={};player.phase=0;player.last_time=-1;player.started=0
		actor.direction=facing;actor.path=PackedVector2Array();actor.foot=start
		for index in range(204):
			var elapsed:float=index/60.0
			actor.state="weld";actor.goal="construction";actor.stage="";actor.timer=0.0
			if elapsed<.3 or elapsed>=3.14:
				actor.state="idle";actor.goal=""
			elif elapsed<.82:actor.timer=elapsed-.3
			elif elapsed<2.62:actor.timer=.52+elapsed-.82
			else:actor.timer=9.48+elapsed-2.62
			game.visual_time_seconds+=1.0/60.0
			await motion_capture(str(facing),index,region)
			if index in [0,18,50,157,190]:
				var snap:Dictionary=player.snapshot();player.current_key="";player.restore_snapshot(snap)
				check(player.snapshot()==snap,"source player restores at handoff")
		var seen:Dictionary={}
		for sample in samples:
			if sample.direction==facing:seen[sample.key+"/"+str(sample.slot)]=true
		for action in ["torch-draw","weld","torch-stow"]:
			var key:String=action+"-"+str(facing)
			for slot in range(player.frames[key].size()):check(seen.has(key+"/"+str(slot)),"every source hold submitted "+key+str(slot))
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"scope":"Normal main scene/player/rendering and actual construction animation_state/action_elapsed at prescribed advancing60Hz timers; idle/draw/weld/stow/idle in reachable furnished room. Render-marker guard, all18tool holds/cardinal. Not autonomous dispatch, paid job completion or real-time playback."},"\t"));file.close()
	print("MARSH WORK REVIEW: ",checks," checks, ",failures," failures; ",samples.size()," samples")
	marker_layer.queue_free();await process_frame;quit(1 if failures else 0)

func motion_capture(facing:String,index:int,region:Rect2i):
	var actor=game.marsh_npc
	var texture:Texture2D=game.grid_view._get_marsh_frame(game)
	var key:String=actor.animation_state()+"-"+actor.direction
	var slot:int=game.grid_view.marsh_player.frames[key].find(texture)
	check(slot>=0,"normal selected source slot present")
	if key.begins_with("weld-") and not "--before" in OS.get_cmdline_user_args():
		var offset:Vector2=preload("res://scripts/station_effects.gd").torch_tip_offset(game,actor)
		var pixel:Vector2=offset*float(texture.get_meta("crew_standing_height"))/65.28+Vector2(texture.get_meta("crew_pivot"))
		var source:Image=texture.get_image()
		var found:=false
		for y in range(maxi(0,int(pixel.y)-2),mini(source.get_height(),int(pixel.y)+3)):
			for x in range(maxi(0,int(pixel.x)-2),mini(source.get_width(),int(pixel.x)+3)):
				var color:Color=source.get_pixel(x,y)
				if Vector2(x+.5,y+.5).distance_to(pixel)<=1.6 and color.a>.8 and color.r>.7 and color.r>color.g*1.1 and color.b<.67:found=true
		check(found,"actual spark anchor lands on selected authored flame pixels")
	var marker_index: int=samples.size()+1
	marker.color=Color8(marker_index%256,(marker_index/256)%256,150)
	game.grid_view.queue_redraw()
	var image:Image
	for attempt in range(20):
		await process_frame;await RenderingServer.frame_post_draw
		image=root.get_texture().get_image()
		if image.get_pixel(2,2).is_equal_approx(marker.color):break
	check(image.get_pixel(2,2).is_equal_approx(marker.color),"current rendered sample marker observed")
	check(game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"actual source frozen during sample render")
	check(Rect2i(Vector2i.ZERO,image.get_size()).encloses(region),"full native motion crop inside actual saved viewport")
	var name:String=facing+"-%03d.png"%index
	check(image.get_region(region).save_png(OUTPUT+name)==OK,"native sample saved")
	check(texture.get_image().save_png(OUTPUT+"source-"+name)==OK,"selected source sample saved")
	var position:Vector2=game.get_marsh_position()
	var canvas:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*(position+Vector2(0,game.get_cell_size()*.038))
	check(region.encloses(Rect2i(Vector2i(canvas)-Vector2i(60,130),Vector2i(120,160))),"whole actor margin inside fixed motion crop")
	samples.append({"direction":facing,"index":index,"file":name,"durationMs":1000.0/60.0,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"canvasPosition":[canvas.x,canvas.y],"region":[region.position.x,region.position.y,400,400],"actualViewportSize":[image.get_width(),image.get_height()],"paused":game.paused,"visualTime":game.visual_time_seconds,"playerPhase":game.grid_view.marsh_player.phase,"runActive":actor.run_motion_active(),"snapshotValid":Normal.valid_marsh_snapshot(actor.snapshot())})
