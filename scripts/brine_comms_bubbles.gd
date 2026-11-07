extends Control
const PORTRAIT_CROP := Rect2(0, 0, 1, 1)
## Sparse glass bubbles, masked by BRINE's foreground silhouette.
var FOREGROUND := PackedVector2Array([
	Vector2(.43,.03), Vector2(.56,.03), Vector2(.68,.10),
	Vector2(.75,.23), Vector2(.77,.48), Vector2(.74,.60),
	Vector2(.69,.74), Vector2(.69,.80), Vector2(.83,.85),
	Vector2(.96,.87), Vector2(1.0,.93), Vector2(1.0,1.0),
	Vector2(0,1.0), Vector2(0,.92), Vector2(.10,.86),
	Vector2(.27,.83), Vector2(.35,.78), Vector2(.35,.73),
	Vector2(.27,.68), Vector2(.22,.52), Vector2(.21,.34),
	Vector2(.25,.21), Vector2(.33,.10)])
var elapsed := 0.0

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

func advance(delta: float) -> void:
	elapsed += delta
	queue_redraw()

func glass_at(point: Vector2) -> bool:
	return point.x > .025 and point.x < .975 and point.y > .04 and point.y < .94 and not Geometry2D.is_point_in_polygon(point, FOREGROUND)

func cropped_glass_at(point: Vector2) -> bool:
	return glass_at(PORTRAIT_CROP.position + point * PORTRAIT_CROP.size)

func _draw() -> void:
	var side := minf(size.x, size.y)
	var origin := (size - Vector2.ONE * side) * .5
	# Staggered bubbles are already in flight when the portrait opens.
	# Wider glass lanes keep them visible beside the hair at thumbnail sizes.
	for index in range(5):
		var age := fposmod(elapsed + index * 1.45 + 1.0, 7.5)
		var center := Vector2(.10 if index % 2 == 0 else .90, .91 - age * .112)
		center.x += sin(age * 1.8 + index) * .012
		var radius := .006 if index % 2 == 0 else .0045
		var opacity := minf(age * 2.0, 1.0) * minf((7.5-age)*2.0, 1.0) * .55
		for segment in range(24):
			var a := center + Vector2.from_angle(TAU * segment / 24.0) * radius
			var b := center + Vector2.from_angle(TAU * (segment+1) / 24.0) * radius
			if cropped_glass_at(a) and cropped_glass_at(b):
				draw_line(origin+a*side, origin+b*side, Color(.82,1.0,.98,opacity), .6, true)
