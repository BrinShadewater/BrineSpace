extends RefCounted
## Raw PNG playback shared by the start pod and recovered wards.
static var frames := {}
static var empty_frames := {}
static var closed_texture: Texture2D
static var recovery_players := {}
static var mist_texture: CanvasTexture
const RECOVERY_MANIFESTS := {
	"bill":"res://character/cryo-fall-recovery-v1/bill/manifest.json",
	"veld":"res://character/cryo-fall-recovery-v1/veld/manifest.json",
	"branforth":"res://character/cryo-fall-recovery-v1/branforth/manifest.json",
}
const OPEN_PATHS := {
	"bill":"res://character/cryo-material-pass-v1/bill-open.png",
	"veld":"res://character/cryo-material-pass-v1/veld-open.png",
	"branforth":"res://character/cryo-material-pass-v1/branforth-open.png",
}
const COLD_COLOR := Color(0.66,0.82,1.0)
const EXIT_SECONDS := 4.6
const OPEN_SECONDS := 0.55
const STEP_SECONDS := 1.4
const FALL_START := OPEN_SECONDS+STEP_SECONDS
const GROUND_START := FALL_START+0.7
const RISE_START := GROUND_START+0.55
const IDLE_START := RISE_START+1.25

static func chamber_mist() -> Texture2D:
	# Match the crew's matte sampling at gameplay scale without filtering housing.
	if mist_texture==null:
		var source:=preload("res://scripts/environment_art.gd").texture("leak-puff")
		if source==null: return null
		mist_texture=CanvasTexture.new()
		mist_texture.diffuse_texture=source
		mist_texture.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
	return mist_texture

static func exit_elapsed(wake: float, duration: float) -> float:
	return maxf(0.0,wake-maxf(0.0,duration-EXIT_SECONDS))

static func recovery_player(id: String):
	if not recovery_players.has(id):
		var player=preload("res://scripts/crew_sprite_player.gd").new()
		player.load_manifest(RECOVERY_MANIFESTS[id])
		recovery_players[id]=player
	return recovery_players[id]

static func recovery_frame(id: String, elapsed: float) -> Texture2D:
	if elapsed<FALL_START or elapsed>=IDLE_START: return null
	var player=recovery_player(id)
	if elapsed<GROUND_START:
		return player.frame_at_elapsed("cryo-fall",elapsed-FALL_START)
	if elapsed<RISE_START:
		return player.frames["cryo-fall"].back()
	return player.frame_at_elapsed("cryo-rise",elapsed-RISE_START)

static func exit_step(wake: float, duration: float) -> float:
	return smoothstep(0.0,1.0,clampf((exit_elapsed(wake,duration)-OPEN_SECONDS)/STEP_SECONDS,0.0,1.0))

static func vapour_strength(wake: float, duration: float) -> float:
	var age:=wake-maxf(0.0,duration-EXIT_SECONDS)-0.06
	if age<=0.0 or age>=4.35: return 0.0
	return smoothstep(0.0,0.16,age)*(1.0-smoothstep(1.35,4.35,age))

static func draw_opening_vapour(canvas: CanvasItem, base: Vector2, wake: float, duration: float, tint: Color, reduced_motion: bool) -> void:
	var strength:=vapour_strength(wake,duration)
	if strength<=0.0: return
	var texture:=chamber_mist()
	if texture==null: return
	var age:=wake-maxf(0.0,duration-EXIT_SECONDS)-0.06
	# A finite burst from the lower chamber seam, not the actor's moving feet.
	# Fixed lobes and saved wake time make pause/Continue reproduce the same puff.
	for index in range(5):
		var lobe_age:=age-float(index)*0.035
		if lobe_age<=0.0: continue
		# Fast pressure release settles into a broad, slowly drifting floor cloud.
		var phase:=0.75 if reduced_motion else 1.0-pow(1.0-clampf(lobe_age/0.75,0.0,1.0),2.0)
		var drift:=0.0 if reduced_motion else maxf(0.0,lobe_age-0.75)*0.7
		var side: float=-1.0 if index%2==0 else 1.0
		var center:=base+Vector2(side*(2.0+index*2.0+phase*12.0+drift),2.0+(index%3)*3.0+phase*4.0)
		var extent:=Vector2(45.0+index*3.0,15.0+index*0.7)*lerpf(0.65,1.6,phase)
		var color:=Color(0.70,0.83,0.94,0.16*strength*smoothstep(0.0,0.12,lobe_age))*tint
		canvas.draw_texture_rect(texture,Rect2(center-extent*0.5,extent),false,color)

static func thaw_color(wake: float, duration: float) -> Color:
	# Cold colour persists through the fall, then recedes as circulation returns.
	var progress := clampf((exit_elapsed(wake,duration)-GROUND_START)/(IDLE_START-GROUND_START),0.0,1.0)
	return COLD_COLOR.lerp(Color.WHITE,smoothstep(0.0,1.0,progress))

static func unfreeze_progress(wake: float, duration: float) -> float:
	# The existing pre-opening wait visibly clears the frost over a few seconds.
	var opening_at:=maxf(0.0,duration-EXIT_SECONDS)
	return smoothstep(0.0,1.0,clampf(wake/maxf(0.001,opening_at),0.0,1.0))

