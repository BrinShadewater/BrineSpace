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
			# Neutral metal outside; department identity is a separate inset hairline.
			var trim:=Color(p.r*.70,p.g*.76,p.b*.79,1.0)
			var out:=fill.lerp(trim,p.a)
			var q: Vector2=(Vector2(x+.5,y+.5)-Vector2(100,142)).abs()-Vector2(88,130)
			var distance:=q.max(Vector2.ZERO).length()+minf(maxf(q.x,q.y),0.0)-12.0
			out.a=lerpf(fill.a,1.0,p.a)*clampf(.5-distance,0.0,1.0)
			image.set_pixel(x,y,out)
	var style:=StyleBoxTexture.new()
	style.texture=ImageTexture.create_from_image(image)
	for side in [SIDE_LEFT,SIDE_TOP,SIDE_RIGHT,SIDE_BOTTOM]:style.set_texture_margin(side,16)
	style.content_margin_left=8;style.content_margin_right=8
	style.content_margin_top=8;style.content_margin_bottom=7
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

# Node2D avoids participating in PanelContainer layout; draw over the content.
class InnerOutline extends Node2D:
	var outline := StyleBoxFlat.new()
	func _draw() -> void:
		var card := get_parent() as Control
		if card != null:
			draw_style_box(outline, Rect2(Vector2(6,6),card.size-Vector2(12,12)))

static func update_inner_outline(card: Control, color: Color, active: bool) -> void:
	var edge := card.get_node_or_null("CardInnerOutline") as InnerOutline
	if edge == null:
		if not active:return
		edge=InnerOutline.new()
		edge.name="CardInnerOutline"
		# No z_index: as the last child it already paints over the content, and a raised z put every card's
		# outline above its neighbours in the fan (owner playtest, Sept 29).
		edge.outline.draw_center=false
		edge.outline.border_width_left=3;edge.outline.border_width_right=3
		edge.outline.border_width_top=3;edge.outline.border_width_bottom=3
		edge.outline.set_corner_radius_all(6)
		card.add_child(edge)
		card.resized.connect(edge.queue_redraw)
	edge.visible=active
	edge.outline.border_color=color
	edge.queue_redraw()
