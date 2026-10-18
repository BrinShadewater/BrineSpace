extends "res://scripts/crew_storage/base_batch.gd"
## Private experiment: main-thread PNG/prefetch ownership, bounded independent
## worker compression/bounds, main-thread frame adoption. No GPU worker calls.
const WORK_WINDOW:=8
const TABLET_WORK_WINDOW:=4
var work_window:=WORK_WINDOW
var skipped_png_decodes:=0
var fingerprint_usec:=0
var pending_image_bytes:=0
var peak_pending_image_bytes:=0
func _init():
	var tree:=Engine.get_main_loop() as SceneTree
	if OS.has_feature("ios") or (tree!=null and bool(tree.root.get_meta("tablet_controls",false))):work_window=TABLET_WORK_WINDOW
const Prefetch=preload("res://scripts/image_prefetch.gd")
var jobs:Dictionary={}
var key_jobs:Dictionary={}
var path_jobs:Dictionary={}
var job_paths:Dictionary={}
var dedup_hits:=0
var submitted:=0
var peak_jobs:=0
var wait_usec:=0
var worker_usec:=0
var worker_compress_usec:=0
var worker_bounds_usec:=0
var unused_jobs:=0
func prepare_path(path:String):
	if path_jobs.has(path):return
	var known:WeakRef=cpu_sources.get(path)
	if known!=null and known.get_ref()!=null:return
	# PNG-byte identity is the existing immutable sharing key. Check it before
	# decoding another path for the same art; never retain the encoded file.
	if work_window==TABLET_WORK_WINDOW and FileAccess.file_exists(path):
		var hash_started:=Time.get_ticks_usec()
		var digest:=FileAccess.get_sha256(path)
		fingerprint_usec+=Time.get_ticks_usec()-hash_started
		known=cpu_pixels.get(digest)
		if known!=null and known.get_ref()!=null:
			cpu_sources[path]=known;skipped_png_decodes+=1;return
		if key_jobs.has(digest):
			var primary:String=key_jobs[digest]
			path_jobs[path]=primary;job_paths[primary].append(path)
			dedup_hits+=1;skipped_png_decodes+=1;return
	var image:=Image.new()
	var started:=Time.get_ticks_usec()
	var error:int=preload("res://scripts/safe_image.gd").load_png(image,path,true)
	png_usec+=Time.get_ticks_usec()-started
	assert(error==OK)
	var key:String=image.get_meta("png_sha256",path)
	known=cpu_pixels.get(key)
	if known!=null and known.get_ref()!=null:
		cpu_sources[path]=known;return
	if key_jobs.has(key):
		var primary:String=key_jobs[key]
		path_jobs[path]=primary;job_paths[primary].append(path);dedup_hits+=1
		return
	var result:Dictionary={"key":key}
	var task:=WorkerThreadPool.add_task(func():
		var work_started:=Time.get_ticks_usec()
		var pixels:=image.get_data()
		result.dimensions=image.get_size();result.format=image.get_format()
		result.mipmaps=image.has_mipmaps();result.mipmap_count=image.get_mipmap_count()
		result.raw_bytes=pixels.size()
		var compression_started:=Time.get_ticks_usec()
		result.packed=pixels.compress(FileAccess.COMPRESSION_ZSTD)
		result.compress_usec=Time.get_ticks_usec()-compression_started
		var bounds_started:=Time.get_ticks_usec()
		result.used=Rect2(image.get_used_rect())
		result.bounds_usec=Time.get_ticks_usec()-bounds_started
		result.worker_usec=Time.get_ticks_usec()-work_started,true)
	jobs[path]={"task":task,"result":result,"image_bytes":image.get_data_size()}
	pending_image_bytes+=image.get_data_size();peak_pending_image_bytes=maxi(peak_pending_image_bytes,pending_image_bytes)
	key_jobs[key]=path;path_jobs[path]=path;job_paths[path]=[path]
	submitted+=1;peak_jobs=maxi(peak_jobs,jobs.size())
func materialize(display:Texture2D,early:bool=true)->void:
	var texture:Texture2D=display.diffuse_texture if display is CanvasTexture else display
	var id:int=texture.get_instance_id()
	if not pending.has(id):return
	var item:Dictionary=pending[id]
	if not path_jobs.has(item.path):super.materialize(display,early);return
	var primary:String=path_jobs[item.path]
	var job:Dictionary=jobs[primary]
	var started:=Time.get_ticks_usec()
	WorkerThreadPool.wait_for_task_completion(job.task)
	wait_usec+=Time.get_ticks_usec()-started
	pending_image_bytes-=int(job.image_bytes)
	jobs.erase(primary)
	var result:Dictionary=job.result
	worker_usec+=int(result.worker_usec);worker_compress_usec+=int(result.compress_usec)
	worker_bounds_usec+=int(result.bounds_usec)
	var known:WeakRef=cpu_pixels.get(result.key)
	var source:Texture2D=known.get_ref() if known!=null else null
	if source==null:
		source=CpuFrame.new()
		source.dimensions=result.dimensions;source.pixel_format=result.format
		source.mipmaps=result.mipmaps;source.mipmap_count=result.mipmap_count
		source.raw_bytes=result.raw_bytes;source.packed=result.packed
		source.set_meta("crew_immutable_pixels",true)
		source.set_meta("private_source_used_rect",result.used)
		cpu_pixels[result.key]=weakref(source);decoded+=1;bounds_scans+=1
	for path in job_paths[primary]:
		cpu_sources[path]=weakref(source);path_jobs.erase(path)
	job_paths.erase(primary);key_jobs.erase(result.key)
	# Base adoption now finds the prepared immutable source and preserves wrapper
	# pivot/density/filter metadata and loaded/early counters without PNG work.
	super.materialize(display,early)
func finish()->Dictionary:
	var ids:Array=pending.keys();var next:=0
	if Prefetch.active and Prefetch.batch_order:
		var order:=PackedStringArray()
		for id in ids:
			if pending[id].texture.get_ref()!=null:order.append(pending[id].path)
		Prefetch.prime(order)
	for id in ids:
		while next<ids.size() and jobs.size()<work_window:
			var ahead:int=ids[next];next+=1
			if not pending.has(ahead):continue
			if pending[ahead].texture.get_ref()!=null:prepare_path(pending[ahead].path)
		if not pending.has(id):continue
		var texture:ImageTexture=pending[id].texture.get_ref()
		if texture==null:
			pending.erase(id);stats.discarded+=1
		else:materialize(texture,false)
	for path in jobs.keys():
		WorkerThreadPool.wait_for_task_completion(jobs[path].task);unused_jobs+=1
	jobs.clear();key_jobs.clear();path_jobs.clear();job_paths.clear();pending_image_bytes=0
	var result:Dictionary=super.finish()
	result.merge({"private_work_window":work_window,"private_skipped_png_decodes":skipped_png_decodes,"private_fingerprint_usec":fingerprint_usec,"private_peak_pending_image_bytes":peak_pending_image_bytes,"private_pending_content_hits":dedup_hits,"private_key_jobs_left":key_jobs.size(),"private_path_jobs_left":path_jobs.size(),"private_compress_jobs":submitted,"private_compress_peak_jobs":peak_jobs,
		"private_compress_wait_usec":wait_usec,"private_worker_usec":worker_usec,
		"private_worker_compress_usec":worker_compress_usec,"private_worker_bounds_usec":worker_bounds_usec,
		"private_compress_unused_jobs":unused_jobs,"private_compress_jobs_left":jobs.size()})
	return result
