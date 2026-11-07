extends SceneTree
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(value:bool,label:String):
	checks+=1
	if not value:failures+=1;push_error(label)
func run():
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR")
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--profile="):expected=arg.trim_prefix("--profile=")
	if expected.is_empty() or OS.get_user_data_dir().replace(char(92),"/").simplify_path()!=expected:quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	preload("res://tools/release_benchmark.gd").configure_test_window(root)
	root.set_disable_input(true)
	var library=load("res://scripts/room_asset_library.gd")
	check(library.has_method("template_metadata"),"Geometry-only template API missing")
	if failures>0:print("GALLEY METADATA RED");quit(1);return
	var serving_id:="library/side-galley-serving-south"
	var serving_source:String=library.entries()[serving_id].data.source
	var room=preload("res://rooms/underwater/galley-v1/galley_view.gd").new()
	room.embedded=true;room.hide();root.add_child(room)
	check(not library.source_textures.has(serving_source),"Room geometry uploaded discarded serving artwork")
	check(room.textures.is_empty() and room.regions.is_empty(),"Old PNGs loaded without a requesting prop")
	check(room.north_kitchen_art.is_empty(),"Old north kitchen loaded at ready")
	for id in ["kitchen","serving"]:
		var prop:Dictionary={"id":id,"rect":Rect2(-80,-60,160,60)}
		var bounds:Rect2=room.prop_visual_bounds(prop)
		var image:=Image.new()
		check(preload("res://scripts/safe_image.gd").load_png(image,room.LEGACY_TEXTURE_PATHS[id])==OK,"Fallback source unavailable")
		check(room.textures[id].get_image().get_data()==image.get_data(),"Fallback decoded pixels changed")
		check(room.regions[id]==Rect2(image.get_used_rect()),"Fallback source region changed")
		check(bounds.size.x==160 and bounds.end.y==prop.rect.end.y,"Fallback placement changed")
		var original:Texture2D=room.textures[id]
		room.prop_visual_bounds(prop)
		check(room.textures[id]==original,"Repeated bounds uploaded a second texture")
		if id=="kitchen":check(not room.textures.has("serving"),"Kitchen requested serving art")
	check(room.north_kitchen_art.is_empty(),"Bounds requested unused north artwork")
	room.free()
	var metadata:Dictionary=library.template_metadata(serving_id)
	check(metadata.library_texture==null,"Metadata owns a GPU texture")
	var full:Dictionary=library.template(serving_id)
	var previous:Texture2D=full.library_texture
	var left:Dictionary=metadata.duplicate(true)
	var right:Dictionary=full.duplicate(true)
	for prop in [left,right]:prop.erase("library_texture");prop.erase("library_template_id")
	check(left==right,"Metadata differs from complete prop geometry or registration")
	check(library.template_metadata("library/missing-template-test").is_empty(),"Missing metadata returned invented art")
	var scope=preload("res://scripts/session_art_cache.gd")
	var first:=Node.new();var second:=Node.new()
	for owner in [first,second]:root.add_child(owner);scope.retain(owner)
	first.free()
	check(library.catalog[serving_id].has("template_metadata"),"Overlapping owner lost metadata")
	second.free()
	check(not library.catalog[serving_id].has("template_metadata"),"Final owner retained metadata cache")
	check(not library.catalog[serving_id].has("template") and library.source_textures.is_empty(),"Final owner retained texture lookup")
	metadata=library.template_metadata(serving_id)
	check(metadata.library_texture==null and not library.source_textures.has(serving_source),"Metadata reload uploaded pixels")
	check(library.template(serving_id).library_texture.get_image().get_data()==previous.get_image().get_data(),"Reloaded artwork pixels changed")
	print("GALLEY LAZY ART ",checks," checks, ",failures," failures")
	quit(0 if failures==0 else 1)
