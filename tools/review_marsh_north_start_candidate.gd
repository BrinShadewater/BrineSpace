extends SceneTree
## Staged source-clock audition. No invented physical travel or normal admission.
class View extends Node2D:
	var pose: Texture2D
	var idle: Texture2D
	var caption := ""
	func _draw():
		draw_rect(Rect2(0,0,900,460),Color("293b40"))
		draw_string(ThemeDB.fallback_font,Vector2(20,28),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,18)
		for entry in [[pose,180.0,"Candidate / gait"],[idle,600.0,"Selected idle"]]:
			var texture: Texture2D = entry[0]
			for pair in [[1.0,230.0],[65.28/148.0,410.0]]:
				var anchor := Vector2(entry[1],pair[1])
				var scale: float = pair[0]
				draw_line(anchor-Vector2(100,0),anchor+Vector2(100,0),Color("839597"))
				draw_texture_rect(texture,Rect2(anchor-texture.get_meta("crew_pivot")*scale,texture.get_size()*scale),false)
			draw_string(ThemeDB.fallback_font,Vector2(entry[1]-80,56),entry[2],HORIZONTAL_ALIGNMENT_LEFT,-1,16)
var failures := 0
var checks := 0
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	checks += 1
	if not ok: failures += 1; push_error(message)
func run():
	if DisplayServer.get_name()=="headless": quit(2); return
	root.size=Vector2i(900,460);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1
	var grid=load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var player=grid.marsh_player
	var material_trial := "north-walk-material" in OS.get_cmdline_user_args()
	var material_installed := FileAccess.file_exists("res://character/marsh-north-walk-material-v1/selection.json")
	var use_material := material_trial or material_installed
	if material_trial:
		player.load_manifest("res://character/marsh-north-walk-material-v1/candidate-01/manifest.json",true)
	var idle: Texture2D=player.frames["idle-north"][0]
	var endpoint: Texture2D=player.frames["walk-north"][1]
	player.load_manifest("res://character/marsh-north-walk-material-v1/candidate-01/north-start/manifest.json" if use_material else "res://character/marsh-ground-cardinal-v1/north-start-candidate-01/manifest.json",true)
	check(player.frames["walk-start-north"][0].get_image().get_data()==idle.get_image().get_data(),"exact selected idle entry")
	check(player.frames["walk-start-north"][-1].get_image().get_data()==endpoint.get_image().get_data(),"exact selected lifted-boot gait endpoint")
	check(is_equal_approx(player.cycle_seconds("walk-start-north"),.4),"400ms one-shot")
	var output="res://output/marsh-animation-audit/north-start-candidate-2026-10-02/"
	if material_trial: output="res://output/marsh-animation-audit/north-walk-material-trial-2026-10-02/"
	elif material_installed: output="res://output/marsh-animation-audit/north-walk-material-installed-native-2026-10-02/"
	DirAccess.make_dir_recursive_absolute(output)
	var view=View.new();view.idle=idle;view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
	var records: Array=[];var seen: Dictionary={};var last=""
	for step in range(141):
		var time:=step*.02
		var key: String="idle-north" if time<.65 else "walk-start-north" if time<1.05 else "walk-north"
		var elapsed: float=time if key=="idle-north" else time-.65 if key=="walk-start-north" else fmod(.15+time-1.05,.9)
		var texture: Texture2D=player.frame_at_elapsed(key,elapsed)
		var slot: int=player.frames[key].find(texture)
		check(slot>=0,"source slot available")
		check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"registered ruler retained")
		check(player.frame_at_elapsed(key,elapsed)==texture,"same clock freezes source")
		seen[key+":"+str(slot)]=true
		var selector:=key+":"+str(slot)
		if selector!=last:
			view.pose=texture;view.caption="Staged North start / %s #%d / %.2fs; source-clock only" % [key,slot,time]
			view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			var file: String="pose-%03d.png" % records.size()
			check(root.get_texture().get_image().save_png(output+file)==OK,"capture saved")
			records.append({"file":file,"time":time,"key":key,"slot":slot,"elapsed":elapsed})
			last=selector
	for i in range(5): check(seen.has("walk-start-north:"+str(i)),"all five candidate slots observed")
	for i in range(6): check(seen.has("walk-north:"+str(i)),"all six existing gait slots observed")
	var file=FileAccess.open(output+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":records,"scope":"Actual selected loader and elapsed player; 20ms clock, explicit .15s gait phase. No actor/world travel, foot-lock, Continue, stop or production admission."},"\t"));file.close()
	print("MARSH NORTH START CANDIDATE: %d checks, %d captures, %d failures" % [checks,records.size(),failures])
	grid.free();quit(1 if failures else 0)
