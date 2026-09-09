extends RefCounted
## Dimensioned front/edge-on construction with registered concept surfaces.
const SOURCE := "res://rooms/doors/department-source-v1.png"
const VARIANTS := ["bio","life-support","engineering","generic","brine","metal"]
static var leaf_art: ImageTexture
const APERTURE := 72.0
const SIDE_POST_DEPTH := 16.0 # Same as the canonical wall/socket cap.
const SIDE_HEIGHT := 3.0 # Same top lift as the shared room wall cutaway.
const WALL_SOURCE := "res://rooms/whole-room/nursery-master.png"

static func side_post_rect(north: bool) -> Rect2:
	# Project identical ground footprints upward, rather than tuning two heights.
	var ground_start := -APERTURE/2.0-SIDE_POST_DEPTH if north else APERTURE/2.0
	return Rect2(-8,ground_start-SIDE_HEIGHT,16,SIDE_POST_DEPTH+SIDE_HEIGHT)

static func department(room: Dictionary) -> String:
	match str(room.get("id","")):
		"corridor", "corner", "tee_corridor": return "metal"
		"mycelium_nursery", "hydroponics_bay", "biodome", "biomass_digester": return "bio"
		"life_support", "med_bay", "med_office", "med_center", "cryo_chamber", "clone_lab", "airlock": return "life-support"
		"reactor", "mining_drone_bay", "ore_refinery", "maintenance_bay", "battery_array", "solar_array", "thermal_power_control", "construction_drone_bay": return "engineering"
		"brine_core": return "brine"
	return "generic"

static func pair_variant(a: Dictionary, b: Dictionary) -> String:
	if department(a)=="metal" or department(b)=="metal": return "metal"
	return department(a) if department(a)==department(b) else "generic"

static func make_materials(host: Node, source: Texture2D) -> Dictionary:
	var result := {}
	for mode in ["paint","generic","emission"]:
		var viewport := SubViewport.new()
		viewport.name = "DoorMaterial"+mode
		viewport.size = source.get_size()
		viewport.transparent_bg = true
		viewport.disable_3d = true
		viewport.render_target_update_mode = SubViewport.UPDATE_ONCE
		var sprite := Sprite2D.new()
		sprite.texture = source
		sprite.centered = false
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		var shader := Shader.new()
		shader.code = """shader_type canvas_item;
render_mode unshaded;
uniform int mode = 0;
void fragment() {
 vec4 s = texture(TEXTURE,UV);
 vec2 p = UV * vec2(1536.0,1024.0);
 float origin = p.x < 500.0 ? 52.0 : (p.x < 1000.0 ? 554.0 : 1050.0);
 float x = p.x-origin;
 bool jamb = p.y>280.0 && p.y<347.0 && (x<26.0 || x>388.0);
 bool head = p.y>130.0 && p.y<160.0 && ((x>50.0 && x<77.0) || (x>177.0 && x<237.0) || (x>337.0 && x<371.0));
 float lens = (jamb || head) ? smoothstep(0.62,0.84,min(s.r,min(s.g,s.b))) : 0.0;
 vec3 paint = mix(s.rgb,vec3(0.12,0.14,0.15),lens);
 if(mode==1) paint=vec3(dot(paint,vec3(0.299,0.587,0.114)));
 COLOR = mode==2 ? vec4(vec3(1.0),s.a*lens) : vec4(paint,s.a);
}
"""
		var material := ShaderMaterial.new()
		material.shader = shader
		material.set_shader_parameter("mode",["paint","generic","emission"].find(mode))
		sprite.material = material
		viewport.add_child(sprite)
		host.add_child(viewport)
		result[mode] = viewport.get_texture()
	var wall_image := Image.new()
	if wall_image.load_png_from_buffer(FileAccess.get_file_as_bytes(WALL_SOURCE))==OK:
		result["wall"] = ImageTexture.create_from_image(wall_image)
	return result

static func piece(rect: Rect2, source: Rect2, depth: float, floor_piece := false) -> Dictionary:
	return {"rect":rect,"source":source,"depth":depth,"floor":floor_piece}

static func parts(frame: int, vertical: bool, variant: String) -> Array:
	# Shared cutaway height keeps a north/south crossing visible above the track.
	# Retain rigid sliding leaves and the same 72-unit aperture in both orientations.
	return side_parts(frame,variant) if vertical else corridor_parts(frame,false,variant)

static func side_open_prototype(variant: String) -> Array:
	# Retained fixture entry point; the accepted silhouette now has moving leaves.
	return side_parts(9,variant)

