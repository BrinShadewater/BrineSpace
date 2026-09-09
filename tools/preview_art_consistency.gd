extends SceneTree
## Native art review. Run with isolated APPDATA/LOCALAPPDATA; never an owner save.
## godot --path . --script res://tools/preview_art_consistency.gd
const OUT := "res://output/art-consistency/"
const Architects = preload("res://scripts/architects.gd")
const Companions = preload("res://scripts/companions.gd")
var game
var captures := []
func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(6): await process_frame
	await RenderingServer.frame_post_draw
func capture(label: String) -> void:
	await settle()
	var picture := root.get_texture().get_image()
	assert(picture.get_size()==root.size)
	assert(picture.save_png(OUT+label+".png")==OK)
	captures.append(label)
func run() -> void:
	if DisplayServer.get_name()=="headless":
		push_error("Art review requires native rendering")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(OUT)
	root.gui_disable_input = true
	root.size = Vector2i(1600,900)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://art_consistency.meta"
	game.run_save_path = "user://art_consistency.loop"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	game.crew_comms.dismiss()
	game.crew_comms.set_process(false)
	game._set_paused(true,false)
	game.selected_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	await capture("station-context")
	for region in preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd").REGIONS:
		game._set_grid_zoom(0.20,true,region.center/40.0)
		await capture("habitat-"+region.biome)
	game._fit_station_view()
	for width in [1600,960]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		for identity in ["brine"]+Architects.IDS:
			game.crew_comms.current = {"speaker":identity,"text":"Pressure holds. The next compartment has not answered."}
			game.crew_comms.present_current()
			game.crew_comms.advance()
			game.crew_comms.place_panel()
			assert(game.crew_comms.portrait.texture!=null)
			assert(game.grid_scroll.get_global_rect().encloses(game.crew_comms.panel.get_global_rect()))
			if identity!="brine":
				assert(game.crew_comms.portrait.texture==Architects.selection_portrait(identity))
			await capture("comms-%s-%d"%[identity,width])
	game.crew_comms.dismiss()
	# Representative frames come from the actual loaded, merged runtime packs.
	var players := {"bill":game.grid_view.human_water_player,"veld":game.grid_view.veld_player,
		"branforth":game.grid_view.branforth_player,"marsh":game.grid_view.marsh_player}
	for id in Companions.IDS:
		players[id] = game.companion_actors[id].player
	var samples := []
	for id in players:
		for state in ["idle-south","walk-east","repair-east","swim-east"]:
			if not players[id].frames.has(state): continue
			var frames: Array = players[id].frames[state]
			for index in [0,frames.size()/2,frames.size()-1]:
				var name: String = "sprite-%s-%s-%d.png"%[id,state,index]
				assert(frames[index].get_image().save_png(OUT+name)==OK)
				samples.append({"actor":id,"state":state,"frame":index,"image":name})
	# Check the full-resolution set's selected bytes, not just non-null textures.
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/portraits-realism-v2/manifest.json"))
	for entry in manifest.portraits:
		var path: String = "res://character/portraits-realism-v2/%s.png"%entry.id
		assert(FileAccess.get_sha256(path).to_lower()==str(entry.sha256).to_lower())
		var texture: Texture2D = Architects.selection_portrait(entry.id) if Architects.IDS.has(entry.id) else Companions.portrait(entry.id)
		assert(texture!=null and texture.get_width()>=1000)
	game.hide()
	for id in Architects.IDS: game.meta.unlocked_architect_ids[id] = true
	for id in Companions.IDS: game.meta.unlocked_companion_ids[id] = true
	var picker = preload("res://scripts/architect_selection.gd").new()
	picker.meta_state = game.meta
	root.add_child(picker)
	for width in [1600,960]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		var scroll: ScrollContainer = picker.find_children("*","ScrollContainer",true,false)[0]
		for id in Architects.IDS:
			scroll.ensure_control_visible(picker.entries[id])
			await capture("picker-%s-%d"%[id,width])
		for id in Companions.IDS:
			scroll.ensure_control_visible(picker.companion_buttons[id])
			await capture("picker-%s-%d"%[id,width])
	picker.queue_free()
	await process_frame
	root.size = Vector2i(1600,900)
	for index in range(Architects.IDS.size()):
		var preview := preload("res://scripts/checkpoint_preview.gd").new()
		preview.configure({"architects":{"selected":Architects.IDS[index]},"state":{"placed_rooms":[{"pos":Vector2i(20,20),"id":"brine_core","category":"Core"}]}})
		preview.position = Vector2(80,80+index*110)
		preview.size = Vector2(500,84)
		root.add_child(preview)
		assert(preview.portrait==Architects.selection_portrait(Architects.IDS[index]))
	await capture("checkpoint-portraits")
	var file := FileAccess.open(OUT+"native-review.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":captures,"runtime_sprite_samples":samples},"  "))
	file.close()
	print("ART CONSISTENCY PASS: %d native captures, %d runtime sprite samples, seven portrait hashes and consumers verified"%[captures.size(),samples.size()])
	quit()
