extends RefCounted
## Raw PNG playback shared by the start pod and recovered wards.
static var frames := {}
static var empty_texture: Texture2D
const EMPTY_OUTLINE := [Vector2(281,193),Vector2(416,193),Vector2(441,206),Vector2(451,235),Vector2(456,241),Vector2(456,289),Vector2(447,300),Vector2(447,533),Vector2(434,548),Vector2(262,548),Vector2(251,535),Vector2(252,393),Vector2(244,389),Vector2(244,333),Vector2(252,330),Vector2(252,313),Vector2(244,308),Vector2(244,245),Vector2(252,239),Vector2(259,213)]

static func frame(id: String, index: int) -> Texture2D:
	if not frames.has(id):
		var result: Array[Texture2D]=[]
		for i in range(6):
			var path := "res://assets/material-polish-cryo-recovery-v1/%s/wake-%d.png" % ["bill" if id=="" else id,i]
			if id=="marsh":path="res://character/marsh-v1/cryo.png"
			var image:=Image.new()
			assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK)
			result.append(ImageTexture.create_from_image(image))
		frames[id]=result
	return frames[id][clampi(index,0,5)]

static func draw(canvas: CanvasItem, rect: Rect2, occupant: Dictionary, tint := Color.WHITE) -> void:
	if occupant.get("charging_pod",false) or occupant.get("architect_id","")=="marsh":
		preload("res://scripts/marsh_charging_art.gd").draw(canvas,rect,occupant,tint)
		return
	var base:=Vector2(rect.get_center().x,rect.end.y)
	if occupant.get("recovered",false):
		if empty_texture==null:
			var image:=Image.new()
			assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/material-polish-cryo-v1/cryo-equipment.png"))==OK)
			empty_texture=ImageTexture.create_from_image(image)
		var vertices:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for point in EMPTY_OUTLINE:
			vertices.append(base+(point-Vector2(350,548))*rect.size.x/216.0)
			uv.append(point/empty_texture.get_size())
		canvas.draw_polygon(vertices,PackedColorArray([tint]),uv,empty_texture)
		return
	var duration: float=occupant.get("wake_duration",7.0)
	var texture:=frame(occupant.get("architect_id","bill"),mini(5,int(float(occupant.get("wake",0.0))/duration*6.0)))
	var scale:=rect.size.x/290.0
	canvas.draw_texture_rect(texture,Rect2(base-Vector2(210,560)*scale,Vector2(418,627)*scale),false,tint)
