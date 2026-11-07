extends SceneTree
## Native smaller-window and larger-menu-text geometry. Scratch APPDATA required.
var checks := 0
var failures := 0
func _initialize() -> void: run.call_deferred()
func check(ok: bool, message: String) -> void:
	checks+=1
	if not ok:
		failures+=1
		push_error(message)
func settle() -> void:
	for _frame in range(8): await process_frame
func capture(name: String) -> void:
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png("res://output/ui-layout-audit-2026-10-04/"+name+".png")==OK,"Capture "+name)
func run() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.Preferences.save_path = "user://responsive-ui.cfg"
	game.meta.save_path = "user://responsive-ui.meta"
	game.run_save_path = "user://responsive-ui.loop"
	root.add_child(game)
	current_scene = game
	var frames := 0
	while not game.startup_complete and frames<600:
		frames+=1
		await process_frame
	check(game.startup_complete,"Gameplay initializes")
	game.Preferences.reduced_motion = true
	game._set_paused(true,false)
	game.crew_comms.minimize()
	for id in game.Architects.IDS:
		if not game.Architects.present(game,id): game.recovered_crew.append({"architect_id":id,"alive":true})
	var crew = game.find_child("CrewPortraitPanel",true,false)
	crew.selected = "bill"
	crew.refresh()
	game.selected_room_cell = Vector2i(20,20)
	game._refresh_all()
	for resolution in [Vector2i(960,540),Vector2i(1280,720),Vector2i(1280,1024),Vector2i(1600,900)]:
		root.size = resolution
		await settle()
		var tag := "%dx%d" % [resolution.x,resolution.y]
		check(root.content_scale_size.x==(1600 if resolution.x<1440 else 1920),tag+": compact window uses readable scale and larger window restores desktop scale")
		var view := root.get_visible_rect()
		check(view.encloses(game.resource_bar.get_global_rect()),tag+": resource bar inside viewport")
		check(view.encloses(game.find_child("NavigationRow",true,false).get_global_rect()),tag+": navigation buttons inside viewport")
		check(view.encloses(game.find_child("SideDock",true,false).get_global_rect()),tag+": side dock inside viewport")
		check(view.encloses(game.find_child("ControlsPanel",true,false).get_global_rect()),tag+": time controls inside viewport")
		check(crew.get_global_rect().end.x<=game.grid_scroll.get_global_rect().end.x,tag+": expanded four-portrait crew strip fits main view")
		for id in game.resource_labels:
			var label: Label = game.resource_labels[id]
			check(label.get_combined_minimum_size().x<=label.size.x+1,tag+": resource text fits "+str(id))
		await capture("gameplay-"+tag)
		game.Preferences.text_scale = 1.3
		game._open_menu()
		await settle()
		check(view.encloses(game.menu_center.get_child(0).get_global_rect()),tag+": large-text pause menu inside viewport")
		for button in game.menu_center.find_children("*","Button",true,false):
			if not button.is_visible_in_tree(): continue
			var text_size: Vector2 = button.get_theme_font("font").get_string_size(button.text,HORIZONTAL_ALIGNMENT_LEFT,-1,button.get_theme_font_size("font_size"))
			check(text_size.x<=button.size.x-16,tag+": large-text action fits "+button.text)
		await capture("menu-large-"+tag)
		game._close_menu()
		game._open_resource_details("oxygen",game.resource_chips.oxygen)
		await settle()
		check(view.encloses(game.archive_label.get_global_rect()),tag+": large-text journal reader inside viewport")
		check(view.encloses(game.journal_layer.get_meta("close_button").get_global_rect()),tag+": journal close control remains reachable")
		check(game.archive_label.get_theme_font_size("normal_font_size")>=22,tag+": journal honours large text")
		if resolution==Vector2i(1280,720): await capture("journal-large-1280x720")
		game._toggle_journal()
		if resolution==Vector2i(1280,720):
			var original: Dictionary = game.resources.duplicate(true)
			for key in game.BASE_STORAGE_CAPACITY:
				if key=="integrity": continue
				var id: String = "rare" if key=="rare_minerals" else str(key)
				game.resources[key] = 0
				game._set_resource_chip(id,id.to_upper()+"\n0/30  +4",Color.WHITE)
				game._apply_resource_outlook(id,str(key),4)
			await settle()
			check(view.encloses(game.resource_bar.get_global_rect()),"Longest refill captions remain inside compact viewport")
			check(view.encloses(game.find_child("NavigationRow",true,false).get_global_rect()),"Longest refill captions keep Menu/navigation reachable")
			for id in game.resource_labels:
				var label: Label = game.resource_labels[id]
				check(label.get_combined_minimum_size().x<=label.size.x+1,"Longest compact resource caption fits: "+str(id))
			await capture("compact-header-stress")
			game.resources = original
			game._refresh_all()
	game.Preferences.text_scale = 1.0
	print("RESPONSIVE UI: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