static func corridor_parts(frame: int, vertical: bool, variant: String) -> Array:
	# Narrow hulls need a low front collar too, not the full-height room arch.
	if vertical: return side_parts(frame,variant)
	var result: Array = []
	for source_part in side_parts(frame,variant):
		var part: Dictionary = source_part.duplicate()
		var r: Rect2 = part.rect
		if part.floor or part.get("leaf",false):
			part.rect = Rect2(Vector2(r.position.y,r.position.x),Vector2(r.size.y,r.size.x))
			part.depth = 0.0
			part["front_leaf"] = part.get("leaf",false)
			part.erase("leaf") # Front surface retains the generated leaf material.
		else:
			var ground_y := -52.0 if float(part.depth)<0 else 36.0
			part.rect = Rect2(Vector2(ground_y+r.position.x+8,r.position.y-ground_y-8),r.size)
			part.depth = 8.0
		result.append(part)
	return result

static func side_parts(frame: int, variant: String) -> Array:
	# Match draw_wall/draw_cap's 3-unit lift and 4-unit fascia. No overhead rail.
	var trim: Color = {"bio":Color("78886a"),"life-support":Color("71898a"),"engineering":Color("aa764c"),"generic":Color("8a8d8a")}.get(variant,Color("8a8d8a"))
	var out: Array = []
	out.append(solid_piece(Rect2(-10,-36,20,72),Color("39434a"),0,true))
	out.append(solid_piece(Rect2(-8,-36,16,72),Color("657075"),0,true))
	# Recessed center track is part of the floor, always beneath feet/shadow.
	out.append(solid_piece(Rect2(-1,-36,2,72),Color("303a40"),0,true))
	var t := clampf(frame/9.0,0,1)
	var travel := roundf(72*t*t*(3-2*t))/2.0
	var remaining := 36.0-travel
	if remaining>0:
		# Clip two rigid panel surfaces at the pocket mouths; no height stretching.
		for north in [true,false]:
			var y := -36.0 if north else travel
			var leaf := solid_piece(Rect2(-5,y,10,remaining),trim,-36+remaining if north else 36)
			leaf["leaf"] = true
			leaf["north"] = north
			out.append(leaf)
	for north in [true,false]:
		var ground_y := -52.0 if north else 36.0
		var depth := ground_y+16.0
		out.append(solid_piece(Rect2(-8,ground_y+13,16,4),Color("252e33"),depth))
		out.append(solid_piece(Rect2(-8,ground_y-3,16,16),Color("a9a89a"),depth))
		var cap := piece(Rect2(-7.3,ground_y-2.3,14.6,14.6),Rect2(78,47,30,27),depth)
		cap["wall"] = true
		out.append(cap)
		var lens := solid_piece(Rect2(-1,ground_y+3,2,4),Color.WHITE,depth)
		lens["emissive"] = true
		out.append(lens)
	return out

static func solid_piece(rect: Rect2, color: Color, depth: float, floor_piece := false) -> Dictionary:
	return {"rect":rect,"color":color,"depth":depth,"floor":floor_piece}

static func draw_piece(canvas: CanvasItem, materials: Dictionary, variant: String, part: Dictionary, level: float) -> void:
	if part.get("wall",false):
		canvas.draw_texture_rect_region(preload("res://rooms/doors/door_finish.gd").texture("low"),part.rect,Rect2(84,183,62,340),preload("res://rooms/doors/door_finish.gd").tint(variant))
		return
	if part.has("color"):
		var color: Color = part.color
		if part.get("emissive",false): color = Color("29353a").lerp(Color("abb8a9"),clampf(level,0,1))
		canvas.draw_rect(part.rect,color)
		if part.get("leaf",false) or part.get("front_leaf",false):
			preload("res://rooms/doors/door_finish.gd").low_leaf(canvas,part.rect,part.get("north",false),not part.get("front_leaf",false),variant)
		if part.get("leaf",false):
			var r: Rect2 = part.rect
			canvas.draw_rect(Rect2(r.position,Vector2(1,r.size.y)),Color("bfc5bb"))
			canvas.draw_rect(Rect2(r.position+Vector2(8,0),Vector2(2,r.size.y)),Color("303a40"))
			var seam_y := r.end.y-1 if part.north else r.position.y
			canvas.draw_rect(Rect2(r.position.x,seam_y,10,minf(1,r.size.y)),Color("202b30"))
		return
	for mode in ["generic" if variant=="generic" else "paint","emission"]:
		if mode=="emission" and level<=0: continue
		var texture: Texture2D = materials[mode]
		var tint := Color(1,1,1,clampf(level,0,1)) if mode=="emission" else Color.WHITE
		var rect: Rect2 = part.rect
		var source: Rect2 = part.source
		if not part.get("chamfer",false):
			canvas.draw_texture_rect_region(texture,rect,source,tint)
		else:
			var points := PackedVector2Array([Vector2(0,36),Vector2(30,0),Vector2(386,0),Vector2(418,36),Vector2(418,69),Vector2(0,69)])
			var vertices := PackedVector2Array()
			var uv := PackedVector2Array()
			for p in points:
				vertices.append(rect.position+p*rect.size/source.size)
				uv.append((source.position+p)/Vector2(texture.get_size()))
			canvas.draw_polygon(vertices,PackedColorArray([tint]),uv,texture)
