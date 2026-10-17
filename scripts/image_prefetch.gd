extends RefCounted
## Startup image pre-decoding (owner playtest: the loading screen looked like it was about to
## crash). The October 4 station requests ~32,000 PNGs, including repeated poses. Without
## prefetch, these decode one after another on the main thread. While active, SafeImage asks here
## first: the order images were requested on the previous launch is replayed on worker
## threads, a bounded window ahead of the main thread, so decoding runs in parallel without
## holding every image at once. Each launch records the order again for the next one.
##
## Only the title screen's loading transition turns this on. Fixtures that instantiate the
## game directly decode exactly as before.

const MANIFEST := "user://startup_images.txt"
const WINDOW := 96
# A short, bounded decode cache serves repeated animation poses during startup.
# Images handed to callers are copies: raw-image consumers may edit their pixels.
const CACHE_BYTES := 16 * 1024 * 1024
const CACHE_IMAGES := 128

static var active := false
static var manifest_path := MANIFEST
static var recorded := PackedStringArray()
static var completed_requests := 0
static var paths := PackedStringArray()
static var index_of: Dictionary = {}
static var tasks: Dictionary = {}
static var results: Dictionary = {}
static var next_submit := 0
static var batch_order := false
static var primed_paths := 0
static var hits := 0
static var cache_hits := 0
static var worker_submissions := 0
static var peak_pending := 0
static var decoded_bytes := 0
static var peak_decoded_bytes := 0
static var unused_results := 0
static var worker_decode_usec := 0
static var cached_bytes := 0
static var recent_images: Dictionary = {}
static var reuse_recent_images := true # Diagnostic comparison; returned images remain independent.
static var mutex := Mutex.new()
# Startup holds one long frame. While images arrive, keep the window answering the OS (no "Not
# Responding") and redraw the loading screen with progress roughly eight times a second.
static var progress_callback: Callable
static var last_pump := 0
static var pumps := 0
const PUMP_MS := 120

static func begin(manifest := MANIFEST) -> void:
	if active: return
	active = true
	manifest_path = manifest
	recorded = PackedStringArray()
	completed_requests = 0
	paths = PackedStringArray()
	index_of = {}
	tasks = {}
	results = {}
	next_submit = 0
	batch_order = false
	primed_paths = 0
	hits = 0
	cache_hits = 0
	worker_submissions = 0
	peak_pending = 0
	decoded_bytes = 0
	peak_decoded_bytes = 0
	unused_results = 0
	worker_decode_usec = 0
	cached_bytes = 0
	recent_images.clear()
	pumps = 0
	last_pump = Time.get_ticks_msec()
	if FileAccess.file_exists(manifest):
		for line in FileAccess.get_file_as_string(manifest).split("\n", false):
			if line.begins_with("res://") and not index_of.has(line):
				index_of[line] = paths.size()
				paths.append(line)
	batch_order = paths.is_empty()

# A new profile has no previous order, but a completed crew batch already knows
# its surviving paths. Announce them without decoding or inventing requests.
# Repeat launches keep their learned order, including non-crew artwork.
static func prime(order: PackedStringArray) -> void:
	if not active or not batch_order: return
	# Keep the existing iPad first-launch decode schedule; eager desktop batches
	# can retain hundreds of MiB beyond the tablet drone cache policy.
	var tree := Engine.get_main_loop() as SceneTree
	if OS.has_feature("ios") or (tree != null and bool(tree.root.get_meta("tablet_controls", false))): return
	for path in order:
		if path.begins_with("res://") and not index_of.has(path):
			index_of[path] = paths.size()
			paths.append(path)
			primed_paths += 1

# An independent decoded image, or null to use the ordinary decoder. Recently used
# poses can be served again; older repeats fall back after their bounded cache entry expires.
static func take(path: String) -> Image:
	if not active: return null
	recorded.append(path)
	_pump()
	if recent_images.has(path):
		var cached: Image = recent_images[path]
		recent_images.erase(path)
		recent_images[path] = cached
		var copy := Image.new()
		copy.copy_from(cached)
		if cached.has_meta("png_sha256"): copy.set_meta("png_sha256", cached.get_meta("png_sha256"))
		cache_hits += 1
		return copy
	if not index_of.has(path): return null
	var i: int = index_of[path]
	# Images the new order skipped would otherwise stay decoded; release those well behind.
	for j in tasks.keys():
		if j < i - WINDOW:
			WorkerThreadPool.wait_for_task_completion(tasks[j])
			tasks.erase(j)
			mutex.lock()
			if results.has(j):
				unused_results += 1
				if results[j] != null: decoded_bytes -= results[j].get_data_size()
			results.erase(j)
			mutex.unlock()
	# A new manifest can jump thousands of slots ahead. Never queue the skipped
	# prefix: retain at most one window behind and predecode one window ahead.
	next_submit = maxi(next_submit, i)
	_submit_up_to(i + WINDOW)
	if not tasks.has(i): return null
	WorkerThreadPool.wait_for_task_completion(tasks[i])
	tasks.erase(i)
	mutex.lock()
	var image: Image = results.get(i)
	if image != null: decoded_bytes -= image.get_data_size()
	results.erase(i)
	mutex.unlock()
	if image != null: remember(path, image)
	if image != null: hits += 1
	return image

