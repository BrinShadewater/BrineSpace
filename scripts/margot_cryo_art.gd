extends RefCounted
## One painted chassis/door, selected cat density and saved powered thaw clock.
const FOOT := Vector2(75,125)
const PIVOT := Vector2(256,448)
const DENSITY := 148.0/65.28
const GLASS := Rect2i(226,311,61,91)
# Leave 9 of the 91 glass pixels over the chamber's upper edge (~10%).
const DOOR_TRAVEL := 82
const OPEN_START := 3.8
const OPEN_END := 4.8
const LANDING := 6.6
const PATHS := {
	"chassis":"res://character/cryo-ward-layered-v5/frames/pet-chassis.png",
	"door":"res://character/cryo-ward-layered-v5/frames/pet-door.png",
}
static var layers := {}
static var cache := {}

static func layer(key: String) -> Image:
	if not layers.has(key):
		var image:=Image.new()
		image.load_png_from_buffer(FileAccess.get_file_as_bytes(PATHS[key]))
		layers[key]=image
	return layers[key]

static func graded(image: Image, tint: Color) -> Image:
	var result: Image=image.duplicate()
	for y in result.get_height():
		for x in result.get_width():
			var pixel:=result.get_pixel(x,y)
			if pixel.a>0.0:result.set_pixel(x,y,pixel*tint)
	return result

static func blend_inside(canvas: Image, cloud: Image, at: Vector2i) -> void:
	var visible:=Rect2i(at,cloud.get_size()).intersection(GLASS)
	if visible.has_area():canvas.blend_rect(cloud,Rect2i(visible.position-at,visible.size),visible.position)

static func fit_inside(foot: Vector2, bounds: Rect2i) -> Vector2:
	foot.x=clampf(foot.x,GLASS.position.x+3-bounds.position.x+92,GLASS.end.x-3-bounds.end.x+92)
	return foot

static func departure(boot: float) -> float:
	return smoothstep(OPEN_END,LANDING,boot)

static func hop_height(boot: float) -> float:
	var progress:=clampf((boot-OPEN_END)/(LANDING-OPEN_END),0.0,1.0)
	return 4.0*7.0*progress*(1.0-progress)

static func cold_color(boot: float) -> Color:
	return Color(0.66,0.82,1.0).lerp(Color.WHITE,smoothstep(LANDING,7.8,boot))

static func unfreezing(boot: float) -> float:
	return smoothstep(0.6,OPEN_START,boot)

static func lid_travel(boot: float, started: bool, recovered: bool) -> int:
	return DOOR_TRAVEL if recovered else roundi(DOOR_TRAVEL*smoothstep(OPEN_START,OPEN_END,boot)) if started else 0

static func cover_rect(boot: float, started: bool) -> Rect2i:
	return Rect2i(GLASS.position-Vector2i(0,lid_travel(boot,started,false)),GLASS.size)

