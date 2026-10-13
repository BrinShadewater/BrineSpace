extends SceneTree
var OUTPUT="res://output/marsh-animation-audit/south-step-source-native-v1-2026-10-02/"
var candidate:="03"
class Study extends Control:
	var pose: Texture2D
	var idle: Texture2D
	var caption:=""
	func _draw():
		draw_rect(Rect2(Vector2.ZERO,size),Color("293b40"))
		var font=ThemeDB.fallback_font
		draw_string(font,Vector2(40,50),"UNSELECTED South short-step source study / fixed anchors",HORIZONTAL_ALIGNMENT_LEFT,-1,24,Color.WHITE)
		draw_string(font,Vector2(40,85),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,21,Color.WHITE)
		for i in range(3):
			var anchor:=Vector2(220+330*i,360)
			var scale:=65.28/148.0 if i==2 else 1.0
			var texture=idle if i==0 else pose
			draw_line(anchor-Vector2(70,0),anchor+Vector2(70,0),Color("639f92"))
			draw_texture_rect(texture,Rect2(anchor-Vector2(92,172)*scale,Vector2(184,184)*scale),false)
			draw_string(font,anchor+Vector2(-110,70),["Selected idle /148px","Step source /148px","Step native /65.28px"][i],HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
		draw_string(font,Vector2(40,500),"Four complete generated interiors. Exact idle0 endpoints; idle1 preparation. No root/controller/admission proof.",HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color.WHITE)
		draw_string(font,Vector2(40,535),"Open: reach projection, trailing-foot lateral closure, width/face/material joins; whole-figure repairs only.",HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color.WHITE)
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--candidate="):candidate=arg.trim_prefix("--candidate=")
	check(candidate in ["03","04","05"],"explicit supported source candidate")
	if candidate!="03":OUTPUT="res://output/marsh-animation-audit/south-step-source-native-"+candidate+"-2026-10-02/"
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1200,600);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	check(root.content_scale_size==Vector2i.ZERO and is_equal_approx(root.content_scale_factor,1.0),"fixture disables project window downscale for true pixel rulers")
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations();var player=grid.marsh_player
	check(not player.frames.has("walk-step-south"),"normal catalog does not silently select this source study")
	player.load_manifest("res://character/marsh-south-step-v1/candidate-"+candidate+"/manifest.json",true)
	var key:="walk-step-south";check(player.frames[key].size()==7,"seven declared slots available")
	check(player.timing[key].durations==[120.0,120.0,120.0,120.0,120.0,120.0,120.0] and not player.timing[key].loop,"finite840ms120ms source contract")
	check(player.frames[key][0].get_image().get_data()==player.frames["idle-south"][0].get_image().get_data() and player.frames[key][6].get_image().get_data()==player.frames["idle-south"][0].get_image().get_data(),"byte-exact selected idle endpoints")
	check(player.frames[key][1].get_image().get_data()==player.frames["idle-south"][1].get_image().get_data(),"preparation is exact selected breathing source")
	var view=Study.new();root.add_child(view);view.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT);view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;view.idle=player.frames["idle-south"][0]
	var seen: Dictionary={};var captures: Array=[];var last_slot:=-1
	for step in range(50):
		var elapsed: float=step*.02;var texture: Texture2D=player.frame_at_elapsed(key,elapsed)
		var slot: int=player.frames[key].find(texture)
		check(slot>=0,"bounded advancing source selection")
		check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"common runtime ruler")
		check(player.frame_at_elapsed(key,elapsed)==texture,"same elapsed freeze preserves source")
		seen[slot]=true
		if slot==last_slot:continue
		view.pose=texture;view.caption="slot%d / %.2fs / explicitly loaded candidate%s"%[slot,elapsed,candidate];view.queue_redraw()
		await process_frame;await RenderingServer.frame_post_draw
		var native_file: String="native-%03d.png"%captures.size();var source_file: String="source-%03d.png"%captures.size()
		check(root.get_texture().get_image().save_png(OUTPUT+native_file)==OK and texture.get_image().save_png(OUTPUT+source_file)==OK,"native/source pair saved")
		captures.append({"file":native_file,"sourceFile":source_file,"slot":slot,"elapsed":elapsed});last_slot=slot
	for slot in range(7):check(seen.has(slot),"every declared source hold observed")
	check(last_slot==6 and captures.size()==7,"finite source completes on exact idle")
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"candidate":candidate,"checks":checks,"failures":failures,"captures":captures,"scope":"Explicitly unselected candidate"+candidate+" seven-slot840ms South short-step source playback at148/65.28 declared standing rulers; selected South idle baseline, fixed pivot/source anchors. No physical root movement, actor priorities, path safety, snapshot/Continue or production admission. All seven source/native plate pairs submitted."},"\t"));file.close()
	grid.free();print("MARSH SOUTH STEP SOURCE: %d checks,%d captures,%d failures"%[checks,captures.size(),failures]);quit(1 if failures else 0)
