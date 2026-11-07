extends SceneTree

const Floors = preload("res://rooms/whole-room/modular_floor.gd")
const Common = preload("res://rooms/large-rooms/common.gd")
const Session = preload("res://scripts/session_art_cache.gd")
const SOURCE = "res://assets/department-floors-v1/engineering-tread.png"
var failures := 0
var checks := 0

func _init(): call_deferred("run")
func check(ok: bool, label: String):
	checks += 1
	if not ok:
		failures += 1
		push_error(label)
func pixels(image: Image) -> PackedByteArray:
	var copy: Image = image.duplicate()
	if copy.is_compressed(): copy.decompress()
	copy.convert(Image.FORMAT_RGBA8)
	return copy.get_data()
func settle():
	for index in 3: await process_frame
	await RenderingServer.frame_post_draw
func run():
	if OS.get_user_data_dir() != OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name() == "headless":
		quit(2)
		return
	var path := "res://scripts/tablet_floor_texture.gd"
	var loader = load(path) if ResourceLoader.exists(path) else null
	check(loader != null, "Supported tablets can load prebaked floor pixel storage")
	if loader == null:
		quit(1)
		return
	var original := Image.new()
	check(original.load_png_from_buffer(FileAccess.get_file_as_bytes(SOURCE)) == OK, "Original floor remains available")
	loader.enabled = false
	check(loader.image_for(SOURCE) == null, "Desktop/reference path bypasses tablet storage")
	check(pixels(Floors.texture(SOURCE).get_image()) == pixels(original), "Desktop floor pixels remain exact")
	Floors.textures.clear()
	loader.enabled = true
	loader.supported = false
	check(loader.image_for(SOURCE) == null, "Unsupported driver uses original PNG fallback")
	loader.supported = true
	var encoded: Image = loader.image_for(SOURCE)
	check(encoded != null and encoded.is_compressed(), "Supported path loads precompressed pixels without runtime encoding")
	if encoded == null:
		quit(1)
		return
	check(encoded.get_size() == Vector2i(1254, 1254), "Block compression preserves original logical dimensions")
	check(encoded.get_data_size() < original.get_data_size() / 4, "Floor pixel payload is substantially smaller")
	check(encoded.get_meta("source_sha256") == FileAccess.get_sha256(SOURCE), "Derived floor matches current source artwork")
	var valid_record: Dictionary = loader.RECORDS[SOURCE]
	var stale: Image = encoded.duplicate()
	stale.set_meta("source_sha256", "stale")
	check(not loader.valid_image(stale, SOURCE, valid_record), "Stale derived metadata is rejected")
	check(not loader.valid_image(original, SOURCE, valid_record), "Uncompressed derived resources are rejected")
	check(not loader.valid_image(encoded, "res://wrong.png", valid_record), "Wrong source identity is rejected")
	for source in loader.RECORDS:
		var candidate: Image = loader.image_for(source)
		check(candidate != null and candidate.get_meta("source_sha256") == FileAccess.get_sha256(source), "Every selected floor matches source identity")
	var expected := pixels(encoded)
	check(expected != pixels(original), "Fixture actually exercises the compressed trial")
	for ordinary_first in [true, false]:
		Floors.textures.clear()
		Common.art_textures.clear()
		var owner := Node.new()
		root.add_child(owner)
		Session.retain(owner)
		if ordinary_first: Floors.texture(SOURCE)
		var large: Texture2D = Common._floor_texture(SOURCE)
		var ordinary: Texture2D = Floors.texture(SOURCE)
		check(large.get_rid() == ordinary.get_rid(), "Large and ordinary floors share one upload in either load order")
		check(ordinary.get_size() == Vector2(1254, 1254), "Texture dimensions preserve existing UV coordinates")
		check(pixels(ordinary.get_image()) == expected, "Actual floor factory serves the compressed trial pixels")
		var weak: WeakRef = weakref(ordinary)
		large = null
		ordinary = null
		owner.queue_free()
		await settle()
		check(weak.get_ref() == null, "Final drawing owner releases tablet floor texture")
	check(loader.image_for("res://assets/room-floor-tiles-v5/command-inlay.png") == null, "Unselected artwork retains the normal loading path")
	loader.enabled = false
	print("TABLET FLOOR VRAM: %d checks; %d failures" % [checks, failures])
	quit(1 if failures else 0)
