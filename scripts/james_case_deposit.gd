extends RefCounted
## Cosmetic case belongs to the remaining extraction site, never to return cargo.
const CASES={
	"east":{"path":"res://character/james-case-release-east-v1/case.png","offset":Vector2(178,127)-Vector2(128,128),"size":Vector2(45,39)},
	"west":{"path":"res://character/james-case-release-west-v1/case.png","offset":Vector2(54,130)-Vector2(128,128),"size":Vector2(30,31)},
	"north":{"path":"res://character/james-case-release-north-v1/case.png","offset":Vector2(105,67)-Vector2(128,128),"size":Vector2(47,26)},
	"south":{"path":"res://character/james-case-release-south-v1/case.png","offset":Vector2(111,187)-Vector2(128,128),"size":Vector2(41,30)}
}
static var case_textures:Dictionary={}

static func valid(value:Variant,cell:Vector2i)->bool:
	if not value is Dictionary:return false
	if value.is_empty():return true
	if not CASES.has(value.get("direction")) or not value.get("foot") is Vector2:return false
	var foot:Vector2=value.foot
	return foot.is_finite() and foot.x>=0 and foot.y>=0 and foot.x<=15360 and foot.y<=15360 and foot.distance_to((Vector2(cell)+Vector2.ONE*.5)*384)<=768

static func place(main,actor)->void:
	var target:Vector2i=actor.expedition.target
	var site:Dictionary=main.drone_fleet.sites.get(target,{})
	if site.is_empty() or site.units<=0:return
	site.james_case_release={"direction":actor.exterior_cancel.direction,"foot":actor.foot}

static func rectangle(value:Dictionary,cell_size:float)->Rect2:
	var scale:=cell_size*.17/148.0
	var spec:Dictionary=CASES[value.direction]
	return Rect2(value.foot/384.0*cell_size+spec.offset*scale,spec.size*scale)

static func draw(canvas:CanvasItem,site:Dictionary,cell_size:float)->void:
	var value:Dictionary=site.get("james_case_release",{})
	if value.is_empty() or site.units<=0:return
	var direction:String=value.direction
	if not case_textures.has(direction):
		var image:=Image.new()
		if preload("res://scripts/safe_image.gd").load_png(image,CASES[direction].path)!=OK:return
		case_textures[direction]=ImageTexture.create_from_image(image)
	canvas.draw_texture_rect(case_textures[direction],rectangle(value,cell_size),false)
