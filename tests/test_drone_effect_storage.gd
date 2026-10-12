extends SceneTree
## Lossless LA8 effect storage: drawn pixels match the original sheets exactly, unsupported
## contexts and invalid storage fall back to the original, loaded art stays immutable and the
## session releases it. Native lane; isolated APPDATA and BRINESPACE_TEST_USER_DIR required.
const Motion=preload("res://scripts/drone_animation.gd")
const Storage=preload("res://scripts/drone_effect_storage.gd")
const Catalog=preload("res://scripts/drone_effect_storage_catalog.gd")
const Session=preload("res://scripts/session_art_cache.gd")
const Flood=preload("res://scripts/flood_submersion.gdshader")
const FIXTURE_SOURCE:="user://drone-effect-storage-fixture-source.png"
const FIXTURE_STORAGE:="user://drone-effect-storage-fixture-la.png"
const FIXTURE_PLAIN:="user://drone-effect-storage-fixture-plain.png"
var checks:=0
var failures:=0

class Painter extends Node2D:
	var motion
	var record:Dictionary
	var frame_id:=0
	var cell:=Vector2.ONE
	var tint:=Color.WHITE
	var reference:Texture2D
	func _draw():
		if record.is_empty():return
		var rect:=Rect2(Vector2.ZERO,cell)
		if reference!=null:
			var columns:=int(record.columns)
			draw_texture_rect_region(reference,rect,Rect2(Vector2(frame_id%columns,frame_id/columns)*cell,cell),tint)
		else:
			motion.begin(self);motion.atlas(self,record,frame_id,rect,cell,tint)

func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func settle():
	for i in 2:
		await process_frame;await RenderingServer.frame_post_draw
func stage(cell:Vector2)->Painter:
	var viewport:=SubViewport.new()
	viewport.size=Vector2i(cell);viewport.transparent_bg=true
	viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var painter:=Painter.new();painter.cell=cell;painter.motion=Motion
	viewport.add_child(painter)
	return painter
func reset_motion():
	for job in Motion.image_jobs.values():WorkerThreadPool.wait_for_task_completion(job.task)
	Motion.image_jobs.clear();Motion.textures.clear();Motion.texture_order.clear();Motion.texture_bytes.clear()
	Motion.last_used.clear();Motion.weak_images.clear();Motion.invisible_images.clear();Motion.cached_bytes=0
func write_bytes(path:String,bytes:PackedByteArray):
	var file:=FileAccess.open(path,FileAccess.WRITE);file.store_buffer(bytes);file.close()

