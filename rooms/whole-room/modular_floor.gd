extends RefCounted
## Pilot tile geometry. Cached in room-local coordinates; no zoom or light state in keys.
const SCIENCE="res://assets/department-floors-v2/science-panels.png"
const HALL_TILES="res://assets/hallway-floor-tiles-v2/source.png"
const HALL_QUIET="res://assets/hallway-floor-tiles-v1/source.png"
const DECK="res://assets/floors-and-details-v5/corridor-deck.png"
const MATERIALS=["Original","Sealed panel","Steel plate","Grating"]
const LIMIT=96
static var enabled:=not OS.get_cmdline_user_args().has("--reference-floor-tiles")
static var cache: Dictionary={}
static var textures: Dictionary={}
static var cell_cache: Dictionary={}
static var builds:=0
static var hits:=0
static func texture(path: String) -> Texture2D:
	if not textures.has(path):
		var im:=Image.new()
		assert(im.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK)
		textures[path]=ImageTexture.create_from_image(im)
	return textures[path]
static func pilot(id: String) -> bool: return id in ["research_lab", "reactor", "life_support", "crew_hab", "corridor", "corner", "tee_corridor", "hydroponics_bay", "mycelium_nursery", "tidal_condenser", "quarantine_cell", "cryo_chamber", "clone_lab", "med_bay", "storage_bay", "pressure_control", "crew_lounge", "mining_drone_bay", "ore_refinery", "listening_post", "xeno_lab", "maintenance_bay", "bio_lab", "isolation_vault", "current_turbine", "biomass_digester", "heat_recovery", "airlock", "construction_drone_bay", "brine_core", "solar_array", "battery_array", "salvage_drone_bay", "gravity_loom", "data_archive", "biodome", "anomaly_lab", "command_center", "holographic_core", "med_center", "med_office", "radio_lab", "shield_generator", "observation_room", "salvage_workshop", "galley", "cold_store"]
static func tile_key(cell: Vector2i) -> String: return "tile/%d/%d" % [cell.x,cell.y]
static func material_key(cell: Vector2i) -> String: return "floor/material/%d/%d" % [cell.x,cell.y]
static func tile_at(point: Vector2) -> Vector2i: return Vector2i(((point+Vector2.ONE*192)/48).floor())
static func floor_values(values: Dictionary) -> Dictionary:
	var result: Dictionary={}
	for key in values:
		if str(key).begins_with("tile/") or str(key).begins_with("floor/"): result[key]=values[key]
	return result
static func rectangle(rect: Rect2) -> PackedVector2Array:
	return PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
static func footprint(corridor: bool, q: int, shape:="corridor") -> PackedVector2Array:
	if not corridor: return rectangle(Rect2(-192,-192,384,384))
	var result:=PackedVector2Array()
	for p in preload("res://rooms/underwater/corridor_geometry.gd").floor_for(shape=="corner",shape=="tee_corridor"):
		result.append(preload("res://tools/modular_room_geometry.gd").turn(p,q))
	return result
static func cells(corridor: bool, q: int, shape:="corridor") -> Array[Vector2i]:
	var key:=str(corridor)+str(q if corridor else 0)+shape
	if cell_cache.has(key): return cell_cache[key]
	var result: Array[Vector2i]=[]
	var poly:=footprint(corridor,q,shape)
	for y in range(8):
		for x in range(8):
			var cell:=Vector2i(x,y)
			if Geometry2D.is_point_in_polygon(Vector2(cell)*48-Vector2.ONE*168,poly): result.append(cell)
	cell_cache[key]=result
	return result
static func tile_material(values: Dictionary, cell: Vector2i) -> int:
	var value=values.get(material_key(cell),0)
	return clampi(int(value),0,3) if value is int or value is float else 0
static func add_polygon(groups: Dictionary, path: String, poly: PackedVector2Array, rect: Rect2, uv_rect: Rect2, color: Color, corridor_original:=false, q:=0) -> void:
	var triangles:=Geometry2D.triangulate_polygon(poly)
	if triangles.is_empty(): return
	if not groups.has(path): groups[path]={"vertices":PackedVector3Array(),"uv":PackedVector2Array(),"colors":PackedColorArray(),"indices":PackedInt32Array()}
	var group: Dictionary=groups[path]
	var offset: int=group.vertices.size()
	for p in poly:
		group.vertices.append(Vector3(p.x,p.y,0))
		group.uv.append((preload("res://tools/modular_room_geometry.gd").turn(p,-q)+Vector2.ONE*192)/384 if corridor_original else uv_rect.position+(p-rect.position)/rect.size*uv_rect.size)
		group.colors.append(color)
	for index in triangles: group.indices.append(index+offset)
static var finish_catalog: Dictionary={}
static func finishes() -> Dictionary:
	if not finish_catalog.is_empty(): return finish_catalog
	var result: Dictionary={"Station deck":DECK,"Industrial hallway deck":HALL_TILES,"Quiet hallway panels":HALL_QUIET}
	for row in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/floor-profiles-v1/rooms.json")):
		var path:=str(row.source)
		if path in result.values(): continue
		result[path.get_file().get_basename().replace("-"," ").capitalize()]=path
	finish_catalog=result
	return result

