extends SceneTree
## Cropped cargo storage: unscaled drawing matches the original sheets exactly; scaled drawing
## stays within the owner-accepted bound (October 11, 2026): every drawn pixel is a source pixel
## within half a source pixel of where the full sheet samples. Unsupported contexts and invalid storage
## fall back to the original, loaded art stays immutable and the session releases it.
## Native lane; isolated APPDATA and BRINESPACE_TEST_USER_DIR required.
const Motion=preload("res://scripts/drone_animation.gd")
const Storage=preload("res://scripts/drone_cargo_storage.gd")
const Catalog=preload("res://scripts/drone_cargo_storage_catalog.gd")
const Session=preload("res://scripts/session_art_cache.gd")
const Flood=preload("res://scripts/flood_submersion.gdshader")
const FIXTURE_SOURCE:="user://drone-cargo-storage-fixture-source.png"
const FIXTURE_STORAGE:="user://drone-cargo-storage-fixture-frames.png"
var checks:=0
var failures:=0
var scaled_pixels:=0
var scaled_shifted:=0

class Painter extends Node2D:
	var motion
	var record:Dictionary
	var frame_id:=0
	var cell:=Vector2.ONE
	var target:=Rect2()
	var tint:=Color.WHITE
	var reference:Texture2D
	## Source offset in pixels, reference lane only.
	var shift:=Vector2.ZERO
	func _draw():
		if record.is_empty():return
		if reference!=null:
			var columns:=int(record.columns)
			draw_texture_rect_region(reference,target,Rect2(Vector2(frame_id%columns,frame_id/columns)*cell+shift,cell),tint)
		else:
			motion.begin(self);motion.atlas(self,record,frame_id,target,cell,tint)

func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func settle():
	for i in 2:
		await process_frame;await RenderingServer.frame_post_draw
func stage(cell:Vector2)->Painter:
	var viewport:=SubViewport.new()
	viewport.size=Vector2i(1024,1024);viewport.transparent_bg=true
	viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var painter:=Painter.new();painter.cell=cell;painter.motion=Motion
	viewport.add_child(painter)
	return painter
func shot(painter:Painter)->Image:
	return painter.get_viewport().get_texture().get_image()
func reset_motion():
	for job in Motion.image_jobs.values():WorkerThreadPool.wait_for_task_completion(job.task)
	Motion.image_jobs.clear();Motion.textures.clear();Motion.texture_order.clear();Motion.texture_bytes.clear()
	Motion.last_used.clear();Motion.weak_images.clear();Motion.invisible_images.clear();Motion.cached_bytes=0
func write_bytes(path:String,bytes:PackedByteArray):
	var file:=FileAccess.open(path,FileAccess.WRITE);file.store_buffer(bytes);file.close()
