extends SceneTree
class Review extends Node2D:
	var textures: Array=[]
	var label := ""
	func _draw() -> void:
		draw_rect(Rect2(0,0,1000,800),Color("263139"))
		for i in range(textures.size()):
			var x: float=(i%3)*330+10
			var y: float=(i/3)*185+45
			var texture: Texture2D=textures[i]
			for size in [1.0,65.28/148.0]:
				var pivot: Vector2=texture.get_meta("crew_pivot")
				var anchor:=Vector2(x+(105 if size==1.0 else 270),y+150)
				draw_line(anchor+Vector2(-45,0),anchor+Vector2(45,0),Color("62747a"))
				draw_texture_rect(texture,Rect2(anchor-pivot*size,texture.get_size()*size),false)
			draw_string(ThemeDB.fallback_font,Vector2(x,y-12),["Bill","Veld","Branforth"][i%3]+" / "+["south","east","north","west"][i/3]+" / "+label,HORIZONTAL_ALIGNMENT_LEFT,-1,16)
func _init() -> void: call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1000,800);root.content_scale_size=Vector2i.ZERO
	var grid=load("res://scripts/grid_canvas.gd").new()
	grid._load_major_bill_animations();grid._load_replacement_crew_animations()
	var players=[grid.human_water_player,grid.veld_player,grid.branforth_player]
	var review:=Review.new();review.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(review)
	var destination:="res://output/crew-walk-v2-native/"
	DirAccess.make_dir_recursive_absolute(destination)
	for tick in range(120):
		var time:=tick*0.05
		var state:="idle" if tick<15 or tick>=105 else "walk"
		review.label=state;review.textures=[]
		for direction in ["south","east","north","west"]:
			for p in players:
				# Each cell is independently sampled from the production-loaded clip.
				var key: String=state+"-"+direction
				var elapsed: float=fposmod(maxf(0,time-0.75),p.cycle_seconds(key))
				review.textures.append(p.frame_at_elapsed(key,elapsed))
		review.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(destination+"frame-%03d.png"%tick)
	grid.free();print("CREW WALK V2 NATIVE: 120 production-loader transition captures")
	quit()
