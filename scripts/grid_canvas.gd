extends Control
class_name GridCanvas

signal cell_clicked(cell: Vector2i)
signal cell_secondary_clicked(cell: Vector2i)
signal cell_hovered(cell: Vector2i)

const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const SeabedBackground := preload("res://assets/environment/seabed-v1/seabed_background.gd")
var seabed_background := SeabedBackground.new()
const WreckView := preload("res://assets/environment/wrecked-rooms-v1/wreck_view.gd")
var wreck_view := WreckView.new()
const RockView := preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
var rock_view := RockView.new()
var harvest_site_art := preload("res://scripts/harvest_site_art.gd").new()
const NurseryView := preload("res://rooms/whole-room/nursery_furnished_view.gd")
var nursery_view: NurseryView
const LifeSupportView := preload("res://rooms/whole-room/underwater_life_support_view.gd")
var life_support_view: LifeSupportView
const HydroponicsView := preload("res://rooms/whole-room/hydroponics_view.gd")
var hydroponics_view: HydroponicsView
const ReactorView := preload("res://rooms/whole-room/reactor_view.gd")
var reactor_view: ReactorView
const MedBayView := preload("res://rooms/whole-room/med_bay_view.gd")
var med_bay_view: MedBayView
const CrewHabView = preload("res://rooms/whole-room/crew_hab_view.gd")
var crew_hab_view: CrewHabView
const CryoView = preload("res://rooms/underwater/batch-two/cryo_chamber_view.gd")
var cryo_view: CryoView
const CloneView = preload("res://rooms/underwater/batch-two/clone_lab_view.gd")
var clone_view: CloneView
const ArchiveView = preload("res://rooms/underwater/batch-two/data_archive_view.gd")
var archive_view: ArchiveView
const BiodomeView = preload("res://rooms/underwater/batch-two/biodome_view.gd")
var biodome_view: BiodomeView
const XenoView = preload("res://rooms/underwater/batch-two/xeno_lab_view.gd")
var xeno_view: XenoView
const AnomalyView = preload("res://rooms/underwater/batch-two/anomaly_lab_view.gd")
var anomaly_view: AnomalyView
const BioView = preload("res://rooms/underwater/batch-two/bio_lab_view.gd")
var bio_view: BioView
const HoloView = preload("res://rooms/underwater/batch-two/holographic_core_view.gd")
var holo_view: HoloView
const MedCenterView = preload("res://rooms/underwater/batch-two/med_center_view.gd")
var med_center_view: MedCenterView
const MedOfficeView = preload("res://rooms/underwater/batch-two/med_office_view.gd")
var med_office_view: MedOfficeView
const TidalView = preload("res://rooms/underwater/tidal-condenser/tidal_condenser_view.gd")
var tidal_view: TidalView
const GravityView = preload("res://rooms/underwater/gravity-loom/gravity_loom_view.gd")
var gravity_view: GravityView
const BrineView = preload("res://rooms/underwater/brine-core/brine_core_view.gd")
var brine_view: BrineView
var rare_room_views := {}
const AirlockView=preload("res://rooms/underwater/airlock-v1/airlock_view.gd")
var airlock_view: AirlockView
const HullView = preload("res://rooms/underwater/hull-integrity/shield_generator_view.gd")
var hull_view: HullView
const AcousticView = preload("res://rooms/underwater/acoustic-comms/radio_lab_view.gd")
var acoustic_view: AcousticView
const ThermalView = preload("res://rooms/underwater/thermal-control/solar_array_view.gd")
var thermal_view: ThermalView
const BatteryView = preload("res://rooms/production-ten/battery_array_view.gd")
var battery_view: BatteryView
const ResearchView = preload("res://rooms/production-ten/research_lab_view.gd")
var research_view: ResearchView
const MaintenanceView = preload("res://rooms/production-ten/maintenance_bay_view.gd")
var maintenance_view: MaintenanceView
const StorageView = preload("res://rooms/production-ten/storage_bay_view.gd")
var storage_view: StorageView
const RefineryView = preload("res://rooms/production-ten/ore_refinery_view.gd")
var refinery_view: RefineryView
const MiningView = preload("res://rooms/production-ten/mining_drone_bay_view.gd")
var mining_view: MiningView
const ConstructionView = preload("res://rooms/production-ten/construction_drone_bay_view.gd")
var construction_view: ConstructionView
const DroneArt = preload("res://scripts/drone_art.gd")
const SalvageView = preload("res://rooms/production-ten/salvage_drone_bay_view.gd")
var salvage_view: SalvageView
const LoungeView = preload("res://rooms/production-ten/crew_lounge_view.gd")
var lounge_view: LoungeView
const CommandView = preload("res://rooms/production-ten/command_center_view.gd")
var command_view: CommandView
const QuarantineView = preload("res://rooms/production-ten/quarantine_cell_view.gd")
var quarantine_view: QuarantineView
const RoomLighting := preload("res://rooms/whole-room/room_lighting.gd")
const RoomDoor := preload("res://rooms/whole-room/room_door.gd")
const AnimatedDoorAtlas := preload("res://rooms/whole-room/animated_door_atlas.gd")
var room_light_levels := {}
const CorridorGeometry = preload("res://rooms/underwater/corridor_geometry.gd")
const CorridorArt = preload("res://rooms/underwater/corridor_surfaces.gd")
var corridor_textures: Array = []
var side_open_door_prototype := false # Explicit review fixture only; no normal-run state override.

func _room_light_target(room: Dictionary) -> float:
	var main = _get_main()
	if room.id=="brine_core" and not main.architect_run.is_empty() and not main.architect_run.core.recovered: return 1.0
	var cell: Vector2i = room.pos
	var reason := str(main.offline_reasons.get(cell,""))
	return 1.0 if RoomLighting.has_light_power(main.powered_room_cells.has(cell),reason,main.unpowered_room_cells.has(cell)) else 0.0

func _room_light_level(room: Dictionary) -> float:
	return float(room_light_levels.get(room.pos,_room_light_target(room)))

func _advance_room_lights(delta: float) -> void:
	var main = _get_main()
	if main.paused: return
	for cell in room_light_levels.keys():
		if not main.occupied.has(cell): room_light_levels.erase(cell)
	for room in main.placed_rooms:
		if _uses_layered_art(room):
			room_light_levels[room.pos] = move_toward(_room_light_level(room),_room_light_target(room),delta/RoomLighting.FADE_SECONDS)

func _draw_layered_lighting() -> void:
	var main = _get_main()
	var size := _cell_size()
	# Post-assembly shading is cell-clipped: no neighbor can repaint a shared
	# wall over the shade, and no dark rectangle extends into another room.
	for room in visible_draw_rooms:
		if not _uses_layered_art(room): continue
		if _is_narrow_corridor(room): continue # Hull-local lighting; do not darken surrounding water.
		var level := _room_light_level(room)
		var rect := Rect2(Vector2(room.pos)*size,Vector2.ONE*size)
		draw_target.draw_rect(rect,Color(0.025,0.045,0.07,lerpf(0.72,0.0,level)))
	for room in visible_draw_rooms:
		if not _uses_layered_art(room): continue
		if _is_narrow_corridor(room): continue # Fixtures mount on the narrow hull, not full-cell north.
		draw_target.draw_set_transform((Vector2(room.pos)+Vector2.ONE*0.5)*size,0,Vector2.ONE*size/384.0)
		RoomLighting.draw_fixtures(draw_target,_room_light_level(room),room.get("id","") in ["med_bay","life_support","cryo_chamber","clone_lab","data_archive","biodome","xeno_lab","med_office","med_center","holographic_core","bio_lab","anomaly_lab"],room.get("id","")=="crew_hab")
		draw_target.draw_set_transform(Vector2.ZERO)

func _uses_layered_art(room: Dictionary) -> bool:
	if room.get("id","")=="airlock": return true
	return room.get("id", "") in ["construction_drone_bay", "mycelium_nursery", "life_support", "hydroponics_bay", "reactor", "med_bay", "crew_hab", "cryo_chamber", "clone_lab", "data_archive", "biodome", "xeno_lab", "med_office","med_center","holographic_core","bio_lab","anomaly_lab", "battery_array", "research_lab", "maintenance_bay", "storage_bay", "ore_refinery", "mining_drone_bay", "salvage_drone_bay", "crew_lounge", "command_center", "quarantine_cell", "solar_array", "radio_lab", "shield_generator", "tidal_condenser", "gravity_loom", "brine_core", "corridor", "corner", "tee_corridor", "pressure_control", "listening_post", "isolation_vault"]

func _is_narrow_corridor(room: Dictionary) -> bool:
	return room.get("id","") in ["corridor","corner","tee_corridor"]

const DOOR_SHEET_COLUMNS := 4
const DOOR_SHEET_ROWS := 3
const DOOR_OPEN_FRAMES := 10
const DOOR_DRAW_SIZE := Vector2(0.225, 0.162)
const DOOR_UNDERLAY_FRACTION := 0.28
const ROOM_TEXTURE_OVERDRAW := 0.012
const ROOM_SOURCE_MARGIN := 8

const CrewSpritePlayer = preload("res://scripts/crew_sprite_player.gd")
var veld_player = CrewSpritePlayer.new()
var branforth_player = CrewSpritePlayer.new()

var human_sprite: Texture2D
var door_texture: Texture2D
var layered_door_texture: Texture2D
const DepartmentDoor = preload("res://rooms/doors/department_door.gd")
var department_door_materials := {}
var space_background_texture: Texture2D
var human_sprites := {}
var human_animations := {}
var human_equipment_frames: Dictionary = {}
var human_animation_timing := {}
var human_animation_key := ""
var human_animation_started := 0.0
var human_animation_last_time := -1.0
var human_animation_phase := 0.0
var human_animation_last_position := Vector2.ZERO
var human_stride_distance := {}
var drone_sprites := {}
var drone_animations := {}
var brine_core_overlays := {}
var room_textures := {}
var room_texture_variants := {}
var texture_source_regions := {}
var star_points: Array[Dictionary] = []
var room_texture_paths := {
	"airlock": "res://rooms/decoration-integration/airlock.png",
	"anomaly_lab": "res://rooms/decoration-integration/anomaly_lab.png",
	"battery_array": "res://rooms/decoration-integration/battery_array.png",
	"bio_lab": "res://rooms/decoration-integration/bio_lab.png",
	"biodome": "res://rooms/decoration-integration/biodome.png",
	"brine_core": "res://rooms/decoration-integration/brine_core.png",
	"clone_lab": "res://rooms/decoration-integration/clone_lab.png",
	"command_center": "res://rooms/decoration-integration/command_center.png",
	"construction_drone_bay": "res://rooms/decoration-integration/construction_drone_bay.png",
	"corner": "res://rooms/decoration-integration/corner.png",
	"corridor": "res://rooms/decoration-integration/corridor.png",
	"crew_hab": "res://rooms/decoration-integration/crew_hab.png",
	"crew_lounge": "res://rooms/decoration-integration/crew_lounge.png",
	"cryo_chamber": "res://rooms/decoration-integration/cryo_chamber.png",
	"data_archive": "res://rooms/decoration-integration/data_archive.png",
	"gravity_loom": "res://rooms/decoration-integration/gravity_loom.png",
	"holographic_core": "res://rooms/decoration-integration/holographic_core.png",
	"hydroponics_bay": "res://rooms/decoration-integration/hydroponics_bay.png",
	"isolation_vault": "res://rooms/decoration-integration/isolation_vault.png",
	"life_support": "res://rooms/decoration-integration/life_support.png",
	"listening_post": "res://rooms/decoration-integration/listening_post.png",
	"maintenance_bay": "res://rooms/decoration-integration/maintenance_bay.png",
	"med_bay": "res://rooms/decoration-integration/med_bay.png",
	"med_center": "res://rooms/decoration-integration/med_center.png",
	"med_office": "res://rooms/decoration-integration/med_office.png",
	"mining_drone_bay": "res://rooms/decoration-integration/mining_drone_bay.png",
	"mycelium_nursery": "res://rooms/decoration-integration/mycelium_nursery.png",
	"ore_refinery": "res://rooms/decoration-integration/ore_refinery.png",
	"pressure_control": "res://rooms/decoration-integration/pressure_control.png",
	"quarantine_cell": "res://rooms/decoration-integration/quarantine_cell.png",
	"radio_lab": "res://rooms/decoration-integration/radio_lab.png",
	"reactor": "res://rooms/decoration-integration/reactor.png",
	"research_lab": "res://rooms/decoration-integration/research_lab.png",
	"salvage_drone_bay": "res://rooms/decoration-integration/salvage_drone_bay.png",
	"shield_generator": "res://rooms/decoration-integration/shield_generator.png",
	"solar_array": "res://rooms/decoration-integration/solar_array.png",
	"storage_bay": "res://rooms/decoration-integration/storage_bay.png",
	"tee_corridor": "res://rooms/decoration-integration/tee_corridor.png",
	"tidal_condenser": "res://rooms/decoration-integration/tidal_condenser.png",
	"xeno_lab": "res://rooms/decoration-integration/xeno_lab.png"
}
var room_texture_variant_paths := {
	"airlock": ["res://rooms/decoration-integration/airlock.png"],
	"anomaly_lab": ["res://rooms/decoration-integration/anomaly_lab.png"],
	"battery_array": ["res://rooms/decoration-integration/battery_array.png"],
	"bio_lab": ["res://rooms/decoration-integration/bio_lab.png"],
	"biodome": ["res://rooms/decoration-integration/biodome.png"],
	"brine_core": ["res://rooms/decoration-integration/brine_core.png"],
	"clone_lab": ["res://rooms/decoration-integration/clone_lab.png"],
	"command_center": ["res://rooms/decoration-integration/command_center.png"],
	"construction_drone_bay": ["res://rooms/decoration-integration/construction_drone_bay.png"],
	"corner": ["res://rooms/decoration-integration/corner-0.png", "res://rooms/decoration-integration/corner-1.png", "res://rooms/decoration-integration/corner-2.png"],
	"corridor": ["res://rooms/decoration-integration/corridor-0.png", "res://rooms/decoration-integration/corridor-1.png", "res://rooms/decoration-integration/corridor-2.png"],
	"crew_hab": ["res://rooms/decoration-integration/crew_hab.png"],
	"crew_lounge": ["res://rooms/decoration-integration/crew_lounge.png"],
	"cryo_chamber": ["res://rooms/decoration-integration/cryo_chamber.png"],
	"data_archive": ["res://rooms/decoration-integration/data_archive.png"],
	"gravity_loom": ["res://rooms/decoration-integration/gravity_loom.png"],
	"holographic_core": ["res://rooms/decoration-integration/holographic_core.png"],
	"hydroponics_bay": ["res://rooms/decoration-integration/hydroponics_bay.png"],
	"isolation_vault": ["res://rooms/decoration-integration/isolation_vault.png"],
	"life_support": ["res://rooms/decoration-integration/life_support.png"],
	"listening_post": ["res://rooms/decoration-integration/listening_post.png"],
	"maintenance_bay": ["res://rooms/decoration-integration/maintenance_bay.png"],
	"med_bay": ["res://rooms/decoration-integration/med_bay.png"],
	"med_center": ["res://rooms/decoration-integration/med_center.png"],
	"med_office": ["res://rooms/decoration-integration/med_office.png"],
	"mining_drone_bay": ["res://rooms/decoration-integration/mining_drone_bay.png"],
	"mycelium_nursery": ["res://rooms/decoration-integration/mycelium_nursery.png"],
	"ore_refinery": ["res://rooms/decoration-integration/ore_refinery.png"],
	"pressure_control": ["res://rooms/decoration-integration/pressure_control.png"],
	"quarantine_cell": ["res://rooms/decoration-integration/quarantine_cell.png"],
	"radio_lab": ["res://rooms/decoration-integration/radio_lab.png"],
	"reactor": ["res://rooms/decoration-integration/reactor.png"],
	"research_lab": ["res://rooms/decoration-integration/research_lab.png"],
	"salvage_drone_bay": ["res://rooms/decoration-integration/salvage_drone_bay.png"],
	"shield_generator": ["res://rooms/decoration-integration/shield_generator.png"],
	"solar_array": ["res://rooms/decoration-integration/solar_array.png"],
	"storage_bay": ["res://rooms/decoration-integration/storage_bay.png"],
	"tee_corridor": ["res://rooms/decoration-integration/tee_corridor-0.png", "res://rooms/decoration-integration/tee_corridor-1.png", "res://rooms/decoration-integration/tee_corridor-2.png"],
	"tidal_condenser": ["res://rooms/decoration-integration/tidal_condenser.png"],
	"xeno_lab": ["res://rooms/decoration-integration/xeno_lab.png"]
}

