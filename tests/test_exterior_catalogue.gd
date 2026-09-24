extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Library=preload("res://scripts/room_asset_library.gd")
var failures := 0
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	if not ok: failures+=1;push_error(message)
func run():
	Store.path="res://output/procedural-sites-2026-09-23/studio-test.json"
	Store.defaults_path="res://output/procedural-sites-2026-09-23/studio-defaults.json"
	Store.loaded=true;Store.data={}
	var e=Editor.open(root)
	await process_frame
	e.free_placement.button_pressed=true
	var exterior := "library/tileset-uw1-188"
	check(not e.add_library_asset(exterior,Vector2.ZERO),"exterior cannot be newly placed")
	check(e.add_library_asset("library/tileset-mat-123",Vector2.ZERO),"indoor aquarium equipment remains placeable")
	# Existing saved placements still resolve and remain ordinary editable entities.
	var placed:=exterior+"#1"
	e.draft[placed]=[0,0]
	e.selected=placed;e.selected_many.clear();e.refresh()
	check(not e.selected_prop().is_empty(),"saved exterior resolves in editor")
	e.draft[placed]=[40,20];e.refresh()
	check(e.draft[placed]==[40,20] and not e.selected_prop().is_empty(),"saved exterior remains movable")
	var before: int=e.draft.size()
	e.duplicate_selected()
	check(e.draft.size()==before,"duplicate does not reintroduce exterior props")
	e.favourites[exterior]=true
	for filter_id in range(e.library_filter.item_count):
		e.library_filter.select(filter_id)
		e.library_signature=[];e.rebuild_library()
		for i in range(e.library_list.item_count):
			check(not Library.is_exterior(str(e.library_list.get_item_metadata(i))),"exterior excluded from filter "+str(filter_id))
	e.library_search.text="Boulders"
	e.library_signature=[];e.rebuild_library()
	for i in range(e.library_list.item_count): check(not Library.is_exterior(str(e.library_list.get_item_metadata(i))),"search excludes scenery")
	for members in e.variant_members:
		for id in members: check(not Library.is_exterior(id),"variants exclude scenery")
	e.selected=placed;e.remove_library_asset()
	check(e.draft.get(placed)==null,"saved exterior can be removed")
	if DisplayServer.get_name()!="headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/procedural-sites-2026-09-23/studio-filter.png")
	print("EXTERIOR CATALOGUE: failures=",failures)
	quit(0 if failures==0 else 1)

