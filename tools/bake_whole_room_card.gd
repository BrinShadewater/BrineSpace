extends SceneTree
const View = preload("res://rooms/whole-room/nursery_furnished_view.gd")
const LifeView = preload("res://rooms/whole-room/underwater_life_support_view.gd")
var life := false
const HydroView = preload("res://rooms/whole-room/hydroponics_view.gd")
var hydro := false
const ReactorView = preload("res://rooms/whole-room/reactor_view.gd")
const GravityView = preload("res://rooms/underwater/gravity-loom/gravity_loom_view.gd")
const BrineView = preload("res://rooms/underwater/brine-core/brine_core_view.gd")
const MedView = preload("res://rooms/whole-room/med_bay_view.gd")
const CrewView = preload("res://rooms/whole-room/crew_hab_view.gd")
const CryoView = preload("res://rooms/underwater/batch-two/cryo_chamber_view.gd")
const CloneView = preload("res://rooms/underwater/batch-two/clone_lab_view.gd")
const ArchiveView = preload("res://rooms/underwater/batch-two/data_archive_view.gd")
const BiodomeView = preload("res://rooms/underwater/batch-two/biodome_view.gd")
const XenoView = preload("res://rooms/underwater/batch-two/xeno_lab_view.gd")
const AnomalyView = preload("res://rooms/underwater/batch-two/anomaly_lab_view.gd")
const BioView = preload("res://rooms/underwater/batch-two/bio_lab_view.gd")
const HoloView = preload("res://rooms/underwater/batch-two/holographic_core_view.gd")
const MedCenterView = preload("res://rooms/underwater/batch-two/med_center_view.gd")
const MedOfficeView = preload("res://rooms/underwater/batch-two/med_office_view.gd")
const TidalView = preload("res://rooms/underwater/tidal-condenser/tidal_condenser_view.gd")
const HullView = preload("res://rooms/underwater/hull-integrity/shield_generator_view.gd")
const AcousticView = preload("res://rooms/underwater/acoustic-comms/radio_lab_view.gd")
const ThermalView = preload("res://rooms/underwater/thermal-control/solar_array_view.gd")
const BatteryView = preload("res://rooms/production-ten/battery_array_view.gd")
const ResearchView = preload("res://rooms/production-ten/research_lab_view.gd")
const MaintenanceView = preload("res://rooms/production-ten/maintenance_bay_view.gd")
const StorageView = preload("res://rooms/production-ten/storage_bay_view.gd")
const RefineryView = preload("res://rooms/production-ten/ore_refinery_view.gd")
const QuarantineView = preload("res://rooms/production-ten/quarantine_cell_view.gd")
const CommandView = preload("res://rooms/production-ten/command_center_view.gd")
const LoungeView = preload("res://rooms/production-ten/crew_lounge_view.gd")
const SalvageView = preload("res://rooms/production-ten/salvage_drone_bay_view.gd")
const ConstructionView = preload("res://rooms/production-ten/construction_drone_bay_view.gd")
const MiningView = preload("res://rooms/production-ten/mining_drone_bay_view.gd")
var reactor := false
var output_override := ""
class Card extends Node2D:
	var room
	var sides: Array = []
	func _draw() -> void:
		if room==null: return
		room.configure_embedded(0,sides,false,0.0)
		room.render_into(self,Vector2(256,256),1.16)
		draw_set_transform(Vector2(256,256),0,Vector2.ONE*1.16)
		preload("res://rooms/whole-room/room_lighting.gd").draw_fixtures(self,1.0,room is MedView or room is LifeView or room is CryoView or room is CloneView or room is ArchiveView or room is BiodomeView or room is XenoView,room is CrewView)
		draw_set_transform(Vector2.ZERO)
func _init() -> void:
	life = "--life" in OS.get_cmdline_user_args()
	hydro = "--hydro" in OS.get_cmdline_user_args()
	reactor = "--reactor" in OS.get_cmdline_user_args()
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): output_override = arg.trim_prefix("--output=")
	call_deferred("run")
