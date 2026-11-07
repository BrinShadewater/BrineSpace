extends SceneTree
## Compare selected runtime frames against the independently reconstructed local repair.
const OUT="res://output/bill-walk-repair-2026-09-12/"
class Review extends Node2D:
	var selected: Array=[]
	var distance := 0.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,1000,760),Color("293b40"))
		draw_string(ThemeDB.fallback_font,Vector2(110,25),"Selected runtime walk",HORIZONTAL_ALIGNMENT_LEFT,-1,20)
		draw_string(ThemeDB.fallback_font,Vector2(610,25),"Rebuilt local reference",HORIZONTAL_ALIGNMENT_LEFT,-1,20)
		for row in range(4):
			var floor_y:=200.0+row*175
			var heading:=1.0 if row<2 else -1.0
			for col in range(2):
				var anchor:=Vector2(230+col*500,floor_y)
				draw_line(Vector2(col*500,floor_y),Vector2(col*500+480,floor_y),Color("839597"))
				for mark in range(11):
					var x:=col*500+fposmod(mark*48-distance*384*2*heading,480)
					draw_line(Vector2(x,floor_y),Vector2(x,floor_y+7),Color("839597"))
				var texture: Texture2D=selected[row*2+col]
				var scale: float=65.28/float(texture.get_meta("crew_standing_height"))*2
				draw_texture_rect(texture,Rect2(anchor-texture.get_meta("crew_pivot")*scale,texture.get_size()*scale),false)
			draw_string(ThemeDB.fallback_font,Vector2(8,floor_y-130),("east" if row<2 else "west")+(" / helmet" if row%2 else " / bare"),HORIZONTAL_ALIGNMENT_LEFT,-1,15)
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	root.mode=Window.MODE_WINDOWED;root.content_scale_size=Vector2i(1000,760);root.size=Vector2i(1000,760)
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations()
	var players: Array=[]
	for row in range(4):
		var original=load("res://scripts/crew_sprite_player.gd").new()
		original.frames=grid.human_water_player.frames;original.timing=grid.human_water_player.timing;original.strides=grid.human_water_player.strides;original.equipment_frames=grid.human_equipment_frames
		var candidate=load("res://scripts/crew_sprite_player.gd").new();candidate.load_manifest(OUT+"bare-manifest.json")
		if not candidate.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json"):quit(1);return
		players.append(original);players.append(candidate)
	var review:=Review.new();review.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(review)
	DirAccess.make_dir_recursive_absolute(OUT+"native-selected")
	var failures:=0
	for i in range(60):
		review.distance=i*.04*.08;review.selected.clear()
		for row in range(4):
			var facing: String="east" if row<2 else "west"
			var equipment: String="diving-helmet" if row%2 else ""
			for col in range(2):review.selected.append(players[row*2+col].frame("walk",facing,i*.04,Vector2(review.distance,0),equipment))
			if review.selected[row*2].get_image().get_data()!=review.selected[row*2+1].get_image().get_data():
				failures+=1;push_error("Walk reference mismatch: "+facing+equipment+" sample "+str(i))
		review.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(OUT+"native-selected/frame-%03d.png"%i)
	grid.free()
	print("BILL WALK NATIVE: 240 distance-driven frame comparisons, %d failures"%failures)
	quit(1 if failures else 0)
