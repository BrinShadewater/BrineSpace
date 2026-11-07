extends RefCounted
## Resolve layered crew packs before decoding/uploading their surviving frames.
## Weak references preserve every retained bank without keeping replaced art alive.
static var enabled := true # Diagnostic A/B switch; normal play always batches.
var pending := {}
var pool: RefCounted
var stats := {"requested": 0, "loaded": 0, "discarded": 0, "early": 0}

func add(texture: ImageTexture, display: Texture2D, filename: String) -> void:
	pending[texture.get_instance_id()] = {"texture": weakref(texture), "display": weakref(display), "path": filename}
	stats.requested += 1
	# Manifest assembly can spend seconds without requesting a PNG. Register first:
	# servicing the loading window may reenter drawing and inspect this batch.
	preload("res://scripts/image_prefetch.gd").service_loading()

static func populate(texture: ImageTexture, display: Texture2D, filename: String) -> void:
	var image := Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, filename)
	texture.set_image(image)
	var used := Rect2(image.get_used_rect())
	var pivot: Vector2 = texture.get_meta("crew_pivot")
	var density := 65.28 / float(texture.get_meta("crew_standing_height"))
	var extent := Rect2((used.position - pivot) * density, used.size * density)
	texture.set_meta("crew_alpha_extent", extent)
	if display != null and display != texture: display.set_meta("crew_alpha_extent", extent)

func materialize(display: Texture2D, early: bool = true) -> void:
	var texture: Texture2D = display.diffuse_texture if display is CanvasTexture else display
	var id := texture.get_instance_id()
	if not pending.has(id): return
	var record: Dictionary = pending[id]
	# Remove before decoding: the loading screen may pump reentrant drawing.
	pending.erase(id)
	var wrapper: Texture2D = record.display.get_ref()
	if pool != null and wrapper is CanvasTexture:
		var shared: Dictionary = pool.acquire(record.path, wrapper.texture_filter)
		var density := 65.28 / float(texture.get_meta("crew_standing_height"))
		var pivot: Vector2 = texture.get_meta("crew_pivot")
		var used: Rect2 = shared.used
		wrapper.set_meta("crew_alpha_extent", Rect2((used.position - pivot) * density, used.size * density))
		wrapper.diffuse_texture = shared.texture
	else:
		populate(texture, wrapper, record.path)
	stats.loaded += 1
	if early: stats.early += 1

func finish() -> Dictionary:
	for id in pending.keys():
		var texture: ImageTexture = pending[id].texture.get_ref()
		if texture == null:
			pending.erase(id)
			stats.discarded += 1
		else:
			materialize(texture, false)
	return stats.duplicate()