func run() -> void:
	root.size = Vector2i(512,512)
	root.content_scale_size = Vector2i(512,512)
	root.transparent_bg = true
	var view = HydroView.new() if hydro else (LifeView.new() if life else View.new())
	if reactor:
		view.free()
		view = ReactorView.new()
	view.embedded = true
	if "--construction" in OS.get_cmdline_user_args():
		view.free()
		view=ConstructionView.new()
		view.embedded=true
	if "--brine" in OS.get_cmdline_user_args():
		view.free()
		view=BrineView.new()
		view.embedded=true
	if "--gravity" in OS.get_cmdline_user_args():
		view.free()
		view=GravityView.new()
		view.embedded=true
	if "--crew" in OS.get_cmdline_user_args():
		view.free()
		view=CrewView.new()
		view.embedded=true
	if "--med" in OS.get_cmdline_user_args():
		view.free()
		view = MedView.new()
		view.embedded = true
	if "--cryo" in OS.get_cmdline_user_args():
		view.free()
		view=CryoView.new()
		view.embedded=true
	if "--battery" in OS.get_cmdline_user_args():
		view.free()
		view=BatteryView.new()
		view.embedded=true
	if "--clone" in OS.get_cmdline_user_args():
		view.free()
		view=CloneView.new()
		view.embedded=true
	if "--research" in OS.get_cmdline_user_args():
		view.free()
		view=ResearchView.new()
		view.embedded=true
	if "--maintenance" in OS.get_cmdline_user_args():
		view.free()
		view=MaintenanceView.new()
		view.embedded=true
	if "--storage" in OS.get_cmdline_user_args():
		view.free()
		view=StorageView.new()
		view.embedded=true
	if "--archive" in OS.get_cmdline_user_args():
		view.free()
		view=ArchiveView.new()
		view.embedded=true
	if "--biodome" in OS.get_cmdline_user_args():
		view.free()
		view=BiodomeView.new()
		view.embedded=true
	if "--xeno" in OS.get_cmdline_user_args():
		view.free()
		view=XenoView.new()
		view.embedded=true
	if "--anomaly" in OS.get_cmdline_user_args():
		view.free()
		view=AnomalyView.new()
		view.embedded=true
	if "--refinery" in OS.get_cmdline_user_args():
		view.free()
		view=RefineryView.new()
		view.embedded=true
	if "--mining" in OS.get_cmdline_user_args():
		view.free()
		view=MiningView.new()
		view.embedded=true
	if "--salvage" in OS.get_cmdline_user_args():
		view.free()
		view=SalvageView.new()
		view.embedded=true
	if "--lounge" in OS.get_cmdline_user_args():
		view.free()
		view=LoungeView.new()
		view.embedded=true
	if "--command" in OS.get_cmdline_user_args():
		view.free()
		view=CommandView.new()
		view.embedded=true
	if "--quarantine" in OS.get_cmdline_user_args():
		view.free()
		view=QuarantineView.new()
		view.embedded=true
	if "--bio" in OS.get_cmdline_user_args():
		view.free()
		view=BioView.new()
		view.embedded=true
	if "--holo" in OS.get_cmdline_user_args():
		view.free()
		view=HoloView.new()
		view.embedded=true
	if "--thermal" in OS.get_cmdline_user_args():
		view.free()
		view=ThermalView.new()
		view.embedded=true
	if "--med-center" in OS.get_cmdline_user_args():
		view.free()
		view=MedCenterView.new()
		view.embedded=true
	if "--acoustic" in OS.get_cmdline_user_args():
		view.free()
		view=AcousticView.new()
		view.embedded=true
	if "--med-office" in OS.get_cmdline_user_args():
		view.free()
		view=MedOfficeView.new()
		view.embedded=true
	if "--hull" in OS.get_cmdline_user_args():
		view.free()
		view=HullView.new()
		view.embedded=true
	if "--tidal" in OS.get_cmdline_user_args():
		view.free()
		view=TidalView.new()
		view.embedded=true
	for argument in OS.get_cmdline_user_args():
		if not argument.begins_with("--view="): continue
		if output_override.is_empty():
			push_error("Custom view requires an explicit new --output path")
			quit(1)
			return
		var custom_script=load(argument.trim_prefix("--view="))
		if custom_script==null:
			quit(1)
			return
		view.free()
		view=custom_script.new()
		view.embedded=true
	view.hide()
	root.add_child(view)
	var card := Card.new()
	card.room = view
	root.add_child(card)
	await process_frame
	await RenderingServer.frame_post_draw
	var output := "res://rooms/whole-room/life-support-card-v1.png" if life else "res://rooms/whole-room/nursery-card-v1.png"
	if not output_override.is_empty(): output = output_override
	assert(not FileAccess.file_exists(output),"Do not overwrite card")
	assert(root.get_texture().get_image().save_png(output)==OK)
	print("WHOLE ROOM CARD: 512 square, embedded host draw path, shared geometry, offline master art")
	quit()
