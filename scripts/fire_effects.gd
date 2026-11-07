extends RefCounted
## Authored fire atlases; sources and reproducible bake live in assets/fire-effects-v1.
const PATHS := {
	"flame":"res://assets/fire-effects-v1/flame-96x128-v3.png",
	"smoke":"res://assets/fire-effects-v1/smoke-96x128.png",
	"embers":"res://assets/fire-effects-v1/embers-96x128.png",
	"sparks":"res://legacy/default/assets/electrical-sparks-v1/sparks-96x128.png",
}
const ELECTRICAL_MACHINERY := {"reactor":true,"biomass_digester":true,"galley":true,"salvage_workshop":true}
const CELL := Vector2(96,128)
const PIVOT := Vector2(48,118)
static var sheets := {}
static var attempted := false

static func ready() -> bool:
	if attempted: return sheets.size()==PATHS.size()
	attempted=true
	for kind in PATHS:
		var path: String=PATHS[kind]
		if not FileAccess.file_exists(path):
			push_warning("Fire atlas missing; using procedural fallback: "+path)
			continue
		var picture := Image.new()
		if picture.load_png_from_buffer(FileAccess.get_file_as_bytes(path))!=OK or picture.get_size()!=Vector2i(384,256):
			push_warning("Fire atlas invalid; using procedural fallback: "+path)
			continue
		sheets[kind]=ImageTexture.create_from_image(picture)
	return sheets.size()==PATHS.size()

static func frame(time: float,fps: float,phase: int) -> int:
	return posmod(floori(time*fps)+phase,8)

static func sprite(canvas,kind: String,foot: Vector2,scale: float,time: float,fps: float,phase: int,opacity:=1.0) -> void:
	var index := frame(time,fps,phase)
	var source := Rect2(Vector2(index%4,index/4)*CELL,CELL)
	canvas.draw_texture_rect_region(sheets[kind],Rect2(foot-PIVOT*scale,CELL*scale),source,Color(1,1,1,opacity))

static func spark_time(time: float, seed: int) -> float:
	# Eight frames at 12 fps, followed by a quiet interval. Simulation time pauses.
	return fposmod(time+float(seed)*0.29,2.8)

static func draw(canvas,game,rooms: Array,size: float) -> bool:
	if not ready(): return false
	var time: float=game.get_visual_time_seconds()
	var unit := size/384.0
	for room in rooms:
		var intensity: float=room.get("fire",0.0)
		var fault: bool=bool(room.get("electrical_fault",false)) or float(room.get("fire_heat",0))>=0.75
		if intensity<=0 and not fault: continue
		var foot: Vector2=(Vector2(room.pos)+Vector2(.5,.40))*size
		var seed: int=posmod(room.pos.x*3+room.pos.y*5,8)
		var scale := unit*(.55+intensity*.65)
		if intensity>0:
			# Smoke stays behind the hotter folds. Separate phases avoid matching columns.
			sprite(canvas,"smoke",foot-Vector2(0,18)*unit,scale*1.25,time,6,seed,.64)
			if intensity>.4:
				sprite(canvas,"flame",foot+Vector2(-23,-3)*unit,scale*.76,time,8,seed+3)
			if intensity>.7:
				sprite(canvas,"flame",foot+Vector2(24,3)*unit,scale*.72,time,8,seed+5)
			sprite(canvas,"flame",foot,scale,time,8,seed)
			sprite(canvas,"embers",foot,scale*1.1,time,8,seed,.85)
		if ELECTRICAL_MACHINERY.has(room.get("id","")) and game.hardware.power and not room.get("suspended",false):
			var burst := spark_time(time,seed)
			if burst<8.0/12.0:
				sprite(canvas,"sparks",foot+Vector2(26,20)*unit,unit*.9,burst,12,0)
	return true
