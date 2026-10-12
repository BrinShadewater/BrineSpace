extends "res://scripts/crew_texture_batch.gd"
const CpuFrame=preload("res://scripts/crew_storage/frame.gd")
var cpu_sources:Dictionary={}
var cpu_pixels:Dictionary={}
var decoded:=0
var cache_bounds:=not OS.get_cmdline_user_args().has("--uncached-bounds")
var bounds_usec:=0
var bounds_scans:=0
var compress_usec:=0
var png_usec:=0
func materialize(display:Texture2D,early:bool=true)->void:
	var texture:Texture2D=display.diffuse_texture if display is CanvasTexture else display
	var id:int=texture.get_instance_id()
	if not pending.has(id):return
	var item:Dictionary=pending[id];pending.erase(id)
	var wrapper:Texture2D=item.display.get_ref()
	assert(wrapper is CanvasTexture)
	var known:WeakRef=cpu_sources.get(item.path)
	var source:Texture2D=known.get_ref() if known!=null else null
	if source==null:
		var image:=Image.new()
		var png_started:=Time.get_ticks_usec()
		var status:int=preload("res://scripts/safe_image.gd").load_png(image,item.path,true)
		png_usec+=Time.get_ticks_usec()-png_started
		assert(status==OK)
		var key:String=image.get_meta("png_sha256",item.path)
		known=cpu_pixels.get(key)
		source=known.get_ref() if known!=null else null
		if source==null:
			var compress_started:=Time.get_ticks_usec()
			source=CpuFrame.new();source.source=image;source.set_meta("crew_immutable_pixels",true)
			compress_usec+=Time.get_ticks_usec()-compress_started
			if cache_bounds:
				var bounds_started:=Time.get_ticks_usec()
				source.set_meta("private_source_used_rect",Rect2(image.get_used_rect()))
				bounds_usec+=Time.get_ticks_usec()-bounds_started;bounds_scans+=1
			cpu_pixels[key]=weakref(source);decoded+=1
		cpu_sources[item.path]=weakref(source)
	var used:Rect2
	if cache_bounds:
		used=source.get_meta("private_source_used_rect")
	else:
		var bounds_started:=Time.get_ticks_usec()
		used=Rect2(source.source.get_used_rect())
		bounds_usec+=Time.get_ticks_usec()-bounds_started;bounds_scans+=1
	var density:=65.28/float(texture.get_meta("crew_standing_height"))
	var pivot:Vector2=texture.get_meta("crew_pivot")
	wrapper.set_meta("crew_alpha_extent",Rect2((used.position-pivot)*density,used.size*density))
	wrapper.diffuse_texture=source
	stats.loaded+=1
	if early:stats.early+=1

func finish()->Dictionary:
	var result:Dictionary=super.finish()
	result.merge({"private_bounds_cache":cache_bounds,"private_bounds_usec":bounds_usec,"private_bounds_scans":bounds_scans,"private_compress_usec":compress_usec,"private_png_usec":png_usec,"private_sources":decoded})
	return result
