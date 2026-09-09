extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Library=preload("res://scripts/room_asset_library.gd")
const Door=preload("res://rooms/whole-room/room_door.gd")
var OUT="res://output/studio-owner-notes-2026-09-08/"
func _init() -> void: call_deferred("run")
func key(editor,code: int) -> void:
	var event:=InputEventKey.new(); event.keycode=code; event.pressed=true
	editor._input(event)
func run() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--out="): OUT=argument.trim_prefix("--out=").trim_suffix("/")+"/"
	root.size=Vector2i(1600,900)
	DirAccess.make_dir_recursive_absolute(OUT)
	Store.path=OUT+"fixture-layouts.json"; Store.defaults_path=OUT+"fixture-defaults.json"
	for path in [Store.path,Store.path+".recovery.json"]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	var file=FileAccess.open(Store.defaults_path,FileAccess.WRITE)
	file.store_string('{"version":1,"layouts":{}}'); file.close()
	Store.loaded=true; Store.data={}
	var editor=Editor.open(root)
	await process_frame; await process_frame
	editor.set_process(false)
	assert(editor.show_riser and editor.riser_toggle.button_pressed,"Studio opens with risers visible")
	assert(editor.autosave_enabled)
	var actions=editor.find_child("RoomActions",true,false)
	assert(actions!=null and actions.get_child_count()==3)
	assert(actions.get_child(0).text=="Rotate Room" and actions.get_child(1).text=="Next Room" and actions.get_child(2).text=="Save")
	editor.free_placement.button_pressed=true
	editor.selected="sample_cooler"
	key(editor,KEY_F)
	assert(editor.draft["flip/sample_cooler"][0])
	var asset: String=editor.entries[editor.index].asset
	editor.selected=""; editor.selected_many.clear(); key(editor,KEY_R)
	assert(editor.quarter==1 and editor.current_room_dirty())
	editor._process(2.1)
	assert(not editor.current_room_dirty())
	Store.loaded=false; Store.data={}; Store.ensure_loaded()
	assert(Store.positions(asset,0).get("flip/sample_cooler",[])[0],"Autosave includes cached rotation")
	for i in range(editor.entries.size()):
		if editor.entries[i].asset=="crew-lounge-built-in": editor.switch_room(i); break
	editor.switch_rotation(0); editor.free_placement.button_pressed=true
	editor.selected="full_wall_crew-lounge-built-in"
	var original: Dictionary=editor.draft.duplicate(true)
	key(editor,KEY_R)
	assert(editor.quarter==0 and editor.draft.has("variant/"+editor.selected),"R cycles selected asset")
	var choice: String=editor.draft["variant/"+editor.selected]
	assert(editor.selected_prop().get("variant_source","")==choice)
	editor.undo(); assert(editor.draft==original); editor.redo()
	editor.save_all_rotations(); Store.loaded=false; Store.data={}; editor.load_room()
	editor.selected="full_wall_crew-lounge-built-in"
	assert(editor.selected_prop().get("variant_source","")==choice,"Directional variant persists")
	Store.apply(editor.room,editor.entries[editor.index].asset)
	Store.apply(editor.room,editor.entries[editor.index].asset)
	assert(editor.selected_prop().get("variant_source","")==choice,"Repeated runtime application keeps native variant")
	assert(Library.family_variants("crew-lounge-built-in").has("library/side-crew-lounge-built-in-east"))
	for i in range(editor.entries.size()):
		if editor.entries[i].asset=="deepwater-listening-wall": editor.switch_room(i); break
	editor.switch_rotation(0); editor.free_placement.button_pressed=true
	editor.selected="flush_back"
	assert(editor.movable(editor.selected))
	var before: Rect2=editor.entity_bounds(editor.selected_prop())
	var at: Array=editor.draft[editor.selected]
	editor.draft[editor.selected]=[at[0]+18,at[1]+12]; editor.dirty=true; editor.refresh()
	assert(editor.entity_bounds(editor.selected_prop()).position.distance_to(before.position+Vector2(18,12))<0.01)
	editor.save_all_rotations(); Store.loaded=false; Store.data={}; editor.load_room(); editor.selected="flush_back"
	assert(editor.entity_bounds(editor.selected_prop()).position.distance_to(before.position+Vector2(18,12))<0.01,"Listening movement persists")
	assert(Door.riser_leaf_rects(0).size()==2 and Door.riser_leaf_rects(1).is_empty())
	assert(Door.riser_leaf_rects(0.5)[0].size.x<Door.riser_leaf_rects(0)[0].size.x)
	await process_frame; await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+"studio-controls.png")
	editor.switch_room(0); editor.switch_rotation(2)
	editor.selected=""; editor.selected_many.clear(); editor.riser_toggle.button_pressed=true
	var door_images: Array=[]
	for phase in ["closed","half","open"]:
		editor.preview_animation=phase!="closed"
		editor.preview_clock=PI/3 if phase=="open" else 0.0
		editor.canvas.queue_redraw()
		await process_frame; await RenderingServer.frame_post_draw
		var capture=root.get_texture().get_image()
		capture.save_png(OUT+"door-"+phase+".png"); door_images.append(capture.get_data())
	assert(door_images[0]!=door_images[1] and door_images[1]!=door_images[2],"Native riser door frames visibly change")
	var uid_path="res://tests/test_studio_owner_notes.gd.uid"
	if not FileAccess.file_exists(uid_path):
		var uid_file=FileAccess.open(uid_path,FileAccess.WRITE); uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id())); uid_file.close()
	print("OWNER NOTES PASS: controls, cached-rotation autosave, R/F, variant persistence, Listening Post movement, door leaf animation")
	editor.dirty=false; editor.rotation_drafts.clear(); editor.close_editor(); quit()