func _ready() -> void:
	draw_target = self
	for id in range(Surface.size()):
		var layer := SurfacePass.new()
		layer.host = self
		layer.pass_id = id
		layer.name = ["Floors","Walls","RearDoors","LiveContents","FrontDoors","Lights","Foreground"][id]
		add_child(layer)
		surface_passes.append(layer)
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	nursery_view = NurseryView.new()
	nursery_view.embedded = true
	nursery_view.hide()
	add_child(nursery_view)
	life_support_view = LifeSupportView.new()
	life_support_view.embedded = true
	life_support_view.hide()
	add_child(life_support_view)
	hydroponics_view = HydroponicsView.new()
	hydroponics_view.embedded = true
	hydroponics_view.hide()
	add_child(hydroponics_view)
	reactor_view = ReactorView.new()
	reactor_view.embedded = true
	reactor_view.hide()
	add_child(reactor_view)
	med_bay_view = MedBayView.new()
	med_bay_view.embedded = true
	med_bay_view.hide()
	add_child(med_bay_view)
	crew_hab_view=CrewHabView.new()
	crew_hab_view.embedded=true
	crew_hab_view.hide()
	add_child(crew_hab_view)
	cryo_view=CryoView.new()
	cryo_view.embedded=true
	cryo_view.hide()
	add_child(cryo_view)
	clone_view=CloneView.new()
	clone_view.embedded=true
	clone_view.hide()
	add_child(clone_view)
	archive_view=ArchiveView.new()
	archive_view.embedded=true
	archive_view.hide()
	add_child(archive_view)
	biodome_view=BiodomeView.new()
	biodome_view.embedded=true
	biodome_view.hide()
	add_child(biodome_view)
	xeno_view=XenoView.new()
	xeno_view.embedded=true
	xeno_view.hide()
	add_child(xeno_view)
	anomaly_view=AnomalyView.new()
	anomaly_view.embedded=true
	anomaly_view.hide()
	add_child(anomaly_view)
	bio_view=BioView.new()
	bio_view.embedded=true
	bio_view.hide()
	add_child(bio_view)
	holo_view=HoloView.new()
	holo_view.embedded=true
	holo_view.hide()
	add_child(holo_view)
	med_center_view=MedCenterView.new()
	med_center_view.embedded=true
	med_center_view.hide()
	add_child(med_center_view)
	med_office_view=MedOfficeView.new()
	med_office_view.embedded=true
	med_office_view.hide()
	add_child(med_office_view)
	tidal_view=TidalView.new()
	tidal_view.embedded=true
	tidal_view.hide()
	add_child(tidal_view)
	gravity_view=GravityView.new()
	gravity_view.embedded=true
	gravity_view.hide()
	add_child(gravity_view)
	brine_view=BrineView.new()
	rare_room_views["pressure_control"]=preload("res://rooms/underwater/rare-dead-ends/pressure_control_view.gd").new()
	rare_room_views["pressure_control"].embedded=true
	rare_room_views["pressure_control"].hide()
	add_child(rare_room_views["pressure_control"])
	rare_room_views["listening_post"]=preload("res://rooms/underwater/rare-dead-ends/listening_post_view.gd").new()
	rare_room_views["listening_post"].embedded=true
	rare_room_views["listening_post"].hide()
	add_child(rare_room_views["listening_post"])
	rare_room_views["isolation_vault"]=preload("res://rooms/underwater/rare-dead-ends/isolation_vault_view.gd").new()
	rare_room_views["isolation_vault"].embedded=true
	rare_room_views["isolation_vault"].hide()
	add_child(rare_room_views["isolation_vault"])
	airlock_view=AirlockView.new()
	airlock_view.embedded=true
	airlock_view.hide()
	add_child(airlock_view)
	brine_view.embedded=true
	brine_view.hide()
	add_child(brine_view)
	hull_view=HullView.new()
	hull_view.embedded=true
	hull_view.hide()
	add_child(hull_view)
	acoustic_view=AcousticView.new()
	acoustic_view.embedded=true
	acoustic_view.hide()
	add_child(acoustic_view)
	thermal_view=ThermalView.new()
	thermal_view.embedded=true
	thermal_view.hide()
	add_child(thermal_view)
	battery_view=BatteryView.new()
	battery_view.embedded=true
	battery_view.hide()
	add_child(battery_view)
	research_view=ResearchView.new()
	research_view.embedded=true
	research_view.hide()
	add_child(research_view)
	maintenance_view=MaintenanceView.new()
	maintenance_view.embedded=true
	maintenance_view.hide()
	add_child(maintenance_view)
	storage_view=StorageView.new()
	storage_view.embedded=true
	storage_view.hide()
	add_child(storage_view)
	refinery_view=RefineryView.new()
	refinery_view.embedded=true
	refinery_view.hide()
	add_child(refinery_view)
	mining_view=MiningView.new()
	mining_view.embedded=true
	mining_view.hide()
	add_child(mining_view)
	construction_view=ConstructionView.new()
	construction_view.embedded=true
	construction_view.hide()
	add_child(construction_view)
	salvage_view=SalvageView.new()
	salvage_view.embedded=true
	salvage_view.hide()
	add_child(salvage_view)
	lounge_view=LoungeView.new()
	lounge_view.embedded=true
	lounge_view.hide()
	add_child(lounge_view)
	command_view=CommandView.new()
	command_view.embedded=true
	command_view.hide()
	add_child(command_view)
	quarantine_view=QuarantineView.new()
	quarantine_view.embedded=true
	quarantine_view.hide()
	add_child(quarantine_view)
	_generate_star_points()
	space_background_texture = _load_png_texture("res://space texture.jpg")
	door_texture = _load_png_texture("res://dooranimated.png")
	var department_source := _load_png_texture(DepartmentDoor.SOURCE)
	if department_source != null:
		department_door_materials = DepartmentDoor.make_materials(self,department_source)
	if door_texture != null:
		layered_door_texture = AnimatedDoorAtlas.create_station_finish(self, door_texture)
	for id in room_texture_paths:
		var texture := _load_png_texture(room_texture_paths[id])
		if texture != null:
			room_textures[id] = texture
	for id in room_texture_variant_paths:
		var textures: Array[Texture2D] = []
		for path_value in room_texture_variant_paths[id]:
			var texture: Texture2D = _load_png_texture(str(path_value))
			if texture != null:
				textures.append(texture)
		if not textures.is_empty():
			room_texture_variants[id] = textures
	veld_player.load_manifest("res://character/dr-veld-v1/final/manifest.json")
	branforth_player.load_manifest("res://character/chief-engineer-branforth-v1/final/manifest.json")
	veld_player.load_manifest("res://character/crew-underwater-v1/pilot/veld-death-ground-east/manifest.json", true)
	branforth_player.load_manifest("res://character/crew-underwater-v1/pilot/branforth-death-ground-east/manifest.json", true)
	_load_water_pilots(veld_player, "veld")
	_load_water_pilots(branforth_player, "branforth")
	_load_dry_helmet_pilots(veld_player, "veld")
	_load_dry_helmet_pilots(branforth_player, "branforth")
	_load_helmet_transitions(veld_player, "veld")
	_load_helmet_transitions(branforth_player, "branforth")
	human_sprite = _load_png_texture("res://character/major-bill-v2/rotations/south.png")
	for direction in ["north", "east", "south", "west"]:
		var texture := _load_png_texture("res://character/major-bill-v2/rotations/%s.png" % direction)
		if texture != null:
			texture.set_meta("major_bill_v2", true)
			human_sprites[direction] = texture
	_load_major_bill_animations()
	_load_drone_assets()
	_load_brine_core_overlays()

func _generate_star_points() -> void:
	star_points.clear()
	for i in range(520):
		var point := {
			"x": float((i * 15485863) % 100000) / 100000.0,
			"y": float((i * 32452843) % 100000) / 100000.0,
			"twinkle": float((i * 97) % 100) / 100.0,
			"size": 1.0
		}
		if i % 23 == 0:
			point["size"] = 2.0
		if i % 113 == 0:
			point["size"] = 3.0
		star_points.append(point)

func _load_png_texture(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var resource := ResourceLoader.load(path)
		if resource is Texture2D:
			_cache_texture_source_region(resource)
			return resource
	var image := Image.new()
	var error := image.load(path)
	if error != OK:
		return null
	var texture := ImageTexture.create_from_image(image)
	_cache_texture_source_region(texture, image)
	return texture

func _cache_texture_source_region(texture: Texture2D, image: Image = null) -> void:
	if texture == null:
		return
	var source_image := image
	if source_image == null:
		source_image = texture.get_image()
	if source_image == null:
		return
	texture_source_regions[texture.get_instance_id()] = _find_content_region(source_image)

func _find_content_region(image: Image) -> Rect2:
	var width := image.get_width()
	var height := image.get_height()
	var min_x := width
	var min_y := height
	var max_x := -1
	var max_y := -1
	for y in range(0, height, 2):
		for x in range(0, width, 2):
			var pixel := image.get_pixel(x, y)
			var is_visible_pixel := pixel.a > 0.04 and maxf(maxf(pixel.r, pixel.g), pixel.b) > 0.018
			if is_visible_pixel:
				min_x = mini(min_x, x)
				min_y = mini(min_y, y)
				max_x = maxi(max_x, x)
				max_y = maxi(max_y, y)
	if max_x < min_x or max_y < min_y:
		return Rect2(Vector2.ZERO, Vector2(width, height))
	min_x = maxi(min_x - ROOM_SOURCE_MARGIN, 0)
	min_y = maxi(min_y - ROOM_SOURCE_MARGIN, 0)
	max_x = mini(max_x + ROOM_SOURCE_MARGIN, width - 1)
	max_y = mini(max_y + ROOM_SOURCE_MARGIN, height - 1)
	return Rect2(Vector2(min_x, min_y), Vector2(max_x - min_x + 1, max_y - min_y + 1))

func _load_human_animation(state: String, base_path: String) -> void:
	var by_direction := {}
	for direction in ["north", "east", "south", "west"]:
		var frames := []
		var dir := DirAccess.open("%s/%s" % [base_path, direction])
		if dir == null:
			continue
		dir.list_dir_begin()
		var file_name := dir.get_next()
		while not file_name.is_empty():
			if not dir.current_is_dir() and file_name.ends_with(".png"):
				frames.append("%s/%s/%s" % [base_path, direction, file_name])
			file_name = dir.get_next()
		dir.list_dir_end()
		frames.sort()
		var textures := []
		for frame_path in frames:
			var texture := _load_png_texture(frame_path)
			if texture != null:
				textures.append(texture)
		if not textures.is_empty():
			by_direction[direction] = textures
	human_animations[state] = by_direction

func _load_major_bill_animations() -> void:
	var base := "res://character/major-bill-v2/final/"
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(base + "manifest.json"))
	human_animations.clear()
	human_animation_timing.clear()
	human_stride_distance = manifest.get("strideDistanceCells", {"walk": 0.12, "run": 0.168})
	for entry: Dictionary in manifest.states:
		var key := str(entry.id)
		var separator := key.find("-")
		var state := key.substr(0, separator)
		var direction := key.substr(separator + 1)
		var textures: Array = []
		for frame_path: String in entry.frameFiles:
			var texture := _load_png_texture((base + frame_path).simplify_path())
			if texture == null:
				push_error("Missing Major Bill frame: " + frame_path)
				continue
			texture.set_meta("major_bill_v2", true)
			textures.append(texture)
		if not human_animations.has(state): human_animations[state] = {}
		human_animations[state][direction] = textures
		human_animation_timing[key] = {"durations": entry.frameDurationsMs, "loop": entry.loop}
	human_animation_key = ""
	human_animation_last_time = -1.0
	var death_pack = CrewSpritePlayer.new()
	death_pack.load_manifest("res://character/crew-underwater-v1/pilot/bill-death-ground-east/manifest.json")
	for texture in death_pack.frames["death-ground-east"]: texture.set_meta("major_bill_v2", true)
	human_animations["death-ground"] = {"east": death_pack.frames["death-ground-east"]}
	human_animation_timing["death-ground-east"] = death_pack.timing["death-ground-east"]
	var water_pack = CrewSpritePlayer.new()
	_load_water_pilots(water_pack, "bill")
	_load_helmet_transitions(water_pack, "bill")
	human_equipment_frames = water_pack.equipment_frames
	var dry_pack = CrewSpritePlayer.new()
	dry_pack.load_manifest("res://character/major-bill-v2/final/manifest.json")
	dry_pack.load_manifest("res://character/crew-underwater-v1/pilot/bill-death-ground-east/manifest.json", true)
	_load_dry_helmet_pilots(dry_pack, "bill")
	for equipment_id in dry_pack.equipment_frames:
		if not human_equipment_frames.has(equipment_id): human_equipment_frames[equipment_id] = {}
		human_equipment_frames[equipment_id].merge(dry_pack.equipment_frames[equipment_id], true)
	for equipment in human_equipment_frames.values():
		for equipped_frames in equipment.values():
			for texture in equipped_frames: texture.set_meta("major_bill_v2", true)
	human_stride_distance.merge(water_pack.strides, true)
	for key in water_pack.frames:
		var split: int = key.rfind("-")
		var state: String = key.substr(0, split)
		var direction: String = key.substr(split + 1)
		if not human_animations.has(state): human_animations[state] = {}
		for texture in water_pack.frames[key]: texture.set_meta("major_bill_v2", true)
		human_animations[state][direction] = water_pack.frames[key]
		human_animation_timing[key] = water_pack.timing[key]

