extends RefCounted
## Registered hull crops, independent of a room's equipment texture.
const MATERIALS={
	"engineering":{"path":"res://assets/material-polish-v3/thermal-equipment.png","horizontal":Rect2(240,34,142,58),"vertical":Rect2(29,106,46,148),"cap":Rect2(28,32,50,52)},
	"habitation":{"path":"res://rooms/production-ten/crew_lounge-source-v2.png","horizontal":Rect2(246,41,130,66),"vertical":Rect2(43,220,43,137),"cap":Rect2(45,43,45,44)},
	"medical":{"path":"res://assets/material-polish-v2/clone-equipment.png","horizontal":Rect2(94,49,123,39),"vertical":Rect2(40,98,36,114),"cap":Rect2(39,45,43,43)}
}
static var textures: Dictionary={}
static func texture(material: String) -> Texture2D:
	if not textures.has(material):
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, MATERIALS[material].path)
		textures[material]=ImageTexture.create_from_image(image)
	return textures[material]
static func wall(canvas: CanvasItem,rect: Rect2,horizontal: bool,material: String) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	canvas.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("22292c"))
	var span:=rect.size.x if horizontal else rect.size.y
	var cursor:=0.0
	while cursor<span:
		var length:=minf(48,span-cursor)
		var target:=Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		var source: Rect2=MATERIALS[material]["horizontal" if horizontal else "vertical"]
		# Preserve texel scale in the final short tile instead of squeezing a whole panel.
		if horizontal: source.size.x*=length/48.0
		else: source.size.y*=length/48.0
		canvas.draw_texture_rect_region(texture(material),target,source)
		cursor+=length
static func cap(canvas: CanvasItem,rect: Rect2,material: String) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	canvas.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("22292c"))
	canvas.draw_texture_rect_region(texture(material),top,MATERIALS[material].cap)
