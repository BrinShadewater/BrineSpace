extends SceneTree
const Player = preload("res://scripts/crew_sprite_player.gd")
const Pool = preload("res://scripts/crew_texture_pool.gd")
var failures := 0
var checks := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func run() -> void:
	var image := Image.create(16, 16, false, Image.FORMAT_RGBA8)
	image.fill(Color.TRANSPARENT)
	image.fill_rect(Rect2i(2, 3, 5, 9), Color.CORAL)
	image.save_png("user://pool-a.png")
	image.save_png("user://pool-b.png")
	var file := FileAccess.open("user://pool.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"pivot": [7, 14], "standingHeight": 12, "states": [
		{"id": "walk-east", "frameFiles": ["pool-a.png", "pool-b.png", "pool-a.png"], "frameDurationsMs": [100, 150, 200], "loop": true,
		"depthOffsets": [0, 1, 2], "facings": ["east", "north", "west"]}]}))
	file.close()
	var pool := Pool.new()
	check(not pool.inventory_enabled, "Normal play does not retain audit records")
	pool.inventory_enabled = true
	var eager := Player.new()
	eager.load_manifest("user://pool.json")
	var player := Player.new()
	player.begin_texture_batch(pool)
	player.load_manifest("user://pool.json")
	player.finish_texture_batch()
	var row: Array = player.frames["walk-east"]
	check(pool.stats.uploads == 1 and pool.stats.source_hits == 1 and pool.stats.pixel_hits == 1, "One upload across identical paths and identical files")
	check(row[0] != row[1] and row[1] != row[2], "Frame identities remain separate")
	check(row[0].diffuse_texture == row[1].diffuse_texture, "GPU pixels are shared")
	for i in row.size():
		check(row[i].get_image().get_data() == eager.frames["walk-east"][i].get_image().get_data(), "Exact pixels")
		check(row[i].texture_filter == CanvasItem.TEXTURE_FILTER_PARENT_NODE, "Original inherited filter preserved")
		for key in eager.frames["walk-east"][i].get_meta_list():
			check(row[i].get_meta(key) == eager.frames["walk-east"][i].get_meta(key), "Independent frame metadata: " + str(key))
	row[0].set_meta("crew_water_facing", "south")
	check(row[1].get_meta("crew_water_facing") == "north", "Metadata mutation cannot reach another frame")
	var copy: Image = row[0].get_image()
	copy.fill(Color.BLUE)
	check(row[1].get_image().get_data() == image.get_data(), "Readback modification cannot corrupt shared texture")
	var held: WeakRef = weakref(row[0].diffuse_texture)
	var filter_hit := pool.acquire("user://pool-a.png", CanvasItem.TEXTURE_FILTER_LINEAR)
	filter_hit.clear()
	check(pool.inventory_snapshot().records[0].requested_filters == [CanvasItem.TEXTURE_FILTER_PARENT_NODE, CanvasItem.TEXTURE_FILTER_LINEAR], "Audit retains both filters when one storage serves mixed wrappers")
	pool.clear_lookup()
	check(pool.sources.is_empty() and pool.pixels.is_empty(), "Startup lookup tables release")
	check(held.get_ref() != null, "Selected bank owns its texture after lookup release")
	var inventory := pool.inventory_snapshot()
	check(inventory.complete and inventory.live_records == 1 and inventory.live_decoded_bytes == 1024, "Inventory counts unique live storage after lookup release")
	check(inventory.records[0].used_rect == [2.0, 3.0, 5.0, 9.0], "Inventory preserves alpha bounds without readback")
	row.clear()
	player.frames.clear()
	check(held.get_ref() == null, "Last bank release frees shared texture")
	check(pool.inventory_snapshot().live_records == 0 and pool.inventory_snapshot().expired_records == 1, "Audit metadata cannot retain textures")
	# A new session must observe an edited source rather than a stale global cache.
	image.fill(Color.GREEN)
	image.save_png("user://pool-a.png")
	var next := Pool.new()
	var loaded := next.acquire("user://pool-a.png")
	check(loaded.texture.get_image().get_data() == image.get_data(), "New session sees changed source")
	check(next.inventory_snapshot().records.is_empty(), "Disabled audit allocates no upload records")
	next.inventory_enabled = true
	next.inventory_limit = 0
	var capped := next.acquire("user://pool-b.png")
	check(capped.texture != null and next.inventory_snapshot().dropped_records == 1 and not next.inventory_snapshot().complete, "Audit cap explicitly marks incomplete coverage without blocking upload")
	print("CREW TEXTURE POOL ", "PASS" if failures == 0 else "FAIL", ": ", checks, " checks, ", failures, " failures")
	quit(1 if failures else 0)
