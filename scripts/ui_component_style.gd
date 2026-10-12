@tool
extends StyleBox
## Small inset controls share the hull palette without inheriting button fittings.
var kind := "field"
var state := "normal"
static var artwork: Dictionary = {}

func _init() -> void:
	content_margin_left = 12
	content_margin_right = 12
	content_margin_top = 7
	content_margin_bottom = 7

func _draw(rid: RID, rect: Rect2) -> void:
	var w := maxi(12, roundi(rect.size.x))
	var h := maxi(8, roundi(rect.size.y))
	var key := [kind,state,w,h]
	if not artwork.has(key):
		if artwork.size() > 128: artwork.clear()
		artwork[key] = render(w,h)
	RenderingServer.canvas_item_add_texture_rect(rid,rect,artwork[key].get_rid())

func render(w: int, h: int) -> Texture2D:
	var face := "0c262c"
	var edge := "4b575d"
	var indicator := "426969"
	if state in ["hover","focus"]: face="15343a";edge="728489";indicator="64939c"
	if state == "selected": face="1b3c41";edge="7e8b8d";indicator="78a29e"
	if state == "disabled": face="18272c";edge="3b464b";indicator="425257"
	if state == "warning": indicator="b19962"
	if state == "danger": indicator="ab6669"
	var svg := '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % [w,h,w,h]
	svg += '<rect x="1" y="1" width="%d" height="%d" rx="4" fill="#%s" stroke="#%s" stroke-width="1"/>' % [w-2,h-2,face,edge]
	# Restrained matte top lip and a recessed seam, with no broad shiny border.
	svg += '<path d="M6 2H%d" stroke="#929b9c" stroke-opacity=".22"/><path d="M6 %dH%d" stroke="#041319" stroke-opacity=".55"/>' % [w-6,h-3,w-6]
	if kind == "tab":
		if state == "selected": svg += '<rect x="10" y="%d" width="%d" height="2" rx="1" fill="#%s"/>' % [h-4,w-20,indicator]
	elif kind == "badge":
		svg += '<circle cx="9" cy="%.1f" r="2.2" fill="#%s"/>' % [h*.5,indicator]
	elif kind == "field" and state == "focus":
		svg += '<rect x="3" y="7" width="2" height="%d" rx="1" fill="#%s"/>' % [maxi(1,h-14),indicator]
	svg += '</svg>'
	var source := Image.new()
	source.load_svg_from_string(svg,2.0)
	return ImageTexture.create_from_image(source)
