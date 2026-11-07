extends RefCounted
const CpuFrame=preload("res://scripts/crew_storage/frame.gd")
var player
var sources:Dictionary={}
var decoded_bytes:=0
var compressed_bytes:=0
var generated_readbacks:=0
var cpu_store:RefCounted
var cpu_store_enabled:=OS.get_cmdline_user_args().has("--bounded-crew-cpu-store")
var offloaded_bytes:=0
func _maybe_offload(texture:Texture2D):
	if not cpu_store_enabled:return
	var tree:=Engine.get_main_loop() as SceneTree
	if not OS.has_feature("ios") and (tree==null or not bool(tree.root.get_meta("tablet_controls",false))):return
	if texture.backing!=null or not texture.has_meta("private_source_png"):return
	if cpu_store==null:
		var candidate=load("res://scripts/crew_storage/cpu_store.gd").new()
		var directory:=OS.get_cache_dir().path_join("BrineSpace/crew-session-v1")
		if DirAccess.make_dir_recursive_absolute(directory)!=OK:return
		var destination:=directory.path_join("%d-%d-%d.bin"%[OS.get_process_id(),Time.get_ticks_usec(),get_instance_id()])
		if not candidate.open(destination):return
		cpu_store=candidate
	var size:int=texture.compressed_size()
	if texture.offload(cpu_store,str(texture.get_meta("private_source_png"))):offloaded_bytes+=size
const Display=preload("res://scripts/crew_storage/display.gd")
func adopt(target):
	player=target
	var generated:Dictionary={};var seen:Dictionary={}
	var banks:Array=[player.frames]
	for gear in player.equipment_frames:banks.append(player.equipment_frames[gear])
	# Historical dictionaries keep the same frame Resource objects.
	if "carry_banks" in player:
		for historical in player.carry_banks.values():
			banks.append(historical.frames)
			for gear in historical.equipment_frames:banks.append(historical.equipment_frames[gear])
	for clips in banks:
		for key in clips:
			for index in clips[key].size():
				var frame:Texture2D=clips[key][index]
				var texture:Texture2D=frame.diffuse_texture if frame is CanvasTexture else frame
				if not texture is CpuFrame:
					if not generated.has(texture.get_instance_id()):
						var replacement:=CpuFrame.new();replacement.source=texture.get_image();generated_readbacks+=1
						for meta in texture.get_meta_list():replacement.set_meta(meta,texture.get_meta(meta))
						generated[texture.get_instance_id()]=replacement
					var replacement:Texture2D=generated[texture.get_instance_id()]
					if frame is CanvasTexture:frame.diffuse_texture=replacement
					else:clips[key][index]=replacement;frame=replacement
					texture=replacement
				sources[frame.get_instance_id()]=texture
				if not seen.has(texture.get_instance_id()):
					seen[texture.get_instance_id()]=true;decoded_bytes+=texture.raw_bytes;compressed_bytes+=texture.compressed_size()
					_maybe_offload(texture)
	for clips in banks:
		for row in clips.values():
			for frame in row:
				assert(frame is CanvasTexture)
				frame.set_script(Display)

func source_image(frame:Texture2D)->Image:return sources[frame.get_instance_id()].source
func frame_size(frame:Texture2D)->Vector2:return Vector2(sources[frame.get_instance_id()].dimensions)
