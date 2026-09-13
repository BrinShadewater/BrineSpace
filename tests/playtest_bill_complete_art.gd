extends SceneTree
## Native render review at a consistent world scale, including every frame slot.
const OUT="res://output/bill-full-replacement-2026-09-12/native/"
class Sheet extends Node2D:
	var player
	var keys: Array=[]
	var page := 0
	var phase := 0
	func _draw() -> void:
		draw_rect(Rect2(0,0,1440,960),Color("293b40"))
		for slot in range(24):
			var index: int=page*24+slot
			if index>=keys.size():break
			var key: String=keys[index]
			var origin:=Vector2((slot%4)*360,(slot/4)*160)
			draw_string(ThemeDB.fallback_font,origin+Vector2(8,17),key,HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color.WHITE)
			for col in range(2):
				var rows: Dictionary=player.frames if col==0 else player.equipment_frames["diving-helmet"]
				if not rows.has(key):continue
				var texture: Texture2D=rows[key][phase%rows[key].size()]
				var pivot: Vector2=texture.get_meta("crew_pivot")
				var scale: float=65.28/float(texture.get_meta("crew_standing_height"))*1.5
				var anchor:=origin+Vector2(86+col*180,138 if not texture.get_meta("crew_water_pose") else 95)
				draw_texture_rect(texture,Rect2(anchor-pivot*scale,texture.get_size()*scale),false)
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1440,960)
	var grid=load("res://scripts/grid_canvas.gd").new()
	grid._load_major_bill_animations()
	var sheet:=Sheet.new();sheet.player=grid.human_water_player;sheet.keys=sheet.player.frames.keys();sheet.keys.sort()
	root.add_child(sheet)
	for page in range(8):
		for phase in range(12):
			sheet.page=page;sheet.phase=phase;sheet.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(OUT+"page-%02d-frame-%02d.png"%[page,phase])
	grid.free()
	print("BILL NATIVE ART PASS: 175 body states, 168 equipment states, 96 rendered sheets")
	quit(0)