static func remember(path: String, image: Image) -> void:
	if not active or not reuse_recent_images or image == null or recent_images.has(path): return
	var bytes := image.get_data_size()
	if bytes > CACHE_BYTES: return
	while not recent_images.is_empty() and (cached_bytes + bytes > CACHE_BYTES or recent_images.size() >= CACHE_IMAGES):
		var oldest: String = recent_images.keys()[0]
		cached_bytes -= recent_images[oldest].get_data_size()
		recent_images.erase(oldest)
	var copy := Image.new()
	copy.copy_from(image)
	if image.has_meta("png_sha256"): copy.set_meta("png_sha256", image.get_meta("png_sha256"))
	recent_images[path] = copy
	cached_bytes += bytes

static func end() -> void:
	if not active: return
	active = false
	progress_callback = Callable()
	for i in tasks: WorkerThreadPool.wait_for_task_completion(tasks[i])
	tasks.clear()
	mutex.lock()
	unused_results += results.size()
	results.clear()
	decoded_bytes = 0
	mutex.unlock()
	recent_images.clear()
	cached_bytes = 0
	if recorded != paths and not recorded.is_empty():
		var file := FileAccess.open(manifest_path, FileAccess.WRITE)
		if file != null:
			file.store_string("\n".join(recorded))
			file.close()
	# Keep report totals, not the thousands of path strings used only by loading.
	completed_requests = recorded.size()
	recorded = PackedStringArray()
	paths = PackedStringArray()
	index_of = {}
	batch_order = false

static func service_loading() -> void:
	if active: _pump()

static func _pump() -> void:
	var now := Time.get_ticks_msec()
	if now - last_pump < PUMP_MS or DisplayServer.get_name() == "headless": return
	last_pump = now
	pumps += 1
	DisplayServer.process_events()
	if progress_callback.is_valid():
		# The previous launch's image count stands in for the total; the first launch has none.
		progress_callback.call(clampf(float(recorded.size()) / float(paths.size()), 0.0, 1.0) if not paths.is_empty() and not batch_order else -1.0)
	RenderingServer.force_draw()

static func _submit_up_to(limit: int) -> void:
	limit = mini(limit, paths.size())
	while next_submit < limit:
		tasks[next_submit] = WorkerThreadPool.add_task(_decode.bind(next_submit, paths[next_submit]))
		worker_submissions += 1
		peak_pending = maxi(peak_pending,tasks.size())
		next_submit += 1

static func _decode(i: int, path: String) -> void:
	var started := Time.get_ticks_usec()
	var image: Image = null
	if FileAccess.file_exists(path):
		var bytes := FileAccess.get_file_as_bytes(path)
		if bytes.size() >= 33 and bytes.slice(0, 8) == PackedByteArray([137, 80, 78, 71, 13, 10, 26, 10]):
			image = Image.new()
			if image.load_png_from_buffer(bytes) != OK or image.is_empty(): image = null
			if image != null: image.set_meta("png_sha256", source_digest(bytes))
	mutex.lock()
	results[i] = image
	worker_decode_usec += Time.get_ticks_usec() - started
	if image != null: decoded_bytes += image.get_data_size()
	peak_decoded_bytes = maxi(peak_decoded_bytes, decoded_bytes)
	mutex.unlock()

static func stats() -> Dictionary:
	mutex.lock()
	var result := {"requests": recorded.size() if active else completed_requests, "prefetch_hits": hits, "recent_hits": cache_hits,
		"worker_submissions": worker_submissions, "peak_pending": peak_pending,
		"primed_paths": primed_paths,
		"unused_results": unused_results, "worker_decode_usec": worker_decode_usec,
		"peak_decoded_bytes": peak_decoded_bytes, "recent_cache_budget_bytes": CACHE_BYTES}
	mutex.unlock()
	return result

static func source_digest(bytes: PackedByteArray) -> String:
	var hash := HashingContext.new()
	hash.start(HashingContext.HASH_SHA256)
	hash.update(bytes)
	return hash.finish().hex_encode()
