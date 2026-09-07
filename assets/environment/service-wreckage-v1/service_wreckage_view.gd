extends RefCounted
## Fixed small debris below station geometry. Room-sized wrecks live in WreckField.
const ROOT := "res://assets/environment/service-wreckage-v1/"
const SOURCES := {
    "collapsed-support": "collapsed-support-v1.png",
    "torn-cable-harness": "torn-cable-harness-v1.png",
    "ruptured-pressure-tank": "ruptured-pressure-tank-v4.png",
    "detached-hatch": "detached-hatch-v1.png",
    "collapsed-sensor-mast": "collapsed-sensor-mast-v1.png"
}
const GROUPS := [
	{"name":"Broken service frame", "anchor":Vector2(24.5,23.5), "items":[
		{"id":"collapsed-support","offset":Vector2.ZERO,"size":0.68},
		{"id":"torn-cable-harness","offset":Vector2(0.31,0.25),"size":0.42},
		{"id":"detached-hatch","offset":Vector2(-0.29,0.48),"size":0.24}]},
	{"name":"Failed pressure line", "anchor":Vector2(13.5,23.5), "items":[
		{"id":"ruptured-pressure-tank","offset":Vector2.ZERO,"size":0.62},
		{"id":"torn-cable-harness","offset":Vector2(0.55,0.19),"size":0.34}]},
	{"name":"Detached access cover", "anchor":Vector2(27.5,14.5), "items":[
		{"id":"detached-hatch","offset":Vector2.ZERO,"size":0.28}]},
	{"name":"Fallen acoustic receiver", "anchor":Vector2(26.5,21.5), "items":[
		{"id":"collapsed-sensor-mast","offset":Vector2.ZERO,"size":0.55}]}
]
var textures: Dictionary = {}
var initialized := false

func prepare() -> void:
	if initialized:
		return
	initialized = true
	for id in SOURCES:
		var source := Image.new()
		if source.load(ROOT+SOURCES[id])==OK:
			textures[id] = ImageTexture.create_from_image(source)

func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	for group in GROUPS:
		for item in group.items:
			if not textures.has(item.id):
				continue
			var texture: Texture2D = textures[item.id]
			var display := texture.get_size()/texture.get_width()*float(item.size)*cell_size
			var at: Vector2 = (group.anchor+item.offset)*cell_size
			canvas.draw_texture_rect(texture,Rect2(at-display*0.5,display),false,Color(0.43,0.57,0.60,0.88))
