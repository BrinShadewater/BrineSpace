extends SceneTree
const Art = preload("res://scripts/lighting_art.gd")
const Lighting = preload("res://rooms/whole-room/room_lighting.gd")
const Effects = preload("res://scripts/station_effects.gd")
const Preferences = preload("res://scripts/title_settings.gd")
const Visibility = preload("res://scripts/underwater_visibility.gd")
var failures := 0
var checks := 0
func expect(value: bool, label: String) -> void:
	checks += 1
	if not value: failures += 1; push_error(label)
class FakeGame:
	extends RefCounted
	var occupied := {}
	var clock := 3.0
	func get_visual_time_seconds() -> float: return clock
class Recorder:
	extends RefCounted
	var calls: Array = []
	func draw_texture_rect_region(_texture, rect, region, color): calls.append([rect,region,color])
	func draw_arc(at,radius,_a,_b,_c,_color,_width,_aa): calls.append([at,radius])
	func draw_circle(at,radius,_color): calls.append([at,radius])
func _initialize() -> void: call_deferred("run")
func run() -> void:
	for key in Art.PATHS:
		var tex := Art.texture(key)
		expect(tex != null,"Load "+key)
		if tex != null: expect(Vector2i(tex.get_size()) == Art.SIZES[key],"Dimensions "+key)
	var native := Lighting.halo_texture().get_image()
	native.resize(64,64,Image.INTERPOLATE_NEAREST)
	expect(native.get_data() == Lighting.procedural_halo_texture().get_image().get_data(),"Authored halo exactly preserves fallback Bayer bands")
	var saved: Dictionary = Art.textures.duplicate()
	Art.textures["warm"] = null
	expect(Lighting.halo_texture() == Lighting.procedural_halo_texture(),"Missing halo returns generated fallback")
	Art.textures["caustics"] = null
	var fallback := Visibility.new()
	expect(fallback.material.get_shader_parameter("use_caustics_tex") != true,"Missing caustic keeps procedural shader")
	Art.textures = saved.duplicate()
	var authored := Visibility.new()
	expect(authored.material.get_shader_parameter("use_caustics_tex") == true,"Caustic sampler bound")
	var game := FakeGame.new()
	var rooms: Array = []
	for x in range(12): rooms.append({"pos":Vector2i(x*2,2)})
	Preferences.effects_quality=1; Preferences.reduced_motion=false
	var recorder := Recorder.new()
	Effects.draw_hull_bubbles(recorder,game,rooms,384)
	expect(not recorder.calls.is_empty(),"Medium bubbles drawn")
	var frozen: Array = recorder.calls.duplicate(true)
	recorder.calls.clear(); Effects.draw_hull_bubbles(recorder,game,rooms,384)
	expect(recorder.calls == frozen,"Unchanged visual clock freezes bubble position and fade")
	Preferences.effects_quality=2; recorder.calls.clear()
	Effects.draw_hull_bubbles(recorder,game,rooms,384)
	expect(recorder.calls.size()*4 == frozen.size()*7,"High keeps seven bubbles versus Medium four")
	Preferences.effects_quality=0; recorder.calls.clear()
	Effects.draw_hull_bubbles(recorder,game,rooms,384)
	expect(recorder.calls.is_empty(),"Low has no bubbles")
	Preferences.effects_quality=2; Preferences.reduced_motion=true
	Effects.draw_hull_bubbles(recorder,game,rooms,384)
	expect(recorder.calls.is_empty(),"Reduced Motion has no bubbles")
	Preferences.reduced_motion=false; Preferences.effects_quality=1
	Art.textures["bubbles"]=null
	Effects.draw_hull_bubbles(recorder,game,rooms,384)
	expect(recorder.calls.size() == frozen.size()*2,"Missing atlas uses arc and highlight fallback")
	Art.textures=saved
	expect(Lighting.BEACON_TURNS_PER_SECOND == .25,"Beacon still takes four seconds per turn")
	expect(Lighting.EMERGENCY_PERIOD >= 1.0,"Emergency pulse stays below three per second")
	print("LIGHTING ART: checks=",checks," failures=",failures)
	quit(1 if failures else 0)