func _load_helmet_transitions(player, actor: String) -> void:
	for action in ["equip-helmet", "remove-helmet"]:
		player.load_manifest("res://character/crew-underwater-v1/locker/%s-%s-east/manifest.json" % [actor, action], true)

func _load_dry_helmet_pilots(player, actor: String) -> void:
	var death_path := "res://character/crew-underwater-v1/equipment/fitting/%s-death-ground-east/manifest.json" % actor
	if FileAccess.file_exists(death_path): player.load_equipment_manifest("diving-helmet", death_path)
	for state in ["idle", "walk", "run", "interact", "kneel", "repair", "stand"]:
		for direction in ["south", "north", "east", "west"]:
			var path := "res://character/crew-underwater-v1/equipment/dry/%s-%s-%s/manifest.json" % [actor, state, direction]
			if FileAccess.file_exists(path): player.load_equipment_manifest("diving-helmet", path)

func _load_water_pilots(player, actor: String) -> void:
	for clip in ["swim-east", "swim-south", "swim-north", "swim-west", "tread-south", "tread-east", "tread-north", "tread-west", "death-water-east"]:
		var path := "res://character/crew-underwater-v1/pilot/%s-%s/manifest.json" % [actor, clip]
		if FileAccess.file_exists(path):
			player.load_manifest(path, true)
			var fitted := "res://character/crew-underwater-v1/equipment/fitting/%s-%s/manifest.json" % [actor, clip]
			if FileAccess.file_exists(fitted): player.load_equipment_manifest("diving-helmet", fitted)
	# Revised arm strokes retain the shoulder pivot but allow a wider forward reach.
	for direction in ["east", "west", "south", "north"]:
		if direction == "north" and actor == "veld": continue
		var version := "v3" if actor == "branforth" and direction == "north" else "v2"
		var revision := "res://character/crew-underwater-v1/revisions/%s-swim-%s-%s/" % [actor, direction, version]
		player.load_manifest(revision + "manifest.json", true)
		player.load_equipment_manifest("diving-helmet", revision + "helmet/manifest.json")

	if actor == "veld":
		var tread_revision := "res://character/crew-underwater-v1/revisions/veld-tread-south-v2/"
		player.load_manifest(tread_revision + "manifest.json", true)
		player.load_equipment_manifest("diving-helmet", tread_revision + "helmet/manifest.json")

func _human_frame_index(key: String, elapsed: float) -> int:
	var timing: Dictionary = human_animation_timing[key]
	var durations: Array = timing.durations
	var total := 0.0
	for duration in durations: total += float(duration)
	var cursor := maxf(0.0, elapsed * 1000.0)
	if timing.loop:
		cursor = fmod(cursor, total)
	elif cursor >= total:
		return durations.size() - 1
	for index in range(durations.size()):
		if cursor < float(durations[index]): return index
		cursor -= float(durations[index])
	return durations.size() - 1

func _advance_human_animation(key: String, time_seconds: float, position_cells: Vector2) -> float:
	var distance := position_cells.distance_to(human_animation_last_position)
	var turning_state := key.get_slice("-", 0)
	if key != human_animation_key and human_animation_key.get_slice("-", 0) == turning_state and human_stride_distance.has(turning_state) and human_animation_timing.has(human_animation_key) and human_animation_timing[human_animation_key].loop and human_animation_timing[key].loop and time_seconds >= human_animation_last_time and distance <= 0.5:
		var old_cycle := 0.0
		var new_cycle := 0.0
		for duration in human_animation_timing[human_animation_key].durations: old_cycle += float(duration) / 1000.0
		for duration in human_animation_timing[key].durations: new_cycle += float(duration) / 1000.0
		human_animation_phase = fmod(human_animation_phase, old_cycle) / old_cycle * new_cycle
		human_animation_key = key
	var reset := key != human_animation_key or time_seconds < human_animation_last_time
	if reset or distance > 0.5:
		human_animation_key = key
		human_animation_started = time_seconds
		human_animation_phase = 0.0
	elif time_seconds > human_animation_last_time:
		var state := key.get_slice("-", 0)
		if human_stride_distance.has(state):
			# Positions are measured in cells, so camera zoom cannot change cadence.
			# Sampling the same position twice never advances the gait twice.
			var cycle_seconds := 0.0
			for duration in human_animation_timing[key].durations:
				cycle_seconds += float(duration) / 1000.0
			human_animation_phase += distance / float(human_stride_distance[state]) * cycle_seconds
		else:
			human_animation_phase = time_seconds - human_animation_started
	human_animation_last_time = time_seconds
	human_animation_last_position = position_cells
	return human_animation_phase

func _load_drone_assets() -> void:
	var directions := ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]
	for direction in directions:
		var texture: Texture2D = _load_png_texture("res://mining-drone-animation/rotations/%s.png" % direction)
		if texture != null:
			drone_sprites[direction] = texture
	_load_drone_animation("fly", "res://mining-drone-animation/animations/2._Flying_Moving_The_drone_tilts_slightly_forward-30d7af04", directions)
	_load_drone_animation("mine", "res://mining-drone-animation/animations/3._Mining_The_drone_stops_in_place_and_extends_its-32d99183", directions)
	_load_drone_animation("idle", "res://mining-drone-animation/animations/Idle_Hover_The_drone_floats_in_place_with_a_slow_m-0332a189", directions)

func _load_drone_animation(state: String, base_path: String, directions: Array) -> void:
	var by_direction := {}
	for direction_value in directions:
		var direction := str(direction_value)
		var direction_dir := _find_direction_animation_dir(base_path, direction)
		if direction_dir.is_empty():
			continue
		var frames: Array[String] = []
		var dir := DirAccess.open(direction_dir)
		if dir == null:
			continue
		dir.list_dir_begin()
		var file_name := dir.get_next()
		while not file_name.is_empty():
			if not dir.current_is_dir() and file_name.ends_with(".png"):
				frames.append("%s/%s" % [direction_dir, file_name])
			file_name = dir.get_next()
		dir.list_dir_end()
		frames.sort()
		var textures: Array[Texture2D] = []
		for frame_path in frames:
			var texture: Texture2D = _load_png_texture(frame_path)
			if texture != null:
				textures.append(texture)
		if not textures.is_empty():
			by_direction[direction] = textures
	drone_animations[state] = by_direction

func _find_direction_animation_dir(base_path: String, direction: String) -> String:
	var exact_path := "%s/%s" % [base_path, direction]
	if DirAccess.dir_exists_absolute(exact_path):
		return exact_path
	var dir := DirAccess.open(base_path)
	if dir == null:
		return ""
	dir.list_dir_begin()
	var file_name := dir.get_next()
	while not file_name.is_empty():
		if dir.current_is_dir() and file_name.begins_with(direction):
			dir.list_dir_end()
			return "%s/%s" % [base_path, file_name]
		file_name = dir.get_next()
	dir.list_dir_end()
	return ""

func _load_brine_core_overlays() -> void:
	var overlay_paths := {
		"body": "res://brinecore-animation/assets/brine_body_temp.png",
		"bubble": "res://brinecore-animation/assets/bubble_particle.png",
		"console": "res://brinecore-animation/assets/console_flicker_spritesheet_temp.png",
		"glass": "res://brinecore-animation/assets/tank_glass_overlay_temp.png",
		"glow": "res://brinecore-animation/assets/tank_glow_overlay.png"
	}
	for id in overlay_paths:
		var texture: Texture2D = _load_png_texture(str(overlay_paths[id]))
		if texture != null:
			brine_core_overlays[id] = texture

const GRID_SIZE := 40
const CELL_SIZE := 720
const GRID_PIXEL_SIZE := GRID_SIZE * CELL_SIZE

func _gui_input(event: InputEvent) -> void:
	var main = _get_main()
	if main._gameplay_input_blocked():
		accept_event()
		return
	if event is InputEventMouseButton and event.pressed and event.shift_pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			main._set_grid_zoom(main.grid_zoom + preload("res://scripts/title_settings.gd").zoom_step())
			accept_event()
			return
		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			main._set_grid_zoom(main.grid_zoom - preload("res://scripts/title_settings.gd").zoom_step())
			accept_event()
			return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var cell_size := _cell_size()
		var cell := Vector2i(floori(event.position.x / cell_size), floori(event.position.y / cell_size))
		cell_clicked.emit(cell)
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_RIGHT:
		var cell_size := _cell_size()
		var cell := Vector2i(floori(event.position.x / cell_size), floori(event.position.y / cell_size))
		cell_secondary_clicked.emit(cell)
	if event is InputEventMouseMotion:
		var cell_size := _cell_size()
		var cell := Vector2i(floori(event.position.x / cell_size), floori(event.position.y / cell_size))
		cell_hovered.emit(cell)

var last_content_viewport := Rect2()

func _process(_delta: float) -> void:
	var main = _get_main()
	var viewport_region := Rect2(Vector2(main.grid_scroll.scroll_horizontal,main.grid_scroll.scroll_vertical),main.grid_scroll.size)
	if viewport_region != last_content_viewport:
		last_content_viewport = viewport_region
		queue_redraw()
	_advance_room_lights(_delta)
	if not main.paused or (not main.selected_card_id.is_empty() and not main._gameplay_input_blocked()):
		queue_redraw()


enum Surface { FLOOR, WALL, REAR_DOORS, LIVE, FRONT_DOORS, LIGHTS, FOREGROUND }
const RoomContents = preload("res://scripts/room_content_canvas.gd")
var retain_room_contents := not OS.get_cmdline_user_args().has("--redraw-room-contents")
var content_canvases := {}

class SurfacePass extends Node2D:
	var host
	var pass_id := 0
	func _draw() -> void:
		host._draw_surface(self,pass_id)

var draw_target: CanvasItem
var surface_passes: Array = []
var surface_key: Array = []
var retain_static_surfaces := not OS.get_cmdline_user_args().has("--redraw-static-surfaces")
var floor_rebuilds := 0
var wall_rebuilds := 0
var retain_doors_lights := not OS.get_cmdline_user_args().has("--redraw-doors-lights")
var door_surface_key: Array = []
var light_surface_key: Array = []
var door_rebuilds := 0
var light_rebuilds := 0

func _door_light_state() -> void:
	if not retain_doors_lights:
		for id in [Surface.REAR_DOORS,Surface.FRONT_DOORS,Surface.LIGHTS]: surface_passes[id].queue_redraw()
		return
	var main = _get_main()
	var size := _cell_size()
	var doors: Array = [size,side_open_door_prototype,department_door_materials]
	var lights: Array = [size]
	for room in visible_draw_rooms:
		lights.append([room.pos,room.id,_room_light_level(room)])
		for side in ["north","east","south","west"]:
			var offset := _offset_from_side(side)
			var neighbor: Vector2i = room.pos+offset
			var connected := _door_has_connected_neighbor(main,room,neighbor,offset)
			if connected and side in ["north","west"]: continue
			var outside_frame := _drone_door_frame(main,room.pos,neighbor)
			if not connected and (main.occupied.has(neighbor) or side not in main.get_room_doors(room) or outside_frame==0): continue
			var other: Dictionary = main.occupied.get(neighbor,room)
			if not _uses_layered_art(room) and not _uses_layered_art(other): continue
			var frame := _door_frame_for_pair(main,room.pos,neighbor) if connected else outside_frame
			var center := _door_edge_center(room.pos,side,size)
			var foot_y: float = _nearest_crew_foot(main,center).y
			var variant := DepartmentDoor.pair_variant(room,other)
			var narrow := _is_narrow_corridor(room) or _is_narrow_corridor(other)
			var depth_mask := 0
			var parts := _department_parts(frame,side in ["east","west"],variant,narrow,side_open_door_prototype and side=="east")
			for i in range(parts.size()):
				if parts[i].floor or foot_y>center.y+float(parts[i].depth)*size/384.0: depth_mask |= 1<<i
			doors.append([room.pos,side,frame,variant,narrow,minf(_room_light_level(room),_room_light_level(other)),depth_mask])
	var enabled := retain_doors_lights and not department_door_materials.is_empty()
	if not enabled or doors != door_surface_key:
		door_surface_key = doors.duplicate(true)
		surface_passes[Surface.REAR_DOORS].queue_redraw()
		surface_passes[Surface.FRONT_DOORS].queue_redraw()
	if not retain_doors_lights or lights != light_surface_key:
		light_surface_key = lights.duplicate(true)
		surface_passes[Surface.LIGHTS].queue_redraw()