static func closed_frame() -> Texture2D:
	if closed_texture==null:
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image,"res://character/cryo-layered-v1/closed.png")
		closed_texture=ImageTexture.create_from_image(image)
	return closed_texture

static func wake_frame_index(wake: float, duration: float) -> int:
	# Thawing is a wait; opening and standing are one short physical action.
	# Spreading six exit poses over the whole timer made each pose hang for seconds.
	var exit_duration := minf(1.2, maxf(duration, 0.001)) # Retained six-pose fallback.
	var elapsed := wake - maxf(0.0, duration - exit_duration)
	if elapsed <= 0.0: return 0
	return clampi(1 + int(elapsed / (exit_duration / 5.0)), 1, 5)

static func empty_frame(id: String) -> Texture2D:
	var actor := id if id in ["bill","veld","branforth"] else "bill"
	if not empty_frames.has(actor):
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image,OPEN_PATHS[actor])
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
	var actor_texture: Texture2D=occupant.get("cryo_actor_texture")
	if actor_texture!=null:
		draw_layered(canvas,rect,occupant,actor_texture,tint)
		return
	var texture: Texture2D=empty_frame(id) if occupant.get("recovered",false) else frame(id,wake_frame_index(float(occupant.get("wake",0.0)),duration))
	var scale:=rect.size.x/290.0
	canvas.draw_texture_rect(texture,Rect2(base-Vector2(210,560)*scale,Vector2(418,627)*scale),false,tint)

static func draw_layered(canvas: CanvasItem, rect: Rect2, occupant: Dictionary, actor: Texture2D, tint: Color) -> void:
	var id: String=occupant.get("architect_id","bill")
	var base:=Vector2(rect.get_center().x,rect.end.y)
	var scale:=rect.size.x/290.0
	var housing:=Rect2(base-Vector2(210,560)*scale,Vector2(418,627)*scale)
	var duration: float=occupant.get("wake_duration",7.0)
	var wake: float=occupant.get("wake",0.0)
	var elapsed:=exit_elapsed(wake,duration)
	var opening:=smoothstep(0.0,OPEN_SECONDS,elapsed)
	if occupant.get("recovered",false):
		canvas.draw_texture_rect(empty_frame(id),housing,false,tint)
		return
	if opening>0.0:
		# Keep the housing opaque beneath the moving reveal. Fading both whole
		# images made the shared shell darken halfway through opening.
		canvas.draw_texture_rect(empty_frame(id),housing,false,tint)
	# Closed and open share a fixed housing registration; only the door changes.
	if opening<1.0:
		var door_tint:=tint
		door_tint.a*=1.0-opening
		canvas.draw_texture_rect(closed_frame(),housing,false,door_tint)
	# Exactly the live renderer's 65.28 world-unit standing height. Never fit a
	# character to the pod image's bounding box or resize individual poses.
	var pixel_scale:=65.28/float(actor.get_meta("crew_standing_height",148.0))
	var step:=exit_step(wake,duration)
	var destination: Vector2=occupant.get("cryo_exit_foot",base+Vector2(0,32.592))
	var foot: Vector2=(base-Vector2(0,30)).lerp(destination,step)
	var actor_rect:=Rect2(foot-Vector2(actor.get_meta("crew_pivot",Vector2(92,172)))*pixel_scale,actor.get_size()*pixel_scale)
	canvas.draw_texture_rect(actor,actor_rect,false,tint*thaw_color(wake,duration))
	if opening<1.0:
		# A restrained glass veil sits over the occupant, not behind their face.
		var glass:=Rect2(housing.position+Vector2(120,145)*scale,Vector2(174,264)*scale)
		var vapour:=chamber_mist()
		if vapour!=null:
			# Cold mist remains inside until the door opens, beneath the glass veil.
			# Saved wake time keeps the slow curl stable on pause and Continue.
			var motion:=0.0 if bool(occupant.get("reduced_motion",false)) else wake
			for index in range(3):
				var center:=Vector2(glass.get_center().x,glass.end.y-(52+index*57)*scale)
				center+=Vector2(sin(motion*1.1+index*2.0)*8.0,sin(motion*0.8+index)*5.0)*scale
				var extent:=Vector2(145,92)*scale
				canvas.draw_texture_rect(vapour,Rect2(center-extent*0.5,extent),false,Color(0.74,0.85,0.94,0.19*(1.0-opening))*tint)
		canvas.draw_rect(glass,Color(0.48,0.74,0.86,0.07*(1.0-opening))*tint)
		var reflection:=Color(0.76,0.91,1.0,0.14*(1.0-opening))*tint
		canvas.draw_line(glass.position+Vector2(5,12)*scale,glass.position+Vector2(22,3)*scale,reflection,scale*2.0,true)
		var frost:=chamber_mist()
		if frost!=null:
			var remaining:=1.0-unfreeze_progress(wake,duration)
			# Painted translucent frost clears from the glass before the door opens.
			for index in range(3):
				var center:=glass.get_center()+Vector2(0,(index-1)*64)*scale
				var extent:=Vector2(160,130)*scale
				canvas.draw_texture_rect(frost,Rect2(center-extent*0.5,extent),false,Color(0.72,0.84,0.93,0.27*remaining)*tint)
	draw_opening_vapour(canvas,base,wake,duration,tint,bool(occupant.get("reduced_motion",false)))
