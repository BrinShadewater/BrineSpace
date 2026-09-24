extends SceneTree
const Save=preload("res://scripts/run_save.gd")
const Discovery=preload("res://scripts/site_discovery.gd")
const Library=preload("res://scripts/room_asset_library.gd")
var game
var failures := 0
const OUT := "res://output/procedural-sites-2026-09-23/"
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	if not ok: failures+=1;push_error(message)
func checkpoint(label: String):
	game._set_paused(true,false)
	check(Save.write(game,game.run_save_path)==OK,"save "+label)
	var data:=Save.read(game.run_save_path)
	check(not data.is_empty(),"read "+label)
	if data.is_empty(): return
	var geography: Dictionary=game.site_layout.duplicate(true)
	var wrecks: Dictionary=game.wrecks.duplicate(true)
	check(Save.restore(game,data),"restore "+label)
	check(game.site_layout==geography and game.wrecks==wrecks,"exact map and occupant restore "+label)
	check(game.paused,"paused restore "+label)
func run():
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://site_runtime_%d.json"%OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	game.set_meta("site_seed",32)
	root.add_child(game);current_scene=game
	game.Preferences.pause_unfocused=false
	while not game.startup_complete: await process_frame
	game._set_paused(true,false)
	checkpoint("unidentified")
	var cell: Vector2i=game.site_layout.recovery_cells[0]
	game.surveyed_water[cell]=true
	check(Discovery.reveal(game)==[cell],"first exploration")
	check(game.wrecks[cell].pods[0].architect_id=="veld","first encounter is Veld")
	checkpoint("revealed")
	game.wrecks[cell].paid=true;game.wrecks[cell].progress=3.0
	checkpoint("partial repair")
	game._place_room("cryo_chamber",cell,true)
	game.occupied[cell].recovered_derelict=true
	game.occupied[cell].rotation=0
	game.wrecks[cell].cleared=true;game.wrecks[cell].progress=18.0
	game.wrecks[cell].pods[0].wake=2.0
	checkpoint("partial wake")
	for other in game.site_layout.recovery_cells: game.surveyed_water[other]=true
	check(Discovery.reveal(game).size()==2,"remaining human and android discoveries")
	var marsh: Vector2i=game.site_layout.recovery_cells[2]
	check(game.wrecks[marsh].kind=="charging","Marsh gets charging chamber")
	game.wrecks[marsh].paid=true;game.wrecks[marsh].progress=18.0;game.wrecks[marsh].cleared=true
	game._place_room("cryo_chamber",marsh,true)
	game.occupied[marsh].recovered_derelict=true;game.occupied[marsh].rotation=0
	game.wrecks[marsh].pods[0].wake=5.0
	checkpoint("partial android charge")
	var invalid:=Save.capture(game)
	invalid.site_layout.recovery_cells[0]=Vector2i(-1,-1)
	var before: Dictionary=game.site_layout.duplicate(true)
	check(not Save.restore(game,invalid) and game.site_layout==before,"invalid map rejected without mutation")
	check(Library.is_exterior("library/tileset-uw1-188"),"exterior classified")
	check(not Library.is_exterior("library/tileset-mat-123"),"indoor filtration retained")
	check(not Library.template("library/tileset-uw1-188").is_empty(),"existing exterior placements still resolve")
	# Portable legacy-format fixture, plus the historical checkpoint when available.
	game.set_meta("authored_site_fixture",true)
	game._start_reboot_cycle()
	var legacy:=Save.capture(game)
	legacy.erase("site_layout")
	check(Save.restore(game,legacy),"legacy format restores")
	check(game.site_layout.is_empty() and game.wrecks==legacy.wrecks,"legacy geography preserved")
	var historical := "res://output/normal-release-review-2026-09-23/checkpoint-frozen.loop"
	if FileAccess.file_exists(historical):
		legacy=Save.read(historical)
		check(not legacy.is_empty(),"historical checkpoint reads")
		check(Save.restore(game,legacy),"historical checkpoint restores")
		check(game.site_layout.is_empty() and game.wrecks==legacy.wrecks,"historical geography preserved")
	# Known-character shuffle remains stable across actual disk save/restore.
	game.remove_meta("authored_site_fixture")
	for id in game.Architects.IDS: game.meta.record_sighting(id)
	game._start_reboot_cycle()
	game._set_paused(true,false)
	var unknown:=Save.capture(game)
	for at in game.site_layout.recovery_cells: game.surveyed_water[at]=true
	Discovery.reveal(game)
	var expected: Dictionary=game.wrecks.duplicate(true)
	check(Save.restore(game,unknown),"known shuffle restores unidentified baseline")
	game.surveyed_water[game.site_layout.recovery_cells[0]]=true
	check(Discovery.reveal(game).size()==1,"known shuffle first reveal")
	checkpoint("known shuffle partial reveal")
	for at in game.site_layout.recovery_cells: game.surveyed_water[at]=true
	check(Discovery.reveal(game).size()==2,"known shuffle remaining reveals")
	check(game.wrecks==expected,"known shuffle disk Continue matches uninterrupted reveal")
	# Return to fresh seed and render actual game fog, rooms, unknown/revealed sites.
	game.remove_meta("authored_site_fixture")
	game._start_reboot_cycle()
	game._set_paused(true,false)
	while game.grid_scroll.size.x<600 or game.grid_scroll.size.y<300: await process_frame
	var center:=Vector2(20.5,20.5)/40.0
	game._set_grid_zoom(.35,true,center)
	var deadline:=Time.get_ticks_msec()+5000
	while game._grid_view_center_ratio().distance_to(center)>.002 and Time.get_ticks_msec()<deadline:
		await process_frame
	check(game._grid_view_center_ratio().distance_to(center)<.002,"native capture centers on BRINE")
	await process_frame
	RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(OUT+"native-site-32.png")
	print("SITE RUNTIME: failures=",failures)
	var music=root.get_node_or_null("StationMusic")
	if music!=null: music.process_mode=Node.PROCESS_MODE_DISABLED
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	quit(0 if failures==0 else 1)

