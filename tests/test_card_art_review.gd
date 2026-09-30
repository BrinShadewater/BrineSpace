extends SceneTree
var failures := 0
var directory := ""
var phase := "before"
func _initialize() -> void: call_deferred("run")
func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="): directory=arg.trim_prefix("--capture-dir=")
		if arg.begins_with("--phase="): phase=arg.trim_prefix("--phase=")
	if directory.is_empty(): quit(2);return
	DirAccess.make_dir_recursive_absolute(directory)
	var prefs=preload("res://scripts/title_settings.gd")
	prefs.save_path="user://card-art-review.cfg"
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://card-art-review.meta";game.run_save_path="user://card-art-review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.tick_timer.stop();game._set_paused(true,false);game.set_process(false)
	game.crew_comms.minimize()
	var metrics: Dictionary={}
	for width in [960,1280,1600,2560]:
		root.size=Vector2i(width,int(width*9.0/16))
		game._refresh_all()
		var previous: Array=[]
		var stable:=0
		var sample: Array=[]
		for frame in range(180):
			await process_frame
			sample=[]
			for card in game.hand_box.find_children("*","PanelContainer",true,false):
				if not card.has_meta("card_id"):continue
				var t: Transform2D=card.get_screen_transform()
				var labels: Array=[]
				for child in card.find_children("*","Control",true,false):
					if child is Label or child is RichTextLabel:
						var rect: Rect2=child.get_global_rect()
						labels.append({"text":child.text,"rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y]})
				sample.append({"id":card.get_meta("card_id"),"logical_size":[card.size.x,card.size.y],
					"screen_origin":[t.origin.x,t.origin.y],"screen_size":[card.size.x*t.x.length(),card.size.y*t.y.length()],"labels":labels})
			stable=stable+1 if sample==previous else 0
			previous=sample.duplicate(true)
			if stable>=3:break
		if stable<3:failures+=1;push_error("Card layout did not settle")
		if sample.is_empty():failures+=1;push_error("No draft cards measured")
		await RenderingServer.frame_post_draw
		var image:=root.get_texture().get_image()
		image.save_png(directory.path_join("cards-%s-%d.png"%[phase,width]))
		metrics[str(width)]={"window":[root.size.x,root.size.y],"capture":[image.get_width(),image.get_height()],"cards":sample}
	var file:=FileAccess.open(directory.path_join("metrics-%s.json"%phase),FileAccess.WRITE)
	file.store_string(JSON.stringify(metrics,"\t"));file.close()
	if phase=="after":
		var before=JSON.parse_string(FileAccess.get_file_as_string(directory.path_join("metrics-before.json")))
		if JSON.parse_string(JSON.stringify(metrics))!=before:failures+=1;push_error("Card size or text layout changed")
	print("CARD ART REVIEW: failures=",failures)
	game.queue_free();await process_frame
	quit(1 if failures else 0)
