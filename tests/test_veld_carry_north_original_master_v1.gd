extends SceneTree
const BARE := "res://character/veld-carry-north-original-master-v1/bare-manifest.json"
const HELMET := "res://character/veld-carry-north-original-master-v1/helmet-manifest.json"
const OLD_BARE := "res://character/veld-carry-north-original-master-v1/baseline-bare-manifest.json"
const OLD_HELMET := "res://character/veld-carry-north-original-master-v1/baseline-helmet-manifest.json"
const OUT := "res://output/veld-carry-north-original-master-v1/"
var checks := 0
var failures := 0
var records: Array = []
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
class Board extends Node2D:
	var previous: Texture2D
	var candidate: Texture2D
	func _draw() -> void:
		draw_rect(Rect2(0,0,760,600),Color("202a30"))
		var heights := [47.0,93.0,148.0]
		var anchors := [70.0,250.0,535.0]
		for row in range(2):
			var tex: Texture2D=previous if row==0 else candidate
			if tex==null: continue
			for i in range(3):
				var scale: float=heights[i]/148.0
				var foot := Vector2(anchors[i],285.0+row*280.0)
				draw_line(foot+Vector2(-60,0),foot+Vector2(60,0),Color("46545c"))
				draw_texture_rect(tex,Rect2(foot-Vector2(128,224)*scale,Vector2(256,256)*scale),false)
				draw_string(ThemeDB.fallback_font,Vector2(anchors[i]-60,22+row*280),"Previous" if row==0 else "Shared",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init() -> void: call_deferred("run")
func run() -> void:
	check(OS.get_environment("APPDATA").contains("veld-north-carry-original-scratch"),"Scratch profile required")
	if failures: quit(1); return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	root.size=Vector2i(760,600);root.content_scale_size=Vector2i.ZERO
	var board := Board.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;root.add_child(board)
	var player=load("res://scripts/crew_sprite_player.gd").new();player.load_manifest(BARE)
	check(player.load_equipment_manifest("diving-helmet",HELMET),"Shared equipment loaded")
	var baseline=load("res://scripts/crew_sprite_player.gd").new();baseline.load_manifest(OLD_BARE)
	check(baseline.load_equipment_manifest("diving-helmet",OLD_HELMET),"Original body family loaded")
	for gear in ["bare","helmet"]:
		var equipment: String="" if gear=="bare" else "diving-helmet"
		var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BARE if gear=="bare" else HELMET))
		for state in pack.states:
			var action: String=state.id
			var cycle: float=player.cycle_seconds(action,equipment)
			var expected_cycle := 0.0
			for duration in state.frameDurationsMs: expected_cycle+=float(duration)/1000.0
			check(is_equal_approx(cycle,expected_cycle),"Original cycle retained")
			var seen := {}
			for n in range(int(ceil(cycle*30.0))+3):
				var time: float=n/30.0
				var supplied_elapsed: float=fmod(time,cycle) if state.loop else time
				var texture: Texture2D=player.frame_at_elapsed(action,supplied_elapsed,equipment)
				var prior: Texture2D=baseline.frame_at_elapsed(action,supplied_elapsed,equipment)
				var remaining: float=fmod(time,cycle) if state.loop else time
				var index: int=state.frameFiles.size()-1
				for slot in range(state.frameFiles.size()):
					var duration: float=float(state.frameDurationsMs[slot])/1000.0
					if remaining<duration: index=slot;break
					remaining-=duration
				var source := Image.load_from_file(state.frameFiles[index])
				check(texture!=null and texture.get_image().get_data()==source.get_data(),"Actual source clock slot")
				check(texture.get_meta("crew_pivot")==Vector2(128,224),"Physical pivot")
				check(texture.get_meta("crew_standing_height")==148.0,"Physical ruler")
				check(not texture.get_meta("crew_water_pose"),"Dry pose metadata")
				seen[index]=true;board.previous=prior;board.candidate=texture;board.queue_redraw()
				await process_frame;await RenderingServer.frame_post_draw
				var name: String=gear+"-"+action+"-%03d"%n
				check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native capture")
				check(source.save_png(OUT+name+"-source.png")==OK,"Source capture")
				records.append({"name":name,"gear":gear,"action":action,"time":time,"sourceIndex":index,"source":state.frameFiles[index]})
			check(seen.size()==state.frameFiles.size(),"All source slots observed")
		for join in [["unload-north",.52,"idle-north",0.0],["pickup-north",0.0,"idle-north",0.0],["pickup-north",.52,"carry-start-north",0.0],["carry-start-north",.32,"carry-north",0.0],["carry-stop-north",.32,"pickup-north",.52]]:
			check(player.frame_at_elapsed(join[0],join[1],equipment).get_image().get_data()==player.frame_at_elapsed(join[2],join[3],equipment).get_image().get_data(),"Exact lifecycle source join")
	var file := FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"\t"));file.close()
	print("VELD ORIGINAL NORTH CARRY FAMILY: %d checks,%d failures;%dnative presentations"%[checks,failures,records.size()]);quit(1 if failures else 0)
