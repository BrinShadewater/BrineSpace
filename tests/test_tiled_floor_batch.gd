extends SceneTree
const Fixture=preload("res://tests/test_modular_floor.gd")
const Floor=preload("res://rooms/whole-room/modular_floor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Editor=preload("res://scripts/room_layout_editor.gd")
const IDS=["reactor","life_support","crew_hab","corner","tee_corridor"]
func _init() -> void: call_deferred("run")
func frame() -> void: await process_frame; RenderingServer.force_draw()
func run() -> void:
	DirAccess.make_dir_recursive_absolute("res://output/tiled-floor-batch")
	var profiles: Dictionary={}
	for row in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/floor-profiles-v1/rooms.json")): profiles[row.id]=row
	root.size=Vector2i(512,512)
	var surface:=Fixture.SurfaceCanvas.new(); root.add_child(surface)
	var results: Array=[]
	for id in IDS:
		surface.corridor=id in ["corner","tee_corridor"]; surface.shape=id
		surface.source_path=Floor.SCIENCE if surface.corridor else profiles[id].source
		for q in range(4):
			surface.q=q; surface.reference=true; surface.queue_redraw(); await frame()
			var before:=root.get_texture().get_image()
			surface.reference=false; surface.queue_redraw(); await frame()
			var after:=root.get_texture().get_image(); var changed:=0; var maximum:=0.0
			for y in range(512):
				for x in range(512):
					var a:=before.get_pixel(x,y); var b:=after.get_pixel(x,y)
					var delta:=maxf(absf(a.r-b.r),maxf(absf(a.g-b.g),absf(a.b-b.b)))
					maximum=maxf(maximum,delta)
					if delta>0.012: changed+=1
			assert(changed<300,"Default material/footprint pixel parity: "+id+str(q)+" / "+str(changed))
			results.append({"id":id,"q":q,"changed_pixels":changed,"maximum":maximum})
			if surface.corridor:
				var values: Dictionary={}
				for cell in Floor.cells(true,q,id): values[Floor.material_key(cell)]=3
				var meshes:=Floor.meshes(values,true,q,1.0,"",id)
				for batch in meshes:
					var arrays: Array=batch.mesh.surface_get_arrays(0)
					var poly:=Floor.footprint(true,q,id)
					for index in range(0,arrays[Mesh.ARRAY_INDEX].size(),3):
						var center:=Vector2.ZERO
						for j in range(3):
							var p: Vector3=arrays[Mesh.ARRAY_VERTEX][arrays[Mesh.ARRAY_INDEX][index+j]]; center+=Vector2(p.x,p.y)/3
						assert(Geometry2D.is_point_in_polygon(center,poly),"Painted triangles stay inside concave corridor")
	var old:=Floor.meshes({},false,0,0.42,profiles.reactor.source)
	var other:=Floor.meshes({},false,0,0.42,profiles.crew_hab.source)
	assert(old[0].texture!=other[0].texture,"Shared cache must distinguish department materials")
	surface.queue_free(); await process_frame
	root.size=Vector2i(1600,1000)
	Store.path="user://floor-batch.json"; Store.defaults_path="user://no-batch-defaults.json"; Store.loaded=true; Store.data={}
	var e=Editor.open(root); await process_frame
	for id in IDS:
		var found:=false
		for i in range(e.entries.size()):
			if e.entries[i].room==id: e.switch_room(i); found=true; break
		assert(found,"Room in studio: "+id)
		e.layer=1; e.rebuild_list(); assert(e.floor_tools.visible and not e.layers.is_item_disabled(1))
		var tools=e.floor_tools; tools.mode.select(2); tools.brush.select(3)
		var cells: Array=tools.valid_cells(); var selected: Vector2i=cells[cells.size()/2]
		var before: Dictionary=e.draft.duplicate(true)
		var press:=InputEventMouseButton.new(); press.button_index=MOUSE_BUTTON_LEFT; press.pressed=true
		press.position=e.canvas.origin()+(Vector2(selected)*48-Vector2.ONE*168)*e.canvas.factor(); e.canvas_input(press)
		assert(e.history.size()==1 and Floor.tile_material(e.draft,selected)==3,"One-step fill: "+id)
		e.undo(); assert(e.draft==before); e.redo()
		e.save_layout(); assert(Store.positions(e.entries[e.index].asset,0).get(Floor.material_key(selected))==3)
		e.load_room(); e.layer=1; e.rebuild_list(); assert(Floor.tile_material(e.draft,selected)==3)
		tools.reset_floor(); e.show_guides=false; e.canvas.queue_redraw(); await frame()
		root.get_texture().get_image().save_png("res://output/tiled-floor-batch/"+id+".png")
		# Persist original before moving on; prior orientation drafts remain independent.
		e.save_layout()
	e.close_editor(); await process_frame
	var file:=FileAccess.open("res://output/tiled-floor-batch/parity.json",FileAccess.WRITE); file.store_string(JSON.stringify(results,"\t")); file.close()
	print("TILED FLOOR BATCH PASS: five identities, 20 default comparisons, concave clipping, material cache isolation, editor fill/undo/save/reload/reset")
	quit()
