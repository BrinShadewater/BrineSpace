extends RefCounted
## Right-hinged ocean hatch, driven by the existing pressure-cycle pose.
static var textures:Dictionary={}
static func png(path:String) -> Texture2D:
	if not textures.has(path):
		var im:=Image.new()
		var error:=im.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
		assert(error==OK)
		textures[path]=ImageTexture.create_from_image(im)
	return textures[path]
const G=preload("res://tools/modular_room_geometry.gd")
const FACE="res://assets/door-polish-v3/ocean-hatch-interior.png"
const TOP="res://assets/door-polish-v3/ocean-hatch-top.png"
const RIM="res://assets/door-polish-v3/ocean-hatch-rim.png"
const STEEL_DEPTH=11.0
static func angle(amount:float) -> float:
	var t:=clampf(amount,0,1)
	return t*t*(3-2*t)*PI*.5
static func quad(canvas:CanvasItem,texture:Texture2D,source:Rect2,points:PackedVector2Array,color:Color=Color.WHITE) -> void:
	var uv:=PackedVector2Array([source.position,Vector2(source.end.x,source.position.y),source.end,Vector2(source.position.x,source.end.y)])
	for i in range(4):uv[i]/=Vector2(texture.get_size())
	canvas.draw_polygon(points,PackedColorArray([color]),uv,texture)
static func raised(canvas:CanvasItem,amount:float,leaf:bool=true,water:float=0.0,foreground:bool=false) -> void:
	var texture:Texture2D=png(FACE)
	var sx:=56.0/590.0
	var sy:=64.0/925.0
	# Keep the frame fixed, omit its leaf aperture, mirror the painted hinge right.
	for source in [Rect2(0,0,1254,165),Rect2(0,165,330,925),Rect2(920,165,334,925),Rect2(0,1090,1254,164)]:
		if foreground:
			source=source.intersection(Rect2(0,0,1254,165+52/sy))
			if not source.has_area():continue
		var x:float=28-(source.position.x-330)*sx
		var y:float=-248+(source.position.y-165)*sy
		quad(canvas,texture,source,PackedVector2Array([Vector2(x,y),Vector2(x-source.size.x*sx,y),Vector2(x-source.size.x*sx,y+source.size.y*sy),Vector2(x,y+source.size.y*sy)]))
	if not leaf:return
	var turn:=angle(amount)
	var hinge:=Vector2(28,-248)
	var tip:=hinge+Vector2(-cos(turn),-sin(turn))*56
	var outside:=Vector2(sin(turn),-cos(turn))*STEEL_DEPTH
	if sin(turn)>.001:
		quad(canvas,png(RIM),Rect2(1630,252,255,210),PackedVector2Array([tip,tip+outside,tip+outside+Vector2(0,64),tip+Vector2(0,64)]),Color(.82,.82,.82))
		quad(canvas,png(RIM),Rect2(147,228,1879,266),PackedVector2Array([hinge,tip,tip+outside,hinge+outside]))
	if cos(turn)>.04:
		var tint:=Color.WHITE.lerp(Color("2b85af"),clampf(water,0,1)*.1*pow(1-amount,2))
		quad(canvas,texture,Rect2(330,165,590,925),PackedVector2Array([hinge,tip,tip+Vector2(0,64),hinge+Vector2(0,64)]),tint)
static func low(canvas:CanvasItem,q:int,amount:float) -> void:
	var texture:Texture2D=png(TOP)
	for pair in [[Rect2(112,334,187,220),Rect2(-47,-7,11,14)],[Rect2(1480,334,182,220),Rect2(36,-7,11,14)]]:
		low_part(canvas,texture,pair[0],pair[1],q,0,false)
	var depth:=STEEL_DEPTH*72/56
	low_part(canvas,png(RIM),Rect2(147,228,1879,266),Rect2(0,-depth,72,depth),q,-angle(amount),true)
static func low_part(canvas:CanvasItem,texture:Texture2D,source:Rect2,dest:Rect2,q:int,turn:float,leaf:bool) -> void:
	var points:=PackedVector2Array()
	for p in [dest.position,Vector2(dest.end.x,dest.position.y),dest.end,Vector2(dest.position.x,dest.end.y)]:
		var at:Vector2=p.rotated(turn)+Vector2(-36,0) if leaf else p
		at*=Vector2(-56.0/72,56.0/72)
		points.append(G.turn(at+Vector2(0,-184),q))
	quad(canvas,texture,source,points)
