extends Control
## The intro film, played full screen before the title (WIP intro one, owner-approved 2026-09-27).
## SPACE skips it; two seconds after it ends it hands over to the title. The film is made outside this repo
## (Desktop/Projects/Creative/Brine Space Intro, tag wip-intro-1) and exported here as Theora.
## Whole res:// paths on purpose: renames and the release manifest only see whole quoted paths.

const FILM := preload("res://brineui/intro/brine-intro-wip1.ogv")
const TITLE_SCENE := "res://scenes/title_screen.tscn"
const Preferences := preload("res://scripts/title_settings.gd")
const UiFonts := preload("res://scripts/ui_fonts.gd")
## The film is mastered loud (-14 LUFS); this sits it near the station music, then the player's
## music volume applies on top.
const FILM_LEVEL_DB := -10.0
## A beat on the last frame before the title (owner, Sept 29); the title loads during it.
const HOLD_SECONDS := 2.0

var _player: VideoStreamPlayer
var _leaving := false
var _ended := false
var _held := 0.0
var _playing_for := 0.0

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	if DisplayServer.get_name() == "headless":
		# nothing to watch without a display: go straight on, so headless runs never wait on the film
		_to_title.call_deferred()
		return
	Preferences.initialize(get_window())
	theme = UiFonts.apply(Theme.new(), 17)
	var black := ColorRect.new()
	black.color = Color.BLACK
	black.set_anchors_preset(Control.PRESET_FULL_RECT)
	black.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(black)
	_player = VideoStreamPlayer.new()
	_player.stream = FILM
	_player.expand = true
	_player.set_anchors_preset(Control.PRESET_FULL_RECT)
	_player.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_player.volume_db = FILM_LEVEL_DB + linear_to_db(maxf(Preferences.music_volume, 0.0001))
	_player.finished.connect(_film_ended)
	add_child(_player)
	var hint := Label.new()
	hint.text = "SPACE  skip"
	hint.add_theme_color_override("font_color", Color(0.78, 0.86, 0.9, 0.4))
	hint.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	hint.position = Vector2(-150, -52)
	hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(hint)
	_player.play()

# The title is loaded only once the film is over: loading it during playback stalled the main thread for
# about 110 ms mid-film and the film's sound dropped out (owner playtest, Sept 29).
func _film_ended() -> void:
	if _ended:
		return
	_ended = true
	ResourceLoader.load_threaded_request(TITLE_SCENE)

func _process(delta: float) -> void:
	if _player == null or _leaving:
		return
	_playing_for += delta
	# The end signal is not always delivered for the last frame: a stopped player after the start is the end too.
	if not _ended and _playing_for > 1.0 and not _player.is_playing():
		_film_ended()
	if not _ended:
		return
	_held += delta
	if _held >= HOLD_SECONDS and ResourceLoader.load_threaded_get_status(TITLE_SCENE) != ResourceLoader.THREAD_LOAD_IN_PROGRESS:
		_to_title()

func _unhandled_input(event: InputEvent) -> void:
	var key := event as InputEventKey
	if key != null and key.pressed and not key.echo and key.keycode == KEY_SPACE:
		get_viewport().set_input_as_handled()
		_to_title()

func _to_title() -> void:
	if _leaving:
		return
	_leaving = true
	if _player != null:
		_player.stop()
	if ResourceLoader.load_threaded_get_status(TITLE_SCENE) == ResourceLoader.THREAD_LOAD_LOADED:
		get_tree().change_scene_to_packed(ResourceLoader.load_threaded_get(TITLE_SCENE))
	else:
		get_tree().change_scene_to_file(TITLE_SCENE)