func _surface_state() -> Array:
	var main = _get_main()
	var rooms: Array = []
	for room in visible_draw_rooms:
		var ports: Array = []
		for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
			ports.append(_drone_door_frame(main,room.pos,room.pos+offset)>0)
		var ward: Dictionary = main.wrecks.get(room.pos,{})
		rooms.append([room.pos,ports,_room_light_level(room),ward.get("cleared",false),ward.get("kind",""),ward.is_empty(),ward.get("pods",[]).size()])
	# Deep snapshot of structural state; clocks/actors stay on the live pass.
	# Light fades rebuild surfaces to preserve per-room pool/seam draw ordering.
	# Non-layered legacy rooms have no static contract, so keep their floor pass live.
	var legacy_clock := 0.0
	for room in visible_draw_rooms:
		if not _uses_layered_art(room): legacy_clock = main.visual_time_seconds
	return [_cell_size(),main.placed_rooms,main.powered_room_cells,rooms,
		preload("res://scripts/title_settings.gd").raised_walls,main.selected_room_cell,main.architect_run.get("core",{}).is_empty(),legacy_clock]

var visible_draw_rooms: Array = []
var cull_room_drawing := not OS.get_cmdline_user_args().has("--draw-all-rooms")
var profile_draw := false
var draw_profile_usec: Dictionary = {}
var draw_profile_totals_usec: Dictionary = {}

func _profile_draw_stage(label: String, started: int) -> int:
	if not profile_draw: return 0
	var now := Time.get_ticks_usec()
	draw_profile_usec[label] = now - started
	draw_profile_totals_usec[label] = int(draw_profile_totals_usec.get(label,0)) + now - started
	return now

func _draw() -> void:
	draw_target = self
	if profile_draw: draw_profile_usec.clear()
	var stage_time: int = Time.get_ticks_usec() if profile_draw else 0
	var main = _get_main()
	var cell_size := _cell_size()
	var grid_pixel_size := GRID_SIZE * cell_size
	visible_draw_rooms = main.placed_rooms
	if cull_room_drawing:
		visible_draw_rooms = []
		var region := Rect2(Vector2(main.grid_scroll.scroll_horizontal, main.grid_scroll.scroll_vertical), main.grid_scroll.size).grow(cell_size)
		for room in main.placed_rooms:
			if region.intersects(Rect2(Vector2(room.pos)*cell_size,Vector2.ONE*cell_size)):
				visible_draw_rooms.append(room)
	_draw_space_background(grid_pixel_size)
	_draw_stars()
	rock_view.draw_into(draw_target,main.wrecks,cell_size,main.visual_time_seconds,main.selected_room_cell,false)
	wreck_view.draw_into(draw_target,main.wrecks,cell_size,main.visual_time_seconds,main.selected_room_cell,false)
	_draw_cryo_derelicts(main,cell_size)
	harvest_site_art.draw_into(draw_target,main.drone_fleet.sites,main.occupied,cell_size,main.selected_room_cell)
	stage_time = _profile_draw_stage("environment", stage_time)
	if main.admin_mode:
		for x in range(GRID_SIZE + 1):
			var c := Color(0.18, 0.28, 0.34, 0.42)
			draw_target.draw_line(Vector2(x * cell_size, 0), Vector2(x * cell_size, grid_pixel_size), c)
			draw_target.draw_line(Vector2(0, x * cell_size), Vector2(grid_pixel_size, x * cell_size), c)
	if not retain_static_surfaces:
		for layer in surface_passes: layer.hide()
		surface_key = []
		door_surface_key = []
		light_surface_key = []
		_paint_surface(Surface.FLOOR)
		_paint_surface(Surface.WALL)
		_paint_surface(Surface.LIVE)
		return
	for layer in surface_passes: layer.show()
	var checked := Time.get_ticks_usec() if profile_draw else 0
	var next_key := _surface_state()
	if next_key != surface_key:
		surface_key = next_key.duplicate(true)
		surface_passes[Surface.FLOOR].queue_redraw()
		surface_passes[Surface.WALL].queue_redraw()
	if profile_draw: _profile_draw_stage("surface_validation",checked)
	checked = Time.get_ticks_usec() if profile_draw else 0
	_door_light_state()
	if profile_draw: _profile_draw_stage("door_light_validation",checked)
	surface_passes[Surface.LIVE].queue_redraw()
	surface_passes[Surface.FOREGROUND].queue_redraw()

func _draw_surface(target: CanvasItem, pass_id: int) -> void:
	draw_target = target
	_paint_surface(pass_id)
	draw_target = self

func _paint_surface(pass_id: int) -> void:
	var main = _get_main()
	var cell_size := _cell_size()
	var stage_time: int = Time.get_ticks_usec() if profile_draw else 0
	if pass_id == Surface.FLOOR:
		for room in visible_draw_rooms:
			_draw_connectors(room, main.occupied)
		for room in visible_draw_rooms:
			if not _uses_layered_art(room):
				_draw_room(room)
		for room in visible_draw_rooms:
			if _uses_layered_art(room):
				var room_rect := Rect2(Vector2(room.pos) * cell_size, Vector2.ONE * cell_size)
				_draw_nursery(room, room_rect, false, true)
		if profile_draw: _profile_draw_stage("floors",stage_time)
		floor_rebuilds += 1
		return
	if pass_id == Surface.WALL:
		# Floors precede every modular wall, so a neighbor cannot erase half a seam.
		# Finish the shell before assembling doors; jambs must cover wall ends.
		for room in visible_draw_rooms:
			if _uses_layered_art(room):
				_draw_nursery(room, Rect2(Vector2(room.pos)*cell_size, Vector2.ONE*cell_size), false, false, true)
		for room in visible_draw_rooms:
			if preload("res://scripts/title_settings.gd").raised_walls and _uses_layered_art(room) and not _is_narrow_corridor(room) and not main.occupied.has(room.pos+Vector2i.UP):
				draw_target.draw_set_transform((Vector2(room.pos)+Vector2.ONE*0.5)*cell_size,0,Vector2.ONE*cell_size/384.0)
				preload("res://rooms/whole-room/north_wall.gd").draw_into(draw_target,room.id,room.pos)
				draw_target.draw_set_transform(Vector2.ZERO)
		if profile_draw: _profile_draw_stage("walls",stage_time)
		wall_rebuilds += 1
		return
	if pass_id in [Surface.REAR_DOORS,Surface.FRONT_DOORS]:
		_draw_layered_doors(pass_id == Surface.REAR_DOORS)
		door_rebuilds += 1
		if profile_draw: _profile_draw_stage("rear_doors" if pass_id==Surface.REAR_DOORS else "front_doors",stage_time)
		return
	if pass_id == Surface.LIGHTS:
		_draw_layered_lighting()
		light_rebuilds += 1
		if profile_draw: _profile_draw_stage("lights",stage_time)
		return
	if pass_id == Surface.LIVE:
		var visible_cells := {}
		# A reused cell may now contain a procedural corridor, which never
		# submits prop contents. Do not leave its former room's canvas visible.
		for room in visible_draw_rooms:
			if _uses_layered_art(room) and not _is_narrow_corridor(room):
				visible_cells[room.pos] = true
		for cell in content_canvases.keys():
			if not retain_room_contents or not retain_static_surfaces or not visible_cells.has(cell): content_canvases[cell].hide()
			# A replacement corridor does not submit retained room contents.
			# Release the previous occupant's canvas even when the cell stays occupied.
			if not main.occupied.has(cell) or _is_narrow_corridor(main.occupied[cell]) or not _uses_layered_art(main.occupied[cell]):
				content_canvases[cell].hide()
				content_canvases[cell].queue_free()
				content_canvases.erase(cell)
		if not retain_static_surfaces: _draw_layered_doors(true)
		for room in visible_draw_rooms:
			if _uses_layered_art(room):
				_draw_room(room)
		if profile_draw: _profile_draw_stage("live_rooms",stage_time)
		if retain_static_surfaces: return
	if not retain_static_surfaces:
		_draw_layered_doors(false)
		_draw_layered_lighting()
	stage_time = _profile_draw_stage("room_contents", stage_time)
	_draw_synergy_links(main)
	_draw_discovery_bursts(main)
	if main.occupied.has(main.selected_room_cell):
		var selected: Dictionary = main.occupied[main.selected_room_cell]
		var start: Vector2 = (Vector2(main.selected_room_cell) + Vector2.ONE * 0.5) * cell_size
		for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
			var neighbor_cell: Vector2i = main.selected_room_cell + offset
			if main.occupied.has(neighbor_cell) and main._placed_rooms_connected(selected, main.occupied[neighbor_cell], offset):
				draw_target.draw_line(start, (Vector2(neighbor_cell) + Vector2.ONE * 0.5) * cell_size, Color("91e2dd"), 2.0)
				draw_target.draw_rect(Rect2(Vector2(neighbor_cell) * cell_size, Vector2.ONE * cell_size).grow(-3), Color("91e2dd"), false, 2.0)
	_draw_door_foregrounds(main, true)
	_draw_humans(main)
	_draw_door_foregrounds(main, false)
	_draw_drones(main)
	stage_time = _profile_draw_stage("actors_effects", stage_time)
	if not main.selected_card_id.is_empty():
		var mouse_cell := Vector2i(floori(get_local_mouse_position().x / cell_size), floori(get_local_mouse_position().y / cell_size))
		var valid: bool = main.get_placement_problem(main.selected_card_id, mouse_cell).is_empty()
		_draw_room_hologram(main, mouse_cell, valid)
		if not preload("res://scripts/title_settings.gd").placement_guides: return
		for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
			var neighbor_cell: Vector2i = mouse_cell + offset
			if not main.occupied.has(neighbor_cell):
				continue
			var connects: bool = main._doors_connect(main.selected_card_id, main.selected_rotation, offset, main.occupied[neighbor_cell])
			var midpoint := (Vector2(mouse_cell) + Vector2.ONE * 0.5 + Vector2(offset) * 0.5) * cell_size
			var tangent := Vector2(-offset.y, offset.x) * cell_size * 0.12
			draw_target.draw_line(midpoint - tangent, midpoint + tangent, Color("#9ff3df") if connects else Color("#efb777"), 4.0)
			if not connects:
				draw_target.draw_line(midpoint - Vector2.ONE * 5, midpoint + Vector2.ONE * 5, Color("#efb777"), 2.0)
				draw_target.draw_line(midpoint + Vector2(-5, 5), midpoint + Vector2(5, -5), Color("#efb777"), 2.0)

func _draw_space_background(grid_pixel_size: float) -> void:
	seabed_background.render_into(draw_target, grid_pixel_size / GRID_SIZE, GRID_SIZE, _get_main().get_visual_time_seconds())

func _draw_stars() -> void:
	var grid_pixel_size := GRID_SIZE * _cell_size()
	for i in range(star_points.size()):
		var star: Dictionary = star_points[i]
		var x: float = float(star["x"]) * grid_pixel_size
		var y: float = float(star["y"]) * grid_pixel_size
		var alpha: float = 0.18 + float(star["twinkle"]) * 0.55
		var star_size: float = float(star["size"])
		if star_size >= 2.0:
			alpha = 0.85
		if star_size >= 3.0:
			alpha = 0.95
		var star_color := Color(0.45, 0.65, 0.68, alpha*0.20)
		draw_target.draw_rect(Rect2(Vector2(x, y), Vector2(star_size, star_size)), star_color)
		# Underwater suspended particles: no astronomical cross-shaped glints.

func _draw_room(room: Dictionary) -> void:
	var main = _get_main()
	var pos: Vector2i = room["pos"]
	var cell_size := _cell_size()
	var rect := Rect2(Vector2(pos) * cell_size + Vector2.ONE, Vector2(cell_size - 2, cell_size - 2))
	var color := RoomDatabaseScript.category_color(room["category"])
	var offline: bool = main.unpowered_room_cells.has(pos)
	var room_texture: Texture2D = _get_room_texture(room)
	var layered: bool = _uses_layered_art(room)
	var has_texture: bool = room_texture != null or layered
	if not has_texture:
		var shadow_rect := rect.grow(cell_size * 0.018)
		draw_target.draw_rect(Rect2(shadow_rect.position + Vector2(cell_size * 0.018, cell_size * 0.025), shadow_rect.size), Color(0, 0, 0, 0.34))
	if not has_texture:
		draw_target.draw_rect(rect, Color("#151a1f"))
	if layered:
		_draw_nursery(room, rect)
	elif has_texture:
		var overdraw: float = cell_size * ROOM_TEXTURE_OVERDRAW
		var texture_rect: Rect2 = Rect2(-rect.size * 0.5, rect.size).grow(overdraw)
		var source_rect: Rect2 = texture_source_regions.get(room_texture.get_instance_id(), Rect2(Vector2.ZERO, room_texture.get_size()))
		draw_target.draw_set_transform(rect.get_center(), deg_to_rad(float(int(room.get("rotation", 0)) * 90)), Vector2.ONE)
		draw_target.draw_texture_rect_region(room_texture, texture_rect, source_rect)
		draw_target.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
		if room["id"] == "brine_core":
			_draw_brine_core_overlay(rect)
	else:
		draw_target.draw_rect(rect.grow(-2), color.darkened(0.62) if offline else color.darkened(0.25))
	if offline and not layered:
		draw_target.draw_rect(rect.grow(-1), Color(0.05, 0.02, 0.03, 0.58))
	var border_color := Color("#d34e58") if offline else color.darkened(0.10)
	var border_width := 1.5 if not has_texture or main.admin_mode or offline else 0.0
	if main.selected_room_cell == pos:
		border_color = Color("#4fa38d")
		border_width = 4.0
	elif main.hover_cell == pos:
		border_color = Color("#6ab8a3")
		border_width = 3.0
	if border_width > 0.0:
		draw_target.draw_rect(rect, border_color, false, border_width)
	var center := rect.get_center()
	if offline and main.admin_mode:
		draw_target.draw_line(rect.position + Vector2(4, 4), rect.end - Vector2(4, 4), Color("#ff7580"), 2)
		draw_target.draw_line(Vector2(rect.end.x - 4, rect.position.y + 4), Vector2(rect.position.x + 4, rect.end.y - 4), Color("#ff7580"), 2)
		draw_target.draw_circle(center, 4, Color("#ff2537"))
	elif not offline and not has_texture:
		match room["category"]:
			"Core":
				draw_target.draw_circle(center, 4, Color("#e8feff"))
			"Engineering":
				draw_target.draw_line(center + Vector2(-4, 3), center + Vector2(0, -4), Color.BLACK, 2)
				draw_target.draw_line(center + Vector2(0, -4), center + Vector2(4, 3), Color.BLACK, 2)
			"Science":
				draw_target.draw_circle(center, 3, Color.BLACK)
			"Bio":
				draw_target.draw_line(center + Vector2(0, 4), center + Vector2(0, -4), Color.BLACK, 2)
				draw_target.draw_circle(center + Vector2(-3, -1), 2, Color.BLACK)
				draw_target.draw_circle(center + Vector2(3, -1), 2, Color.BLACK)
			"Crew":
				draw_target.draw_circle(center + Vector2(0, -3), 2, Color.BLACK)
				draw_target.draw_line(center + Vector2(0, 0), center + Vector2(0, 4), Color.BLACK, 2)
			"Drone":
				draw_target.draw_rect(Rect2(center - Vector2(3, 3), Vector2(6, 6)), Color.BLACK)
			_:
				draw_target.draw_circle(center, 3, Color.BLACK)
	if main.admin_mode:
		_draw_room_path(room, rect)
		_draw_room_doors(room, rect)

