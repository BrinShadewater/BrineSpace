extends RefCounted
## Startup image pre-decoding (owner playtest: the loading screen looked like it was about to
## crash). Building the station decodes ~8,900 PNGs (~740 MB) one after another on the main
## thread, about 10 of the ~18 seconds the window freezes. While active, SafeImage asks here
## first: the order images were requested on the previous launch is replayed on worker
## threads, a bounded window ahead of the main thread, so decoding runs in parallel without
## holding every image at once. Each launch records the order again for the next one.
##
## Only the title screen's loading transition turns this on. Fixtures that instantiate the
## game directly decode exactly as before.

const MANIFEST := "user://startup_images.txt"
const WINDOW := 96

static var active := false
static var manifest_path := MANIFEST
static var recorded := PackedStringArray()
static var paths := PackedStringArray()
static var index_of: Dictionary = {}
static var tasks: Dictionary = {}
static var results: Dictionary = {}
static var next_submit := 0
static var hits := 0
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
	paths = PackedStringArray()
	index_of = {}
	tasks = {}
	results = {}
	next_submit = 0
	hits = 0
	if FileAccess.file_exists(manifest):
		for line in FileAccess.get_file_as_string(manifest).split("\n", false):
			if line.begins_with("res://") and not index_of.has(line):
				index_of[line] = paths.size()
				paths.append(line)

# The decoded image for a PNG path, or null to decode it the usual way (not active, not in
# the previous launch's order, or already handed out once).
static func take(path: String) -> Image:
	if not active: return null
	recorded.append(path)
	_pump()
	if not index_of.has(path): return null
	var i: int = index_of[path]
	_submit_up_to(i + WINDOW)
	if not tasks.has(i): return null
	WorkerThreadPool.wait_for_task_completion(tasks[i])
	tasks.erase(i)
	mutex.lock()
	var image: Image = results.get(i)
	results.erase(i)
	mutex.unlock()
	# Images the new order skipped would otherwise stay decoded; release those well behind.
	for j in tasks.keys():
		if j < i - WINDOW:
			WorkerThreadPool.wait_for_task_completion(tasks[j])
			tasks.erase(j)
			mutex.lock()
			results.erase(j)
			mutex.unlock()
	if image != null: hits += 1
	return image

static func end() -> void:
	if not active: return
	active = false
	progress_callback = Callable()
	for i in tasks: WorkerThreadPool.wait_for_task_completion(tasks[i])
	tasks.clear()
	mutex.lock()
	results.clear()
	mutex.unlock()
	if recorded != paths and not recorded.is_empty():
		var file := FileAccess.open(manifest_path, FileAccess.WRITE)
		if file != null:
			file.store_string("\n".join(recorded))
			file.close()

static func _pump() -> void:
	var now := Time.get_ticks_msec()
	if now - last_pump < PUMP_MS or DisplayServer.get_name() == "headless": return
	last_pump = now
	pumps += 1
	DisplayServer.process_events()
	if progress_callback.is_valid():
		# The previous launch's image count stands in for the total; the first launch has none.
		progress_callback.call(clampf(float(recorded.size()) / float(paths.size()), 0.0, 1.0) if not paths.is_empty() else -1.0)
	RenderingServer.force_draw()

static func _submit_up_to(limit: int) -> void:
	limit = mini(limit, paths.size())
	while next_submit < limit:
		tasks[next_submit] = WorkerThreadPool.add_task(_decode.bind(next_submit, paths[next_submit]))
		next_submit += 1

static func _decode(i: int, path: String) -> void:
	var image: Image = null
	if FileAccess.file_exists(path):
		var bytes := FileAccess.get_file_as_bytes(path)
		if bytes.size() >= 33 and bytes.slice(0, 8) == PackedByteArray([137, 80, 78, 71, 13, 10, 26, 10]):
			image = Image.new()
			if image.load_png_from_buffer(bytes) != OK or image.is_empty(): image = null
	mutex.lock()
	results[i] = image
	mutex.unlock()
