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
		"res://legacy/default/assets/rooms/solar-array/cards/card.png",
		"res://legacy/default/assets/rooms/reactor/cards/card.png",
		"res://assets/rooms/crew-hab/cards/card.png",
		"res://legacy/default/assets/rooms/research-lab/cards/card.png",
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
	print("IMAGE PREFETCH %s" % ("PASS" if failures == 0 else "FAIL %d" % failures))
	quit(1 if failures else 0)