func _draw_cryo_derelicts(main, cell_size: float) -> void:
	for cell in main.wrecks:
		var ward: Dictionary = main.wrecks[cell]
		if ward.kind!="cryo" or ward.cleared: continue
		cryo_view.recovery = ward
		cryo_view.configure_embedded(int(ward.rotation),[],false,main.visual_time_seconds)
		cryo_view.shell_pass = 0
		cryo_view.render_into(draw_target,(Vector2(cell)+Vector2.ONE*0.5)*cell_size,cell_size/384.0)
		if cell==main.selected_room_cell:
			draw_target.draw_rect(Rect2(Vector2(cell)*cell_size,Vector2.ONE*cell_size).grow(-2),Color("a9c4bf"),false,2)
		if ward.progress>0:
			var bar := Rect2((Vector2(cell)+Vector2(0.12,0.92))*cell_size,Vector2(0.76,0.018)*cell_size)
			draw_target.draw_rect(bar,Color("14282b"))
			bar.size.x *= ward.progress/preload("res://scripts/wreck_field.gd").DURATION
			draw_target.draw_rect(bar,Color("78b8ac"))
	cryo_view.recovery = {}

func _bill_room_view(room: Dictionary):
	var room_view = life_support_view if room.get("id", "") == "life_support" else nursery_view
	if room.get("id", "") == "hydroponics_bay": room_view = hydroponics_view
	if room.get("id", "") == "med_bay": room_view = med_bay_view
	if room.get("id", "") == "crew_hab": room_view = crew_hab_view
	if room.get("id", "") == "cryo_chamber":
		room_view = cryo_view
		cryo_view.recovery = _get_main().wrecks.get(room.get("pos",Vector2i(-1,-1)),{}) if room.get("recovered_derelict",false) else {}
	if room.get("id", "") == "clone_lab": room_view = clone_view
	if room.get("id", "") == "data_archive": room_view = archive_view
	if room.get("id", "") == "biodome": room_view = biodome_view
	if room.get("id", "") == "xeno_lab": room_view = xeno_view
	if room.get("id", "") == "anomaly_lab": room_view = anomaly_view
	if room.get("id", "") == "bio_lab": room_view = bio_view
	if room.get("id", "") == "holographic_core": room_view = holo_view
	if room.get("id", "") == "med_center": room_view = med_center_view
	if room.get("id", "") == "med_office": room_view = med_office_view
	if room.get("id", "") == "tidal_condenser": room_view = tidal_view
	if room.get("id", "") == "gravity_loom": room_view = gravity_view
	if room.get("id", "") == "brine_core":
		room_view = brine_view
		brine_view.architect_pod = _get_main().architect_run.get("core",{}) if room.has("pos") else {}
	if room.get("id", "") == "shield_generator": room_view = hull_view
	if room.get("id", "") == "radio_lab": room_view = acoustic_view
	if room.get("id", "") == "solar_array": room_view = thermal_view
	if room.get("id", "") == "battery_array": room_view = battery_view
	if room.get("id", "") == "research_lab": room_view = research_view
	if room.get("id", "") == "maintenance_bay": room_view = maintenance_view
	if room.get("id", "") == "storage_bay": room_view = storage_view
	if room.get("id", "") == "ore_refinery": room_view = refinery_view
	if room.get("id", "") == "mining_drone_bay": room_view = mining_view
	if room.get("id", "") == "construction_drone_bay": room_view = construction_view
	if room.get("id", "") == "airlock": room_view = airlock_view
	if room.get("id", "") == "salvage_drone_bay": room_view = salvage_view
	if room.get("id", "") == "crew_lounge": room_view = lounge_view
	if room.get("id", "") == "command_center": room_view = command_view
	if room.get("id", "") == "quarantine_cell": room_view = quarantine_view
	if room.get("id", "") == "reactor": room_view = reactor_view
	if rare_room_views.has(room.get("id","")):room_view=rare_room_views[room.id]
	return room_view

# Snapshot the exact registered ground footprints used to draw this room.
# The draw pass reconfigures shared views before use; snapshots own their arrays.
func bill_room_geometry(room: Dictionary, open_sides: Array) -> Dictionary:
	if _is_narrow_corridor(room):
		return {"corridor": true, "room": room.duplicate(true), "props": [], "edges": []}
	if not _uses_layered_art(room):
		return {"legacy": true, "room": room.duplicate(true), "props": [], "edges": []}
	var view = _bill_room_view(room)
	if view == null:
		return {}
	view.configure_embedded(int(room.get("rotation", 0)), open_sides, false, 0.0)
	return {"layout": view.layout.duplicate(true), "props": view.props.duplicate(true), "edges": view.edges.duplicate(true)}

func _draw_nursery(room: Dictionary, rect: Rect2, preview := false, floor_only := false, shell_only := false) -> void:
	var setup_started: int = Time.get_ticks_usec() if profile_draw else 0
	if _is_narrow_corridor(room):
		_draw_narrow_corridor(room,rect,preview,floor_only,shell_only)
		return
	var room_view = _bill_room_view(room)
	if room_view == null:
		return
	var main = _get_main()
	var sides: Array = []
	var omitted: Array = []
	var names := ["north", "east", "south", "west"]
	var pos: Vector2i = room.pos
	for side in range(4):
		var offset := _offset_from_side(names[side])
		if preview and side in preview_open_sides(room):
			sides.append(side)
		if not preview and not main.occupied.has(pos+offset) and names[side] in main.get_room_doors(room) and _drone_door_frame(main,pos,pos+offset)>0:
			sides.append(side)
		if _door_has_connected_neighbor(main, room, pos + offset, offset):
			if not sides.has(side): sides.append(side)
			if floor_only and not _uses_layered_art(main.occupied[pos + offset]):
				# Bridge only the canonical 72/384-cell clear aperture.
				var size := Vector2(0.12, 0.1875) * _cell_size() if side % 2 == 1 else Vector2(0.1875, 0.12) * _cell_size()
				var center := rect.get_center() + Vector2(offset) * _cell_size() * 0.5
				draw_target.draw_rect(Rect2(center - size * 0.5, size), Color("303740"))
		if not preview and main.occupied.has(pos + offset) and _uses_layered_art(main.occupied[pos + offset]) and not _is_narrow_corridor(main.occupied[pos+offset]) and side in [0, 3]:
			omitted.append(side)
	room_view.configure_embedded(int(room.get("rotation", 0)), sides, not preview and main.powered_room_cells.has(pos), main.get_visual_time_seconds(), omitted)
	if room.id=="airlock":
		room_view.cycle_pose=preload("res://scripts/airlock_cycle.gd").pose({} if preview else room)
		room_view.shelf_helmet_visible = preview or preload("res://scripts/airlock_service.gd").helmet_on_shelf(main, pos)
	if room.id in ["mining_drone_bay","salvage_drone_bay","construction_drone_bay"]:
		room_view.drone_deployed = not preview and main.drone_fleet.deployed(pos)
		room_view.hatch_open = main.drone_fleet.hatch_fraction(pos) if not preview else 0.0
	if not preview and main.has_test_walker():
		var actor_pos: Vector2 = main.get_test_walker_position()
		var actor_cell := Vector2i(floori(actor_pos.x / _cell_size()), floori(actor_pos.y / _cell_size()))
		if actor_cell == pos:
			room_view.actor = (actor_pos + Vector2(0, _cell_size() * 0.038) - rect.get_center()) * (384.0 / _cell_size())
			room_view.external_actor_texture = _get_human_frame(main.get_test_walker_state(), main.get_test_walker_direction())
			room_view.show_actor = true
	if not preview and main.has_dr_veld():
		var veld_pos: Vector2 = main.get_dr_veld_position()
		if Vector2i(floori(veld_pos.x / _cell_size()), floori(veld_pos.y / _cell_size())) == pos:
			room_view.external_actors.append({"position": (veld_pos + Vector2(0, _cell_size() * 0.038) - rect.get_center()) * (384.0 / _cell_size()), "texture": _get_veld_frame(main)})
	if not preview and main.has_chief_branforth():
		var branforth_pos: Vector2 = main.get_chief_branforth_position()
		if Vector2i(floori(branforth_pos.x / _cell_size()), floori(branforth_pos.y / _cell_size())) == pos:
			room_view.external_actors.append({"position": (branforth_pos + Vector2(0, _cell_size() * 0.038) - rect.get_center()) * (384.0 / _cell_size()), "texture": _get_branforth_frame(main)})
	if profile_draw:
		draw_profile_usec["detail_room_setup"] = int(draw_profile_usec.get("detail_room_setup",0)) + Time.get_ticks_usec() - setup_started
	room_view.shell_pass = 0 if preview else (1 if shell_only else 2)
	if retain_room_contents and retain_static_surfaces and not preview and not floor_only and not shell_only:
		if not content_canvases.has(pos):
			var canvas := RoomContents.new()
			surface_passes[Surface.LIVE].add_child(canvas)
			content_canvases[pos] = canvas
		var canvas: Node2D = content_canvases[pos]
		canvas.profile_enabled = profile_draw
		canvas.draw_origin = rect.get_center()
		canvas.draw_scale = _cell_size()/384.0
		canvas.show()
		var region := Rect2(Vector2(_get_main().grid_scroll.scroll_horizontal,_get_main().grid_scroll.scroll_vertical),_get_main().grid_scroll.size)
		canvas.clip_region = Rect2((region.position-rect.get_center())/canvas.draw_scale,region.size/canvas.draw_scale)
		room_view.retained_content_host = canvas
	room_view.render_into(draw_target, rect.get_center(), _cell_size() / 384.0, floor_only, preview)
	if floor_only and room.get("flooded",false):
		draw_target.draw_set_transform(rect.get_center(),0,Vector2.ONE*_cell_size()/384.0)
		draw_target.draw_rect(Rect2(-183,-183,366,366),Color(.08,.48,.62,.28))
		draw_target.draw_set_transform(Vector2.ZERO)
	room_view.retained_content_host = null
	room_view.shell_pass = 0
	if preview or floor_only:
		draw_target.draw_set_transform(rect.get_center(),0,Vector2.ONE*_cell_size()/384.0)
		RoomLighting.draw_pools(draw_target,1.0 if preview else _room_light_level(room),room.get("id","") in ["med_bay","life_support","cryo_chamber","clone_lab","data_archive","biodome","xeno_lab","med_office","med_center","holographic_core","bio_lab","anomaly_lab"],room.get("id","")=="crew_hab")
		if preview: RoomLighting.draw_fixtures(draw_target,1.0,room.get("id","") in ["med_bay","life_support","cryo_chamber","clone_lab","data_archive","biodome","xeno_lab","med_office","med_center","holographic_core","bio_lab","anomaly_lab"],room.get("id","")=="crew_hab")
		draw_target.draw_set_transform(Vector2.ZERO)

func _draw_narrow_corridor(room: Dictionary, rect: Rect2, preview: bool, floor_only: bool, shell_only: bool) -> void:
	if corridor_textures.is_empty(): corridor_textures = CorridorArt.load_sources()
	var main = _get_main()
	var q := CorridorGeometry.rotation(room)
	var corner: bool = room.id=="corner"
	var scale := _cell_size()/384.0
	var at: Vector2 = (Vector2(room.pos)+Vector2.ONE*0.5)*_cell_size()
	draw_target.draw_set_transform(at,0,Vector2.ONE*scale)
	if floor_only or preview:
		CorridorArt.draw_hull(draw_target,CorridorGeometry.hull_for(corner,room.id=="tee_corridor"),CorridorGeometry.floor_for(corner,room.id=="tee_corridor"),Vector2.ZERO,q,corridor_textures,corner,true,1.0 if preview else _room_light_level(room),room.id=="tee_corridor",posmod(int(room.get("art_variant",0)),3))
	if shell_only or preview:
		var shade := 1.0 if preview else lerpf(0.35,1.0,_room_light_level(room))
		if preload("res://scripts/title_settings.gd").raised_walls:
			var wall_neighbors: Array=[]
			for direction in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
				if main.occupied.has(room.pos+direction):wall_neighbors.append(direction)
			preload("res://rooms/underwater/corridor_dressing.gd").draw_risers(draw_target,CorridorGeometry.hull_for(corner,room.id=="tee_corridor"),q,int(room.get("art_variant",0)),shade,wall_neighbors)
		for side in main.get_room_doors(room):
			var offset := _offset_from_side(str(side))
			if preview or _door_has_connected_neighbor(main,room,room.pos+offset,offset) or _drone_door_frame(main,room.pos,room.pos+offset)>0: continue
			var edge := Vector2(offset)*192
			var size := Vector2(16,104) if offset.x!=0 else Vector2(104,16)
			draw_target.draw_rect(Rect2(edge-size/2,size),Color("7f9290")*Color(shade,shade,shade))
			draw_target.draw_rect(Rect2(edge-size/2,size).grow(-2),Color("536967")*Color(shade,shade,shade))
	if preview or (not floor_only and not shell_only):
		preload("res://rooms/underwater/corridor_dressing.gd").draw_props(draw_target,q,int(room.get("art_variant",0)),1.0 if preview else lerpf(0.35,1.0,_room_light_level(room)))
	if not preview and not floor_only and not shell_only:
		var crew: Array = []
		if main.has_test_walker():
			var bill_pos: Vector2 = main.get_test_walker_position()
			if Vector2i(floori(bill_pos.x / _cell_size()), floori(bill_pos.y / _cell_size())) == room.pos:
				crew.append({"position": (bill_pos + Vector2(0, _cell_size() * 0.038) - at) / scale, "texture": _get_human_frame(main.get_test_walker_state(), main.get_test_walker_direction())})
		if main.has_dr_veld():
			var veld_pos: Vector2 = main.get_dr_veld_position()
			if Vector2i(floori(veld_pos.x / _cell_size()), floori(veld_pos.y / _cell_size())) == room.pos:
				crew.append({"position": (veld_pos + Vector2(0, _cell_size() * 0.038) - at) / scale, "texture": _get_veld_frame(main)})
		if main.has_chief_branforth():
			var branforth_pos: Vector2 = main.get_chief_branforth_position()
			if Vector2i(floori(branforth_pos.x / _cell_size()), floori(branforth_pos.y / _cell_size())) == room.pos:
				crew.append({"position": (branforth_pos + Vector2(0, _cell_size() * 0.038) - at) / scale, "texture": _get_branforth_frame(main)})
		crew.sort_custom(func(a, b): return a.position.y < b.position.y)
		nursery_view.painter = draw_target
		for member in crew:
			nursery_view.actor = member.position
			nursery_view.external_actor_texture = member.texture
			nursery_view.draw_actor()
		nursery_view.painter = nursery_view
	draw_target.draw_set_transform(Vector2.ZERO)

