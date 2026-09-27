extends RefCounted
const Mission = preload("res://scripts/survey_probe.gd")
static var textures := {}
static func texture(path:String) -> Texture2D:
	if not textures.has(path):
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))!=OK:return null
		textures[path]=ImageTexture.create_from_image(image)
	return textures[path]
static func launcher(q:int) -> Dictionary:
	var direction:String=["north","east","south","west"][posmod(q,4)]
	var data:Dictionary=LAUNCHERS[direction]
	var tex:=texture(data.image)
	var scale_value:=.34*float(data.libraryScale)
	return {"id":"survey_hatch","rect":Rect2(Mission.dock(q)-Vector2(data.anchor[0],data.anchor[1])*scale_value,Vector2(tex.get_size())*scale_value),"sort_y":Mission.dock(q).y+30,"registration":{},"collision_boxes":[[.1,.25,.8,.7]],"texture":tex}
static func draw_clipped(canvas,tex:Texture2D,dest:Rect2,source:Rect2,clip:Rect2) -> void:
	var r:=dest.intersection(clip)
	if not r.has_area():return
	var uv:=Rect2(source.position+(r.position-dest.position)/dest.size*source.size,r.size/dest.size*source.size)
	canvas.draw_texture_rect_region(tex,r,uv)
static func body(canvas,p:Dictionary,origin:Vector2,scale_value:float,clip:Rect2) -> void:
	var center:Vector2=origin+p.position*scale_value
	var rect:=Rect2(center-Vector2.ONE*87.04*scale_value,Vector2.ONE*174.08*scale_value)
	if p.state in ["launch","cruise","return","brake","turn","align"]:
		var frame:=posmod(int(p.time*30),60)
		var wake:=texture(PATHS["wake-"+p.heading])
		draw_clipped(canvas,wake,rect,Rect2((frame%6)*512,(frame/6)*512,512,512),clip)
	var tex:=texture(PATHS[p.heading])
	draw_clipped(canvas,tex,rect,Rect2(Vector2.ZERO,tex.get_size()),clip)
	var angle:=float(Mission.HEADINGS.find(p.heading))*PI/4
	var lamp:=center+Vector2.from_angle(angle)*3.06*scale_value
	if clip.has_point(lamp):
		var color:Color={"yellow":Color("e6bd60"),"red":Color("c36155"),"blue":Color("6ab8df")}[p.get("lamp","yellow" if p.state=="recharge" else "blue")]
		color.a=.4+.6*(.5+.5*cos(float(p.time)*TAU))
		canvas.draw_circle(lamp,.782*scale_value,color)
static func interior(room,prop:Dictionary) -> void:
	room.painter.draw_texture_rect(prop.texture,prop.rect,false)
	var p:=Mission.pose(float(room.survey_clock),int(room.quarter))
	p.lamp=room.survey_status
	body(room.painter,p,Vector2.ZERO,1.0,Rect2(-174,-174,348,348))
	if p.beacon and room.operating and room.survey_status=="blue":
		var offsets:=[Vector2(35,-54),Vector2(79,15),Vector2(36,32),Vector2(-69,13)]
		var at:Vector2=Mission.dock(room.quarter)+offsets[posmod(room.quarter,4)]
		var angle:=float(p.time)/.8*TAU
		room.painter.draw_circle(at,4,Color("594c2d"))
		room.painter.draw_arc(at,3,angle,angle+1.5,12,Color("d7af58"),1.5)
static func exterior(canvas,game,cell_size:float) -> void:
	for room in game.placed_rooms:
		if room.id!="survey_probe_bay":continue
		var p:=Mission.pose(float(room.get("survey_clock",0)),int(room.get("rotation",0)))
		p.lamp=Mission.lamp(game,room)
		var origin:Vector2=(Vector2(room.pos)+Vector2.ONE*.5)*cell_size
		var s:=cell_size/384
		# Leave the pressure wall opaque. The room renderer owns the interior half.
		var hull:=Rect2(origin-Vector2.ONE*cell_size*.5,Vector2.ONE*cell_size)
		for clip in [Rect2(-1e5,-1e5,2e5,hull.position.y+1e5),Rect2(-1e5,hull.end.y,2e5,1e5),Rect2(-1e5,hull.position.y,hull.position.x+1e5,cell_size),Rect2(hull.end.x,hull.position.y,1e5,cell_size)]:
			body(canvas,p,origin,s,clip)
		if p.state=="scan":
			var tex:=texture(PATHS["scan-"+p.heading])
			var frame:=mini(59,int(float(p.scan)*59))
			var center:Vector2=origin+p.position*s
			canvas.draw_texture_rect_region(tex,Rect2(center-Vector2.ONE*148.48*s,Vector2.ONE*296.96*s),Rect2((frame%6)*512,(frame/6)*512,512,512))
const PATHS := {
  "east": "res://assets/survey-probe-v1-2026-09-26/poses/east.png",
  "southeast": "res://assets/survey-probe-v1-2026-09-26/poses/southeast.png",
  "south": "res://assets/survey-probe-v1-2026-09-26/poses/south.png",
  "southwest": "res://assets/survey-probe-v1-2026-09-26/poses/southwest.png",
  "west": "res://assets/survey-probe-v1-2026-09-26/poses/west.png",
  "northwest": "res://assets/survey-probe-v1-2026-09-26/poses/northwest.png",
  "north": "res://assets/survey-probe-v1-2026-09-26/poses/north.png",
  "northeast": "res://assets/survey-probe-v1-2026-09-26/poses/northeast.png",
  "wake-east": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-east.png",
  "scan-east": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-east.png",
  "wake-southeast": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-southeast.png",
  "scan-southeast": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-southeast.png",
  "wake-south": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-south.png",
  "scan-south": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-south.png",
  "wake-southwest": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-southwest.png",
  "scan-southwest": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-southwest.png",
  "wake-west": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-west.png",
  "scan-west": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-west.png",
  "wake-northwest": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-northwest.png",
  "scan-northwest": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-northwest.png",
  "wake-north": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-north.png",
  "scan-north": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-north.png",
  "wake-northeast": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-northeast.png",
  "scan-northeast": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-northeast.png"
}
const LAUNCHERS := {
  "north": {
    "image": "res://assets/survey-probe-v1-2026-09-26/sources/north-launcher.png",
    "anchor": [
      64,
      212
    ],
    "libraryScale": 0.945
  },
  "east": {
    "image": "res://assets/survey-probe-v1-2026-09-26/sources/east-launcher.png",
    "anchor": [
      183,
      90
    ],
    "libraryScale": 0.945
  },
  "south": {
    "image": "res://assets/survey-probe-v1-2026-09-26/sources/south-launcher.png",
    "anchor": [
      70,
      117
    ],
    "libraryScale": 0.945
  },
  "west": {
    "image": "res://assets/survey-probe-v1-2026-09-26/sources/west-launcher.png",
    "anchor": [
      277,
      88
    ],
    "libraryScale": 0.945
  }
}
