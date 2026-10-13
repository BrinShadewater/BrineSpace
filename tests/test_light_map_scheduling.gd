extends SceneTree
const Lighting=preload("res://rooms/whole-room/room_lighting.gd")
const Settings=preload("res://scripts/title_settings.gd")
var checks:=0
var failures:=0
var game
var measurements:=[]
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func compare(label:String):
	Lighting.schedule_light_map=true
	Lighting.update_light_map(game)
	await frame()
	var viewport:SubViewport=game.light_map.get_meta("viewport")
	var retained:Image=viewport.get_texture().get_image()
	var nonwhite:=false
	for y in range(0,retained.get_height(),8):
		for x in range(0,retained.get_width(),8):
			if retained.get_pixel(x,y).r<0.999:nonwhite=true
	check(nonwhite,"Comparison contains actual station lighting: "+label)
	Lighting.update_light_map(game)
	await frame()
	check(viewport.render_target_update_mode!=SubViewport.UPDATE_ALWAYS,"Unchanged map uses one-shot rendering: "+label+" mode="+str(viewport.render_target_update_mode))
	check(retained.get_data()==viewport.get_texture().get_image().get_data(),"Retained map unchanged: "+label)
	Lighting.schedule_light_map=false
	Lighting.update_light_map(game)
	await frame()
	check(retained.get_data()==viewport.get_texture().get_image().get_data(),"Exact scheduled/reference pixels: "+label)
func run():
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/").simplify_path()!=expected or DisplayServer.get_name()=="headless":push_error("Native isolated profile required");quit(2);return
	Settings.save_path="user://light_schedule.cfg";Settings.effects_quality=1
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://light_schedule.meta";game.run_save_path="user://light_schedule.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	game.testing_free_build=true;game.testing_disable_failures=true
	for i in range(8):game._place_room(["life_support","hydroponics_bay","reactor","crew_hab"][i%4],Vector2i(17+i%4,17+i/4),true)
	game.grid_view.set_process(false);game._refresh_all()
	for unused in range(30):await frame()
	var viewport:SubViewport=game.light_map.get_meta("viewport")
	RenderingServer.viewport_set_measure_render_time(viewport.get_viewport_rid(),true)
	root.size=Vector2i(1600,900)
	for zoom in [game.MAX_GRID_ZOOM,game.MAX_GRID_ZOOM*0.7]:
		game._set_grid_zoom(zoom)
		for unused in range(3):await frame()
		for offset in [Vector2i(-80,-50),Vector2i(60,40)]:
			var centre:Vector2=(Vector2(18,18)+Vector2.ONE*.5)*game.get_cell_size()
			game.grid_scroll.scroll_horizontal=maxi(0,int(centre.x-game.grid_scroll.size.x*.5+offset.x))
			game.grid_scroll.scroll_vertical=maxi(0,int(centre.y-game.grid_scroll.size.y*.5+offset.y))
			await compare("zoom/scroll")
	var cell:=Vector2i(17,17)
	for level in [0.0,0.2,0.61,1.0]:
		game.grid_view.room_light_levels[cell]=level
		await compare("fade "+str(level))
	game.power_blackout=true
	for clock in [0.0,0.17,0.54,1.3]:
		game.visual_time_seconds=clock
		await compare("blackout "+str(clock))
	Settings.reduced_motion=true
	await compare("reduced motion")
	game.power_blackout=false;Settings.reduced_motion=false
	game.recovered_crew=[{"architect_id":"bill","alive":true}]
	var actor=game.bill_npc;actor.active=true;actor.dead=false;actor.direction="east"
	for helmet in [false,true]:
		actor.helmet_equipped=helmet
		actor.foot=(Vector2(cell)+Vector2(.3,.6))*384.0
		await compare("helmet "+str(helmet))
	actor.foot+=(Vector2(0.45,0)*384.0)
	await compare("moving lamp")
	Lighting.schedule_light_map=true;Settings.effects_quality=0;Lighting.update_light_map(game)
	await frame()
	check(not game.light_map.visible and viewport.render_target_update_mode==SubViewport.UPDATE_DISABLED,"Low quality disables map")
	Settings.effects_quality=1
	await compare("quality re-enable")
	root.size=Vector2i(1920,1080)
	for unused in range(3):await frame()
	await compare("resize")
	# Measure viewport GPU and actual canvas submissions, outside pixel readbacks.
	for repeat in range(3):
		for scheduled in [false,true]:
			Lighting.schedule_light_map=scheduled;Lighting.update_light_map(game)
			await frame()
			var rows:=[]
			for i in range(60):
				Lighting.update_light_map(game);await frame()
				rows.append({"mode":viewport.render_target_update_mode,"total_calls":Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME),"calls":viewport.get_render_info(Viewport.RENDER_INFO_TYPE_CANVAS,Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME),"gpu_ms":RenderingServer.viewport_get_measured_render_time_gpu(viewport.get_viewport_rid()),"cpu_ms":RenderingServer.viewport_get_measured_render_time_cpu(viewport.get_viewport_rid())})
			measurements.append({"repeat":repeat,"scheduled":scheduled,"samples":rows})
	FileAccess.open("user://light-scheduling.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"measurements":measurements},"\t"))
	game.queue_free();await process_frame
	print("LIGHT MAP SCHEDULING: %d checks; %d failures"%[checks,failures])
	quit(1 if failures else 0)
