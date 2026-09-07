extends SceneTree
const Kit=preload("res://assets/floor-utilities-v1/floor_sprites.gd")
const OUT="res://assets/floor-utilities-v1"
func _init() -> void: call_deferred("run")
class Canvas extends Node2D:
	var assembled:=false
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,1000),Color("18292f"))
		draw_string(ThemeDB.fallback_font,Vector2(24,34),"BRINESPACE / FLOOR UTILITY DECORATIONS",HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color("c7d1c4"))
		if assembled:
			for row in range(4):
				var family: String=["wire","cable","mat","pipe"][row]
				var origin:=Vector2(80,90+row*216)
				draw_rect(Rect2(origin,Vector2(1120,190)),Color("34454b"))
				for x in range(80,1200,80): draw_line(Vector2(x,origin.y),Vector2(x,origin.y+190),Color("253b42"),1)
				draw_string(ThemeDB.fallback_font,origin+Vector2(18,26),family.to_upper()+" / 3x floor placement review",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color("b8c2b4"))
				var straight:=family+"_straight"
				var end_piece:=family+("_elbow" if family=="pipe" else "_t")
				var center:=origin+Vector2(170,90)
				Kit.draw(self,straight,center,3)
				var joint:=Kit.port(straight,"east",center,3)
				var next:=Kit.center_for_port(end_piece,"west",joint,3)
				Kit.draw(self,end_piece,next,3)
				if family!="pipe":
					var far:=Kit.port(end_piece,"east",next,3)
					Kit.draw(self,straight,Kit.center_for_port(straight,"west",far,3),3)
				else:
					Kit.draw(self,"pipe_channel",origin+Vector2(860,98),3)
					Kit.draw(self,"pipe_channel_cover",origin+Vector2(966,98),3)
			return
		var i:=0
		for id in Kit.catalog():
			var origin:=Vector2(16+(i%3)*422,64+(i/3)*183)
			draw_rect(Rect2(origin,Vector2(402,167)),Color("34454b"))
			draw_line(origin+Vector2(200,32),origin+Vector2(200,143),Color("263a41"),1)
			draw_string(ThemeDB.fallback_font,origin+Vector2(12,23),id,HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color("d0d3c3"))
			Kit.draw(self,id,origin+Vector2(116,91),2)
			Kit.draw(self,id,origin+Vector2(307,91),1)
			draw_string(ThemeDB.fallback_font,origin+Vector2(103,154),"2x",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("96aaa5"))
			draw_string(ThemeDB.fallback_font,origin+Vector2(295,154),"1x",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("96aaa5"))
			i+=1

func run() -> void:
	assert(Kit.catalog().size()==13)
	for id in Kit.catalog():
		var spec: Dictionary=Kit.catalog()[id]
		assert(spec.layer=="floor_under_actors" and not spec.collision)
		assert(Kit.texture(id).get_size()==Vector2(spec.size[0],spec.size[1]))
		for port in spec.ports:
			var target:=Vector2(173,129)
			assert(Kit.port(id,port,Kit.center_for_port(id,port,target)).distance_to(target)<0.001)
	if DisplayServer.get_name()!="headless":
		root.size=Vector2i(1280,1000)
		root.content_scale_size=Vector2i.ZERO
		var canvas:=Canvas.new()
		canvas.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(canvas)
		for assembled in [false,true]:
			canvas.assembled=assembled
			canvas.queue_redraw()
			for frame in range(4): await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(OUT.path_join("floor-layouts.png" if assembled else "preview.png"))
	print("FLOOR UTILITY KIT PASS: 13 textures, floor-layer metadata, connector transforms, native scale/layout review")
	quit()
