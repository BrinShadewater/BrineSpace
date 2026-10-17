extends SceneTree
const Original=preload("res://scripts/room_asset_library.gd")
const MeshBuilder=preload("res://scripts/library_base_triangles.gd")
class Paint extends Node2D:
	var painter:CanvasItem=self
	var prop:Dictionary
	var candidate:=false
	var mesh:Dictionary={}
	func _draw():
		draw_set_transform(Vector2(160.375,190.125),0,Vector2(.91,1.03))
		if candidate:MeshBuilder.draw(self,mesh,prop.library_texture)
		else:Original.draw_base(self,prop)
var pairs:=0
var failures:=0
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(320,320)
	var im:=Image.create(64,64,false,Image.FORMAT_RGBA8)
	for y in range(64):
		for x in range(64):im.set_pixel(x,y,Color(float(x)/63.0,float(y)/63.0,.4,float((x+y)%4)/3.0))
	var texture:=ImageTexture.create_from_image(im)
	var views:Array=[];var paints:Array=[]
	for mode in range(2):
		var viewport:=SubViewport.new();viewport.size=Vector2i(320,320);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport);views.append(viewport)
		var canvas:=Paint.new();canvas.candidate=mode==1;canvas.modulate=Color(.8,.9,1,.7);viewport.add_child(canvas);paints.append(canvas)
	var flood:=ShaderMaterial.new();flood.shader=preload("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",190.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
	for mirrored in [false,true]:
		for floor_piece in [false,true]:
			for station in [false,true]:
				for size in [Vector2(90,140),Vector2(180,180),Vector2(130.7,100.3)]:
					for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
						for wet in [false,true]:
							var reg:Dictionary={"width":64,"height":64,"pivot":Vector2(32,64),"pieces":[PackedVector2Array([Vector2(0,0),Vector2(64,0),Vector2(64,64),Vector2(0,64)]),PackedVector2Array([Vector2(10,20),Vector2(50,10),Vector2(40,50),Vector2(30,30),Vector2(0,40)])]}
							if mirrored:reg=Original.mirror_registration(reg)
							var prop:Dictionary={"id":"library/sp-fixture" if station else "library/fixture","registration":reg,"rect":Rect2(-size*.5,size),"floor_piece":floor_piece,"library_texture":texture}
							for canvas in paints:canvas.prop=prop;canvas.texture_filter=filter;canvas.material=flood if wet else null;canvas.mesh=MeshBuilder.build(prop) if canvas.candidate else {};canvas.queue_redraw()
							await process_frame;await RenderingServer.frame_post_draw
							pairs+=1
							var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
							if a.get_data()!=b.get_data():
								failures+=1;print("MISMATCH ",mirrored," ",floor_piece," ",station," ",size," ",filter," ",wet)
								if failures==1:a.save_png("user://original.png");b.save_png("user://candidate.png")
	var ids:Array=[]
	for id in Original.entries():
		if not str(id).begins_with("library/sp-"):continue
		var data:Dictionary=Original.entries()[id].data
		if data.has("drone_dock") or data.has("aquarium"):continue
		ids.append(id)
	ids.sort_custom(func(a,b):return Original.entries()[a].data.pieces.size()>Original.entries()[b].data.pieces.size())
	var selected:Array=[];var sources:Dictionary={}
	for id in ids:
		var source:String=Original.entries()[id].data.source
		if sources.has(source):continue
		var prop:Dictionary=Original.template(id).duplicate(true)
		if prop.is_empty():continue
		sources[source]=true;selected.append(id)
		prop.rect.position=-prop.rect.size*.5
		for scale_value in [.73,1.0]:
			for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
				for wet in [false,true]:
					for canvas in paints:canvas.prop=prop;canvas.scale=Vector2.ONE*scale_value;canvas.texture_filter=filter;canvas.material=flood if wet else null;canvas.mesh=MeshBuilder.build(prop) if canvas.candidate else {};canvas.queue_redraw()
					await process_frame;await RenderingServer.frame_post_draw;pairs+=1
					var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
					if not a.get_used_rect().has_area() or a.get_data()!=b.get_data():
						failures+=1;print("ART_MISMATCH ",id," ",scale_value," ",filter," ",wet)
		if selected.size()>=8:break
	print("ACTUAL_ART ",JSON.stringify(selected))
	FileAccess.open("user://context.json",FileAccess.WRITE).store_string(JSON.stringify({"raster_pairs":pairs,"failures":failures,"actual_props":selected}))
	for view in views:view.queue_free()
	await process_frame
	print("BASE_MESH ",pairs," pairs, ",failures," failures");quit(1 if failures else 0)
