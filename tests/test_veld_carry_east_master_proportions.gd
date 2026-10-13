extends SceneTree
const MANIFESTS := {"bare":"res://character/veld-carry-east-master-proportions-v1/paired-package-v1/bare-manifest.json", "helmet":"res://character/veld-carry-east-master-proportions-v1/paired-package-v1/helmet-manifest.json"}
const OUT := "res://output/veld-carry-east-master-proportions-native-v2/"
var checks := 0
var failures := 0
var records: Array = []
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
class Board extends Node2D:
	var previous: Texture2D
	var candidate: Texture2D
	var time := 0.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,760,600),Color("202a30"))
		var heights := [47.0,93.0,148.0]
		var anchors := [70.0,250.0,535.0]
		for row in range(2):
			var tex: Texture2D = previous if row==0 else candidate
			if tex==null: continue
			for i in range(3):
				var scale: float=heights[i]/148.0
				var foot := Vector2(anchors[i]+time*4.0,285.0+row*280.0)
				draw_line(foot+Vector2(-60,0),foot+Vector2(60,0),Color("46545c"))
				draw_texture_rect(tex,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
				draw_string(ThemeDB.fallback_font,Vector2(anchors[i]-60,22+row*280),"Selected" if row==0 else "Candidate",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init() -> void: call_deferred("run")
func run() -> void:
	check(OS.get_environment("APPDATA").contains("veld-carry-east-master-scratch"),"Scratch owner profile required")
	if failures: quit(1); return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	root.size=Vector2i(760,600);root.content_scale_size=Vector2i.ZERO
	var board := Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(board)
	for gear in ["bare","helmet"]:
		var baseline=load("res://scripts/crew_sprite_player.gd").new()
		baseline.load_manifest("res://character/veld-carry-east-consistent-v1/bare-manifest.json")
		check(baseline.load_equipment_manifest("diving-helmet","res://character/veld-carry-east-consistent-v1/helmet-manifest.json"),"Baseline paired equipment")
		var player=load("res://scripts/crew_sprite_player.gd").new()
		player.load_manifest("res://character/veld-carry-east-master-proportions-v1/paired-package-v1/bare-manifest.json")
		check(player.load_equipment_manifest("diving-helmet","res://character/veld-carry-east-master-proportions-v1/paired-package-v1/helmet-manifest.json"),"Candidate paired equipment")
		var equipment: String="" if gear=="bare" else "diving-helmet"
		var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(MANIFESTS[gear]))
		var seen := {}
		check(is_equal_approx(player.cycle_seconds("carry-east",equipment),.84),"Exact840mscycle")
		for n in range(52):
			var time: float=n/30.0
			var position := Vector2(time*.0872972972972973/.84,0)
			var texture: Texture2D=player.frame("carry","east",time,position,equipment)
			var prior: Texture2D=baseline.frame("carry","east",time,position,equipment)
			var ideal_index: int=int(floor(fposmod(time,.84)/.14+0.000001))%6
			var matched: Array[int]=[]
			for slot in range(6):
				var frozen := Image.load_from_file(str(pack.states[0].frameFiles[slot]))
				if texture!=null and texture.get_image().get_data()==frozen.get_data(): matched.append(slot)
			check(matched.size()==1,"Exactly one frozen authored source displayed "+gear+str(n))
			var index: int=matched[0] if matched.size()==1 else ideal_index
			var boundary_rounding: bool=abs(time/.14-round(time/.14))<0.000001 and abs(player.phase-time)<0.000001 and index==(ideal_index+5)%6
			check(index==ideal_index or boundary_rounding,"Ideal movement slot or adjacent exact-boundary rounding "+gear+str(n))
			check(abs(player.phase-time)<0.000001,"Physical-distance phase matches prescribed time "+gear+str(n))
			var file: String=str(pack.states[0].frameFiles[index])
			var source := Image.load_from_file(file)
			check(texture.get_meta("crew_pivot")==Vector2(128,224),"Candidate physicalpivot")
			check(texture.get_meta("crew_standing_height")==148.0,"Candidate physicalruler")
			check(texture.get_meta("crew_water_kind")=="carry" and not texture.get_meta("crew_water_pose"),"Dry carrying source")
			seen[index]=true;board.previous=prior;board.candidate=texture;board.time=time;board.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var name: String=gear+"-%03d"%n
			check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Actual nativecapture")
			check(source.save_png(OUT+name+"-source.png")==OK,"Exact sourcecapture")
			records.append({"name":name,"gear":gear,"time":time,"sourceIndex":index,"physicalPosition":position,"source":file,"playerPhase":player.phase})
		check(seen.size()==6,"All six phases and loop wraps observed")
	var file := FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"\t"));file.close()
	print("VELD EAST MASTER MOTION: %d checks,%d failures;104native presentations"%[checks,failures]);quit(1 if failures else 0)
