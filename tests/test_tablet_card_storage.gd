extends SceneTree
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	if not ok:failures+=1;push_error(label)
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var main=load("res://scripts/main.gd").new()
	main.set_meta("tablet_controls",true)
	var paths:Dictionary=preload("res://scripts/room_card_art.gd").PATHS
	var first:Texture2D=main._load_card_thumbnail(paths.brine_core)
	check(first.has_method("cpu_storage_bytes"),"Tablet card artwork must defer GPU upload until used")
	if not first.has_method("cpu_storage_bytes"):main.free();quit(1);return
	var cards:Array=[]
	var packed:=0;var decoded:=0
	for id in paths:
		var path:String=paths[id]
		var card:Texture2D=main._load_card_thumbnail(path)
		var original:Image=preload("res://scripts/safe_image.gd").raw_image(path)
		original.generate_mipmaps()
		var copy:Image=card.get_image()
		check(copy.get_data()==original.get_data() and copy.get_size()==original.get_size(),"Complete card pixels and mipmaps preserved: "+str(path))
		check(card.get("uploaded_texture")==null,"Public CPU image does not cause GPU upload")
		packed+=card.cpu_storage_bytes();decoded+=original.get_data_size()
		cards.append(card);main.card_textures[id]=card
	first=main.card_textures.brine_core
	check(main.card_storage_stats().packed_cpu_bytes==packed and main.card_storage_stats().deferred_cards==79,"Live card diagnostics count only retained staging")
	check(packed<decoded,"Compressed unused cards retain less than decoded mipmapped pixels")
	var viewport:=SubViewport.new();viewport.size=Vector2i(320,320);viewport.transparent_bg=true
	viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
	var sprite:=Sprite2D.new();sprite.position=Vector2(160,160);viewport.add_child(sprite)
	var pixels:Image=first.get_image()
	var reference:=ImageTexture.create_from_image(pixels)
	for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS]:
		for factor in [.5,.73]:
			sprite.texture_filter=filter;sprite.scale=Vector2.ONE*factor;sprite.rotation=.17
			sprite.texture=reference
			await process_frame;await RenderingServer.frame_post_draw
			var expected:PackedByteArray=viewport.get_texture().get_image().get_data()
			sprite.texture=first
			await process_frame;await RenderingServer.frame_post_draw
			check(viewport.get_texture().get_image().get_data()==expected,"Native rotated/fractional card sampling remains exact")
	check(first.get("uploaded_texture")!=null,"First display materializes the original image texture")
	check(main.card_storage_stats().deferred_cards==78 and main.card_storage_stats().uploaded_pixel_bytes>0,"Live diagnostics reflect first display without reading pixels")
	check(first.cpu_storage_bytes()==0,"Displayed cards release their compressed staging copy")
	check(first.get_image().get_data()==pixels.get_data(),"Public image remains exact after staging release")
	main.set_meta("tablet_controls",false)
	check(not main._load_card_thumbnail(paths.brine_core).has_method("cpu_storage_bytes"),"Desktop thumbnail policy remains eager")
	print("TABLET CARD STORAGE packed=",packed," decoded=",decoded," failures=",failures)
	viewport.queue_free();main.free();await process_frame
	quit(1 if failures else 0)
