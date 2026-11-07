extends SceneTree
## Startup image pre-decoding (owner playtest: loading looked frozen). Images decoded ahead on
## worker threads must match a normal decode exactly, requests out of the recorded order still
## work, the launch order is recorded for next time, and nothing changes while inactive.
const SafeImage = preload("res://scripts/safe_image.gd")
const Prefetch = preload("res://scripts/image_prefetch.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func direct(path: String) -> Image:
	var image := Image.new()
	image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
	return image

func run() -> void:
	var manifest := "user://image_prefetch_test_%d.txt" % OS.get_process_id()
	var paths: Array = [
		"res://assets/environment/ground-refresh-v1/runtime/silt-plain.png",
		"res://assets/environment/ocean-floor-expansion-v1/runtime/brine-star.png",
		"res://assets/environment/ocean-floor-expansion-v1/runtime/tube-worms.png",
		"res://assets/environment/ocean-floor-expansion-v1/runtime/fractured-stone.png",
		"res://brineui/terminal_button_normal.png",
	]
	for path in paths: check(FileAccess.file_exists(path), "Fixture image exists: " + path)
	var file := FileAccess.open(manifest, FileAccess.WRITE)
	file.store_string("\n".join(paths))
	file.close()

	var inactive := Image.new()
	check(SafeImage.load_png(inactive, paths[0]) == OK and Prefetch.recorded.is_empty(), "Inactive: loads decode as before and record nothing")

	Prefetch.begin(manifest)
	check(Prefetch.paths.size() == paths.size(), "The previous launch's order is read")
	var first := Image.new()
	check(SafeImage.load_png(first, paths[0]) == OK and first.get_data() == direct(paths[0]).get_data(), "A pre-decoded image matches a normal decode")
	# Out of order: the fourth before the second, then a raw texture request.
	var fourth := Image.new()
	check(SafeImage.load_png(fourth, paths[3]) == OK and fourth.get_data() == direct(paths[3]).get_data(), "Requests out of the recorded order still get the right image")
	var raw: Image = SafeImage.raw_image(paths[1])
	check(raw != null and raw.get_data() == direct(paths[1]).get_data(), "raw_image uses the pre-decoded image too")
	var again := Image.new()
	check(SafeImage.load_png(again, paths[0]) == OK and again.get_data() == direct(paths[0]).get_data(), "A repeated request keeps identical pixels")
	check(Prefetch.cache_hits == 1,"A repeated pose avoids another decode")
	raw.fill(Color.RED)
	check(SafeImage.raw_image(paths[1]).get_data() == direct(paths[1]).get_data(),"Editing a returned raw image cannot corrupt the startup cache")
	var unknown := Image.new()
	check(SafeImage.load_png(unknown, "res://icon.svg.missing.png") != OK, "Unknown paths fall back to the normal loader and its failure handling")
	check(Prefetch.hits == 3, "Three images came from the workers: %d" % Prefetch.hits)
	Prefetch.end()
	var worker_stats := Prefetch.stats()
	check(worker_stats.worker_submissions == 5 and worker_stats.unused_results == 2,"Worker waste records prefetched images never consumed")
	check(worker_stats.peak_decoded_bytes > 0 and Prefetch.decoded_bytes == 0,"Peak decoded storage is retained as a counter, not live images")
	check(not Prefetch.active and Prefetch.tasks.is_empty() and Prefetch.results.is_empty() and Prefetch.recent_images.is_empty() and Prefetch.cached_bytes == 0, "Ending waits for workers and releases decoded images")
	check(Prefetch.recorded.is_empty() and Prefetch.paths.is_empty() and Prefetch.index_of.is_empty(), "Ending releases startup order and path lookups")
	var written := FileAccess.get_file_as_string(manifest).split("\n", false)
	check(Array(written) == [paths[0], paths[3], paths[1], paths[0], paths[1], "res://icon.svg.missing.png"], "This launch's order is recorded for the next: %s" % str(written))
	var after := Image.new()
	check(SafeImage.load_png(after, paths[2]) == OK and Prefetch.stats().requests == written.size() and Prefetch.recorded.is_empty(), "After ending, loads are normal and request totals remain available")
	SafeImage.failures.clear()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(manifest))
	# First launch (no manifest) shares only successful PNG decodes, too.
	Prefetch.begin(manifest)
	var cold := SafeImage.raw_image(paths[4])
	check(cold != null and Prefetch.hits == 0,"A cold launch uses the normal decoder")
	cold.fill(Color.BLUE)
	check(SafeImage.raw_image(paths[4]).get_data() == direct(paths[4]).get_data() and Prefetch.cache_hits == 1,"Cold-launch repeat is cached with independent pixels")
	var tiny := Image.create(2,2,false,Image.FORMAT_RGBA8)
	for index in range(Prefetch.CACHE_IMAGES+4): Prefetch.remember(str(index),tiny)
	check(Prefetch.recent_images.size() == Prefetch.CACHE_IMAGES and not Prefetch.recent_images.has("0"),"Cache evicts old entries at its image bound")
	var full := Image.create(2048,2048,false,Image.FORMAT_RGBA8)
	Prefetch.remember("full",full)
	check(Prefetch.cached_bytes == Prefetch.CACHE_BYTES and Prefetch.recent_images.size() == 1,"Byte limit evicts smaller cached images")
	Prefetch.remember("next",tiny)
	check(not Prefetch.recent_images.has("full") and Prefetch.cached_bytes == tiny.get_data_size(),"Next image evicts a full cache")
	Prefetch.end()
	# Synthetic old order: only the final slot is requested. Identical fixture
	# pixels stand in for skipped files; none of those slots should be decoded.
	Prefetch.begin(manifest)
	Prefetch.paths.resize(Prefetch.WINDOW*8+1)
	Prefetch.paths.fill(paths[4])
	Prefetch.index_of = {paths[4]:Prefetch.paths.size()-1}
	check(Prefetch.take(paths[4]).get_data() == direct(paths[4]).get_data(),"Jumping ahead still returns the requested pixels")
	check(Prefetch.worker_submissions == 1 and Prefetch.peak_pending <= Prefetch.WINDOW*2,"A changed startup order never queues its skipped prefix")
	Prefetch.end()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(manifest))
	# A first launch already knows surviving crew paths at batch completion.
	# Announcing them must enable the same bounded decoder without a prior file.
	var decoder:=Prefetch.new()
	Prefetch.begin(manifest)
	if decoder.has_method("prime"):
		decoder.call("prime",PackedStringArray([paths[0], paths[1], paths[0]]))
		check(Array(Prefetch.paths)==[paths[0],paths[1]],"First-launch batch order deduplicates paths")
		check(Prefetch.tasks.is_empty() and Prefetch.recorded.is_empty(),"Priming itself neither decodes nor invents requests")
		var initial:=SafeImage.raw_image(paths[0])
		check(initial.get_data()==direct(paths[0]).get_data() and Prefetch.hits==1,"First-launch batch uses workers with exact pixels")
		initial.fill(Color.RED)
		check(SafeImage.raw_image(paths[0]).get_data()==direct(paths[0]).get_data(),"Primed images remain independent")
		decoder.call("prime",PackedStringArray([paths[2],paths[1]]))
		check(Array(Prefetch.paths)==[paths[0],paths[1],paths[2]],"Later crew batches extend the first-launch order")
		check(SafeImage.raw_image(paths[2]).get_data()==direct(paths[2]).get_data(),"Extended order decodes correctly")
	else:check(false,"First-launch crew batches can prime the decoder")
	Prefetch.end()
	check(Prefetch.tasks.is_empty() and Prefetch.results.is_empty() and Prefetch.paths.is_empty(),"Primed workers and order released")
	var requests:=FileAccess.get_file_as_string(manifest).split("\n",false)
	check(Array(requests)==[paths[0],paths[0],paths[2]],"Only actual primed requests become the next launch's order")
	Prefetch.begin(manifest)
	if decoder.has_method("prime"):
		var learned:=Prefetch.paths.duplicate()
		decoder.call("prime",PackedStringArray([paths[4],paths[3]]))
		check(Prefetch.paths==learned,"Repeat launches preserve the learned order")
	Prefetch.end()
	if decoder.has_method("prime"):
		decoder.call("prime",PackedStringArray([paths[0]]))
		check(Prefetch.paths.is_empty(),"Inactive gameplay does not prime startup decoding")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(manifest))
	# Exercise the real compressed crew batch caller, not just the priming API.
	Prefetch.begin(manifest)
	var batch=preload("res://scripts/crew_storage/worker_batch.gd").new()
	var displays:Array=[]
	for path in [paths[0],paths[1],paths[0]]:
		var texture:=ImageTexture.new()
		texture.set_meta("crew_pivot",Vector2(3,6))
		texture.set_meta("crew_standing_height",65.28)
		var display:=CanvasTexture.new();display.diffuse_texture=texture
		batch.add(texture,display,path);displays.append(display)
	var batch_stats:Dictionary=batch.finish()
	check(Prefetch.hits==2 and Prefetch.worker_submissions==2,"Surviving first-launch crew batch enables workers")
	check(displays[0].diffuse_texture.get_image().get_data()==direct(paths[0]).get_data(),"Compressed primed crew frame has exact pixels")
	check(displays[0].diffuse_texture==displays[2].diffuse_texture,"Repeated crew paths still share immutable storage")
	check(displays[1].get_meta("crew_alpha_extent")==Rect2(Vector2(direct(paths[1]).get_used_rect().position)-Vector2(3,6),Vector2(direct(paths[1]).get_used_rect().size)),"Crew alpha bounds and pivot remain exact")
	check(batch_stats.private_compress_jobs_left==0 and batch_stats.private_compress_peak_jobs<=batch.WORK_WINDOW,"Crew worker bounds and cleanup preserved")
	Prefetch.end()
	DirAccess.remove_absolute(ProjectSettings.globalize_path(manifest))
	# iPad repeat loading must not schedule a desktop-sized decoded window.
	root.set_meta("tablet_controls",true)
	file=FileAccess.open(manifest,FileAccess.WRITE);file.store_string("\n".join(paths));file.close()
	Prefetch.begin(manifest)
	for path in paths:
		var tablet_image:Image=SafeImage.raw_image(path)
		check(tablet_image!=null and tablet_image.get_data()==direct(path).get_data(),"Tablet bounded prefetch preserves pixels")
		check(Prefetch.tasks.size()<=4,"Tablet retains at most four pending image decodes")
	check(Prefetch.peak_pending<=4,"Tablet peak pending stays below desktop window")
	Prefetch.end()
	root.remove_meta("tablet_controls")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(manifest))
	print("IMAGE PREFETCH %s" % ("PASS" if failures == 0 else "FAIL %d" % failures))
	quit(1 if failures else 0)