func _draw_brine_core_overlay(rect: Rect2) -> void:
	var main = _get_main()
	var time_seconds: float = main.get_visual_time_seconds()
	var glow_texture := brine_core_overlays.get("glow") as Texture2D
	if glow_texture != null:
		var glow_alpha := 0.55 + sin(time_seconds * 0.9) * 0.20
		draw_target.draw_texture_rect(glow_texture, rect, false, Color(0.65, 1.0, 1.0, glow_alpha))
	var body_texture := brine_core_overlays.get("body") as Texture2D
	if body_texture != null:
		var body_size := Vector2(rect.size.x * 0.092, rect.size.y * 0.223)
		var body_center := rect.get_center() + Vector2(rect.size.x * 0.005, -rect.size.y * 0.008)
		var body_pos := body_center - body_size * 0.5 + Vector2(0, sin(time_seconds * 1.1) * rect.size.y * 0.004)
		draw_target.draw_texture_rect(body_texture, Rect2(body_pos, body_size), false, Color(1, 1, 1, 0.64))
	var bubble_texture := brine_core_overlays.get("bubble") as Texture2D
	if bubble_texture != null:
		for i in range(10):
			var phase: float = fmod(time_seconds * (0.12 + float(i) * 0.014) + float(i) * 0.17, 1.0)
			var bubble_size: float = rect.size.x * (0.006 + float(i % 4) * 0.002)
			var x_offset: float = sin(float(i) * 2.73 + time_seconds * 0.55) * rect.size.x * 0.044
			var y_start: float = rect.size.y * 0.105
			var y_end: float = -rect.size.y * 0.082
			var y_offset: float = y_start + (y_end - y_start) * phase
			var bubble_pos: Vector2 = rect.get_center() + Vector2(x_offset, y_offset) - Vector2.ONE * bubble_size * 0.5
			draw_target.draw_texture_rect(bubble_texture, Rect2(bubble_pos, Vector2.ONE * bubble_size), false, Color(0.75, 1.0, 1.0, 0.42))
	var glass_texture := brine_core_overlays.get("glass") as Texture2D
	if glass_texture != null:
		draw_target.draw_texture_rect(glass_texture, rect, false, Color(1, 1, 1, 0.72))

func _draw_room_doors(room: Dictionary, rect: Rect2) -> void:
	var main = _get_main()
	for door in main.get_room_doors(room):
		var door_rect := _door_rect(str(door), rect)
		draw_target.draw_rect(door_rect, Color("#4654ff"))
		draw_target.draw_rect(door_rect.grow(-2), Color("#9aa4ff"))

# Door geometry is canonical room-space data, independent of zoom and light.
var door_part_cache := {}
var reuse_door_parts := not OS.get_cmdline_user_args().has("--rebuild-door-parts")
func _department_parts(frame: int, vertical: bool, variant: String, narrow: bool, prototype: bool) -> Array:
	var key := [frame,vertical,variant,narrow,prototype]
	if reuse_door_parts and door_part_cache.has(key): return door_part_cache[key]
	var parts: Array = DepartmentDoor.side_open_prototype(variant) if prototype else DepartmentDoor.parts(frame,vertical,variant)
	if narrow: parts = DepartmentDoor.corridor_parts(frame,vertical,variant)
	# Finite authored frames/variants; cap also protects experimental callers.
	if reuse_door_parts and door_part_cache.size()<256: door_part_cache[key] = parts
	return parts

func _draw_layered_doors(behind_crew: bool) -> void:
	var main = _get_main()
	var cell_size := _cell_size()
	var actor_y := -INF
	if main.has_test_walker(): actor_y = main.get_test_walker_position().y+cell_size*0.038
	for room in visible_draw_rooms:
		# East/south traversal owns each undirected connection exactly once.
		for side in ["north","east","south","west"]:
			var offset := _offset_from_side(side)
			var neighbor: Vector2i = room.pos+offset
			var connected := _door_has_connected_neighbor(main,room,neighbor,offset)
			if connected and side in ["north","west"]: continue
			var outside_frame := _drone_door_frame(main,room.pos,neighbor)
			if not connected and (main.occupied.has(neighbor) or side not in main.get_room_doors(room) or outside_frame==0): continue
			var neighbor_room: Dictionary = main.occupied.get(neighbor,room)
			if not _uses_layered_art(room) and not _uses_layered_art(neighbor_room): continue
			var frame := _door_frame_for_pair(main,room.pos,neighbor) if connected else outside_frame
			var edge_center := _door_edge_center(room.pos,side,cell_size)
			actor_y = _nearest_crew_foot(main, edge_center).y
			if not department_door_materials.is_empty():
				var variant := DepartmentDoor.pair_variant(room,neighbor_room)
				var light := minf(_room_light_level(room),_room_light_level(neighbor_room))
				draw_target.draw_set_transform(edge_center,0,Vector2.ONE*cell_size/384.0)
				var door_parts := _department_parts(frame,side in ["east","west"],variant,_is_narrow_corridor(room) or _is_narrow_corridor(neighbor_room),side_open_door_prototype and side=="east")
				for part in door_parts:
					var behind: bool = part.floor or actor_y>edge_center.y+float(part.depth)*cell_size/384.0
					if behind==behind_crew: DepartmentDoor.draw_piece(draw_target,department_door_materials,variant,part,light)
				draw_target.draw_set_transform(Vector2.ZERO)
				continue
			if door_texture==null:
				if behind_crew: continue
				draw_target.draw_set_transform(edge_center,PI/2 if side in ["east","west"] else 0,Vector2.ONE*cell_size/384.0)
				RoomDoor.draw_door(draw_target,float(frame)/float(DOOR_OPEN_FRAMES-1))
			else:
				draw_target.draw_set_transform(edge_center,0,Vector2.ONE*cell_size/384.0)
				for part in AnimatedDoorAtlas.parts(frame,side in ["east","west"]):
					var behind: bool = part.floor or actor_y>edge_center.y+float(part.depth)*cell_size/384.0
					if behind==behind_crew: AnimatedDoorAtlas.draw_piece(draw_target,layered_door_texture if layered_door_texture != null else door_texture,part)
			draw_target.draw_set_transform(Vector2.ZERO)

func _draw_door_foregrounds(main, underlay: bool = false) -> void:
	if door_texture == null:
		if not underlay:
			_draw_static_door_foregrounds(main)
		return
	if door_texture.get_width() <= 0 or door_texture.get_height() <= 0:
		if not underlay:
			_draw_static_door_foregrounds(main)
		return
	var cell_size: float = _cell_size()
	var drawn: Dictionary = {}
	for room in main.placed_rooms:
		var pos: Vector2i = room["pos"]
		for side_value in main.get_room_doors(room):
			var side: String = str(side_value)
			var offset: Vector2i = _offset_from_side(side)
			var neighbor_pos: Vector2i = pos + offset
			if _uses_layered_art(room) or _uses_layered_art(main.occupied.get(neighbor_pos, {})):
				continue # The modular edge owns its frame; no second legacy door.
			var connected: bool = _door_has_connected_neighbor(main, room, neighbor_pos, offset)
			if connected and _is_duplicate_connected_door_side(side) and not _always_draw_room_doors(room):
				continue
			var key: String = "%s:%s" % [str(pos), side]
			if drawn.has(key):
				continue
			drawn[key] = true
			var edge_center: Vector2 = _door_edge_center(pos, side, cell_size)
			var frame_index: int = _door_frame_for_pair(main, pos, neighbor_pos) if connected else 0
			var source_rect: Rect2 = _door_source_rect(frame_index)
			var door_size: Vector2 = Vector2(cell_size * DOOR_DRAW_SIZE.x, cell_size * DOOR_DRAW_SIZE.y)
			var door_rotation: float = PI * 0.5 if side == "east" or side == "west" else 0.0
			draw_target.draw_set_transform(edge_center, door_rotation, Vector2.ONE)
			if underlay:
				_draw_door_floor_patch(door_size)
			_draw_door_texture_layer(source_rect, door_size, underlay)
			draw_target.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)

func _draw_static_door_foregrounds(main) -> void:
	var cell_size: float = _cell_size()
	var drawn: Dictionary = {}
	for room in visible_draw_rooms:
		var pos: Vector2i = room["pos"]
		for side_value in main.get_room_doors(room):
			var side: String = str(side_value)
			var offset: Vector2i = _offset_from_side(side)
			var neighbor_pos: Vector2i = pos + offset
			if _uses_layered_art(room) or _uses_layered_art(main.occupied.get(neighbor_pos, {})):
				continue # The modular edge owns its frame; no second legacy door.
			var connected: bool = _door_has_connected_neighbor(main, room, neighbor_pos, offset)
			if connected and _is_duplicate_connected_door_side(side) and not _always_draw_room_doors(room):
				continue
			var key: String = "%s:%s" % [str(pos), side]
			if drawn.has(key):
				continue
			drawn[key] = true
			var edge_center: Vector2 = _door_edge_center(pos, side, cell_size)
			var vertical: bool = side == "east" or side == "west"
			var frame_size: Vector2 = Vector2(cell_size * 0.026, cell_size * 0.10) if vertical else Vector2(cell_size * 0.10, cell_size * 0.026)
			draw_target.draw_rect(Rect2(edge_center - frame_size * 0.5, frame_size), Color(0.04, 0.07, 0.08, 0.82))

func _door_has_connected_neighbor(main, room: Dictionary, neighbor_pos: Vector2i, offset: Vector2i) -> bool:
	return main.occupied.has(neighbor_pos) and main._placed_rooms_connected(room, main.occupied[neighbor_pos], offset)

func _is_duplicate_connected_door_side(side: String) -> bool:
	return side == "north" or side == "west"

func _always_draw_room_doors(room: Dictionary) -> bool:
	var id := str(room.get("id", ""))
	return id == "reactor" or id == "brine_core"

func _door_frame_for_pair(main, cell_a: Vector2i, cell_b: Vector2i) -> int:
	var drone_frame := _drone_door_frame(main,cell_a,cell_b)
	if main.bill_npc.active or main.has_dr_veld() or main.has_chief_branforth():
		if not main._connected_neighbor_cells(cell_a).has(cell_b): return 0
		var center := (Vector2(cell_a + cell_b) * 0.5 + Vector2.ONE * 0.5) * _cell_size()
		var distance := _nearest_crew_foot(main, center).distance_to(center) * 384.0 / _cell_size()
		# Fully open before either crew member reaches the threshold; close
		# only after both have left its proximity zone.
		var amount := clampf((100.0 - distance) / 45.0, 0.0, 1.0)
		return maxi(drone_frame,roundi(amount * float(DOOR_OPEN_FRAMES - 1)))
	if main.test_walker_next_cell == Vector2i(-1, -1):
		return drone_frame
	var current: Vector2i = main.test_walker_cell
	var next: Vector2i = main.test_walker_next_cell
	var crossing: bool = (current == cell_a and next == cell_b) or (current == cell_b and next == cell_a)
	if not crossing:
		return drone_frame
	var progress: float = clampf(float(main.test_walker_progress), 0.0, 1.0)
	var open_amount: float = 1.0
	if progress < 0.16:
		open_amount = progress / 0.16
	elif progress > 0.84:
		open_amount = (1.0 - progress) / 0.16
	return maxi(drone_frame,clampi(int(round(open_amount * float(DOOR_OPEN_FRAMES - 1))), 0, DOOR_OPEN_FRAMES - 1))

func _drone_door_frame(main, cell_a: Vector2i, cell_b: Vector2i) -> int:
	var center := (Vector2(cell_a)+Vector2(cell_b))*0.5
	var amount := 0.0
	for drone in main.drone_fleet.drones.values():
		if drone.phase not in ["outbound","returning"] or drone.get("route",[]).is_empty(): continue
		var previous: Vector2i = drone.get("last_cell",drone.home)
		var next := Vector2i(drone.route[0])
		if not ((previous==cell_a and next==cell_b) or (previous==cell_b and next==cell_a)): continue
		amount = maxf(amount,clampf((0.34-Vector2(drone.position).distance_to(center))/0.15,0,1))
	return roundi(amount*float(DOOR_OPEN_FRAMES-1))

func _nearest_crew_foot(main, center: Vector2) -> Vector2:
	var nearest := Vector2(-1000000, -1000000)
	if main.has_test_walker():
		nearest = main.get_test_walker_position() + Vector2(0, _cell_size() * 0.038)
	if main.has_dr_veld():
		var foot: Vector2 = main.get_dr_veld_position() + Vector2(0, _cell_size() * 0.038)
		if foot.distance_squared_to(center) < nearest.distance_squared_to(center): nearest = foot
	if main.has_chief_branforth():
		var foot: Vector2 = main.get_chief_branforth_position() + Vector2(0, _cell_size() * 0.038)
		if foot.distance_squared_to(center) < nearest.distance_squared_to(center): nearest = foot
	return nearest

func _door_source_rect(frame_index: int) -> Rect2:
	var clamped_frame: int = clampi(frame_index, 0, DOOR_OPEN_FRAMES - 1)
	var frame_width: float = float(door_texture.get_width()) / float(DOOR_SHEET_COLUMNS)
	var frame_height: float = float(door_texture.get_height()) / float(DOOR_SHEET_ROWS)
	var column: int = clamped_frame % DOOR_SHEET_COLUMNS
	var row: int = floori(float(clamped_frame) / float(DOOR_SHEET_COLUMNS))
	return Rect2(Vector2(float(column) * frame_width, float(row) * frame_height), Vector2(frame_width, frame_height))

