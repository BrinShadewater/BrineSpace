extends SceneTree

const Scope = preload("res://scripts/session_art_cache.gd")
const Common = preload("res://rooms/large-rooms/common.gd")
const Studio = preload("res://scripts/room_layout_editor.gd")
const PATHS = [
	"res://rooms/large-rooms/art/cargo_gantry.png",
	"res://rooms/large-rooms/art/cargo_wall_bank.png",
	"res://rooms/large-rooms/art/grow_beds.png",
	"res://rooms/large-rooms/art/grow_wall_bank.png",
	"res://rooms/large-rooms/art/mini_sub.png",
	"res://rooms/large-rooms/art/launch_wall_bank.png",
	"res://rooms/large-rooms/art/tidal_turbine.png",
	"res://rooms/large-rooms/art/tidal_wall_bank.png",
]
var checks := 0
var failures := 0

class Painter extends Node2D:
	func _draw():
		for index in PATHS.size():
			Common.sprite(self, PATHS[index], Rect2((index % 4) * 128, (index / 4) * 128, 128, 128))

func _init(): call_deferred("run")

func check(ok: bool, label: String):
	checks += 1
	if not ok:
		failures += 1
		push_error(label)

func settle():
	for index in 3: await process_frame
	await RenderingServer.frame_post_draw

func run():
	if OS.get_user_data_dir() != OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name() == "headless":
		quit(2)
		return
	root.set_disable_input(true)
	var capture := SubViewport.new()
	capture.size = Vector2i(512, 256)
	capture.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(capture)
	# Real Studio registration must protect images when gameplay closes first.
	# Closing Studio first must likewise leave the gameplay owner's drawing intact.
	for studio_first in [false, true]:
		var game := Painter.new()
		capture.add_child(game)
		Scope.retain(game)
		await settle()
		var pixels := capture.get_texture().get_image().get_data()
		var refs: Array[WeakRef] = []
		for path in PATHS: refs.append(weakref(Common.art_textures[path]))
		var studio = Studio.new()
		root.add_child(studio)
		await settle()
		check(Scope.owners.size() == 2, "Actual Studio and gameplay both register ownership")
		if studio_first:
			studio.queue_free()
		else:
			game.queue_free()
		await settle()
		for ref in refs: check(ref.get_ref() != null, "Surviving owner protects large-room artwork")
		if studio_first:
			check(pixels == capture.get_texture().get_image().get_data(), "Closing Studio preserves retained gameplay pixels")
			game.queue_free()
		else:
			studio.queue_free()
		game = null
		studio = null
		await settle()
		check(Scope.owners.is_empty(), "Final drawing owner exited")
		for ref in refs: check(ref.get_ref() == null, "Final owner releases large-room texture allocation")
		check(Common.art_textures.is_empty(), "Final owner leaves no large-room image aliases")
		game = Painter.new()
		capture.add_child(game)
		Scope.retain(game)
		await settle()
		check(pixels == capture.get_texture().get_image().get_data(), "Reentry regenerates exact original artwork pixels")
		game.queue_free()
		game = null
		await settle()
	var reference := Painter.new()
	capture.add_child(reference)
	Scope.retain(reference)
	await settle()
	var retained: WeakRef = weakref(Common.art_textures[PATHS[0]])
	Scope.enabled = false
	reference.queue_free()
	reference = null
	await settle()
	check(Scope.owners.is_empty() and retained.get_ref() != null, "Reference mode retains art without retaining scene leases")
	Scope.enabled = true
	var final_owner := Node.new()
	root.add_child(final_owner)
	Scope.retain(final_owner)
	final_owner.queue_free()
	await settle()
	check(retained.get_ref() == null and Common.art_textures.is_empty(), "Restored cleanup releases reference-mode art after next final exit")
	capture.queue_free()
	await settle()
	print("LARGE ROOM ART LIFETIME: %d checks; %d failures" % [checks, failures])
	quit(1 if failures else 0)
