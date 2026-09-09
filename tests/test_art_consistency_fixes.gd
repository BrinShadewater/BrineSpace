extends SceneTree
## Native title animation and non-repeating habitat review; source PNGs stay intact.
const Ground = preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const OUT := "res://output/title-consistency/"
func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
class Field extends Control:
	var source: Texture2D
	var meshes := []
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("10242c"))
		for i in range(4):
			var origin := Vector2(285+(i%2)*570,245+(i/2)*470)
			draw_mesh(meshes[i],source,Transform2D(0,Vector2.ONE*42,0,origin))
			draw_string(ThemeDB.fallback_font,origin+Vector2(-230,-195),["Previous / source color","Previous / runtime tint","Continuous field / source color","Continuous field / runtime tint"][i],HORIZONTAL_ALIGNMENT_LEFT,-1,19,Color("c6d6ca"))
func run() -> void:
	assert(DisplayServer.get_name()!="headless","Native rendering required")
	root.gui_disable_input = true
	root.content_scale_size = Vector2i.ZERO
	DirAccess.make_dir_recursive_absolute(OUT)
	var preferences = preload("res://scripts/title_settings.gd")
	preferences.initialized = true
	preferences.reduced_motion = false
	var cover = preload("res://scripts/title_cover.gd").new()
	root.add_child(cover)
	cover.set_process(false)
	for width in [960,1600,2560]:
		root.size = Vector2i(width,roundi(width*672.0/1584.0))
		cover.size = root.size
		cover.elapsed = 0
		cover._process(0)
		await settle()
		var first := root.get_texture().get_image()
		var logo_area := Rect2i(roundi(width*0.24),0,roundi(width*0.53),roundi(width*0.08))
		var logo := first.get_region(logo_area).get_data()
		for phase in [2.0,4.0,6.0]:
			cover._process(2.0)
			await settle()
			var frame := root.get_texture().get_image()
			assert(frame.get_region(logo_area).get_data()==logo,"Logo remains stationary throughout character float")
			assert(frame.save_png(OUT+"title-%d-phase-%d.png"%[width,int(phase)])==OK)
		assert(cover.character.position.y< -2.9,"Independent float reaches its upper extreme")
		assert(first.get_data()!=root.get_texture().get_image().get_data(),"Title animation changes visible pixels")
		preferences.reduced_motion = true
		var frozen := root.get_texture().get_image().get_data()
		cover._process(60)
		await settle()
		assert(frozen==root.get_texture().get_image().get_data(),"Reduced motion freezes all title layers")
		preferences.reduced_motion = false
	cover.free()
	var regions: Array = Ground.REGIONS.duplicate()
	for script in [preload("res://assets/environment/shell-shoal-v1/shell_shoal_view.gd"),preload("res://assets/environment/volcanic-ash-v1/volcanic_ash_view.gd"),preload("res://assets/environment/clay-silt-v1/clay_silt_view.gd"),preload("res://assets/environment/ripple-sand-v1/ripple_sand_view.gd")]:
		regions.append({"center":script.CENTER,"radius":script.RADIUS})
	for region in regions:
		var arrays: Array = Ground.ground_mesh(region.center,region.radius).surface_get_arrays(0)
		var seen := {}
		var uv: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV]
		var colors: PackedColorArray = arrays[Mesh.ARRAY_COLOR]
		for i in range(uv.size()):
			if colors[i].a<0.01: continue
			assert(Rect2(0,0,1,1).has_point(uv[i]),"Visible ground stays inside its source field")
			var key := Vector2i((uv[i]*1000000).round())
			assert(not seen.has(key),"Different ground positions must not sample repeated/mirrored source positions")
			seen[key] = true
	var view := Ground.new()
	view.prepare()
	var field := Field.new()
	root.size = Vector2i(1140,940)
	field.size = root.size
	for index in range(4):
		var arrays: Array = Ground.ground_mesh(Vector2.ZERO,Vector2(5,4)).surface_get_arrays(0)
		var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
		if index<2:
			var old_uv := PackedVector2Array()
			for vertex in vertices:
				var at := Vector2(vertex.x,vertex.y)/4.0
				old_uv.append(Vector2(1-absf(fposmod(at.x,2)-1),1-absf(fposmod(at.y,2)-1)))
			arrays[Mesh.ARRAY_TEX_UV] = old_uv
		if index%2==0:
			var colors: PackedColorArray = arrays[Mesh.ARRAY_COLOR]
			for i in range(colors.size()): colors[i] = Color(1,1,1,colors[i].a)
			arrays[Mesh.ARRAY_COLOR] = colors
		var mesh := ArrayMesh.new()
		mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
		field.meshes.append(mesh)
	root.add_child(field)
	for id in Ground.DEFINITIONS:
		field.source = view.textures[id+"-ground"]
		field.queue_redraw()
		await settle()
		assert(root.get_texture().get_image().save_png(OUT+"ground-comparison-"+id+".png")==OK)
	print("ART FIXES PASS: title motion, stationary logo and reduced motion at three sizes; eleven unique ground fields; seven native source/tint comparisons")
	quit()