## Pixels of the stored draw that match none of the reference draws: the exact one first, then
## eight with the source moved half a pixel, which settles a sample landing exactly between two
## source pixels onto each side. Counts drawn and neighbour-sourced pixels as it goes.
func unexplained_pixels(drawn:Image,references:Array)->int:
	var data:=drawn.get_data()
	var exact:PackedByteArray=references[0]
	var area:Rect2i=drawn.get_used_rect()
	scaled_pixels+=area.get_area()
	if data==exact:return 0
	var unexplained:=0
	for y in range(area.position.y,area.end.y):
		for x in range(area.position.x,area.end.x):
			var k:int=(y*drawn.get_width()+x)*4
			if data[k]==exact[k] and data[k+1]==exact[k+1] and data[k+2]==exact[k+2] and data[k+3]==exact[k+3]:continue
			var found:=false
			for i in range(1,references.size()):
				var other:PackedByteArray=references[i]
				if data[k]==other[k] and data[k+1]==other[k+1] and data[k+2]==other[k+2] and data[k+3]==other[k+3]:found=true;break
			if found:scaled_shifted+=1
			else:unexplained+=1
	return unexplained

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
	check(Motion.cargo_storage_enabled==windows,"Cargo storage is enabled by default on Windows only")
	check(Motion.cargo_storage==Catalog.DATA and Catalog.DATA.size()==8,"Normal source uses the generated eight-sheet catalog")
	# Everything below exercises the storage path itself, whatever the platform default is.
	Motion.cargo_storage_enabled=true
	var owner:=Node.new();root.add_child(owner);Session.retain(owner)

	# The catalog must describe sheets the mining rover really draws, with matching bytes.
	var mining:Dictionary=Motion.catalog("mining")
	var cell:=Vector2(mining.frameWidth,mining.frameHeight)
	var records:Dictionary={}
	for clip in mining.states.values():
		if clip.has("cargoAtlas") and Catalog.DATA.has(clip.cargoAtlas.path):records[clip.cargoAtlas.path]=clip.cargoAtlas
	check(records.size()==Catalog.DATA.size(),"Every stored sheet is a mining cargo atlas in the runtime manifest")
	for source in Catalog.DATA:
		var spec:Dictionary=Catalog.DATA[source]
		check(FileAccess.file_exists(source) and FileAccess.get_sha256(source)==spec.original_sha256,"Original sheet matches its recorded hash: "+source)
		check(FileAccess.file_exists(spec.path) and FileAccess.get_sha256(spec.path)==spec.sha256,"Stored sheet matches its recorded hash: "+spec.path)
		check(records.has(source) and int(records[source].columns)==int(spec.columns) and Vector2(spec.cell[0],spec.cell[1])==cell,"Stored frame grid matches the runtime manifest: "+source)

	var stored:=stage(cell)
	var plain:=stage(cell)
	var flood:=ShaderMaterial.new();flood.shader=Flood
	for source in records:
		var spec:Dictionary=Catalog.DATA[source]
		var full_bytes:int=int(spec.width)*int(spec.height)*4
		var record:Dictionary=records[source]
		var frames:int=int(record.columns)*int(int(spec.height)/int(cell.y))
		var decoded:=Image.new();decoded.load_png_from_buffer(FileAccess.get_file_as_bytes(source))
		var reference:=ImageTexture.create_from_image(decoded)
		var display:Texture2D=Motion.texture(source)
		check(display is Storage and display.original==null and display.frames.is_empty(),"Sheet loads as cropped frames with nothing uploaded yet: "+source)
		check(display.get_size()==Vector2(spec.width,spec.height) and Motion.texture_bytes[source]*20<full_bytes,"Stored sheet keeps its size and accounts under a twentieth of the bytes")
		check(display.get_image().get_data()==decoded.get_data(),"Public image is the original artwork")
		stored.record=record;plain.record=record;plain.reference=reference
		var frame_draws:int=Motion.cargo_frame_draws
		# Unscaled at a whole-pixel origin must be exact, with any tint and under the flood material.
		for frame_id in [0,17,60,frames-1]:
			for mode in (["plain","alpha","tint","flood"] if frame_id==60 else ["plain"]):
				for painter in [stored,plain]:
					painter.frame_id=frame_id;painter.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
					painter.target=Rect2(Vector2(20,20),cell)
					painter.tint=Color(1,1,1,.5) if mode=="alpha" else Color(.5,.8,1,1) if mode=="tint" else Color.WHITE
					painter.material=flood if mode=="flood" else null
					painter.queue_redraw()
				await settle()
				var drawn:Image=shot(stored)
				check(not drawn.is_invisible(),"Cargo frame is visible: %s frame %d"%[source.get_file(),frame_id])
				check(drawn.get_data()==shot(plain).get_data(),"Unscaled stored draw matches original pixels: %s frame %d %s"%[source.get_file(),frame_id,mode])
		# A scaled sample landing between two source pixels may take either one, never anything else.
		for scale in [2.0,0.9,0.73,0.5,0.3]:
			var origin:=Vector2(20.37,20.81) if scale==0.73 else Vector2(20,20)
			stored.frame_id=60;stored.material=null;stored.tint=Color.WHITE
			stored.target=Rect2(origin,cell*scale);stored.queue_redraw()
			plain.frame_id=60;plain.material=null;plain.tint=Color.WHITE;plain.target=stored.target
			var references:Array=[]
			for shift in [Vector2.ZERO,Vector2(-.5,-.5),Vector2(0,-.5),Vector2(.5,-.5),Vector2(-.5,0),Vector2(.5,0),Vector2(-.5,.5),Vector2(0,.5),Vector2(.5,.5)]:
				plain.shift=shift;plain.queue_redraw()
				await settle()
				references.append(shot(plain).get_data())
			plain.shift=Vector2.ZERO
			var drawn:Image=shot(stored)
			check(not drawn.is_invisible() and unexplained_pixels(drawn,references)==0,"Scaled stored draw uses a source pixel the full sheet's sample touches: %s scale %s"%[source.get_file(),scale])
		check(Motion.cargo_frame_draws>frame_draws and display.original==null,"Supported contexts draw cropped frames and never upload the original")
		check(display.frames.size()==4,"Only the frames drawn were uploaded")
		# Unsupported contexts must draw the original artwork itself.
		var fallback_draws:int=Motion.cargo_fallback_draws
		for mode in ["linear","repeat"]:
			for painter in [stored,plain]:
				painter.frame_id=60;painter.material=null;painter.tint=Color.WHITE;painter.target=Rect2(Vector2(20,20),cell*.73)
				painter.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR if mode=="linear" else CanvasItem.TEXTURE_FILTER_NEAREST
				painter.texture_repeat=CanvasItem.TEXTURE_REPEAT_ENABLED if mode=="repeat" else CanvasItem.TEXTURE_REPEAT_PARENT_NODE
				painter.queue_redraw()
			await settle()
			check(shot(stored).get_data()==shot(plain).get_data(),"Fallback draw matches original pixels: %s %s"%[source.get_file(),mode])
		stored.texture_repeat=CanvasItem.TEXTURE_REPEAT_PARENT_NODE;plain.texture_repeat=CanvasItem.TEXTURE_REPEAT_PARENT_NODE
		check(Motion.cargo_fallback_draws>=fallback_draws+2 and display.original!=null,"Unsupported contexts use the original fallback")
		check(Motion.texture_bytes[source]==display.base_bytes+full_bytes,"Fallback upload is added to the cache accounting")
		# One sheet resident at a time keeps this fixture's texture memory bounded.
		var held:WeakRef=weakref(display)
		display=null;reference=null;plain.reference=null;stored.record={};plain.record={}
		stored.queue_redraw();plain.queue_redraw();await settle()
		stored.set_meta("drone_texture_pins",{});Motion.active_canvas=null
		reset_motion()
		await settle()
		check(held.get_ref()==null,"Dropping cache ownership frees the stored sheet")

	# Scratch one-frame sheet: validation, fallbacks and immutability without touching real art.
	var art:=Image.create(4,4,false,Image.FORMAT_RGBA8)
	for y in [1,2]:
		for x in [1,2]:art.set_pixel(x,y,Color8(90+x,120+y,60,255))
	art.save_png(FIXTURE_SOURCE);art.save_png(FIXTURE_STORAGE)
	var source_bytes:=FileAccess.get_file_as_bytes(FIXTURE_SOURCE)
	var storage_bytes:=FileAccess.get_file_as_bytes(FIXTURE_STORAGE)
	var fixture_spec:={"path":FIXTURE_STORAGE,"sha256":FileAccess.get_sha256(FIXTURE_STORAGE),"width":4,"height":4,"cell":[4,4],"columns":1,"box":[0,0,4,4],"original_sha256":FileAccess.get_sha256(FIXTURE_SOURCE)}
	Motion.cargo_storage={FIXTURE_SOURCE:fixture_spec}
	var loaded:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(loaded!=null and loaded.get_meta("drone_cargo_source","")==FIXTURE_SOURCE,"Valid storage loads as a tagged image")
	var fixture:Texture2D=Motion.make_native_texture(FIXTURE_SOURCE,loaded)
	check(fixture is Storage and fixture.frame(0)!=null and fixture.frame(1)==null and fixture.frame(-1)==null,"Tagged image becomes cropped storage with bounded frames")
	var red:=Image.create(4,4,false,Image.FORMAT_RGBA8);red.fill(Color.RED);red.save_png(FIXTURE_SOURCE)
	check(fixture.get_image().get_data()==art.get_data(),"Loaded sheet ignores a later edit of its source file")
	var caller:Image=fixture.get_image();caller.fill(Color.BLUE)
	check(fixture.get_image().get_data()==art.get_data(),"Caller edits cannot reach the loaded sheet")
	check(fixture.original_texture().get_image().get_data()==art.get_data(),"Lazy fallback uses the loaded original bytes")
	var stale:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(stale!=null and not stale.has_meta("drone_cargo_source") and stale.get_data()==red.get_data(),"Edited source invalidates its storage and loads as itself")
	check(Motion.make_native_texture(FIXTURE_SOURCE,stale) is ImageTexture,"Untagged image stays an ordinary texture")
	write_bytes(FIXTURE_SOURCE,source_bytes)
	check(Motion.load_native_or_original(FIXTURE_SOURCE).has_meta("drone_cargo_source"),"Restored source selects storage again")
	red.save_png(FIXTURE_STORAGE)
	var invalid:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(invalid!=null and not invalid.has_meta("drone_cargo_source") and invalid.get_data()==art.get_data(),"Storage with the wrong hash falls back to the original")
	DirAccess.remove_absolute(FIXTURE_STORAGE)
	var missing:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(missing!=null and not missing.has_meta("drone_cargo_source") and missing.get_data()==art.get_data(),"Missing storage falls back to the original")
	write_bytes(FIXTURE_STORAGE,storage_bytes)
	var wrong_grid:Dictionary=fixture_spec.duplicate(true);wrong_grid.box=[0,0,2,2]
	Motion.cargo_storage={FIXTURE_SOURCE:wrong_grid}
	check(not Motion.load_native_or_original(FIXTURE_SOURCE).has_meta("drone_cargo_source"),"Storage whose size disagrees with its catalog entry falls back to the original")
	Motion.cargo_storage={FIXTURE_SOURCE:fixture_spec}
	Motion.cargo_storage_enabled=false
	var guarded:Image=Motion.load_native_or_original(FIXTURE_SOURCE)
	check(guarded!=null and not guarded.has_meta("drone_cargo_source") and Motion.make_native_texture(FIXTURE_SOURCE,guarded) is ImageTexture,"Platform guard off keeps original storage")
	Motion.cargo_storage_enabled=true
	fixture=null
	for path in [FIXTURE_SOURCE,FIXTURE_STORAGE]:DirAccess.remove_absolute(path)
	Motion.cargo_storage=Catalog.DATA

	# The last session owner leaving releases stored sheets with the rest of the drone cache.
	var first:String=records.keys()[0]
	var session_held:WeakRef=weakref(Motion.texture(first))
	check(session_held.get_ref() is Storage,"Stored sheet resident before session release")
	stored.get_viewport().queue_free();plain.get_viewport().queue_free()
	owner.queue_free();await settle()
	check(Motion.textures.is_empty() and Motion.image_jobs.is_empty() and Motion.cached_bytes==0,"Session release clears the drone cache")
	check(session_held.get_ref()==null,"Session release frees the stored sheet and its original bytes")
	Motion.cargo_storage_enabled=windows
	FileAccess.open("user://drone-cargo-storage.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"scaled_pixels":scaled_pixels,"scaled_pixels_from_neighbour":scaled_shifted}))
	print("DRONE_CARGO_STORAGE scaled_pixels=%d from_neighbour=%d checks=%d failures=%d"%[scaled_pixels,scaled_shifted,checks,failures]);quit(1 if failures else 0)
