extends RefCounted
## Raw PNG playback shared by the start pod and recovered wards.
static var frames := {}
static var empty_frames := {}
const EXIT_SECONDS := 1.2

static func wake_frame_index(wake: float, duration: float) -> int:
	# Thawing is a wait; opening and standing are one short physical action.
	# Spreading six exit poses over the whole timer made each pose hang for seconds.
	var exit_duration := minf(EXIT_SECONDS, maxf(duration, 0.001))
	var elapsed := wake - maxf(0.0, duration - exit_duration)
	if elapsed <= 0.0: return 0
	return clampi(1 + int(elapsed / (exit_duration / 5.0)), 1, 5)

static func empty_frame(id: String) -> Texture2D:
	var actor := id if id in ["bill","veld","branforth"] else "bill"
	if not empty_frames.has(actor):
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image,"res://assets/material-polish-cryo-open-v1/%s.png"%actor)
		empty_frames[actor]=ImageTexture.create_from_image(image)
	return empty_frames[actor]

static func frame(id: String, index: int) -> Texture2D:
	if not frames.has(id):
		var result: Array[Texture2D]=[]
		for i in range(6):
			var path := "res://assets/material-polish-cryo-recovery-v1/%s/wake-%d.png" % ["bill" if id=="" else id,i]
			if id=="marsh":path="res://character/marsh-v1/cryo.png"
			var image:=Image.new()
			preload("res://scripts/safe_image.gd").load_png(image, path)
			result.append(ImageTexture.create_from_image(image))
		frames[id]=result
	return frames[id][clampi(index,0,5)]

static func draw(canvas: CanvasItem, rect: Rect2, occupant: Dictionary, tint := Color.WHITE) -> void:
	var opacity := tint.a
	tint *= Color.WHITE*lerpf(0.16,1.0,float(occupant.get("startup_power",1.0)))
	tint.a=opacity
	if occupant.get("charging_pod",false) or occupant.get("architect_id","")=="marsh":
		preload("res://scripts/marsh_charging_art.gd").draw(canvas,rect,occupant,tint)
		return
	var base:=Vector2(rect.get_center().x,rect.end.y)
	var duration: float=occupant.get("wake_duration",7.0)
	# A spent pod stays open. Use the exit's registration and matching housing,
	# rather than snapping to an unrelated closed pod when the actor is released.
	var id: String=occupant.get("architect_id","bill")
	var texture: Texture2D=empty_frame(id) if occupant.get("recovered",false) else frame(id,wake_frame_index(float(occupant.get("wake",0.0)),duration))
	var scale:=rect.size.x/290.0
	canvas.draw_texture_rect(texture,Rect2(base-Vector2(210,560)*scale,Vector2(418,627)*scale),false,tint)
