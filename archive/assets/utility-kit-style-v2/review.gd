extends SceneTree
const Kit=preload("res://assets/utility-kit-style-v2/utility_sprites.gd")
const OUT="res://assets/utility-kit-style-v2"
var failures:=0
func _init() -> void: call_deferred("run")
class Canvas extends Node2D:
	var assemblies:=false
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,1000),Color("14252d"))
		draw_string(ThemeDB.fallback_font,Vector2(24,32),"BRINESPACE / UTILITY KIT — 20 SOURCE SPRITES",HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color("c4d0c6"))
		if assemblies:
			draw_string(ThemeDB.fallback_font,Vector2(24,60),"Authored connector anchors / 3x detail review / no automatic tiling guarantee",HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color("95a9a5"))
			for row in range(5):
				var family: String=["pipe","duct","tube","power","wire"][row]
				var a:=family+"_straight"
				var b:=family+("_y" if family=="tube" else "_t")
				var center:=Vector2(220,140+row*163)
				Kit.draw(self,a,center,3)
				var joint:=Kit.port(a,"east",center,3)
				var next:=Kit.center_for_port(b,"west",joint,3)
				Kit.draw(self,b,next,3)
				var end:=Kit.port(b,"east",next,3)
				Kit.draw(self,a,Kit.center_for_port(a,"west",end,3),3)
				draw_string(ThemeDB.fallback_font,Vector2(750,center.y),family.to_upper(),HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("c2c9b7"))
			return
		var i:=0
		for id in Kit.catalog():
			var column:=i%4
			var row:=i/4
			var origin:=Vector2(16+column*316,60+row*180)
			draw_rect(Rect2(origin,Vector2(300,165)),Color("213740"))
			draw_string(ThemeDB.fallback_font,origin+Vector2(10,23),id,HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color("cad2c4"))
			Kit.draw(self,id,origin+Vector2(91,94),2)
			Kit.draw(self,id,origin+Vector2(237,94),1)
			draw_string(ThemeDB.fallback_font,origin+Vector2(72,155),"2x",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("829c9b"))
			draw_string(ThemeDB.fallback_font,origin+Vector2(217,155),"1x",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("829c9b"))
			i+=1

func run() -> void:
	var catalog:=Kit.catalog()
	assert(catalog.size()==20)
	for id in catalog:
		var entry: Dictionary=catalog[id]
		var tex:=Kit.texture(id)
		assert(tex.get_width()==entry.size[0] and tex.get_height()==entry.size[1])
		for name in entry.ports:
			var target:=Vector2(193,241)
			assert(Kit.port(id,name,Kit.center_for_port(id,name,target)).distance_to(target)<0.001)
	if DisplayServer.get_name()!="headless":
		root.size=Vector2i(1280,1000)
		root.content_scale_size=Vector2i.ZERO
		var canvas:=Canvas.new()
		canvas.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(canvas)
		for assembled in [false,true]:
			canvas.assemblies=assembled
			canvas.queue_redraw()
			for frame in range(4): await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(OUT.path_join("assemblies.png" if assembled else "preview.png"))
	print("UTILITY KIT PASS: 20 textures, all connector anchor transforms, native 1x/2x and assembly review")
	quit()
