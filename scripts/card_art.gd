extends RefCounted
## Optional raw card art. Neutral stock is kept separate from department-tinted trim.
const SafeImage = preload("res://scripts/safe_image.gd")
const PATHS := {
	"frame":"res://assets/sea-life-v1/cards/card-frame.png",
	"back":"res://assets/sea-life-v1/cards/card-back.png",
	"Operations":"res://assets/sea-life-v1/cards/emblem-operations.png",
	"Engineering":"res://assets/sea-life-v1/cards/emblem-engineering.png",
	"Science":"res://assets/sea-life-v1/cards/emblem-science.png",
	"Life Support":"res://assets/sea-life-v1/cards/emblem-life-support.png",
	"Recreation":"res://assets/sea-life-v1/cards/emblem-recreation.png",
	"Anomaly":"res://assets/sea-life-v1/cards/emblem-anomaly.png",
	"Robotics":"res://assets/sea-life-v1/cards/emblem-robotics.png",
	"Derelict":"res://assets/sea-life-v1/cards/emblem-derelict.png",
	"core":"res://assets/sea-life-v1/cards/rarity-core.png",
	"common":"res://assets/sea-life-v1/cards/rarity-common.png",
	"uncommon":"res://assets/sea-life-v1/cards/rarity-uncommon.png",
	"rare":"res://assets/sea-life-v1/cards/rarity-rare.png",
	"derelict":"res://assets/sea-life-v1/cards/rarity-derelict.png",
}
static var enabled := true
static var textures: Dictionary={}
static var styles: Dictionary={}
static func texture(key: String) -> Texture2D:
	if not enabled or not PATHS.has(key): return null
	if textures.has(key):return textures[key]
	var result:=SafeImage.raw_texture(PATHS[key])
	var expected:=Vector2i(200,284) if key in ["frame","back"] else (Vector2i(48,48) if key.to_lower()==key else Vector2i(64,64))
	if result!=null and Vector2i(result.get_size())!=expected:result=null
	textures[key]=result
	if result==null:push_warning("Card art unavailable: %s; original card rendering retained."%PATHS[key])
	return result

static func frame_style(fill: Color, border: Color) -> StyleBoxTexture:
	var frame:=texture("frame")
	if frame==null:return null
	var key:=fill.to_html()+"/"+border.to_html()
	if styles.has(key):return styles[key]
	var source:=frame.get_image()
	var image:=Image.create(200,284,false,Image.FORMAT_RGBA8)
	image.fill(fill)
	for y in range(284):
		for x in range(200):
			if x>=16 and x<184 and y>=16 and y<268:continue
			var p:=source.get_pixel(x,y)
			# Inset painted department line is the backing; authored metal paints last.
			var trim:=Color(p.r*.70,p.g*.76,p.b*.79,1.0)
			# Move the painted outline beneath the inner edge of the authored rail.
			# Four pixels of backing keep its exposed colour solid when the card turns.
			var inner_q: Vector2 = (Vector2(x+.5,y+.5)-Vector2(100,142)).abs()-Vector2(90,132)
			var inner_distance := inner_q.max(Vector2.ZERO).length()+minf(maxf(inner_q.x,inner_q.y),0.0)-6.0
			var coverage := clampf(.5-inner_distance,0.0,1.0)*clampf(inner_distance+4.5,0.0,1.0)
			var backing := fill.lerp(border,coverage)
			# Near-opaque authored rail pixels are solid metal, not paint-tinted stock.
			var metal_alpha := 1.0 if p.a >= .98 else p.a
			var out:=backing.lerp(trim,metal_alpha)
			var q: Vector2=(Vector2(x+.5,y+.5)-Vector2(100,142)).abs()-Vector2(88,130)
			var distance:=q.max(Vector2.ZERO).length()+minf(maxf(q.x,q.y),0.0)-12.0
			out.a=lerpf(fill.a,1.0,p.a)*clampf(.5-distance,0.0,1.0)
			image.set_pixel(x,y,out)
	image.generate_mipmaps()
	var style:=StyleBoxTexture.new()
	style.texture=ImageTexture.create_from_image(image)
	for side in [SIDE_LEFT,SIDE_TOP,SIDE_RIGHT,SIDE_BOTTOM]:style.set_texture_margin(side,16)
	style.content_margin_left=12;style.content_margin_right=12
	style.content_margin_top=10;style.content_margin_bottom=10
	styles[key]=style
	return style

static func add_mark(parent: Control, key: String, at: Vector2, size: Vector2, color: Color, name: String) -> void:
	var art:=texture(key)
	if art==null:return
	var mark:=TextureRect.new()
	mark.expand_mode=TextureRect.EXPAND_IGNORE_SIZE
	mark.name=name;mark.texture=art;mark.position=at;mark.size=size
	mark.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	mark.modulate=color;mark.mouse_filter=Control.MOUSE_FILTER_IGNORE
	parent.add_child(mark)
