extends SceneTree
class View extends Node2D:
	var pose: Texture2D
	var idle: Texture2D
	var caption := ""
	func _draw():
		draw_rect(Rect2(0,0,900,460),Color("293b40"))
		draw_string(ThemeDB.fallback_font,Vector2(20,28),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,18)
		for entry in [[pose,180.0,"Staged step"],[idle,600.0,"Selected idle"]]:
			for pair in [[1.0,230.0],[65.28/148.0,410.0]]:
				var texture: Texture2D = entry[0]
				var anchor := Vector2(entry[1],pair[1])
				var density: float = pair[0]
				draw_line(anchor-Vector2(100,0),anchor+Vector2(100,0),Color("839597"))
				draw_texture_rect(texture,Rect2(anchor-texture.get_meta("crew_pivot")*density,texture.get_size()*density),false)
			draw_string(ThemeDB.fallback_font,Vector2(entry[1]-80,56),entry[2],HORIZONTAL_ALIGNMENT_LEFT,-1,16)
var checks := 0
var failures := 0
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	checks += 1
	if not ok: failures += 1; push_error(message)
func run():
	if DisplayServer.get_name()=="headless": quit(2); return
	root.size=Vector2i(900,460); root.content_scale_size=Vector2i.ZERO; root.content_scale_factor=1
	var grid=load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var player=grid.marsh_player
	check(not player.frames.has("walk-step-north"),"North step remains unselected")
	var landing: bool="landing" in OS.get_cmdline_user_args()
	var key: String="north-step-landing-study" if landing else "walk-step-north"
	var count: int=3 if landing else 7
	player.load_manifest("res://character/marsh-north-step-v1/candidate-08/manifest.json" if landing else "res://character/marsh-north-step-v1/candidate-04/manifest.json",true)
	var view=View.new(); view.idle=player.frames["idle-north"][0]
	view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST; root.add_child(view)
	var output="res://output/marsh-animation-audit/north-step-native-2026-10-02/"
	if landing: output="res://output/marsh-animation-audit/north-step-landing-native-2026-10-02/"
	DirAccess.make_dir_recursive_absolute(output)
	check(player.frames[key][0].get_image().get_data()==view.idle.get_image().get_data(),"exact idle entry")
	check(player.frames[key][-1].get_image().get_data()==view.idle.get_image().get_data(),"exact idle exit")
	check(is_equal_approx(player.cycle_seconds(key),count*.12),"finite audition clock")
	var records: Array=[]; var seen: Dictionary={}; var last_slot := -1
	for step in range(count*6+7):
		var elapsed=step*.02
		var texture: Texture2D=player.frame_at_elapsed(key,elapsed)
		# Entry and exit are equal pixels but remain distinct source textures.
		var slot: int=player.frames[key].find(texture)
		check(slot>=0,"source available")
		check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"shared runtime ruler")
		check(player.frame_at_elapsed(key,elapsed)==texture,"frozen clock preserves exact source")
		seen[slot]=true
		if slot!=last_slot:
			view.pose=texture; view.caption="Unselected North shuffle source / slot%d / %.2fs" % [slot,elapsed]
			view.queue_redraw(); await process_frame; await RenderingServer.frame_post_draw
			var file="pose-%03d.png" % records.size()
			check(root.get_texture().get_image().save_png(output+file)==OK,"native capture saved")
			records.append({"file":file,"slot":slot,"elapsed":elapsed}); last_slot=slot
	for slot in range(count): check(seen.has(slot),"all audition holds observed")
	check(last_slot==count-1,"finite end holds final idle")
	var file=FileAccess.open(output+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":records,"scope":"Normal selected loader plus explicitly unselected candidate08 isolated landing study; three presentation holds, not a completed step." if landing else "Explicitly unselected candidate04;20ms source-clock playback at148/65.28 density. No root travel/controller, contact curve, natural routes, production admission or Continue."},"\t")); file.close()
	print("MARSH NORTH STEP SOURCES: %d checks,%d captures,%d failures" % [checks,records.size(),failures])
	grid.free(); quit(1 if failures else 0)
