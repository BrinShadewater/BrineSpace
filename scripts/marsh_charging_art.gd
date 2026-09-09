extends RefCounted
## Fluid travels through source-registered hoses, driven only by saved charge time.
static var textures := {}
const PATHS := [
	[Vector2(254,895),Vector2(258,864),Vector2(283,835),Vector2(311,807),Vector2(324,770),Vector2(330,705)],
	[Vector2(770,895),Vector2(766,864),Vector2(741,835),Vector2(713,807),Vector2(700,770),Vector2(694,705)],
	[Vector2(363,638),Vector2(397,633),Vector2(424,615),Vector2(441,591),Vector2(450,558)],
	[Vector2(661,638),Vector2(627,633),Vector2(600,615),Vector2(583,591),Vector2(574,558)]
]

static func texture(empty: bool) -> Texture2D:
	var key := "empty" if empty else "occupied"
	if not textures.has(key):
		var image := Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/marsh-charging-v1/%s.png" % key)) != OK: push_error("Failed to load image (scripts/marsh_charging_art.gd)")
		textures[key]=ImageTexture.create_from_image(image)
	return textures[key]

static func draw(canvas: CanvasItem, rect: Rect2, pod: Dictionary, tint := Color.WHITE) -> void:
	var empty: bool=pod.get("recovered",false)
	var scale: float=rect.size.x/684.0
	var origin := Vector2(rect.get_center().x,rect.end.y)-Vector2(512,1435)*scale
	canvas.draw_texture_rect(texture(empty),Rect2(origin,Vector2(1024,1536)*scale),false,tint)
	if empty: return
	var wake: float=pod.get("wake",0.0)
	var duration: float=pod.get("wake_duration",12.0)
	if wake<=0.0: return
	var fill := clampf(wake/2.0,0,1)
	for x in [254.0,770.0]:
		canvas.draw_rect(Rect2(origin+Vector2(x-18,1140-125*fill)*scale,Vector2(36,125*fill)*scale),Color("d9ded6")*tint)
	for path in PATHS:
		for i in range(path.size()-1):
			var segment_fill := clampf(fill*(path.size()-1)-i,0,1)
			if segment_fill<=0: break
			var start: Vector2=origin+path[i]*scale
			var end: Vector2=origin+path[i].lerp(path[i+1],segment_fill)*scale
			canvas.draw_line(start,end,Color("bdc9c3")*tint,10*scale,true)
		# Moving bright slugs make the direction of pumping readable; wake freezes on outages.
		for slug in range(2):
			var t := fposmod(wake*1.8+slug*2.5,float(path.size()-1))
			if t>fill*(path.size()-1): continue
			var i := mini(int(t),path.size()-2)
			var a: Vector2=path[i].lerp(path[i+1],t-i)
			var b: Vector2=path[i].lerp(path[i+1],minf(1,t-i+0.4))
			canvas.draw_line(origin+a*scale,origin+b*scale,Color("f0f0de")*tint,10*scale,true)
	canvas.draw_rect(Rect2(origin+Vector2(472,114)*scale,Vector2(80*clampf(pod.get("battery_fraction",wake/duration),0,1),12)*scale),Color("8bab87")*tint)
