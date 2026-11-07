extends SceneTree
## Isolated native candidate review. Never selects production character art.
const BODY = "res://character/crew-polish-v1/veld-painted-v2/manifest.json"
const HELMET = "res://character/crew-polish-v1/veld-painted-v2-helmet/manifest.json"
const OUT = "res://character/crew-polish-v1/review/native"
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(why)
class Review extends Node2D:
	var player
	var elapsed := 0.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,900),Color("242b2e"))
		var dirs = ["east","west","south","north"]
		for row in range(4):
			for col in range(5):
				var kind: String = ["idle","walk","kneel","repair","stand"][col]
				var key: String = kind+"-"+dirs[row]
				draw_string(ThemeDB.fallback_font,Vector2(col*256+8,row*220+22),key,HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color.WHITE)
				for gear in range(2):
					var t: Texture2D = player.frame_at_elapsed(key,fmod(elapsed,player.cycle_seconds(key)),"diving-helmet" if gear else "")
					var k: float = 65.28/float(t.get_meta("crew_standing_height"))*(1.0 if gear==0 else 2.0)
					var pivot: Vector2 = t.get_meta("crew_pivot")
					var anchor:=Vector2(col*256+55+gear*120,row*220+196)
					draw_line(anchor-Vector2(43,0),anchor+Vector2(43,0),Color("506368"))
					draw_texture_rect(t,Rect2(anchor-pivot*k,t.get_size()*k),false)
func _init() -> void: call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless": quit(2); return
	if not FileAccess.file_exists("res://tools/review_crew_polish.gd.uid"):
		var uid_file = FileAccess.open("res://tools/review_crew_polish.gd.uid",FileAccess.WRITE)
		uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1280,900);root.content_scale_size=Vector2i.ZERO
	var p=preload("res://scripts/crew_sprite_player.gd").new()
	p.load_manifest(BODY)
	check(p.load_equipment_manifest("diving-helmet",HELMET),"Matched equipped timing and registration")
	check(p.frames.size()==20,"Twenty candidate states")
	for key in p.frames:
		var elapsed:=0.0
		for i in range(p.frames[key].size()):
			var d:float=p.timing[key].durations[i]/1000.0
			for gear in ["","diving-helmet"]:
				var row:Array=p.frames[key] if gear.is_empty() else p.equipment_frames[gear][key]
				check(p.frame_at_elapsed(key,elapsed+d*.5,gear)==row[i],"Native phase "+key)
			elapsed+=d
	for d in ["east","west","south","north"]:
		for gear in ["","diving-helmet"]:
			var rows:Dictionary=p.frames if gear.is_empty() else p.equipment_frames[gear]
			for join in [["idle-",0,"kneel-",0],["kneel-",-1,"repair-",0],["repair-",0,"stand-",0],["stand-",-1,"idle-",0]]:
				check(rows[join[0]+d][join[1]].get_image().get_data()==rows[join[2]+d][join[3]].get_image().get_data(),"Shared join "+str(join)+d)
	p.frame("walk","east",1.0,Vector2.ZERO)
	p.frame("walk","east",1.2,Vector2(.02,0))
	var saved:Dictionary=p.snapshot()
	p.frame("walk","east",1.2,Vector2(.02,0))
	check(p.snapshot()==saved,"Paused clock holds")
	p.frame("walk","east",1.4,Vector2(.04,0));p.restore_snapshot(saved)
	check(p.snapshot()==saved,"Playback restore")
	var sheet:=Review.new();sheet.player=p;sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	for i in range(24):
		sheet.elapsed=i/24.0;sheet.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(OUT.path_join("frame-%03d.png"%i))
	var report=FileAccess.open(OUT.path_join("checks.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"nativeCaptures":24,"scope":"Candidate sprite player only; not production selection, room occlusion or world contact acceptance"},"  "))
	print("CREW POLISH checks=",checks," failures=",failures)
	quit(1 if failures else 0)