func _draw_door_texture_layer(source_rect: Rect2, door_size: Vector2, underlay: bool) -> void:
	var underlay_height: float = source_rect.size.y * DOOR_UNDERLAY_FRACTION
	var overlay_height: float = source_rect.size.y - underlay_height
	var underlay_dest_height: float = door_size.y * DOOR_UNDERLAY_FRACTION
	var overlay_dest_height: float = door_size.y - underlay_dest_height
	if underlay:
		var source: Rect2 = Rect2(
			source_rect.position + Vector2(0.0, overlay_height),
			Vector2(source_rect.size.x, underlay_height)
		)
		var dest: Rect2 = Rect2(
			Vector2(-door_size.x * 0.5, -door_size.y * 0.5 + overlay_dest_height),
			Vector2(door_size.x, underlay_dest_height)
		)
		draw_target.draw_texture_rect_region(door_texture, dest, source, Color(1.85, 1.85, 1.85, 1.0))
		_draw_door_light_wash(dest, false)
	else:
		var source: Rect2 = Rect2(source_rect.position, Vector2(source_rect.size.x, overlay_height))
		var dest: Rect2 = Rect2(
			Vector2(-door_size.x * 0.5, -door_size.y * 0.5),
			Vector2(door_size.x, overlay_dest_height)
		)
		draw_target.draw_texture_rect_region(door_texture, dest, source, Color(2.25, 2.25, 2.25, 1.0))
		_draw_door_light_wash(dest, true)

func _draw_door_light_wash(dest: Rect2, upper_piece: bool) -> void:
	var wash_alpha := 0.10 if upper_piece else 0.07
	draw_target.draw_rect(dest, Color(0.36, 0.78, 0.95, wash_alpha))
	var stripe_height := maxf(dest.size.y * 0.08, 1.0)
	var stripe := Rect2(
		dest.position + Vector2(dest.size.x * 0.18, dest.size.y * (0.28 if upper_piece else 0.54)),
		Vector2(dest.size.x * 0.64, stripe_height)
	)
	draw_target.draw_rect(stripe, Color(0.68, 0.96, 1.0, wash_alpha * 1.8))

func _draw_door_floor_patch(door_size: Vector2) -> void:
	var patch_size: Vector2 = Vector2(door_size.x * 0.72, door_size.y * 0.86)
	var patch: Rect2 = Rect2(-patch_size * 0.5 + Vector2(0.0, door_size.y * 0.02), patch_size)
	draw_target.draw_rect(patch, Color("#323c40"))
	draw_target.draw_rect(patch.grow(-2), Color("#3f484b"))
	var line_color := Color(0.68, 0.75, 0.74, 0.30)
	draw_target.draw_line(Vector2(patch.position.x, patch.get_center().y), Vector2(patch.end.x, patch.get_center().y), line_color, 1.0)
	draw_target.draw_line(Vector2(patch.get_center().x, patch.position.y), Vector2(patch.get_center().x, patch.end.y), line_color, 1.0)

func _offset_from_side(side: String) -> Vector2i:
	match side:
		"north":
			return Vector2i.UP
		"east":
			return Vector2i.RIGHT
		"south":
			return Vector2i.DOWN
		_:
			return Vector2i.LEFT

func _door_edge_center(pos: Vector2i, side: String, cell_size: float) -> Vector2:
	var origin: Vector2 = Vector2(pos) * cell_size
	match side:
		"north":
			return origin + Vector2(cell_size * 0.5, 0.0)
		"east":
			return origin + Vector2(cell_size, cell_size * 0.5)
		"south":
			return origin + Vector2(cell_size * 0.5, cell_size)
		_:
			return origin + Vector2(0.0, cell_size * 0.5)

func _draw_synergy_links(main) -> void:
	if main.connected_synergy_links.is_empty():
		return
	var cell_size: float = _cell_size()
	for link_value in main.connected_synergy_links:
		var link: Dictionary = link_value
		var synergy_id := str(link.get("id", ""))
		if not main.meta.discovered_synergy_ids.has(synergy_id):
			continue
		var cells: Array = link.get("cells", [])
		if cells.size() < 2:
			continue
		var color_text := str(link.get("fx_color", "4FA38D")).trim_prefix("#")
		var link_color := Color("#%s" % color_text)
		var center_a := (Vector2(cells[0]) + Vector2.ONE * 0.5) * cell_size
		var center_b := (Vector2(cells[1]) + Vector2.ONE * 0.5) * cell_size
		if not _is_functioning_link(main.active_synergy_links, link):
			draw_target.draw_line(center_a, center_b, Color(link_color.r, link_color.g, link_color.b, 0.18), maxf(1.5, cell_size * 0.006), true)
			continue
		_draw_functioning_synergy(link, center_a, center_b, link_color, cell_size, float(main.visual_time_seconds))

func _is_functioning_link(active_links: Array, candidate: Dictionary) -> bool:
	var candidate_key := str(candidate.get("key", ""))
	for active_value in active_links:
		var active: Dictionary = active_value
		if not candidate_key.is_empty() and str(active.get("key", "")) == candidate_key:
			return true
		if str(active.get("id", "")) == str(candidate.get("id", "")) and active.get("cells", []) == candidate.get("cells", []):
			return true
	return false

func _draw_functioning_synergy(link: Dictionary, center_a: Vector2, center_b: Vector2, color: Color, cell_size: float, time_seconds: float) -> void:
	var profile := str(link.get("fx_profile", "flow"))
	var direction := center_a.direction_to(center_b)
	var tangent := Vector2(-direction.y, direction.x)
	var shared_door := center_a.lerp(center_b, 0.5)
	var line_width := maxf(1.6, cell_size * 0.007)
	var mote_radius := maxf(2.4, cell_size * 0.013)
	var pulse_alpha := 0.55 + sin(time_seconds * 4.0) * 0.2
	var soft_color := Color(color.r, color.g, color.b, 0.22)
	var bright_color := Color(color.r, color.g, color.b, clampf(pulse_alpha, 0.25, 0.88))
	draw_target.draw_line(center_a, center_b, soft_color, maxf(1.5, line_width * 0.34), true)
	draw_target.draw_circle(shared_door, cell_size * (0.052 + pulse_alpha * 0.012), Color(color.r, color.g, color.b, pulse_alpha * 0.16))
	draw_target.draw_arc(shared_door, cell_size * 0.045, 0.0, TAU, 28, bright_color, maxf(2.0, line_width * 0.45), true)
	var edge_a := center_a + direction * cell_size * 0.39
	var edge_b := center_b - direction * cell_size * 0.39
	var segment_half := tangent * cell_size * 0.10
	var edge_alpha_a := pulse_alpha
	var edge_alpha_b := pulse_alpha
	if profile == "containment":
		var alternate := 1.0 if sin(time_seconds * 5.0) >= 0.0 else 0.28
		edge_alpha_a *= alternate
		edge_alpha_b *= 1.28 - alternate
	draw_target.draw_line(edge_a - segment_half, edge_a + segment_half, Color(color.r, color.g, color.b, edge_alpha_a), line_width, true)
	draw_target.draw_line(edge_b - segment_half, edge_b + segment_half, Color(color.r, color.g, color.b, edge_alpha_b), line_width, true)
	draw_target.draw_circle(edge_a, mote_radius * 0.74, Color(color.r, color.g, color.b, edge_alpha_a * 0.38))
	draw_target.draw_circle(edge_b, mote_radius * 0.74, Color(color.r, color.g, color.b, edge_alpha_b * 0.38))
	for mote_index in range(2):
		var phase := _synergy_mote_phase(profile, time_seconds, mote_index)
		var mote_t := lerpf(0.16, 0.84, phase)
		var mote_position := center_a.lerp(center_b, mote_t)
		draw_target.draw_circle(mote_position, mote_radius * 1.8, Color(color.r, color.g, color.b, 0.08))
		draw_target.draw_circle(mote_position, mote_radius, Color(color.r, color.g, color.b, 0.82))
		draw_target.draw_circle(mote_position, mote_radius * 0.34, Color(0.94, 1.0, 1.0, 0.92))

func _synergy_mote_phase(profile: String, time_seconds: float, mote_index: int) -> float:
	var speed := 0.28
	if profile == "power":
		speed = 0.72
	elif profile == "signal":
		speed = 0.46
	elif profile == "care":
		speed = 0.22
	elif profile == "containment":
		speed = 0.34
	var phase := fmod(time_seconds * speed + float(mote_index) * 0.5, 1.0)
	match profile:
		"logistics":
			return floor(phase * 7.0) / 7.0
		"signal":
			return 0.5 - cos(phase * TAU) * 0.5
		"care":
			var mirrored := fmod(time_seconds * speed, 1.0)
			return mirrored if mote_index == 0 else 1.0 - mirrored
		"containment":
			return 0.24 if int(floor(time_seconds * 4.0)) % 2 == mote_index else 0.76
		_:
			return phase

func _draw_discovery_bursts(main) -> void:
	var cell_size: float = _cell_size()
	for burst_value in main.discovery_bursts:
		var burst: Dictionary = burst_value
		var cells: Array = burst.get("cells", [])
		if cells.size() < 2:
			continue
		var remaining := clampf(float(burst.get("remaining", 0.0)), 0.0, 1.2)
		var progress := 1.0 - remaining / 1.2
		var color: Color = burst.get("color", Color("#55E6FF"))
		var alpha := (1.0 - progress) * 0.88
		var center_a := (Vector2(cells[0]) + Vector2.ONE * 0.5) * cell_size
		var center_b := (Vector2(cells[1]) + Vector2.ONE * 0.5) * cell_size
		var ring_radius := cell_size * lerpf(0.10, 0.42, progress)
		for center in [center_a, center_b]:
			draw_target.draw_arc(center, ring_radius, 0.0, TAU, 48, Color(color.r, color.g, color.b, alpha), maxf(3.0, cell_size * 0.012), true)
		var shared_door := center_a.lerp(center_b, 0.5)
		draw_target.draw_circle(shared_door, cell_size * lerpf(0.12, 0.035, progress), Color(color.r, color.g, color.b, alpha * 0.48))

func _draw_room_hologram(main, cell: Vector2i, valid: bool) -> void:
	var cell_size := _cell_size()
	var room := RoomDatabaseScript.get_room(main.selected_card_id).duplicate(true)
	if room.is_empty():
		return
	room["pos"] = cell
	room["rotation"] = main.selected_rotation
	var rect := Rect2(Vector2(cell) * cell_size + Vector2.ONE, Vector2(cell_size - 2, cell_size - 2))
	var tint := Color(0.22, 0.74, 0.60, 0.045) if valid else Color(0.88, 0.18, 0.20, 0.085)
	draw_target.draw_rect(rect, tint)
	var room_texture: Texture2D = _get_room_texture(room)
	if _uses_layered_art(room):
		_draw_nursery(room, rect, true)
		draw_target.draw_rect(rect, Color(0.12, 0.35, 0.3, 0.22) if valid else Color(0.45, 0.08, 0.08, 0.28))
	elif room_texture != null:
		draw_target.draw_set_transform(rect.get_center(), deg_to_rad(float(main.selected_rotation * 90)), Vector2.ONE)
		draw_target.draw_texture_rect(room_texture, Rect2(-rect.size * 0.5, rect.size), false, Color(0.64, 0.95, 0.82, 0.17) if valid else Color(1.0, 0.54, 0.54, 0.19))
		draw_target.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	else:
		draw_target.draw_rect(rect.grow(-4), tint)
	draw_target.draw_rect(rect, Color(0.35, 0.82, 0.68, 0.58) if valid else Color(1.0, 0.35, 0.39, 0.58), false, 2.0)
	var corner_len := cell_size * 0.16
	var corner_color := Color(0.68, 0.96, 0.84, 0.50) if valid else Color(1.0, 0.55, 0.58, 0.50)
	for corner in [rect.position, Vector2(rect.end.x, rect.position.y), rect.end, Vector2(rect.position.x, rect.end.y)]:
		var sx := 1.0 if corner.x == rect.position.x else -1.0
		var sy := 1.0 if corner.y == rect.position.y else -1.0
		draw_target.draw_line(corner, corner + Vector2(corner_len * sx, 0), corner_color, 4)
		draw_target.draw_line(corner, corner + Vector2(0, corner_len * sy), corner_color, 4)
	_draw_preview_openings(main, room, rect)
	if main.admin_mode:
		_draw_room_path(room, rect)

func _get_room_texture(room: Dictionary) -> Texture2D:
	var id := str(room.get("id", ""))
	if room_texture_variants.has(id):
		var textures: Array = room_texture_variants[id]
		if not textures.is_empty():
			var variant_index := int(room.get("art_variant", 0)) % textures.size()
			return textures[variant_index]
	if room_textures.has(id):
		return room_textures[id]
	return null

func _door_rect(side: String, rect: Rect2) -> Rect2:
	var thickness := 40.0
	var length := 196.0
	match side:
		"north":
			return Rect2(Vector2(rect.get_center().x - length * 0.5, rect.position.y - 2), Vector2(length, thickness))
		"east":
			return Rect2(Vector2(rect.end.x - thickness + 2, rect.get_center().y - length * 0.5), Vector2(thickness, length))
		"south":
			return Rect2(Vector2(rect.get_center().x - length * 0.5, rect.end.y - thickness + 2), Vector2(length, thickness))
		_:
			return Rect2(Vector2(rect.position.x - 2, rect.get_center().y - length * 0.5), Vector2(thickness, length))

