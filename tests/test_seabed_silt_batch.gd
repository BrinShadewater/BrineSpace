extends SceneTree
const Candidate=preload("res://assets/environment/seabed-v1/seabed_background.gd")
class Reference extends "res://assets/environment/seabed-v1/seabed_background.gd":
	func render_still(canvas: CanvasItem, cell_size: float, grid_size: int, layout: Dictionary = {}) -> void:
		prepare()
		var bounds := Rect2(Vector2.ZERO, Vector2.ONE * cell_size * grid_size)
		canvas.draw_rect(bounds, Color("09222d"))
		# Let the canvas clip the small fixed set of tiles. Manual viewport culling
		# here used stale transforms during a paused window resize at 1280 pixels.
		var visible := bounds
		if textures.has("silt-plain"):
			var tile_size := cell_size * 3.0
			var first := Vector2i((visible.position / tile_size).floor())
			var last := Vector2i((visible.end / tile_size).ceil())
			for y in range(first.y, last.y):
				for x in range(first.x, last.x):
					# Alternating mirrored repeats join identical edge pixels. No claim
					# that the unmodified source itself is a seamless material.
					var tile := Rect2(Vector2(x, y) * tile_size, Vector2.ONE * tile_size)
					var uv:=PackedVector2Array([Vector2.ZERO,Vector2.RIGHT,Vector2.ONE,Vector2.DOWN])
					for i in range(uv.size()):
						if x%2!=0:uv[i].x=1.0-uv[i].x
						if y%2!=0:uv[i].y=1.0-uv[i].y
					canvas.draw_polygon(PackedVector2Array([tile.position,tile.position+Vector2(tile.size.x,0),tile.end,tile.position+Vector2(0,tile.size.y)]),PackedColorArray([Color(.49,.60,.64)]),uv,textures["silt-plain"])
		sync_site(layout)
		sub_biomes.render_ground(canvas,cell_size,fungi_biome.render_ground)
	
class Painter extends Node2D:
	var renderer
	var size:=96.0
	var grid_size:=41
	func _draw():renderer.render_still(self,size,grid_size,{})
class Fog extends Node2D:
	var size:=96.0
	var grid_size:=41
	func _draw():draw_rect(Rect2(Vector2.ZERO,Vector2.ONE*size*grid_size),Color.WHITE)
var draw_counts:Array=[]
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	var a:=SubViewport.new();var b:=SubViewport.new()
	for vp in [a,b]:vp.size=Vector2i(480,320);vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp)
	var left:=Painter.new();left.renderer=Reference.new();a.add_child(left)
	var right:=Painter.new();right.renderer=Candidate.new();b.add_child(right)
	var visibility=preload("res://scripts/underwater_visibility.gd").new()
	visibility.mask.fill(Color(0,1,.2,1));visibility.mask_texture.update(visibility.mask)
	var material:ShaderMaterial=visibility.material
	var lights:=PackedVector4Array();lights.resize(48);lights[0]=Vector4(4,3,9,1)
	var directions:=PackedVector4Array();directions.resize(48);directions[0]=Vector4(1,0,0,0)
	material.set_shader_parameter("lights",lights);material.set_shader_parameter("directions",directions);material.set_shader_parameter("light_count",1)
	var glows:=PackedVector4Array();glows.resize(32);glows[0]=Vector4(6,4,3,.7)
	var colors:=PackedColorArray();colors.resize(32);colors[0]=Color(.3,.8,.7,1)
	material.set_shader_parameter("glows",glows);material.set_shader_parameter("glow_colors",colors);material.set_shader_parameter("glow_count",1)
	material.set_shader_parameter("silt",Vector4(3,3,.7,0))
	var overlays:Array=[]
	for vp in [a,b]:
		var overlay:=Fog.new();overlay.material=material;vp.add_child(overlay);overlays.append(overlay)
	for quality in [0,1,2]:
		preload("res://scripts/title_settings.gd").effects_quality=quality
		var atmosphere:Dictionary=preload("res://scripts/title_settings.gd").atmosphere()
		material.set_shader_parameter("shafts",atmosphere.shafts);material.set_shader_parameter("caustic_light",atmosphere.caustics);material.set_shader_parameter("depth_tint",atmosphere.tint);material.set_shader_parameter("snow_boost",atmosphere.snow)
		for motion in [0.0,1.0]:
			material.set_shader_parameter("motion",motion)
			for clock in [0.0,17.23]:
				material.set_shader_parameter("clock",clock)
				for size in [64.125,96.0]:
					for grid in [41,44]:
						for zoom in [.23,1.0]:
							for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
								for offset in [Vector2.ZERO,Vector2(3.0,3.0),Vector2(20.75,18.25)]:
									material.set_shader_parameter("cell_size",size)
									for overlay in overlays:overlay.size=size;overlay.grid_size=grid;overlay.scale=Vector2.ONE*zoom;overlay.position=-offset*size*zoom+Vector2(.37,.61);overlay.queue_redraw()
									for painter in [left,right]:painter.size=size;painter.grid_size=grid;painter.scale=Vector2.ONE*zoom;painter.position=-offset*size*zoom+Vector2(.37,.61);painter.texture_filter=filter;painter.queue_redraw()
									await process_frame;await RenderingServer.frame_post_draw
									var old_calls:=RenderingServer.viewport_get_render_info(a.get_viewport_rid(),RenderingServer.VIEWPORT_RENDER_INFO_TYPE_CANVAS,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME)
									var new_calls:=RenderingServer.viewport_get_render_info(b.get_viewport_rid(),RenderingServer.VIEWPORT_RENDER_INFO_TYPE_CANVAS,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME)
									check(new_calls<old_calls,"Production fog stack keeps native draw-call reduction")
									draw_counts.append([old_calls,new_calls])
									var reference:=a.get_texture().get_image();var candidate:=b.get_texture().get_image()
									check(reference.get_data()==candidate.get_data(),"Exact silt batch size=%s grid=%s zoom=%s filter=%s offset=%s"%[size,grid,zoom,filter,offset])
									if failures==1:reference.save_png("user://reference-failure.png");candidate.save_png("user://candidate-failure.png")
	a.get_texture().get_image().save_png("user://reference.png");b.get_texture().get_image().save_png("user://candidate.png")
	a.queue_free();b.queue_free();await process_frame
	FileAccess.open("user://result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"draw_counts":draw_counts}))
	print("SEABED_SILT_BATCH ",checks," checks ",failures," failures");quit(1 if failures else 0)
