extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const Library=preload("res://scripts/room_asset_library.gd")
const Editor=preload("res://scripts/room_layout_editor.gd")
var OUT="res://output/brine-corner-service-2026-09-08/"
var pack="res://assets/brine-corner-service-v1/"
var ID="library/brine-corner-service-nw"
class Preview extends Node2D:
	var room
	func _draw() -> void:
		room.configure_embedded(0,[],false,0.0)
		Store.apply(room,"room-brine_core")
		room.set_meta("raised_north_visible",true)
		room.render_into(self,Vector2(256,290),1.06,true)
		draw_set_transform(Vector2(256,290),0,Vector2.ONE*1.06)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self,"brine_core",Vector2i.ZERO,false,false,room)
		room.render_into(self,Vector2(256,290),1.06,false,false)
func _init() -> void: call_deferred("run")
func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--out="): OUT=arg.trim_prefix("--out=").trim_suffix("/")+"/"
		if arg.begins_with("--pack="): pack=arg.trim_prefix("--pack=").trim_suffix("/")+"/"
		if arg=="--northeast": ID="library/brine-corner-analysis-ne"
	DirAccess.make_dir_recursive_absolute(OUT)
	Store.path=OUT+"fixture-layouts.json";Store.loaded=true;Store.data={}
	root.size=Vector2i(1600,900)
	var editor=Editor.open(root);editor.autosave_enabled=false
	await process_frame;await process_frame
	for i in range(editor.entries.size()):
		if editor.entries[i].room=="brine_core": editor.switch_room(i);break
	editor.switch_rotation(0);editor.rebuild_library()
	var found:=false
	for i in range(editor.library_list.item_count):
		if editor.library_list.get_item_metadata(i)==ID: found=true
	assert(found,"BRINE corner appears in Room Default tray")
	var prop:=Library.template(ID)
	var at:=Vector2(-184,preload("res://rooms/whole-room/riser_geometry.gd").BASE_Y)
	if ID.ends_with("-ne"):
		at.x=56
		editor.draft["brine_dual_workstation"]=null
	editor.draft[ID]=[at.x,at.y];editor.refresh();editor.selected=ID
	assert(editor.issues().is_empty(),"Fitted corner must clear room props and doors: "+str(editor.issues()))
	var bounds: Rect2=editor.entity_bounds(editor.selected_prop())
	assert(bounds.position.distance_to(at)<0.01 and absf(bounds.size.x-128)<0.01)
	editor.riser_toggle.button_pressed=true
	for i in range(4): editor._process(.01);await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+"studio.png")
	editor.dirty=false;editor.rotation_drafts.clear();editor.close_editor()
	await process_frame
	Store.data={"room-brine_core/0":{ID:[at.x,at.y]}}
	if ID.ends_with("-ne"): Store.data["room-brine_core/0"]["brine_dual_workstation"]=null
	root.size=Vector2i(512,512);root.content_scale_size=root.size;root.transparent_bg=true
	var room=preload("res://rooms/underwater/brine-core/brine_core_view.gd").new();room.embedded=true;root.add_child(room);room.hide()
	room.architect_pod={"id":"core_architect","architect_id":"bill","wake":0.0,"wake_duration":10.0,"recovered":false}
	var preview:=Preview.new();preview.room=room;root.add_child(preview)
	await process_frame;await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+"room.png")
	for seconds in [0.0,5.0,9.9,10.0]:
		room.architect_pod={"id":"core_architect","architect_id":"bill","wake":seconds,"wake_duration":10.0,"recovered":seconds>=10.0}
		preview.queue_redraw()
		await process_frame;await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(OUT+"thaw-"+str(seconds)+".png")
	var export=preload("res://tools/capture_style_polish.gd").Art.new()
	export.setup(JSON.parse_string(FileAccess.get_file_as_string(pack+"registration.json")))
	var viewport:=SubViewport.new();viewport.size=Vector2i(export.texture.get_size());viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport);viewport.add_child(export)
	await process_frame;await RenderingServer.frame_post_draw
	viewport.get_texture().get_image().save_png(pack+"asset.png")
	var uid_path: String=get_script().resource_path+".uid"
	if not FileAccess.file_exists(uid_path):
		var f=FileAccess.open(uid_path,FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));f.close()
	print("BRINE CORNER PASS: default tray, 128-unit width, flush corner bounds, editor prop/door clearance and native alpha export")
	quit()
