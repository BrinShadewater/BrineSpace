extends SceneTree
## Native mission-phase captures; run only with scratch APPDATA.

const MainScene = preload("res://scenes/main.tscn")
const Mission = preload("res://scripts/moonbay_missions.gd")
var game

func _init() -> void:
	call_deferred("run")

func settle() -> void:
	for _i in range(10): await process_frame
	await RenderingServer.frame_post_draw

func run() -> void:
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i(1920,1080)
	root.size = Vector2i(1600,900)
	game = MainScene.instantiate()
	game.meta.save_path = "user://moonbay_review.meta"
	game.run_save_path = "user://moonbay_review.loop"
	root.add_child(game)
	current_scene = game
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.wrecks.clear()
	var home := Vector2i(19,19)
	game._place_room("moonbay",home,true)
	game._place_room("command_center",Vector2i(21,20),true)
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.selected_room_cell = home
	game._refresh_all()
	game._set_grid_zoom(0.36)
	await settle()
	var at: Vector2 = Vector2(home+Vector2i.ONE)*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal = roundi(at.x)
	game.grid_scroll.scroll_vertical = roundi(at.y)
	var room: Dictionary = game.occupied[home]
	var state := Mission.mission_state(room)
	var actor = game.bill_npc
	actor.active = true
	actor.foot = (Vector2(home+Vector2i.ONE)+Vector2.ONE*0.5)*actor.CELL
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://output/moonbay-review"))
	var scenes := [
		{"name":"idle","phase":"idle","water":0.0,"damage":0},
		{"name":"boarding","phase":"approach","water":0.0,"damage":0},
		{"name":"flooding","phase":"flood","water":0.5,"damage":0},
		{"name":"launching","phase":"launch","water":1.0,"damage":0},
		{"name":"at-sea","phase":"work","water":1.0,"damage":0},
		{"name":"returning","phase":"return","water":1.0,"damage":0},
		{"name":"draining","phase":"drain","water":0.5,"damage":0},
		{"name":"damaged","phase":"idle","water":0.0,"damage":1}
	]
	for scene in scenes:
		state.phase = scene.phase
		state.progress = 3.0
		state.chamber_water = scene.water
		state.damage = scene.damage
		state.crew = "bill" if scene.phase!="idle" else ""
		state.order = "survey" if scene.phase!="idle" else ""
		state.target = Vector2i(29,29) if scene.phase!="idle" else Vector2i(-1,-1)
		state.station_open = scene.phase in ["idle","approach"]
		state.ocean_open = scene.phase=="launch"
		actor.moonbay_assignment = {"home":home,"onboard":true} if scene.phase!="idle" else {}
		actor.goal = "moonbay" if scene.phase!="idle" else ""
		game._refresh_inspector()
		game.find_child("MoonbayPanel",true,false).refresh()
		game.grid_view.queue_redraw()
		await settle()
		var path := "res://output/moonbay-review/%s.png" % scene.name
		if root.get_texture().get_image().save_png(path)!=OK:
			push_error("Capture failed: "+path)
			quit(1)
			return
		print("CAPTURE ",path)
	quit()
