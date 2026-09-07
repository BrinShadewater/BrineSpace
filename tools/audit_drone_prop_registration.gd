extends SceneTree
## Read-only decoded-alpha envelope audit. Not a physical footprint/occlusion test.
const Art = preload("res://scripts/drone_art.gd")
func _init() -> void:
	call_deferred("run")

func asset_bounds(id: String, center: Vector2, width: float, atlas_image: Image) -> Rect2:
	var region: Rect2 = Art.REGIONS[id]
	var used := atlas_image.get_region(Rect2i(region)).get_used_rect()
	var scale := width / region.size.x
	return Rect2(center-region.size*scale*0.5+Vector2(used.position)*scale,Vector2(used.size)*scale)

func rect_values(rect: Rect2) -> Array:
	return [rect.position.x,rect.position.y,rect.size.x,rect.size.y]

func run() -> void:
	var atlas_image: Image = Art.atlas().get_image()
	var records: Array = []
	var failures := 0
	for kind in ["mining","salvage"]:
		var path := "res://rooms/production-ten/%s_drone_bay_view.gd" % kind
		var view = load(path).new()
		view.embedded = true
		root.add_child(view)
		for q in range(4):
			view.configure_embedded(q,[],false,0.0)
			for prop in view.props:
				if prop.id not in [kind+"_rov",kind+"_hatch"]: continue
				var center := Vector2(prop.rect.get_center().x,prop.rect.end.y-35)
				var actual: Rect2
				if str(prop.id).ends_with("_rov"):
					actual = asset_bounds("cradle",center,90,atlas_image).merge(asset_bounds(kind,center-Vector2(0,15),70,atlas_image))
				else:
					actual = asset_bounds("hatch",center,90,atlas_image)
				var registered: Rect2 = view.prop_visual_bounds(prop)
				if not registered.grow(0.01).encloses(actual): failures += 1
				records.append({"room":kind,"quarter":q,"prop":prop.id,"registered_visual":rect_values(registered),"decoded_alpha":rect_values(actual),"proxy_encloses_alpha":registered.grow(0.01).encloses(actual),"alpha_inside_walls":Rect2(-180,-180,360,360).encloses(actual),"ground_rect":rect_values(prop.rect),"sort_y":prop.sort_y,"alpha_bottom_minus_sort":actual.end.y-float(prop.sort_y)})
		view.free()
	print(JSON.stringify({"scope":"Occupied stationary atlas alpha envelopes only; excludes diagnostic lenses, hatch aperture and physical occlusion approval","atlas_sha256":FileAccess.get_sha256(Art.SOURCE),"records":records},"\t"))
	quit(1 if "--require-enclosure" in OS.get_cmdline_user_args() and failures > 0 else 0)
