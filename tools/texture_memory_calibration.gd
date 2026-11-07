extends SceneTree
## Isolated native calibration of engine counters; no GPU pixel readback or global correction.
var rows:Array=[]
var failures:=0
func _init():call_deferred("run")
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(512,512)
	for index in range(8):await frame()
	for dimensions in [Vector2i(64,64),Vector2i(448,448),Vector2i(2688,8960)]:
		for format in [Image.FORMAT_R8,Image.FORMAT_RG8,Image.FORMAT_RGBA8]:
			var full_mips:Image=Image.create(dimensions.x,dimensions.y,true,format)
			var full_bytes:int=full_mips.get_data_size();full_mips=null
			for mipmaps in [false,true]:
				var image:Image=Image.create(dimensions.x,dimensions.y,mipmaps,format)
				image.fill(Color(0.5,0.7,0.9,1.0))
				var before:int=int(Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED))
				var texture:ImageTexture=ImageTexture.create_from_image(image)
				for index in range(3):await frame()
				var after:int=int(Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED))
				var row:Dictionary={"width":dimensions.x,"height":dimensions.y,"format":format,"mipmaps":image.has_mipmaps(),"mipmap_count":image.get_mipmap_count(),"decoded_bytes":image.get_data_size(),"full_chain_bytes":full_bytes,"reported_delta":after-before}
				texture=null;image=null
				for index in range(3):await frame()
				row["release_delta"]=int(Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED))-before
				row["counter_model"]="full_mipmap_chain" if row.reported_delta==full_bytes else "decoded_payload" if row.reported_delta==row.decoded_bytes else "other"
				if row.release_delta!=0:failures+=1;push_error("Texture allocation did not release to baseline")
				rows.append(row)
	var result:Dictionary={"rows":rows,"failures":failures,"debug":OS.is_debug_build(),"engine":Engine.get_version_info(),"os":OS.get_name(),"renderer":RenderingServer.get_current_rendering_method(),"scope":"Engine counter versus known image payload; not physical driver VRAM. Do not apply a global ratio to game memory."}
	var file:=FileAccess.open("user://texture-memory-calibration.json",FileAccess.WRITE)
	if file==null:push_error("Cannot write calibration result");quit(1);return
	file.store_string(JSON.stringify(result));file.close()
	print("TEXTURE_CALIBRATION ",rows.size()," allocations; ",failures," failures")
	quit(1 if failures else 0)