static func hall_module(local: Vector2, shape: String, variant:=0) -> Dictionary:
	var shape_index:=0 if shape=="corridor" else 1 if shape=="corner" else 2
	var v:=posmod(variant,3)
	var borders: Array=[Vector2(6,0),Vector2(1,0),Vector2(2,1),Vector2(5,1),Vector2(4,2),Vector2(2,3),Vector2(5,3),Vector2(3,4),Vector2(6,4)]
	var border: Vector2=borders[shape_index*3+v]
	var rhythm:=posmod(int(floor(absf(local.x)/24))*3+int(floor(absf(local.y)/24))*5+shape_index*2+v,11)
	if rhythm in [3,8]: border=Vector2(6,0)
	elif rhythm==6: border=Vector2(2,1)
	# A two-module service lane lies between solid perimeter strips.
	var horizontal:=absf(local.y)<24 and (shape!="corner" or local.x<24)
	var vertical:=shape!="corridor" and absf(local.x)<24 and local.y>-24
	if not horizontal and not vertical: return {"tile":border,"turn":0}
	if horizontal and vertical:
		# Symmetric grated manifold covers join either lane at an elbow or branch.
		return {"tile":Vector2(0,0),"turn":0}
	# Identical pipe/grating lanes keep reciprocal sockets aligned after 180-degree turns.
	var along:=local.x if horizontal else local.y
	var middle:=Vector2(7,0)
	if absf(along)<144:
		if v==0: middle=Vector2(4,0) if posmod(int(floor(along/24))+shape_index,4)<2 else Vector2(0,0)
		elif v==2:
			middle=[Vector2(2,0),Vector2(2,4),Vector2(4,3)][shape_index]
			if posmod(int(floor(absf(along)/24)),5)==2: middle=Vector2(0,0)
	return {"tile":middle,"turn":1 if horizontal else 0}

static func add_hall_cell(groups: Dictionary, rect: Rect2, poly: PackedVector2Array, q: int, shape: String, color: Color, variant:=0) -> void:
	var turn=preload("res://tools/modular_room_geometry.gd")
	for y in range(2):
		for x in range(2):
			var small:=Rect2(rect.position+Vector2(x,y)*24,Vector2.ONE*24)
			var module:=hall_module(turn.turn(small.get_center(),-q),shape,variant)
			for clipped in Geometry2D.intersect_polygons(rectangle(small),poly):
				var offset: int=groups.get(HALL_TILES,{"uv":[]}).uv.size()
				add_polygon(groups,HALL_TILES,clipped,small,Rect2(module.tile/8,Vector2.ONE/8),color)
				for i in range(clipped.size()):
					var local:=turn.turn((clipped[i]-small.get_center())/24,-q-int(module.turn))+Vector2.ONE*.5
					groups[HALL_TILES].uv[offset+i]=(module.tile+local)/8

static func meshes(values: Dictionary, corridor: bool, q:=0, opacity:=0.42, source_path:=SCIENCE, shape:="corridor", variant:=0) -> Array:
	var relevant:=floor_values(values)
	var key:=hash([relevant,corridor,q,opacity,source_path,shape,variant])
	if cache.has(key): hits+=1; return cache[key]
	var groups: Dictionary={}
	var poly:=footprint(corridor,q,shape)
	for cell in cells(corridor,q,shape):
		var rect:=Rect2(Vector2(cell)*48-Vector2.ONE*192,Vector2.ONE*48)
		var regions:=Geometry2D.intersect_polygons(rectangle(rect),poly)
		var material:=tile_material(values,cell)
		var path: String=(HALL_TILES if corridor else source_path) if material==0 else (DECK if material in [2,3] else SCIENCE)
		var finish: String=str(values.get("floor/finish",""))
		if finish in finishes().values(): path=finish
		var uv_rect: Rect2
		if material==0:
			var source=values.get(tile_key(cell),[cell.x,cell.y] if corridor else [cell.x%4,cell.y%4])
			if not source is Array or source.size()!=2 or not (source[0] is int or source[0] is float) or not (source[1] is int or source[1] is float): source=[cell.x,cell.y] if corridor else [cell.x%4,cell.y%4]
			var divisions:=8 if corridor and path not in [HALL_TILES,HALL_QUIET] else 4
			uv_rect=Rect2(Vector2(posmod(int(source[0]),divisions),posmod(int(source[1]),divisions))/divisions,Vector2.ONE/divisions)
		elif material==1: uv_rect=Rect2(0.40,0.185,0.18,0.065)
		elif material==2: uv_rect=Rect2(0.16,0.05,0.16,0.20)
		else: uv_rect=Rect2(0.20,0.37,0.20,0.20)
		var shade:=1.0
		if values.get("floor/variation",false): shade=0.975+float(posmod(hash([cell,values.get("floor/seed",1)]),6))*0.01
		var color:=Color(shade,shade,shade,1.0 if corridor else opacity)
		if corridor and path==HALL_TILES and material==0 and not values.has(tile_key(cell)):
			add_hall_cell(groups,rect,poly,q,shape,color,variant)
			continue
		for region in regions: add_polygon(groups,path,region,rect,uv_rect,color,corridor and material==0 and path not in [HALL_TILES,HALL_QUIET],q)
	var result: Array=[]
	for path in groups:
		var group: Dictionary=groups[path]
		var arrays:=[]; arrays.resize(Mesh.ARRAY_MAX)
		arrays[Mesh.ARRAY_VERTEX]=group.vertices; arrays[Mesh.ARRAY_TEX_UV]=group.uv
		arrays[Mesh.ARRAY_COLOR]=group.colors; arrays[Mesh.ARRAY_INDEX]=group.indices
		var mesh:=ArrayMesh.new(); mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
		result.append({"mesh":mesh,"texture":texture(path)})
	if cache.size()>=LIMIT: cache.erase(cache.keys()[0])
	cache[key]=result; builds+=1
	return result
static func draw(canvas: CanvasItem, values: Dictionary, corridor: bool, q:=0, opacity:=0.42, center:=Vector2.ZERO, light:=1.0, source_path:=SCIENCE, shape:="corridor", variant:=0) -> void:
	for batch in meshes(values,corridor,q,opacity,source_path,shape,variant):
		canvas.draw_mesh(batch.mesh,batch.texture,Transform2D(0,center),Color(light,light,light))
