extends RefCounted
## Studio's Characters & Companions: one preview actor per cast member, each with its own
## activity, so several can share a room for judging scale. Preview only; never saved into
## a layout or inserted into the live crew.
const Actor = preload("res://scripts/room_scale_preview.gd")
const CAST = Actor.CAST
const ACTIVITY_NAMES = Actor.ACTIVITY_NAMES
# The activities a Studio row offers (Standing stays available to the card tools).
const ROW_ACTIVITIES := [Actor.HIDDEN, Actor.WALKING, Actor.RUNNING, Actor.SWIMMING, Actor.INTERACTING]
var actors: Array = []
var room_key: Array = []

func _init() -> void:
	for index in range(CAST.size()):
		var actor = Actor.new()
		actor.cast_index = index
		# Spread the starting spots so members do not begin on top of one another.
		actor.foot = Vector2((index % 3 - 1) * 70, (index / 3 - 1) * 70)
		actors.append(actor)

func mode_of(index: int) -> int:
	return actors[index].mode

func set_mode(index: int, value: int, room = null, id := "", quarter := 0) -> void:
	var actor = actors[index]
	actor.mode = value
	actor.action_index = index
	actor.action_started = actor.clock
	if value != Actor.HIDDEN:
		actor.load_art()
		if room != null: actor.rebuild(room, id, quarter)

func any_shown() -> bool:
	return actors.any(func(actor): return actor.mode != Actor.HIDDEN)

func hide_all() -> void:
	for actor in actors: actor.mode = Actor.HIDDEN

func rebuild(room, id: String, quarter: int) -> void:
	for actor in actors:
		if actor.mode != Actor.HIDDEN: actor.rebuild(room, id, quarter)

func clear_signatures() -> void:
	for actor in actors: actor.signature.clear()

func advance(delta: float) -> void:
	for actor in actors: actor.advance(delta)

func members() -> Array:
	var result: Array = []
	for actor in actors: result.append_array(actor.members())
	return result
