extends SceneTree
## Native candidate comparison only. No production dispatch or save changes.
var destination:=""
var failures:=0
class MedFootPanel extends Node2D:
	var room
	var quarter:=0
	var world_scale:=2.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,1000,1040),Color("17232c"))
		room.configure_embedded(quarter,[],false,0.2)
		room.render_into(self,Vector2(500,540),world_scale)
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): destination=arg.trim_prefix("--output=")
	call_deferred("run")
func check(value: bool,message: String) -> void:
	if not value:
		failures+=1
		push_error(message)
func run() -> void:
	if not destination.begins_with("res://output/") or destination.contains("..") or DirAccess.dir_exists_absolute(destination):
		push_error("Use a new output directory")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(destination)
	root.size=Vector2i(1000,1040)
	root.content_scale_size=root.size
	var baseline=load("res://rooms/whole-room/med_bay_view.gd").new()
	var candidate=load("res://rooms/whole-room/med_bed_foot_edge_study.gd").new()
	for room in [baseline,candidate]:
		room.embedded=true
		room.hide()
		root.add_child(room)
	# Reconstruct only the former two diagonal edges for a stable old/new comparison.
	for i in range(2):
		var offset:=Vector2(0,457*i)
		baseline.life_items[i].outline.erase(Vector2(384,494)+offset)
		baseline.life_items[i].outline.erase(Vector2(229,494)+offset)
	baseline.rebuild()
	var panel:=MedFootPanel.new()
	root.add_child(panel)
	if "--negative-footboard-cut" in OS.get_cmdline_user_args():
		for i in range(2):
			var offset:=Vector2(0,457*i)
			var outline: Array=candidate.life_items[i].outline
			outline.erase(Vector2(229,494)+offset)
			outline.insert(outline.find(Vector2(229,543)+offset),Vector2(229,494)+offset)
		candidate.rebuild()
	var retained:=0
	for i in range(2):
		var offset:=Vector2(0,457*i)
		var original:=PackedVector2Array(baseline.life_items[i].outline)
		var revised:=PackedVector2Array(candidate.life_items[i].outline)
		for x in range(232,382,3):
			for y in range(496,541,3):
				var point:=Vector2(x,y)+offset
				check(Geometry2D.is_point_in_polygon(point,original) and Geometry2D.is_point_in_polygon(point,revised),"Footboard/base retention at "+str(point))
				retained+=1
		for point in [Vector2(225,520),Vector2(388,510)]:
			check(Geometry2D.is_point_in_polygon(point+offset,original) and not Geometry2D.is_point_in_polygon(point+offset,revised),"Candidate removes targeted floor wedge")
		check(baseline.life_items[i].rect==candidate.life_items[i].rect,"Ground footprint unchanged")
	var captures:=0
	for q in range(4):
		panel.quarter=q
		for scale in [2.0,0.7]:
			panel.world_scale=scale
			for name in ["baseline","candidate"]:
				panel.room=baseline if name=="baseline" else candidate
				panel.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				check(root.get_texture().get_image().save_png(destination.path_join("%s-q%d-scale%s.png"%[name,q,scale]))==OK,"Save native comparison")
				captures+=1
	print("MED FOOT STUDY: ",retained," interior retention points, four excluded wedge points, ",captures," native full-room captures; ",failures," failures; silhouette/visual review remains separate")
	quit(1 if failures else 0)
