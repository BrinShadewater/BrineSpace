extends RefCounted
## Visual-only stages use the saved powered recovery clock; no wall-clock motion.
const PATHS = {
	"josh": [
		"res://character/robot-rescue-v1/josh/opening-occupied-00.png",
		"res://character/robot-rescue-v1/josh/opening-occupied-01.png",
		"res://character/robot-rescue-v1/josh/opening-occupied-02.png",
		"res://character/robot-rescue-v1/josh/opening-occupied-03.png",
		"res://character/robot-rescue-v1/josh/opening-occupied-04.png",
		"res://character/robot-rescue-v1/josh/opening-occupied-05.png",
		"res://character/robot-rescue-v1/josh/opening-occupied-06.png",
		"res://character/robot-rescue-v1/josh/opening-occupied-07.png",
		"res://character/robot-rescue-v1/josh/reboot-00.png",
		"res://character/robot-rescue-v1/josh/reboot-01.png",
		"res://character/robot-rescue-v1/josh/reboot-02.png",
		"res://character/robot-rescue-v1/josh/reboot-03.png"],
	"river": [
		"res://character/robot-rescue-v1/river/opening-occupied-00.png",
		"res://character/robot-rescue-v1/river/opening-occupied-01.png",
		"res://character/robot-rescue-v1/river/opening-occupied-02.png",
		"res://character/robot-rescue-v1/river/opening-occupied-03.png",
		"res://character/robot-rescue-v1/river/opening-occupied-04.png",
		"res://character/robot-rescue-v1/river/opening-occupied-05.png",
		"res://character/robot-rescue-v1/river/opening-occupied-06.png",
		"res://character/robot-rescue-v1/river/opening-occupied-07.png",
		"res://character/robot-rescue-v1/river/reboot-00.png",
		"res://character/robot-rescue-v1/river/reboot-01.png",
		"res://character/robot-rescue-v1/river/reboot-02.png",
		"res://character/robot-rescue-v1/river/reboot-03.png",
		"res://character/robot-rescue-v1/river/reboot-04.png",
		"res://character/robot-rescue-v1/river/reboot-05.png"]}
# Josh and River are drawn at half the crew's height (owner, Sept 29), so their container frames are
# drawn at twice the source density and the walk-out composite below uses the same density.
const STANDING_HEIGHT := 296.0
const DENSITY := STANDING_HEIGHT / (384.0 * 0.17)
const OPENING_ENDS := [.10,.21,.32,.44,.57,.72,.90,1.20]
static var cache := {}
static var departures := {}
const EMPTY_PATHS := {"josh":"res://character/robot-rescue-v1/josh/empty-open.png","river":"res://character/robot-rescue-v1/river/empty-open.png"}

static func empty_frame(id: String) -> Texture2D:
	var path: String=EMPTY_PATHS[id]
	if not cache.has(path):
		var img:=Image.new()
		if img.load_png_from_buffer(FileAccess.get_file_as_bytes(path))!=OK:return null
		cache[path]=make_texture(img)
	return cache[path]

static func make_texture(img: Image) -> Texture2D:
	var result := ImageTexture.create_from_image(img)
	result.set_meta("crew_frame_92",true)
	result.set_meta("crew_pivot",Vector2(160,280))
	result.set_meta("crew_standing_height",STANDING_HEIGHT)
	return result

static func frame(id: String, index: int) -> Texture2D:
	var path: String = PATHS[id][index]
	if not cache.has(path):
		var img := Image.new()
		if img.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) != OK:return null
		cache[path] = make_texture(img)
	return cache[path]

static func texture(id: String, opened: bool, boot: float, recovered: bool, actor = null, exit_offset := Vector2(0,40)) -> Texture2D:
	if recovered:return empty_frame(id)
	if not opened:return frame(id,0)
	if boot < 1.2:
		for i in OPENING_ENDS.size():
			if boot<OPENING_ENDS[i]:return frame(id,i)
	if boot < 6.4 or actor == null:
		var count: int = PATHS[id].size()-8
		return frame(id,8+mini(count-1,int(clampf((boot-1.2)/5.2,0,1)*count)))
	# Composite the selected walking sprite at its actual navigation exit. This keeps
	# the robot in front of the open interior until it becomes a live depth-sorted NPC.
	var step := clampi(roundi((boot-6.4)/1.6*24),0,24)
	var key := str([id,step,exit_offset])
	if not departures.has(key):
		var img := empty_frame(id).get_image()
		var start := Vector2(0,-2 if id=="josh" else -18)
		var offset := start.lerp(exit_offset*DENSITY,step/24.0)
		var body: Texture2D = actor.player.frame_at_elapsed("walk-south",fmod(step/24.0*1.6,actor.player.cycle_seconds("walk-south")))
		var at := Vector2i((Vector2(160,280)+offset-Vector2(92,172)).round())
		img.blend_rect(body.get_image(),Rect2i(Vector2i.ZERO,body.get_size()),at)
		if departures.size()>=128:departures.clear()
		departures[key]=make_texture(img)
	return departures[key]
