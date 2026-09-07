extends RefCounted
## Conservative draw envelopes, not collision footprints or ground depth anchors.
const Art = preload("res://scripts/drone_art.gd")

static func asset_rect(id: String, center: Vector2, width: float) -> Rect2:
	var source: Rect2 = Art.REGIONS[id]
	var size := Vector2(width,width*source.size.y/source.size.x)
	return Rect2(center-size*0.5,size)

static func bounds(prop: Dictionary, kind: String) -> Rect2:
	var center := Vector2(prop.rect.get_center().x,prop.rect.end.y-35)
	if str(prop.id).ends_with("_hatch"):
		# The fully open aperture and its outline remain inside this atlas quad.
		return asset_rect("hatch",center,90)
	# Keep a stable envelope when deployed; layout must not jump with fleet state.
	# The two cradle diagnostic lenses are also inside the cradle draw quad.
	return asset_rect("cradle",center,90).merge(asset_rect(kind,center-Vector2(0,15),70))