func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	OS.set_environment("BRINE_SILENT","1")
	AudioServer.set_bus_mute(AudioServer.get_bus_index("Master"),true)
	var primary:int=DisplayServer.get_primary_screen()
	for screen in DisplayServer.get_screen_count():
		var extent:Vector2i=DisplayServer.screen_get_size(screen)
		if screen!=primary and extent.x>=1920 and extent.y>=1080:
			root.current_screen=screen;root.position=DisplayServer.screen_get_position(screen)+Vector2i(100,100)
			break
	root.set_disable_input(true)
	var windows:bool=OS.get_name()=="Windows"
	check(Motion.native_effect_storage==windows,"Storage is enabled by default on Windows only")
	check(Motion.effect_storage==Catalog.DATA and Catalog.DATA.size()==3,"Normal source uses the generated three-sheet catalog")
	# Everything below exercises the storage path itself, whatever the platform default is.
	Motion.native_effect_storage=true
	var owner:=Node.new();root.add_child(owner);Session.retain(owner)

	# The catalog must describe sheets the mining rover really draws, with matching bytes.
	var mining:Dictionary=Motion.catalog("mining")
	var cell:=Vector2(mining.frameWidth,mining.frameHeight)
	var records:Dictionary={}
	for clip in mining.states.values():
		if clip.has("effectAtlas") and Catalog.DATA.has(clip.effectAtlas.path):records[clip.effectAtlas.path]=clip.effectAtlas
	check(records.size()==Catalog.DATA.size(),"Every stored sheet is a mining effect atlas in the runtime manifest")
	for source in Catalog.DATA:
		var spec:Dictionary=Catalog.DATA[source]
		check(FileAccess.file_exists(source) and FileAccess.get_sha256(source)==spec.original_sha256,"Original sheet matches its recorded hash: "+source)
		check(FileAccess.file_exists(spec.path) and FileAccess.get_sha256(spec.path)==spec.sha256,"Stored sheet matches its recorded hash: "+spec.path)

	var native:=stage(cell)
	var plain:=stage(cell)
	var flood:=ShaderMaterial.new();flood.shader=Flood
	var visible_pairs:=0
	for source in records:
		var spec:Dictionary=Catalog.DATA[source]
		var la_bytes:int=int(spec.width)*int(spec.height)*2
		var rgba_bytes:int=la_bytes*2
		var record:Dictionary=records[source]
		var frames:int=int(record.columns)*int(int(spec.height)/int(cell.y))
		var decoded:=Image.new();decoded.load_png_from_buffer(FileAccess.get_file_as_bytes(source))
		var reference:=ImageTexture.create_from_image(decoded)
		var display:Texture2D=Motion.texture(source)
		check(display is Storage and display.mask!=null and display.original==null,"Sheet loads as stored mask without the RGBA upload: "+source)
		check(display.get_size()==Vector2(spec.width,spec.height) and Motion.texture_bytes[source]==la_bytes,"Stored sheet keeps its size and accounts two channels")
		check(display.get_image().get_data()==decoded.get_data(),"Public image is the original artwork")
		native.record=record;plain.record=record;plain.reference=reference
		# Supported contexts: nearest filtering, white RGB, no material or the flood material.
		var mask_draws:int=Motion.native_mask_draws
		for frame_id in [0,7,59,60,119,frames-1]:
			for mode in (["plain","alpha","flood"] if frame_id==60 else ["plain"]):
				for painter in [native,plain]:
					painter.frame_id=frame_id;painter.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
					painter.modulate=Color.WHITE;painter.tint=Color(1,1,1,.5) if mode=="alpha" else Color.WHITE
					painter.material=flood if mode=="flood" else null
					painter.queue_redraw()
				await settle()
				var drawn:Image=native.get_viewport().get_texture().get_image()
				if not drawn.is_invisible():visible_pairs+=1
				check(drawn.get_data()==plain.get_viewport().get_texture().get_image().get_data(),"Stored draw matches original pixels: %s frame %d %s"%[source.get_file(),frame_id,mode])
		check(Motion.native_mask_draws>mask_draws and display.original==null,"Supported contexts draw the mask and never upload the original")
		# Unsupported contexts must draw the original artwork itself.
		var fallback_draws:int=Motion.native_fallback_draws
		for mode in ["linear","tint","modulate"]:
			for painter in [native,plain]:
				painter.frame_id=60;painter.material=null
				painter.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR if mode=="linear" else CanvasItem.TEXTURE_FILTER_NEAREST
				painter.tint=Color(.5,.8,1,1) if mode=="tint" else Color.WHITE
				painter.modulate=Color(1,.6,.6,1) if mode=="modulate" else Color.WHITE
				painter.queue_redraw()
			await settle()
			check(native.get_viewport().get_texture().get_image().get_data()==plain.get_viewport().get_texture().get_image().get_data(),"Fallback draw matches original pixels: %s %s"%[source.get_file(),mode])
		check(Motion.native_fallback_draws>=fallback_draws+3 and display.original!=null,"Unsupported contexts use the original fallback")
		check(Motion.texture_bytes[source]==la_bytes+rgba_bytes and Motion.cached_bytes==la_bytes+rgba_bytes,"Fallback upload is added to the cache accounting")
		check(Motion.cache_diagnostics().native_encoded_original_bytes==display.original_png.size(),"Diagnostics report the retained encoded original")
		# One sheet resident at a time keeps this fixture's texture memory bounded.
		var held:WeakRef=weakref(display)
		display=null;reference=null;plain.reference=null;native.record={};plain.record={}
		native.queue_redraw();plain.queue_redraw();await settle()
		native.set_meta("drone_texture_pins",{});Motion.active_canvas=null
		reset_motion()
		await settle()
		check(held.get_ref()==null,"Dropping cache ownership frees the stored sheet")
	check(visible_pairs>=3,"Compared frames include visible effect pixels")

	# Scratch 1x1 sheet: validation, fallbacks and immutability without touching real art.
	var rgba:=Image.create(1,1,false,Image.FORMAT_RGBA8);rgba.set_pixel(0,0,Color8(135,139,125,255));rgba.save_png(FIXTURE_SOURCE)
	var la:=Image.create_from_data(1,1,false,Image.FORMAT_LA8,PackedByteArray([255,255]));la.save_png(FIXTURE_STORAGE)
	var source_bytes:=FileAccess.get_file_as_bytes(FIXTURE_SOURCE)
	var storage_bytes:=FileAccess.get_file_as_bytes(FIXTURE_STORAGE)
	Motion.effect_storage={FIXTURE_SOURCE:{"path":FIXTURE_STORAGE,"sha256":FileAccess.get_sha256(FIXTURE_STORAGE),"width":1,"height":1,"original_sha256":FileAccess.get_sha256(FIXTURE_SOURCE)}}
	var loaded:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(loaded!=null and loaded.get_format()==Image.FORMAT_LA8 and loaded.get_meta("native_effect_source","")==FIXTURE_SOURCE,"Valid storage loads as a tagged two-channel image")
	var fixture:Texture2D=Motion.make_native_texture(FIXTURE_SOURCE,loaded)
	check(fixture is Storage,"Tagged image becomes stored sheet")
	var red:=Image.create(1,1,false,Image.FORMAT_RGBA8);red.fill(Color.RED);red.save_png(FIXTURE_SOURCE)
	check(fixture.get_image().get_data()==rgba.get_data(),"Loaded sheet ignores a later edit of its source file")
	var caller:Image=fixture.get_image();caller.fill(Color.BLUE)
	check(fixture.get_image().get_data()==rgba.get_data(),"Caller edits cannot reach the loaded sheet")
	check(fixture.original_texture().get_image().get_data()==rgba.get_data(),"Lazy fallback uses the loaded original bytes")
	var stale:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(stale!=null and stale.get_format()==Image.FORMAT_RGBA8 and stale.get_data()==red.get_data(),"Edited source invalidates its storage and loads as itself")
	check(Motion.make_native_texture(FIXTURE_SOURCE,stale) is ImageTexture,"Untagged image stays an ordinary texture")
	write_bytes(FIXTURE_SOURCE,source_bytes)
	check(Motion.load_native_or_original(FIXTURE_SOURCE).get_format()==Image.FORMAT_LA8,"Restored source selects storage again")
	Image.create_from_data(1,1,false,Image.FORMAT_LA8,PackedByteArray([0,255])).save_png(FIXTURE_STORAGE)
	var invalid:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(invalid!=null and invalid.get_format()==Image.FORMAT_RGBA8 and invalid.get_data()==rgba.get_data(),"Storage with the wrong hash falls back to the original")
	DirAccess.remove_absolute(FIXTURE_STORAGE)
	var missing:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(missing!=null and missing.get_format()==Image.FORMAT_RGBA8 and missing.get_data()==rgba.get_data(),"Missing storage falls back to the original")
	write_bytes(FIXTURE_STORAGE,storage_bytes)
	Motion.native_effect_storage=false
	var guarded:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(guarded!=null and guarded.get_format()==Image.FORMAT_RGBA8 and Motion.make_native_texture(FIXTURE_SOURCE,guarded) is ImageTexture,"Platform guard off keeps original storage")
	Motion.native_effect_storage=true
	# Ordinary two-channel art is not proof that derived storage was validated.
	Image.create_from_data(1,1,false,Image.FORMAT_LA8,PackedByteArray([93,255])).save_png(FIXTURE_PLAIN)
	var grey:Image=Motion.load_native_or_original(FIXTURE_PLAIN)
	check(grey!=null and Motion.make_native_texture(FIXTURE_PLAIN,grey) is ImageTexture,"Uncatalogued two-channel art stays ordinary")
	Image.create_from_data(1,1,false,Image.FORMAT_LA8,PackedByteArray([93,255])).save_png(FIXTURE_SOURCE)
	var grey_source:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(grey_source!=null and Motion.make_native_texture(FIXTURE_SOURCE,grey_source) is ImageTexture,"Edited two-channel source is not mistaken for storage")
	check(Motion.load_native_or_original("user://drone-effect-storage-absent.png")==null,"Missing artwork reports null")
	fixture=null
	for path in [FIXTURE_SOURCE,FIXTURE_STORAGE,FIXTURE_PLAIN]:DirAccess.remove_absolute(path)
	Motion.effect_storage=Catalog.DATA

	# The last session owner leaving releases stored sheets with the rest of the drone cache.
	var first:String=records.keys()[0]
	var session_held:WeakRef=weakref(Motion.texture(first))
	check(session_held.get_ref() is Storage,"Stored sheet resident before session release")
	native.get_viewport().queue_free();plain.get_viewport().queue_free()
	owner.queue_free();await settle()
	check(Motion.textures.is_empty() and Motion.image_jobs.is_empty() and Motion.cached_bytes==0,"Session release clears the drone cache")
	check(session_held.get_ref()==null,"Session release frees the stored sheet and its original bytes")
	Motion.native_effect_storage=windows
	FileAccess.open("user://drone-effect-storage.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("DRONE_EFFECT_STORAGE checks=",checks," failures=",failures);quit(1 if failures else 0)
