extends SceneTree
## A corner piece's equipment shadow follows the two arms of its L, so the open floor inside the corner
## stays clear (Brine Core, owner report Sept 29). Ordinary props and props with a footprint shade one area.
const RoomLighting = preload("res://rooms/whole-room/room_lighting.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	# The Brine Core's north-east corner console, as measured in the running game.
	var rect := Rect2(36.0, -192.0, 150.1587, 139.3225)
	var corner := {"rect": rect, "corner": "northeast", "collision_boxes": [[0.0, 0.0, 1.0, 0.29], [0.75, 0.29, 0.25, 0.71]]}
	var feet: Array = RoomLighting.shadow_feet(corner, rect)
	expect(feet.size() == 2, "A corner piece shades its two arms (got %d areas)" % feet.size())
	var inside := rect.position + rect.size * Vector2(0.35, 0.65) # open floor inside the L
	var covered := false
	for foot in feet: if foot.has_point(inside): covered = true
	expect(not covered, "The open floor inside the corner is not shaded")
	var shaded := 0.0
	for foot in feet: shaded += foot.get_area()
	expect(shaded < rect.get_area() * 0.6, "The arms cover well under the whole art box (%.0f%%)" % (100.0 * shaded / rect.get_area()))
	var plain := {"rect": rect}
	expect(RoomLighting.shadow_feet(plain, rect) == [rect], "An ordinary prop shades its whole footprint")
	var footed := {"rect": rect, "footprint": [0.0, 0.7, 1.0, 0.3], "corner": "northeast", "collision_boxes": corner.collision_boxes}
	expect(RoomLighting.shadow_feet(footed, Rect2(1, 2, 3, 4)) == [Rect2(1, 2, 3, 4)], "A prop with an authored footprint keeps it")
	print("CORNER SHADOW: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