func _draw_room_path(room: Dictionary, rect: Rect2) -> void:
	var main = _get_main()
	var center := rect.get_center()
	var points := {
		"north": Vector2(center.x, rect.position.y + 2),
		"east": Vector2(rect.end.x - 2, center.y),
		"south": Vector2(center.x, rect.end.y - 2),
		"west": Vector2(rect.position.x + 2, center.y)
	}
	var doors: Array = main.get_room_doors(room)
	var path_type := str(main.get_room_layout(room).get("path", "cross"))
	match path_type:
		"ring":
			var ring := Rect2(center - Vector2(186, 186), Vector2(372, 372))
			draw_target.draw_rect(ring, Color("#ff2537"), false, 20)
			for door in doors:
				draw_target.draw_line(center, points[str(door)], Color("#ff2537"), 20)
		"perimeter":
			var loop := Rect2(center - Vector2(168, 168), Vector2(336, 336))
			draw_target.draw_rect(loop, Color("#ff2537"), false, 20)
			for door in doors:
				var side := str(door)
				var anchor := center
				match side:
					"north":
						anchor = Vector2(center.x - 168, center.y - 168)
					"east":
						anchor = Vector2(center.x + 168, center.y - 168)
					"south":
						anchor = Vector2(center.x + 168, center.y + 168)
					_:
						anchor = Vector2(center.x - 168, center.y + 168)
				draw_target.draw_line(anchor, points[side], Color("#ff2537"), 20)
		"elbow":
			if doors.size() >= 2:
				var corner := Vector2(points[str(doors[0])].x, points[str(doors[1])].y)
				draw_target.draw_line(points[str(doors[0])], corner, Color("#ff2537"), 20)
				draw_target.draw_line(corner, points[str(doors[1])], Color("#ff2537"), 20)
		_:
			for door in doors:
				draw_target.draw_line(center, points[str(door)], Color("#ff2537"), 20)

func _draw_humans(main) -> void:
	_draw_veld_legacy(main)
	_draw_branforth_legacy(main)
	if human_sprite == null or not main.has_test_walker():
		return
	var walker_pos: Vector2 = main.get_test_walker_position()
	var walker_cell := Vector2i(floori(walker_pos.x / _cell_size()), floori(walker_pos.y / _cell_size()))
	if _uses_layered_art(main.occupied.get(walker_cell, {})):
		return # Already drawn in the nursery's ground-depth queue.
	var direction: String = main.get_test_walker_direction()
	var state: String = main.get_test_walker_state()
	var texture: Texture2D = _get_human_frame(state, direction)
	if texture == null: return
	var pos: Vector2 = main.get_test_walker_position()
	var cell_size := _cell_size()
	var source_rect := Rect2(Vector2.ZERO, texture.get_size())
	var pixel_scale := cell_size * 0.17 / 74.0
	var sprite_size := texture.get_size() * pixel_scale
	var foot_pos := pos + Vector2(0, cell_size * 0.038)
	var sprite_rect := Rect2(foot_pos - Vector2(texture.get_meta("crew_pivot", Vector2(46, 86))) * pixel_scale, sprite_size)
	var shadow_pos := foot_pos
	draw_target.draw_set_transform(shadow_pos, 0.0, Vector2(cell_size * 0.00125, cell_size * 0.00028))
	draw_target.draw_circle(Vector2.ZERO, 23, Color(0, 0, 0, 0.36))
	draw_target.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	draw_target.draw_texture_rect_region(texture, sprite_rect, source_rect)

func _draw_veld_legacy(main) -> void:
	if not main.has_dr_veld(): return
	var pos: Vector2 = main.get_dr_veld_position()
	var cell := Vector2i(floori(pos.x / _cell_size()), floori(pos.y / _cell_size()))
	if _uses_layered_art(main.occupied.get(cell, {})): return
	var texture := _get_veld_frame(main)
	if texture == null: return
	var pixel_scale := _cell_size() * 0.17 / 74.0
	var foot := pos + Vector2(0, _cell_size() * 0.038)
	draw_target.draw_texture_rect(texture, Rect2(foot - Vector2(texture.get_meta("crew_pivot", Vector2(46, 86))) * pixel_scale, texture.get_size() * pixel_scale), false)

func _get_veld_frame(main) -> Texture2D:
	if main.veld_npc.helmet_action_active():
		var key: String = main.veld_npc.state + "-east"
		return veld_player.frame_at_elapsed(key, veld_player.cycle_seconds(key) - main.veld_npc.timer)
	return veld_player.frame(main.veld_npc.animation_state(), main.veld_npc.direction, main.get_visual_time_seconds(), main.get_dr_veld_position() / _cell_size(), "diving-helmet" if main.veld_npc.helmet_equipped else "")

func _draw_branforth_legacy(main) -> void:
	if not main.has_chief_branforth(): return
	var pos: Vector2 = main.get_chief_branforth_position()
	var cell := Vector2i(floori(pos.x / _cell_size()), floori(pos.y / _cell_size()))
	if _uses_layered_art(main.occupied.get(cell, {})): return
	var texture := _get_branforth_frame(main)
	if texture == null: return
	var pixel_scale := _cell_size() * 0.17 / 74.0
	var foot := pos + Vector2(0, _cell_size() * 0.038)
	draw_target.draw_texture_rect(texture, Rect2(foot - Vector2(texture.get_meta("crew_pivot", Vector2(46, 86))) * pixel_scale, texture.get_size() * pixel_scale), false)

func _get_branforth_frame(main) -> Texture2D:
	if main.branforth_npc.helmet_action_active():
		var key: String = main.branforth_npc.state + "-east"
		return branforth_player.frame_at_elapsed(key, branforth_player.cycle_seconds(key) - main.branforth_npc.timer)
	return branforth_player.frame(main.branforth_npc.animation_state(), main.branforth_npc.direction, main.get_visual_time_seconds(), main.get_chief_branforth_position() / _cell_size(), "diving-helmet" if main.branforth_npc.helmet_equipped else "")

func crew_playback_snapshot() -> Dictionary:
	return {"bill": {"key": human_animation_key, "phase": human_animation_phase,
		"last_time": human_animation_last_time, "started": human_animation_started,
		"last_position": human_animation_last_position}, "veld": veld_player.snapshot(), "branforth": branforth_player.snapshot()}

func restore_crew_playback(data: Dictionary) -> void:
	var bill: Dictionary = data.bill
	if bill.key.is_empty() or human_animation_timing.has(bill.key):
		human_animation_key = bill.key
		human_animation_phase = float(bill.phase)
		human_animation_last_time = float(bill.last_time)
		human_animation_started = float(bill.started)
		human_animation_last_position = bill.last_position
	veld_player.restore_snapshot(data.veld)
	if data.has("branforth"): branforth_player.restore_snapshot(data.branforth)

func _get_human_frame(state: String, direction: String) -> Texture2D:
	if human_animations.has(state):
		var by_direction: Dictionary = human_animations[state]
		if by_direction.has(direction):
			var frames: Array = by_direction[direction]
			if frames.is_empty(): return human_sprites.get(direction, human_sprite)
			var key := state + "-" + direction
			var main = _get_main()
			if main.bill_npc.helmet_action_active():
				var total := 0.0
				for duration in human_animation_timing[key].durations: total += float(duration) / 1000.0
				return frames[_human_frame_index(key, maxf(0.0, total - main.bill_npc.timer))]
			var time_seconds: float = main.get_visual_time_seconds()
			var position_cells: Vector2 = main.get_test_walker_position() / _cell_size()
			var elapsed := _advance_human_animation(key, time_seconds, position_cells)
			var index := _human_frame_index(key, elapsed)
			var equipment := "diving-helmet" if main.bill_npc.helmet_equipped else ""
			if not equipment.is_empty():
				if not human_equipment_frames.has(equipment) or not human_equipment_frames[equipment].has(key): return null
				return human_equipment_frames[equipment][key][index]
			return frames[index]
	return human_sprites.get(direction, human_sprite)

func _draw_connectors(room: Dictionary, occupied: Dictionary) -> void:
	var main = _get_main()
	var cell_size := _cell_size()
	var pos: Vector2i = room["pos"]
	var center := Vector2(pos) * cell_size + Vector2(cell_size, cell_size) * 0.5
	for offset in [Vector2i.RIGHT, Vector2i.DOWN]:
		if occupied.has(pos + offset) and main._placed_rooms_connected(room, occupied[pos + offset], offset):
			var neighbor_center := Vector2(pos + offset) * cell_size + Vector2(cell_size, cell_size) * 0.5
			draw_target.draw_line(center, neighbor_center, Color("#88939a"), 5)
			draw_target.draw_line(center, neighbor_center, Color("#1d252b"), 2)

func drone_anchors(room: Dictionary) -> Dictionary:
	if room.id == "brine_core": return {"dock":Vector2(0,0.15)*384,"hatch":Vector2(0,0.35)*384}
	var view = _bill_room_view(room)
	view.configure_embedded(int(room.get("rotation",0)),[],false,0.0)
	var anchors := {}
	for prop in view.props:
		if str(prop.id).ends_with("_rov"): anchors["dock"] = Vector2(prop.rect.get_center().x,prop.rect.end.y-50)
		if str(prop.id).ends_with("_hatch"): anchors["hatch"] = Vector2(prop.rect.get_center().x,prop.rect.end.y-35)
	return anchors

func _draw_drones(main) -> void:
	var cell_size := _cell_size()
	var fleet = main.drone_fleet
	var pending: Array = fleet.orders.duplicate()
	for drone in fleet.drones.values():
		if not drone.order.is_empty(): pending.append(drone.order)
	for order in pending:
		var center := (Vector2(order.pos)+Vector2.ONE*0.5)*cell_size
		var rect := Rect2(center-Vector2.ONE*cell_size*0.43,Vector2.ONE*cell_size*0.86)
		draw_target.draw_rect(rect,Color(0.26,0.35,0.38,0.35))
		draw_target.draw_rect(rect,Color("ba884c"),false,2)
		for i in range(5):
			var x := rect.position.x+rect.size.x*i/4.0
			draw_target.draw_line(Vector2(x,rect.position.y),Vector2(x,rect.end.y),Color(0.7,0.58,0.36,0.35),1)
		draw_target.draw_string(get_theme_default_font(),center+Vector2(-cell_size*0.32,0),"CONSTRUCTION",HORIZONTAL_ALIGNMENT_CENTER,cell_size*0.64,maxi(8,int(cell_size*0.045)),Color("cdb591"))
	for drone in fleet.drones.values():
		if drone.phase == "docked": continue
		var room: Dictionary = main.occupied.get(drone.home,{})
		if room.is_empty(): continue
		var home := (Vector2(drone.home)+Vector2.ONE*0.5)*cell_size
		var anchors := drone_anchors(room)
		var dock_offset: Vector2 = anchors.dock*cell_size/384.0
		var hatch_offset: Vector2 = anchors.hatch*cell_size/384.0
		var pos := (Vector2(drone.position)+Vector2.ONE*0.5)*cell_size
		var width := cell_size*0.18
		if drone.phase == "launching":
			var f := clampf(float(drone.elapsed)/1.2,0,1)
			pos = home+dock_offset.lerp(hatch_offset,f)
			width *= 1.0-f*0.35
		elif drone.phase == "docking":
			var f := clampf(float(drone.elapsed)/1.2,0,1)
			pos = home+hatch_offset.lerp(dock_offset,f)
			width *= 0.65+f*0.35
		elif drone.phase in ["outbound","returning"]:
			var from_home: float = clampf(Vector2(drone.position).distance_to(Vector2(drone.home))/0.30,0,1)
			pos += hatch_offset*(1.0-from_home)
		DroneArt.draw_drone(draw_target,drone.kind,pos,width,float(drone.get("clock",0.0)),drone.phase=="working",drone.phase in ["launching","outbound","returning","docking"])

func _get_drone_frame(state: String, direction: String) -> Texture2D:
	if drone_animations.has(state):
		var by_direction: Dictionary = drone_animations[state]
		if by_direction.has(direction):
			var frames: Array = by_direction[direction]
			var fps := 8.0
			if state == "mine":
				fps = 6.0
			elif state == "idle":
				fps = 4.0
			var time_seconds: float = _get_main().get_visual_time_seconds()
			var index: int = int(time_seconds * fps) % frames.size()
			return frames[index]
	if drone_sprites.has(direction):
		return drone_sprites[direction]
	if drone_sprites.has("south"):
		return drone_sprites["south"]
	return null

func _direction_for_vector(vector: Vector2) -> String:
	if vector.length() <= 0.001:
		return "south"
	var angle := rad_to_deg(vector.angle())
	if angle < 0.0:
		angle += 360.0
	if angle >= 337.5 or angle < 22.5:
		return "east"
	if angle < 67.5:
		return "south-east"
	if angle < 112.5:
		return "south"
	if angle < 157.5:
		return "south-west"
	if angle < 202.5:
		return "west"
	if angle < 247.5:
		return "north-west"
	if angle < 292.5:
		return "north"
	return "north-east"

func _get_main():
	return get_tree().current_scene

func _cell_size() -> float:
	return _get_main().get_cell_size()

func preview_open_sides(room: Dictionary) -> Array:
	var result: Array = []
	var names := ["north", "east", "south", "west"]
	for side in _get_main().get_room_doors(room): result.append(names.find(side))
	return result

func _draw_preview_openings(main, room: Dictionary, rect: Rect2) -> void:
	if not preload("res://scripts/title_settings.gd").placement_guides: return
	for side in main.get_room_doors(room):
		var normal := Vector2(_offset_from_side(str(side)))
		var tangent := Vector2(-normal.y,normal.x)
		var center := rect.get_center()+normal*_cell_size()*0.5
		var neighbor: Vector2i = room.pos+Vector2i(normal)
		var occupied: bool = main.occupied.has(neighbor)
		var matches: bool = occupied and main._doors_connect(room.id,int(room.rotation),Vector2i(normal),main.occupied[neighbor])
		var color := Color("9ff3df") if matches else (Color("efb777") if occupied else Color("69cfff"))
		var half_width := _cell_size()*0.09375
		# An outlined aperture and outward chevron remain readable on every wall orientation.
		var a := center-tangent*half_width
		var b := center+tangent*half_width
		draw_target.draw_line(a,b,Color("071822"),maxf(10.0,_cell_size()*0.035))
		draw_target.draw_line(a,b,color,maxf(4.0,_cell_size()*0.013))
		for jamb in [a,b]: draw_target.draw_line(jamb-normal*10,jamb+normal*10,color,3.0)
		var tip := center+normal*maxf(16.0,_cell_size()*0.06)
		draw_target.draw_line(tip-normal*9-tangent*7,tip,color,3.0)
		draw_target.draw_line(tip-normal*9+tangent*7,tip,color,3.0)
		if occupied and not matches:
			draw_target.draw_line(center-Vector2(5,5),center+Vector2(5,5),color,3.0)
			draw_target.draw_line(center+Vector2(5,-5),center+Vector2(-5,5),color,3.0)