static func texture(actor, boot: float, started: bool, recovered: bool, exit_offset: Vector2, reduced_motion: bool) -> Texture2D:
	var tick:=clampi(roundi(boot*25.0),0,200) if started else 0
	var key:=str([tick,started,recovered,exit_offset,reduced_motion])
	if cache.has(key):return cache[key]
	var time:=tick/25.0
	# The navigation landing can lie below the pod's 512px export. Keep its
	# full paws visible without moving the registered pod or character pivot.
	var canvas:=Image.create(512,640,false,Image.FORMAT_RGBA8)
	canvas.blend_rect(layer("chassis"),Rect2i(0,0,512,512),Vector2i.ZERO)
	var slide:=lid_travel(time,started,recovered)
	if slide>0:
		var rail:=Image.create(2,slide+8,false,Image.FORMAT_RGBA8)
		rail.fill(Color(0.28,0.35,0.38,0.8))
		for x in [219,290]:canvas.blend_rect(rail,Rect2i(Vector2i.ZERO,rail.get_size()),Vector2i(x,292-slide))
	var mist: Image=preload("res://scripts/environment_art.gd").texture("leak-puff").get_image()
	if not recovered:
		var body: Texture2D
		if time<2.0:body=actor.poses.frame_at_elapsed("nap-south",0.0)
		elif time<OPEN_START:body=actor.poses.frame_at_elapsed("nap-exit-south",(time-2.0)/(OPEN_START-2.0)*actor.poses.cycle_seconds("nap-exit-south"))
		elif time<OPEN_END:body=actor.player.frame_at_elapsed("idle-south",0.0)
		elif time<LANDING:body=actor.player.frame_at_elapsed("walk-south",departure(time)*actor.player.cycle_seconds("walk-south"))
		else:body=actor.player.frame_at_elapsed("idle-south",0.0)
		var image:=graded(body.get_image(),cold_color(time))
		var resting_offset:=Vector2(-1.0,lerpf(-35.0,-23.0,smoothstep(2.0,OPEN_START,time)))
		var foot:=PIVOT+resting_offset.lerp(exit_offset,departure(time))*DENSITY
		if time<OPEN_END:foot=fit_inside(foot,image.get_used_rect())
		foot.y-=hop_height(time)*DENSITY
		canvas.blend_rect(image,Rect2i(Vector2i.ZERO,image.get_size()),Vector2i((foot-Vector2(92,172)).round()))
		var thaw:=unfreezing(time) if started else 0.0
		var opening:=smoothstep(OPEN_START,OPEN_END,time) if started else 0.0
		var frost:=mist.duplicate();frost.resize(GLASS.size.x,GLASS.size.y,Image.INTERPOLATE_LANCZOS)
		blend_inside(canvas,graded(frost,Color(0.77,0.87,0.96,0.24*(1.0-thaw)*(1.0-opening))),GLASS.position)
		for index in range(3):
			var cloud:=mist.duplicate();cloud.resize(61,32,Image.INTERPOLATE_LANCZOS)
			var curl:=0.0 if reduced_motion else sin(time*0.65+index)*2.0
			blend_inside(canvas,graded(cloud,Color(0.73,0.85,1.0,0.15*(1.0-opening))),Vector2i(226+curl,314+index*24))
	# Translucent glass travels with the entire painted frame, even after recovery.
	var glass:=Image.create(GLASS.size.x,GLASS.size.y,false,Image.FORMAT_RGBA8)
	glass.fill(Color(0.60,0.76,0.85,0.12))
	glass.fill_rect(Rect2i(3,9,2,65),Color(0.79,0.87,0.91,0.16))
	canvas.blend_rect(glass,Rect2i(Vector2i.ZERO,glass.get_size()),GLASS.position-Vector2i(0,slide))
	canvas.blend_rect(layer("door"),Rect2i(0,0,512,512),Vector2i(0,-slide))
	if not recovered:
		var shade:=Image.create(17,7,false,Image.FORMAT_RGBA8)
		shade.fill(Color(0.05,0.10,0.13,0.50*(1.0-unfreezing(time))))
		for x in [226,267]:canvas.blend_rect(shade,Rect2i(0,0,17,7),Vector2i(x,425))
		if time>OPEN_START:
			var linger:=smoothstep(OPEN_START,4.5,time)*(1.0-smoothstep(6.0,8.0,time))
			for index in range(3):
				var fog:=mist.duplicate();fog.resize(134+index*18,30+index*4,Image.INTERPOLATE_LANCZOS)
				var drift:=0.0 if reduced_motion else (time-OPEN_START)*(index-1)*2.0
				canvas.blend_rect(graded(fog,Color(0.70,0.84,0.96,linger*0.12)),Rect2i(Vector2i.ZERO,fog.get_size()),Vector2i(256-fog.get_width()/2+drift,437+index*4))
	var result:=ImageTexture.create_from_image(canvas)
	var filtered:=CanvasTexture.new();filtered.diffuse_texture=result
	filtered.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
	filtered.set_meta("crew_frame_92",true);filtered.set_meta("crew_pivot",PIVOT)
	filtered.set_meta("crew_standing_height",148.0)
	if cache.size()>=256:cache.clear()
	cache[key]=filtered
	return filtered
