@tool
extends StyleBox
## Illustrated hull rail and fittings, rendered at twice the display density.
var state := "normal"
var bg_color := Color("0b2e36")
var border_color := Color("535c61")
var radius := 6
static var _art: Dictionary = {}

func _init() -> void:
	content_margin_left = 14
	content_margin_right = 14
	content_margin_top = 6
	content_margin_bottom = 8

func _draw(rid: RID, rect: Rect2) -> void:
	var w := maxi(24, roundi(rect.size.x))
	var h := maxi(20, roundi(rect.size.y))
	var key := [w, h, state, bg_color, border_color]
	if not _art.has(key):
		if _art.size() > 128: _art.clear()
		_art[key] = _make_art(w, h)
	RenderingServer.canvas_item_add_texture_rect(rid, rect, _art[key].get_rid())

func _make_art(w: int, h: int) -> Texture2D:
	var face := bg_color.to_html(false)
	if state == "hover": face = "103438"
	elif state == "pressed": face = "09272b"
	elif state == "disabled": face = "243033"
	var light := "507276"
	if state in ["hover", "pressed"]: light = "609ed0"
	elif state == "disabled": light = "ac575d"
	var svg := '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><defs><linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#879198"/><stop offset=".45" stop-color="#616d75"/><stop offset="1" stop-color="#414d55"/></linearGradient><linearGradient id="face" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#%s"/><stop offset="1" stop-color="#09272c"/></linearGradient></defs>' % [w,h,w,h,face]
	# Recessed dark seam, continuous thin rail, then the inset petrol face.
	svg += '<rect x="1" y="2" width="%d" height="%d" rx="7" fill="#172329" stroke="#050e13" stroke-width="2"/>' % [w-2,h-3]
	svg += '<rect x="2" y="1" width="%d" height="%d" rx="6" fill="url(#steel)" stroke="#343d40"/>' % [w-4,h-4]
	svg += '<rect x="5" y="4" width="%d" height="%d" rx="3" fill="url(#face)" stroke="#182e33" stroke-width="1.5"/>' % [w-10,h-10]
	svg += '<path d="M11 4H%dM5 11V%d" stroke="#89949a" stroke-opacity=".35" fill="none"/>' % [w-11,h-11]
	# Four separate stepped corner fittings. Slots and small fasteners stay readable.
	for corner in [[3,3,1,1],[w-3,3,-1,1],[w-3,h-5,-1,-1],[3,h-5,1,-1]]:
		svg += '<g transform="translate(%d %d) scale(%d %d)"><path d="M0 12V3L3 0H18V5H7L5 7V13Z" fill="url(#steel)" stroke="#343b3d" stroke-width=".8"/><path d="M1 11V3L3 1H17" fill="none" stroke="#929da3" stroke-opacity=".8"/><circle cx="4" cy="4" r="1.4" fill="#283438" stroke="#7d8a91" stroke-width=".5"/><path d="M3.2 4H4.8" stroke="#151f23" stroke-width=".7"/></g>' % corner
	# Tall controls use only corner fittings; horizontal buttons carry side catches.
	if w > 72 and h < 100:
		var cy := h * 0.5
		for x in [3,w-11]:
			svg += '<g transform="translate(%d %.1f)"><path d="M1 -12H7L8 -10V10L7 12H1L0 10V-10Z" fill="url(#steel)" stroke="#353e40"/><path d="M2 -10H6V10H2Z" fill="#1c2b31" stroke="#7f8c94" stroke-width=".6"/><rect x="2.5" y="-5" width="3" height="10" rx=".8" fill="#%s"/><path d="M3 -3V3" stroke="#a1b9bd" stroke-opacity=".4" stroke-width=".6"/><circle cx="4" cy="-8" r=".7" fill="#7d8a91"/><circle cx="4" cy="8" r=".7" fill="#7d8a91"/></g>' % [x,cy,light]
	svg += '</svg>'
	var image := Image.new()
	image.load_svg_from_string(svg, 2.0)
	return ImageTexture.create_from_image(image)

func _get_draw_rect(rect: Rect2) -> Rect2:
	return rect
