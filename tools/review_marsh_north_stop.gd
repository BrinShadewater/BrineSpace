extends SceneTree
class View extends Node2D:
	var pose: Texture2D
	var idle: Texture2D
	var caption:=""
	func _draw():
		draw_rect(Rect2(0,0,900,460),Color("293b40"))
		draw_string(ThemeDB.fallback_font,Vector2(20,28),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,18)
		for entry in [[pose,180.0,"Stop source"],[idle,600.0,"Selected idle"]]:
			for pair in [[1.0,230.0],[65.28/148.0,410.0]]:
				var texture: Texture2D=entry[0];var anchor:=Vector2(entry[1],pair[1]);var scale: float=pair[0]
				draw_line(anchor-Vector2(100,0),anchor+Vector2(100,0),Color("839597"))
				draw_texture_rect(texture,Rect2(anchor-texture.get_meta("crew_pivot")*scale,texture.get_size()*scale),false)
			draw_string(ThemeDB.fallback_font,Vector2(entry[1]-80,56),entry[2],HORIZONTAL_ALIGNMENT_LEFT,-1,16)
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(900,460);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=grid.marsh_player
	var phases: bool="phases" in OS.get_cmdline_user_args()
	var refined: bool="refined" in OS.get_cmdline_user_args() or phases
	check(not player.frames.has("walk-stop-north") and not player.frames.has("walk-stop-right-north"),"stop families remain unselected")
	player.load_manifest("res://character/marsh-north-stop-v1/candidate-05/manifest.json" if refined else "res://character/marsh-north-stop-v1/candidate-02/manifest.json",true)
	player.load_manifest("res://character/marsh-north-stop-v1/candidate-06/manifest.json" if refined else "res://character/marsh-north-stop-v1/candidate-04/manifest.json",true)
	if phases:player.load_manifest("res://character/marsh-north-stop-v1/phase-bank-v1/manifest.json",true)
	var view=View.new();view.idle=player.frames["idle-north"][0];view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
	var output="res://output/marsh-animation-audit/north-stop-native-2026-10-02/";DirAccess.make_dir_recursive_absolute(output)
	if refined:output="res://output/marsh-animation-audit/north-stop-refined-native-2026-10-02/";DirAccess.make_dir_recursive_absolute(output)
	if phases:output="res://output/marsh-animation-audit/north-stop-phases-native-2026-10-02/";DirAccess.make_dir_recursive_absolute(output)
	var records: Array=[]
	var branches: Array=[{"key":"walk-stop-north","gait":1},{"key":"walk-stop-right-north","gait":4}]
	if phases:
		branches=[]
		for i in range(6):branches.append({"key":"walk-stop-p%d-north" % i,"gait":i})
	for branch in branches:
		check(player.frames[branch.key][0].get_image().get_data()==player.frames["walk-north"][branch.gait].get_image().get_data(),"exact selected gait entry")
		check(player.frames[branch.key][-1].get_image().get_data()==view.idle.get_image().get_data(),"exact selected idle exit")
		check(is_equal_approx(player.cycle_seconds(branch.key),.4),"finite400ms stop")
		var last:="";var seen: Dictionary={}
		for step in range(51):
			var time:=step*.02
			var key: String="walk-north" if time<.3 else branch.key if time<.7 else "idle-north"
			# Select inside the gait hold: exact .6s can round into slot3, not4.
			var elapsed: float=branch.gait*.15+.001 if time<.3 else time-.3 if time<.7 else time-.7
			var texture: Texture2D=player.frame_at_elapsed(key,elapsed)
			var slot: int=player.frames[key].find(texture)
			if time<.3:check(slot==branch.gait,"prelude uses exact intended outgoing gait slot")
			check(slot>=0,"source slot available")
			check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"runtime ruler/pivot retained")
			check(player.frame_at_elapsed(key,elapsed)==texture,"same clock preserves source")
			seen[key+":"+str(slot)]=true
			var selector:=key+":"+str(slot)
			if selector!=last:
				view.pose=texture;view.caption="Staged North stop / %s #%d / %.2fs; source clock only" % [key,slot,time]
				view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var file: String="pose-%03d.png" % records.size()
				check(root.get_texture().get_image().save_png(output+file)==OK,"native source capture saved")
				records.append({"file":file,"time":time,"branch":branch.key,"key":key,"slot":slot,"elapsed":elapsed});last=selector
		for i in range(5):check(seen.has(branch.key+":"+str(i)),"all five stop slots observed")
	var file=FileAccess.open(output+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":records,"scope":"Actual selected loader plus two staged stop manifests,20ms elapsed player, exact gait1/gait4 to idle seams at148/65.28 display density. No actor/root travel, natural arrivals, arbitrary gait-phase coverage, production admission or Continue."},"\t"));file.close()
	print("MARSH NORTH STOP SOURCES: %d checks,%d captures,%d failures" % [checks,records.size(),failures]);grid.free();quit(1 if failures else 0)
