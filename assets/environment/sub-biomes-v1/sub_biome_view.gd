extends RefCounted
## Decorative habitat patches. Occupancy and excavation remain authoritative elsewhere.
const ROOT := "res://assets/environment/sub-biomes-v1/"
const DEFINITIONS := {
	"sulfur": {"name":"Sulfur vent basin", "props":["anhydrite","bacterial-mat"]},
	"sponge": {"name":"Sponge reef", "props":["vase-sponges","sea-fans"]},
	"brine": {"name":"Brine salt flats", "props":["salt-plates","seep-stones"]},
	"kelp": {"name":"Kelp meadow", "props":["ribbon-kelp","holdfast"]},
	"coral": {"name":"Cold coral garden", "props":["lace-coral","cup-corals"]},
	"nodules": {"name":"Manganese nodule field", "props":["nodule-cluster","brittle-stars"]},
	"iron": {"name":"Iron seep", "props":["mineral-ledges","hydroids"]}
}
const REGIONS := [
	{"biome":"sulfur","center":Vector2(14.5,17.5),"radius":Vector2(5,4)},
	{"biome":"sponge","center":Vector2(25,18),"radius":Vector2(4,4)},
	{"biome":"brine","center":Vector2(20,26),"radius":Vector2(5,3.5)},
	{"biome":"kelp","center":Vector2(10,26),"radius":Vector2(4,4)},
	{"biome":"coral","center":Vector2(29,26),"radius":Vector2(4,4)},
	{"biome":"nodules","center":Vector2(20,9),"radius":Vector2(5,3.5)},
	{"biome":"iron","center":Vector2(30,11),"radius":Vector2(4,3.5)}
]
const SOURCES := {
    "sulfur-ground": "sulfur-ground-v1.png",
    "sulfur-anhydrite": "sulfur-anhydrite-v2.png",
    "sulfur-bacterial-mat": "sulfur-bacterial-mat-v1.png",
    "sponge-ground": "sponge-ground-v1.png",
    "sponge-vase-sponges": "sponge-vase-sponges-v2.png",
    "sponge-sea-fans": "sponge-sea-fans-v2.png",
    "brine-ground": "brine-ground-v1.png",
    "brine-salt-plates": "brine-salt-plates-v1.png",
    "brine-seep-stones": "brine-seep-stones-v1.png",
    "kelp-ground": "kelp-ground-v1.png",
    "kelp-ribbon-kelp": "kelp-ribbon-kelp-v1.png",
    "kelp-holdfast": "kelp-holdfast-v1.png",
    "coral-ground": "coral-ground-v1.png",
    "coral-lace-coral": "coral-lace-coral-v1.png",
    "coral-cup-corals": "coral-cup-corals-v1.png",
    "nodules-ground": "nodules-ground-v1.png",
    "nodules-nodule-cluster": "nodules-nodule-cluster-v1.png",
    "nodules-brittle-stars": "nodules-brittle-stars-v1.png",
    "iron-ground": "iron-ground-v1.png",
    "iron-mineral-ledges": "iron-mineral-ledges-v1.png",
    "iron-hydroids": "iron-hydroids-v1.png"
}
var textures: Dictionary = {}
var meshes: Array[ArrayMesh] = []
var props: Array[Dictionary] = []
var initialized := false

static func coverage(point: Vector2, center: Vector2, radius: Vector2) -> float:
	var normalized := (point-center)/radius
	var angle := atan2(normalized.y,normalized.x)
	var irregular := normalized.length()+0.065*sin(angle*5.0+center.x)+0.035*sin(angle*9.0+center.y)
	return 1.0-smoothstep(0.67,1.0,irregular)

static func ground_mesh(center: Vector2, radius: Vector2) -> ArrayMesh:
	# Each authored habitat gets one continuous material field. Mirroring a small
	# tile made salt veins and sulfur deposits form repeated bilateral diamonds.
	# The irregular alpha boundary hides the source rectangle without repeating it.
	var first := ((center-radius*1.15)*4.0).floor()/4.0
	var last := ((center+radius*1.15)*4.0).ceil()/4.0
	var columns := roundi((last.x-first.x)*4)+1
	var rows := roundi((last.y-first.y)*4)+1
	var vertices := PackedVector3Array()
	var colors := PackedColorArray()
	var uvs := PackedVector2Array()
	var indices := PackedInt32Array()
	for y in range(rows):
		for x in range(columns):
			var at := first+Vector2(x,y)*0.25
			vertices.append(Vector3(at.x,at.y,0))
			colors.append(Color(0.49,0.58,0.57,coverage(at,center,radius)))
			uvs.append((at-center)/(radius*2.3)+Vector2(0.5,0.5))
			if x<columns-1 and y<rows-1:
				var i := y*columns+x
				indices.append_array(PackedInt32Array([i,i+1,i+columns,i+1,i+columns+1,i+columns]))
	var arrays := []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = vertices
	arrays[Mesh.ARRAY_COLOR] = colors
	arrays[Mesh.ARRAY_TEX_UV] = uvs
	arrays[Mesh.ARRAY_INDEX] = indices
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
	return mesh

func prepare() -> void:
	if initialized:
		return
	initialized = true
	for biome in DEFINITIONS:
		for suffix in ["ground"]+DEFINITIONS[biome].props:
			var id: String = biome+"-"+suffix
			var source := Image.new()
			if source.load(ROOT+SOURCES[id])==OK:
				textures[id] = ImageTexture.create_from_image(source)
	var rng := RandomNumberGenerator.new()
	rng.seed = 609202601
	for region in REGIONS:
		meshes.append(ground_mesh(region.center,region.radius))
		for i in range(14):
			var at: Vector2 = region.center+Vector2(rng.randf_range(-0.65,0.65),rng.randf_range(-0.65,0.65))*region.radius
			if coverage(at,region.center,region.radius)<0.65 or at.distance_to(Vector2(20.5,20.5))<2.0:
				continue
			var choices: Array = DEFINITIONS[region.biome].props
			props.append({"id":region.biome+"-"+choices[i%2],"at":at,"size":rng.randf_range(0.3,0.65)})

func render_into(canvas: CanvasItem, cell_size: float) -> void:
	prepare()
	for i in range(REGIONS.size()):
		var id: String = REGIONS[i].biome+"-ground"
		if textures.has(id):
			canvas.draw_mesh(meshes[i],textures[id],Transform2D().scaled(Vector2.ONE*cell_size))
	for prop in props:
		if not textures.has(prop.id):
			continue
		var texture: Texture2D = textures[prop.id]
		var display := texture.get_size()/texture.get_width()*float(prop.size)*cell_size
		canvas.draw_texture_rect(texture,Rect2(prop.at*cell_size-display*0.5,display),false,Color(0.59,0.68,0.66,0.85))
