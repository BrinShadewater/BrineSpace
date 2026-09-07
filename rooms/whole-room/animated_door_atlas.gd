extends RefCounted
## Non-destructive registration of dooranimated.png, 744x534 cells, frames 0..9.
## Frame 9 clear alpha span x216..527 = 312 pixels = 72 world units.
const FRAME := Vector2(744,534)
const CLEAR_PIXELS := 312.0
const APERTURE := 72.0
const SCALE_X := APERTURE/CLEAR_PIXELS

static func create_station_finish(host: Node, source: Texture2D) -> Texture2D:
	# Cached GPU material, not an edited/exported atlas. Preserve source alpha,
	# registration and animation; legacy rooms retain the original texture.
	var viewport := SubViewport.new()
	viewport.name = "StationDoorFinish"
	viewport.size = source.get_size()
	viewport.transparent_bg = true
	viewport.disable_3d = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ONCE
	var sprite := Sprite2D.new()
	sprite.texture = source
	sprite.centered = false
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var shader := Shader.new()
	shader.code = """shader_type canvas_item;
render_mode unshaded;
uniform vec4 lamp_color : source_color = vec4(0.96,0.96,0.96,1.0);
void fragment() {
	vec4 src = texture(TEXTURE, UV);
	float value = max(src.r, max(src.g, src.b));
	float enamel = smoothstep(0.025, 0.16, value);
	vec3 metal = mix(vec3(0.065,0.075,0.09), vec3(0.88,0.84,0.73), enamel);
	metal *= mix(0.90,1.08,value);
	float indicator = smoothstep(0.13,0.30,src.g-src.r) * smoothstep(0.30,0.65,src.g);
	COLOR = vec4(mix(metal,lamp_color.rgb,indicator),src.a);
}
"""
	var material := ShaderMaterial.new()
	material.shader = shader
	sprite.material = material
	viewport.add_child(sprite)
	host.add_child(viewport)
	return viewport.get_texture()

static func parts(frame_index: int, vertical: bool) -> Array:
	var frame := clampi(frame_index,0,9)
	var offset := Vector2(frame%4,floori(frame/4.0))*FRAME
	var pieces: Array = []
	# Only the metal tread spans the walkable floor; it always precedes crew.
	pieces.append({"source":Rect2(offset+Vector2(216,456),Vector2(312,78)),"rect":Rect2(-36,-9,72,18) if not vertical else Rect2(-9,-36,18,72),"floor":true,"depth":0.0,"turn":vertical})
	if not vertical:
		pieces.append({"source":Rect2(offset,Vector2(744,160)),"rect":Rect2(-58,-60,116,21),"floor":false,"depth":0.0,"turn":false})
		for x in [0,528]:
			pieces.append({"source":Rect2(offset+Vector2(x,160),Vector2(216,296)),"rect":Rect2(-58 if x==0 else 36,-39,22,39),"floor":false,"depth":0.0,"turn":false})
		pieces.append({"source":Rect2(offset+Vector2(216,160),Vector2(312,296)),"rect":Rect2(-36,-39,72,39),"floor":false,"depth":0.0,"turn":false})
	else:
		# Upright jambs retain screen-up height; leaf travel follows the wall.
		# This is an edge-on reassembly, not a claimed new directional sprite.
		for sign_value in [-1,1]:
			var source_x := 0 if sign_value==-1 else 528
			pieces.append({"source":Rect2(offset+Vector2(source_x,160),Vector2(216,296)),"rect":Rect2(-11,sign_value*36-39,22,39),"floor":false,"depth":float(sign_value*36),"turn":false})
		pieces.append({"source":Rect2(offset+Vector2(216,0),Vector2(312,160)),"rect":Rect2(-5,-75,10,72),"floor":false,"depth":-36.0,"turn":true})
		pieces.append({"source":Rect2(offset+Vector2(216,160),Vector2(312,296)),"rect":Rect2(-6,-36,12,72),"floor":false,"depth":0.0,"turn":true})
	return pieces

static func draw_piece(canvas: CanvasItem, texture: Texture2D, part: Dictionary) -> void:
	var rect: Rect2 = part.rect
	var source: Rect2 = part.source
	if not part.turn:
		canvas.draw_texture_rect_region(texture,rect,source,Color.WHITE)
		return
	var vertices := PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
	var size := Vector2(texture.get_size())
	var uv := PackedVector2Array([Vector2(source.position.x,source.end.y)/size,source.position/size,Vector2(source.end.x,source.position.y)/size,source.end/size])
	canvas.draw_polygon(vertices,PackedColorArray([Color.WHITE]),uv,texture)
