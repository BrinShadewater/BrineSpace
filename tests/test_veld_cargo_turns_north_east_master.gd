extends SceneTree
const CANDIDATE_BARE := "res://character/veld-cargo-turns-master-family-v1/north-east-candidate-v5/bare-manifest.json"
const CANDIDATE_HELMET := "res://character/veld-cargo-turns-master-family-v1/north-east-candidate-v5/helmet-manifest.json"
const BASELINE_BARE := "res://character/veld-carry-turn-north-east-consistent-v1/bare-manifest.json"
const BASELINE_HELMET := "res://character/veld-unified-turn-helmet-v1/quarter-helmet-manifest.json"
const OUT := "res://output/veld-cargo-turns-north-east-v5-native/"
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
				var foot := Vector2(anchors[i]-time*4.0,285.0+row*280.0)
				draw_line(foot+Vector2(-60,0),foot+Vector2(60,0),Color("46545c"))
				draw_texture_rect(tex,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
				draw_string(ThemeDB.fallback_font,Vector2(anchors[i]-60,22+row*280),"Selected" if row==0 else "Candidate",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init() -> void: call_deferred("run")
func run() -> void:
	check(OS.get_environment("APPDATA").contains("veld-cargo-turn-master-scratch"),"Scratch owner profile required")
	if failures: quit(1); return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	root.size=Vector2i(760,600);root.content_scale_size=Vector2i.ZERO
	var board := Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(board)
	for case in [{"gear":"bare","action":"north-east"},{"gear":"bare","action":"east-north"},{"gear":"helmet","action":"north-east"},{"gear":"helmet","action":"east-north"}]:
		var gear: String=case.gear
		var action: String=case.action
		var baseline=load("res://scripts/crew_sprite_player.gd").new()
		baseline.load_manifest("res://character/veld-carry-turn-north-west-consistent-v1/bare-manifest.json")
		baseline.load_manifest("res://character/veld-carry-turn-east-south-consistent-v1/bare-manifest.json",true)
		baseline.load_manifest("res://character/veld-carry-turn-south-west-consistent-v1/bare-manifest.json",true)
		baseline.load_manifest(BASELINE_BARE,true)
		check(baseline.load_equipment_manifest("diving-helmet",BASELINE_HELMET),"Baseline paired equipment")
		var player=load("res://scripts/crew_sprite_player.gd").new()
		player.load_manifest(CANDIDATE_BARE)
		check(player.load_equipment_manifest("diving-helmet",CANDIDATE_HELMET),"Candidate paired equipment")
		var equipment: String="" if gear=="bare" else "diving-helmet"
		var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(CANDIDATE_BARE if gear=="bare" else CANDIDATE_HELMET))
		var state: Dictionary={}
		for entry in pack.states:
			if entry.id=="carry-turn-"+action:state=entry
		check(not state.is_empty() and not state.loop,"Finite action source")
		var originals: Array=JSON.parse_string(FileAccess.get_file_as_string("res://character/veld-carry-turn-north-east-consistent-v1/original-states.json"))
		var original: Dictionary={}
		for entry in originals:
			if entry.id==state.id:original=entry
		check(state.frameDurationsMs==original.frameDurationsMs and state.facings==original.facings and state.waterKinds==original.waterKinds and state.depthOffsets==original.depthOffsets,"Original turn metadata retained")
		var seen := {}
		check(is_equal_approx(player.cycle_seconds("carry-turn-"+action,equipment),.8),"Exact800msfinite turn")
		for n in range(26):
			var time: float=n/30.0
			var position := Vector2.ZERO
			var texture: Texture2D=player.frame("carry-turn",action,time,position,equipment)
			var prior: Texture2D=baseline.frame("carry-turn",action,time,position,equipment)
			var index: int=5
			var remaining: float=time
			for slot in range(6):
				var duration: float=float(original.frameDurationsMs[slot])/1000.0
				if remaining<duration: index=slot;break
				remaining-=duration
			var file: String=str(state.frameFiles[index])
			var source := Image.load_from_file(file)
			check(texture!=null and texture.get_image().get_data()==source.get_data(),"Finite action source slot "+gear+str(n))
			check(texture.get_meta("crew_pivot")==Vector2(128,224),"Candidate physicalpivot")
			check(texture.get_meta("crew_standing_height")==148.0,"Candidate physicalruler")
			check(texture.get_meta("crew_water_kind")==str(state.waterKinds[index]) and not texture.get_meta("crew_water_pose"),"Original dry action source metadata")
			seen[index]=true;board.previous=prior;board.candidate=texture;board.time=0.0;board.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var name: String=gear+"-"+action+"-%03d"%n
			check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Actual nativecapture")
			check(source.save_png(OUT+name+"-source.png")==OK,"Exact sourcecapture")
			records.append({"name":name,"gear":gear,"action":action,"time":time,"sourceIndex":index,"physicalPosition":position,"source":file,"playerPhase":player.phase})
		check(seen.size()==6,"All six finite poses observed")
	var file := FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"\t"));file.close()
	print("VELD MASTER NORTH EAST TURNS: %d checks,%d failures;104native presentations"%[checks,failures]);quit(1 if failures else 0)
