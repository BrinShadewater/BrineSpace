extends SceneTree
const Prefetch = preload("res://scripts/image_prefetch.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func run() -> void:
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\", "/").trim_suffix("/")
	check(not expected.is_empty() and OS.get_user_data_dir().replace("\\", "/").trim_suffix("/") == expected, "Policy fixture uses the isolated profile")
	if failures: quit(1); return
	# Announce-only names never reach a decoder: this exercises startup policy,
	# with no artificial image allocations or missing-art fallback.
	var order := PackedStringArray(["res://integration-policy/one.png", "res://integration-policy/two.png"])
	root.set_meta("tablet_controls", true)
	Prefetch.begin("user://integration-tablet-prime.images")
	Prefetch.prime(order)
	check(Prefetch.paths.is_empty(), "Tablet does not enqueue additional first-profile images")
	check(int(Prefetch.stats().primed_paths) == 0, "Tablet first-profile priming stays disabled")
	Prefetch.end()
	root.remove_meta("tablet_controls")
	if not OS.has_feature("ios"):
		Prefetch.begin("user://integration-desktop-prime.images")
		Prefetch.prime(order)
		check(Prefetch.paths.size() == 2 and int(Prefetch.stats().primed_paths) == 2, "Desktop retains first-profile priming")
		check(int(Prefetch.stats().worker_submissions) == 0, "Announcing paths does not request their pixels")
		Prefetch.end()
	print("INTEGRATION LOADING POLICY ", "PASS" if failures == 0 else "FAIL", ": ", failures, " failures")
	quit(1 if failures else 0)
