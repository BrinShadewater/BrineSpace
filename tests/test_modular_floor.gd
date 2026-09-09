extends SceneTree
const Floor=preload("res://rooms/whole-room/modular_floor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Editor=preload("res://scripts/room_layout_editor.gd")
class SurfaceCanvas extends Node2D:
	var reference:=false
	var corridor:=false
	var q:=0
	var values: Dictionary={}
	var source_path:=Floor.SCIENCE
	var shape:="corridor"
	func _draw() -> void:
		draw_rect(Rect2(0,0,512,512),Color("0b171e"))
		draw_set_transform(Vector2(256,256))
		if not corridor: draw_rect(Rect2(-192,-192,384,384),Color("343b45"))
		if reference:
			if corridor:
				var points:=Floor.footprint(true,q,shape); var uv:=PackedVector2Array()
				for point in points: uv.append((preload("res://tools/modular_room_geometry.gd").turn(point,-q)+Vector2.ONE*192)/384)
				draw_polygon(points,PackedColorArray([Color.WHITE]),uv,Floor.texture(Floor.DECK))
			else:
				var tex:=Floor.texture(source_path)
				var source_size:=tex.get_size()/4
				for y in range(8):
					for x in range(8):
						var at=values.get("tile/%d/%d"%[x,y],[x%4,y%4])
						draw_texture_rect_region(tex,Rect2(-192+x*48,-192+y*48,48,48),Rect2(Vector2(at[0],at[1])*source_size,source_size),Color(1,1,1,0.42))
		else: Floor.draw(self,values,corridor,q,1.0 if corridor else 0.42,Vector2.ZERO,1.0,source_path,shape)
func _init() -> void: call_deferred("run")
func frame() -> void: await process_frame; RenderingServer.force_draw()
func run() -> void:
	DirAccess.make_dir_recursive_absolute("res://output/tiled-floor-pilot")
	root.size=Vector2i(512,512)
	var surface:=SurfaceCanvas.new(); root.add_child(surface)
	var comparisons: Array=[]
	for corridor in [false,true]:
		for q in range(4):
			surface.corridor=corridor; surface.q=q
			surface.values={"floor/finish":Floor.DECK} if corridor else {}
			surface.reference=true; surface.queue_redraw(); await frame()
			var before:=root.get_texture().get_image()
			surface.reference=false; surface.queue_redraw(); await frame()
			var after:=root.get_texture().get_image(); var maximum:=0.0; var changed:=0
			for y in range(512):
				for x in range(512):
					var a:=before.get_pixel(x,y); var b:=after.get_pixel(x,y)
					var delta:=maxf(absf(a.r-b.r),maxf(absf(a.g-b.g),absf(a.b-b.b)))
					maximum=maxf(maximum,delta)
					if delta>0.012: changed+=1
			comparisons.append({"corridor":corridor,"rotation":q,"max":maximum,"changed_pixels":changed})
			assert(changed<300,"Explicit legacy floor stays visually equivalent: "+str(comparisons[-1]))
			after.save_png("res://output/tiled-floor-pilot/default-%s-%d.png"%[corridor,q])
	var values: Dictionary={"floor/material/3/3":3}
	var batches:=Floor.meshes(values,false); assert(batches.size()==2)
	var count:=Floor.builds
	for i in range(100): Floor.meshes(values,false)
	assert(Floor.builds==count,"Unchanged floors reuse mesh geometry")
	values["light/north"]=[80,-190]; Floor.meshes(values,false)
	assert(Floor.builds==count,"Lighting and prop edits cannot rebuild a base floor")
	surface.queue_free(); await process_frame
	root.size=Vector2i(1600,1000)
	Store.path="user://tiled-floor-test.json"; Store.defaults_path="user://absent-floor-defaults.json"; Store.loaded=true; Store.data={}
	var e=Editor.open(root); await process_frame
	var tools=e.floor_tools
	assert(e.entries[e.index].room=="research_lab")
	e.layer=1; e.rebuild_list(); assert(tools.visible)
	tools.mode.select(3); tools.brush.select(3)
	var original: Dictionary=e.draft.duplicate(true)
	var press:=InputEventMouseButton.new(); press.button_index=MOUSE_BUTTON_LEFT; press.pressed=true
	press.position=e.canvas.origin()+Vector2(-72,24)*e.canvas.factor(); e.canvas_input(press)
	var motion:=InputEventMouseMotion.new(); motion.position=e.canvas.origin()+Vector2(72,72)*e.canvas.factor(); e.canvas_input(motion)
	var release:=InputEventMouseButton.new(); release.button_index=MOUSE_BUTTON_LEFT; release.position=motion.position; e.canvas_input(release)
	assert(e.history.size()==1 and e.draft!=original,"Rectangle uses one undo step")
	var painted: Dictionary=e.draft.duplicate(true)
	e.undo(); assert(e.draft==original); e.redo(); assert(e.draft==painted)
	tools.seed.value=47; tools.vary(); var varied:=Floor.meshes(e.draft,false)
	var variant_builds:=Floor.builds; Floor.meshes(e.draft,false); assert(Floor.builds==variant_builds)
	e.save_layout(); assert(Store.positions(e.entries[e.index].asset,0).get("floor/seed")==47)
	e.show_guides=false; e.canvas.queue_redraw(); await frame()
	root.get_texture().get_image().save_png("res://output/tiled-floor-pilot/editor-research.png")
	for i in range(e.entries.size()):
		if e.entries[i].room=="corridor": e.switch_room(i); break
	e.layer=1; e.rebuild_list(); assert(not e.layers.is_item_disabled(1) and e.entities().size()==16)
	tools.mode.select(2); tools.brush.select(2)
	press.position=e.canvas.origin()+Vector2(24,24)*e.canvas.factor(); e.canvas_input(press)
	assert(Floor.tile_material(e.draft,Vector2i(4,4))==2)
	assert(e.history.size()==1,"Flood fill is one undo step")
	for y in range(8):
		for x in range(8):
			if Vector2i(x,y) not in tools.valid_cells(): assert(not e.draft.has(Floor.material_key(Vector2i(x,y))))
	e.save_layout(); e.canvas.queue_redraw(); await frame()
	root.get_texture().get_image().save_png("res://output/tiled-floor-pilot/editor-corridor.png")
	# Every pilot material survives disk reload independently of decoration/prop state.
	Store.loaded=false; Store.data={}; e.load_room(); e.layer=1; e.rebuild_list()
	assert(Floor.tile_material(e.draft,Vector2i(4,4))==2)
	e.draft["locked/tile/4/4"]=true
	tools.mode.select(1); tools.brush.select(3); e.canvas_input(press); e.canvas_input(release)
	assert(Floor.tile_material(e.draft,Vector2i(4,4))==2,"Painting respects locked tiles")
	tools.reset_floor(); assert(Floor.tile_material(e.draft,Vector2i(4,4))==0)
	e.undo(); assert(Floor.tile_material(e.draft,Vector2i(4,4))==2)
	e.close_editor(); await process_frame
	var file:=FileAccess.open("res://output/tiled-floor-pilot/parity.json",FileAccess.WRITE); file.store_string(JSON.stringify(comparisons,"\t")); file.close()
	print("TILED FLOOR PASS: default pixel parity, rotation/clipping, cache reuse, rectangle, undo/redo, seed, save, corridor fill")
	quit()
