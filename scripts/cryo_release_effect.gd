extends RefCounted
## Cosmetic emergence uses saved simulation time, including pause and Continue.
const DURATION:=4.0
static func age(game,member: Dictionary) -> float:
	if not member.get("alive",false) or not member.has("thawed_at"): return DURATION
	return maxf(0.0,game.get_visual_time_seconds()-float(member.thawed_at))
static func tint(game,id: String) -> Color:
	for member in game.recovered_crew:
		if member.get("architect_id","")==id:
			return Color(0.66,0.86,1.0).lerp(Color.WHITE,clampf(age(game,member)/DURATION,0,1))
	return Color.WHITE
static func texture(game,id: String,source: Texture2D) -> Texture2D:
	if source==null: return null
	var color:=tint(game,id)
	if color==Color.WHITE: return source
	# Wrap without mutating shared animation frames or changing their geometry.
	var result:=AtlasTexture.new()
	result.atlas=source
	result.region=Rect2(Vector2.ZERO,source.get_size())
	for key in source.get_meta_list(): result.set_meta(key,source.get_meta(key))
	result.set_meta("cryo_tint",color)
	return result
static func draw(canvas: CanvasItem,game,cell_size: float) -> void:
	var scale:=cell_size/384.0
	for member in game.recovered_crew:
		var seconds:=age(game,member)
		if seconds>=DURATION or not member.has("thaw_foot"): continue
		var origin: Vector2=member.thaw_foot*scale
		for i in range(28):
			var life:=seconds-float(i%7)*0.055
			if life<0.0: continue
			var fade:=pow(1.0-clampf(life/DURATION,0,1),1.6)
			var side: float=-1.0 if i%2==0 else 1.0
			var drift:=0.3 if game.Preferences.reduced_motion else life
			var at:=origin+Vector2(side*(6+float(i%5)*3+drift*(8+i%4)), -5-float(i%7)*3-drift*(5+i%3))*scale
			canvas.draw_circle(at,(3.0+float(i%4)+drift*1.5)*scale,Color(.60,.84,1.0,fade*.15),true,-1,true)
			if i%4==0: canvas.draw_line(at,at+Vector2(2,-3)*scale,Color(.80,.94,1.0,fade*.55),scale,true)
