extends RefCounted
## Session-owned, immutable pixel storage. Frame wrappers retain their own identity
## and metadata; weak lookup entries cannot keep abandoned animation banks alive.
static var enabled := true # Diagnostic comparison only.
var sources := {}
var pixels := {}
## Opt-in audit retains metadata and weak references only, including after lookup
## release. Never read GPU pixels or traverse the scene to produce this report.
var inventory_enabled := OS.get_cmdline_user_args().has("--texture-inventory=true")
var inventory_limit := 20000
var inventory_records: Array[Dictionary] = []
var inventory_dropped := 0
var stats := {"requests": 0, "source_hits": 0, "pixel_hits": 0, "uploads": 0,
	"requested_bytes": 0, "uploaded_bytes": 0, "decode_usec": 0, "hash_usec": 0, "upload_usec": 0,
	"alpha_bounds_usec": 0}

func acquire(filename: String, frame_filter: int = -1) -> Dictionary:
	stats.requests += 1
	if sources.has(filename):
		var known: Dictionary = sources[filename]
		var live: ImageTexture = known.texture.get_ref()
		if live != null:
			_inventory_filter(known, frame_filter)
			stats.source_hits += 1
			stats.requested_bytes += known.bytes
			return {"texture": live, "used": known.used}
	var stamp := Time.get_ticks_usec()
	var image := Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, filename, true)
	stats.decode_usec += Time.get_ticks_usec() - stamp
	stamp = Time.get_ticks_usec()
	# Identical raw PNG bytes imply identical decoded pixels/format/mipmaps. Hash
	# the small encoded source, not megabytes of transparent decoded canvas.
	var key := str(image.get_meta("png_sha256", ""))
	if key.is_empty(): key = "unavailable:" + filename
	stats.hash_usec += Time.get_ticks_usec() - stamp
	var record: Dictionary = pixels.get(key, {})
	var texture: ImageTexture = record.texture.get_ref() if not record.is_empty() else null
	if texture == null:
		stamp = Time.get_ticks_usec()
		texture = ImageTexture.create_from_image(image)
		texture.set_meta("crew_immutable_pixels",true)
		stats.upload_usec += Time.get_ticks_usec() - stamp
		stats.uploads += 1
		stats.uploaded_bytes += image.get_data_size()
		stamp = Time.get_ticks_usec()
		var used := Rect2(image.get_used_rect())
		stats.alpha_bounds_usec += Time.get_ticks_usec() - stamp
		record = {"texture": weakref(texture), "used": used, "bytes": image.get_data_size(),
			"size": image.get_size(), "format": image.get_format(), "mipmaps": image.has_mipmaps(), "signature": key}
		pixels[key] = record
		if inventory_enabled:
			if inventory_records.size() < inventory_limit:
				record["first_source"] = filename
				inventory_records.append(record)
			else:
				inventory_dropped += 1
	else:
		stats.pixel_hits += 1
	stats.requested_bytes += record.bytes
	sources[filename] = record
	_inventory_filter(record, frame_filter)
	return {"texture": texture, "used": record.used}

func _inventory_filter(record: Dictionary, frame_filter: int) -> void:
	if not inventory_enabled or not record.has("first_source"): return
	if not record.has("requested_filters"): record["requested_filters"] = []
	if not record.requested_filters.has(frame_filter): record.requested_filters.append(frame_filter)

func clear_lookup() -> void:
	# Live frame wrappers own the textures. Discard startup-only path/hash tables.
	sources.clear()
	pixels.clear()

func inventory_snapshot() -> Dictionary:
	var started := Time.get_ticks_usec()
	var rows: Array[Dictionary] = []
	var live_bytes := 0
	var expired := 0
	for record in inventory_records:
		if record.texture.get_ref() == null:
			expired += 1
			continue
		var size: Vector2i = record.size
		var used: Rect2 = record.used
		live_bytes += int(record.bytes)
		rows.append({"source": record.first_source, "bytes": record.bytes,
			"width": size.x, "height": size.y, "format": record.format,
			"mipmaps": record.mipmaps, "signature": record.signature,
			"requested_filters": record.get("requested_filters", []),
			"used_rect": [used.position.x, used.position.y, used.size.x, used.size.y]})
	return {"enabled": inventory_enabled, "scope": "Pool uploads only; first source per storage; decoded bytes, not total GPU residency",
		"complete": inventory_enabled and inventory_dropped == 0,
		"record_limit": inventory_limit, "dropped_records": inventory_dropped,
		"expired_records": expired, "live_records": rows.size(), "live_decoded_bytes": live_bytes,
		"records": rows, "collection_usec": Time.get_ticks_usec() - started}
