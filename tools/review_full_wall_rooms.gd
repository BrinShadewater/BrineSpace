extends SceneTree
const Geometry=preload("res://tools/modular_room_geometry.gd")
var manifest: Array
var views: Array=[]
var relocation_audit := {}
var composition_audit := {}

class Card extends Node2D:
	var room
	func _draw() -> void:
		if room==null: return
		room.configure_embedded(0,[],false,0.0)
		room.render_into(self,Vector2(256,256),1.16)

class Review extends Node2D:
	var entries: Array=[]
	var q := 0
	func _draw() -> void:
		draw_rect(Rect2(0,0,2000,ceili(entries.size()/5.0)*450),Color("17212b"))
		for i in entries.size():
			var entry: Dictionary=entries[i]
			var origin := Vector2(200+(i%5)*400,220+(i/5)*450)
			var pose: int=q if q>=0 else (1 if entry.room in ["mining_drone_bay","ore_refinery","cryo_chamber"] else 0)
			entry.view.configure_embedded(pose,[0,1,2,3],true,1.0)
			entry.view.render_into(self,origin,0.96)
			draw_string(ThemeDB.fallback_font,origin+Vector2(-180,208),entry.room.replace("_"," ").capitalize(),HORIZONTAL_ALIGNMENT_LEFT,-1,19,Color("c5d0d8"))

var selected: PackedStringArray=[]
var output_dir := "res://output/full-wall-v1/previews"
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--review-rooms="): selected=arg.trim_prefix("--review-rooms=").split(",")
		if arg.begins_with("--output-dir="): output_dir=arg.trim_prefix("--output-dir=").trim_suffix("/")
	assert(output_dir.begins_with("res://output/"))
	call_deferred("run")

func run() -> void:
	if not OS.get_cmdline_user_args().has("--owner-layouts"):
		preload("res://scripts/room_layout_store.gd").path="res://output/side-wall-review-isolated-layouts.json"
	manifest=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/manifest.json"))
	if not selected.is_empty():
		manifest=manifest.filter(func(entry): return entry.room in selected)
		assert(manifest.size()==selected.size(),"Every requested room must be registered")
	root.size=Vector2i(2000,ceili(manifest.size()/5.0)*450)
	root.content_scale_size=root.size
	var review := Review.new()
	for entry in manifest:
		var view=load(entry.view).new()
		view.embedded=true
		view.hide()
		root.add_child(view)
		views.append(view)
		composition_audit[entry.room]={}
		review.entries.append({"room":entry.room,"view":view})
		for q in range(4):
			if OS.get_cmdline_user_args().has("--owner-layouts") and (q%2==0 or entry.room not in ["research_lab","med_bay","pressure_control","listening_post","xeno_lab","isolation_vault"]): continue
			for running in [false,true]:
				view.configure_embedded(q,[0,1,2,3],running,2.0)
				var placements: Array=[]
				for item in view.props:
					var vb: Rect2=view.prop_visual_bounds(item)
					placements.append({"id":item.id,"ground":[item.rect.position.x,item.rect.position.y,item.rect.size.x,item.rect.size.y],"visual":[vb.position.x,vb.position.y,vb.size.x,vb.size.y]})
				composition_audit[entry.room][q]=placements
				var count := 0
				for prop in view.props:
					if prop.get("relocated",false):
						for other in view.props:
							if other.id==prop.id: continue
							assert(not view.prop_visual_bounds(prop).intersects(view.prop_visual_bounds(other)),"Relocated art overlaps: "+entry.room+" q"+str(q)+"/"+prop.id+" with "+other.id)
					if not prop.get("full_wall",false): continue
					count+=1
					var envelope := Rect2(-180,-198,360,378)
					if prop.get("wall_mount",false):
						var half: float=(Geometry.CELL+Geometry.WALL)*0.5
						envelope=Rect2(-half,-half,half*2,half*2)
						var inner: float=(Geometry.CELL-Geometry.WALL)*0.5
						var contact: float=-prop.rect.position.y if prop.side_view=="north" else (prop.rect.end.y if prop.side_view=="south" else (-prop.rect.position.x if prop.side_view=="west" else prop.rect.end.x))
						assert(is_equal_approx(contact,inner),entry.room+" backing must meet inner wall face")
					assert(envelope.encloses(view.prop_visual_bounds(prop)),entry.room+" art outside hull")
					for side in range(4):
						if not Geometry.has_port(view.layout[0],side): continue
						var lane := Rect2(-36,-180,72,180) if side==0 else (Rect2(0,-36,180,72) if side==1 else (Rect2(-36,0,72,180) if side==2 else Rect2(-180,-36,180,72)))
						assert(not prop.rect.intersects(lane),entry.room+" installation blocks door lane")
				assert(count==(2 if entry.get("split",false) else (0 if entry.room in ["pressure_control","listening_post"] and q==0 else 1)),entry.room+" installation count")
				if entry.room=="life_support":
					for required in ["life_tank","life_console"]:
						assert(view.props.any(func(item): return item.id==required),"Life Support must retain "+required)
				if entry.room=="hydroponics_bay":
					for required in ["hydro_harvest","hydro_nutrients"]:
						assert(view.props.any(func(item): return item.id==required),"Hydroponics must retain "+required)
				if entry.room=="storage_bay":
					for required in ["storage_lift","storage_crates"]:
						assert(view.props.any(func(item): return item.id==required),"Storage must retain "+required)
				if entry.room=="data_archive":
					for required in ["archive_library","archive_terminal"]:
						assert(view.props.any(func(item): return item.id==required),"Archive must retain "+required)
				if entry.room=="holographic_core":
					for required in ["holo_projector","holo_calibrator"]:
						assert(view.props.any(func(item): return item.id==required),"Holographic Core must retain "+required)
				if entry.room=="command_center":
					for required in ["command_table","command_systems"]:
						assert(view.props.any(func(item): return item.id==required),"Command must retain "+required)
				if entry.room=="battery_array":
					for required in ["battery_breaker","battery_distribution"]:
						assert(view.props.any(func(item): return item.id==required),"Battery must retain "+required)
				if entry.room=="quarantine_cell":
					assert(view.props.any(func(item): return item.id=="quarantine_berth"),"Quarantine berth must survive every rotation")
				if entry.room=="med_center":
					for required in ["medical_treatment","medical_imaging"]:
						assert(view.props.any(func(item): return item.id==required),"Med Center must retain "+required)
				if entry.room=="med_office":
					for required in ["office_exam","office_consultation"]:
						assert(view.props.any(func(item): return item.id==required),"Med Office must retain "+required)
				if entry.room in ["mining_drone_bay","salvage_drone_bay","construction_drone_bay"]:
					var ids: Array=[]
					for prop in view.props: ids.append(prop.id)
					var fleet: String=entry.room.trim_suffix("_drone_bay")
					assert(fleet+"_rov" in ids and fleet+"_hatch" in ids,"Live vehicle and launch hatch retained")
		if entry.room=="cryo_chamber":
			var baseline=load(entry.baseline).new()
			baseline.embedded=true
			baseline.hide()
			root.add_child(baseline)
			for count in [1,2]:
				var pods: Array=[]
				for i in count: pods.append({"id":"review_%d"%i,"wake":0.0,"recovered":false})
				view.recovery={"pods":pods,"cleared":true}
				baseline.recovery=view.recovery.duplicate(true)
				for q in range(4):
					view.configure_embedded(q,[],true,1.0)
					baseline.configure_embedded(q,[],true,1.0)
					assert(view.props==baseline.props,"Recovered cryo layout must match original")
			view.recovery={}
			baseline.queue_free()
		relocation_audit[entry.room]=view.full_wall.placement_reports.duplicate(true)
	root.add_child(review)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output_dir))
	for q in [-1,0,1,2,3]:
		review.q=q
		review.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var filename := "rooms-installed.png" if q<0 else "rooms-q%d.png"%q
		assert(root.get_texture().get_image().save_png(output_dir+"/"+filename)==OK)
	print("FULL WALL DRAFT REVIEW: six new installations x two vertical orientations x two states" if OS.get_cmdline_user_args().has("--owner-layouts") else "FULL WALL REVIEW: %d rooms x 4 rotations x 2 operating states; installation bounds and door lanes checked" % manifest.size())
	var audit := FileAccess.open(output_dir+"/relocations.json",FileAccess.WRITE)
	audit.store_string(JSON.stringify(relocation_audit,"\t"))
	var compositions := FileAccess.open(output_dir+"/compositions.json",FileAccess.WRITE)
	compositions.store_string(JSON.stringify(composition_audit,"\t"))
	review.hide()
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	root.transparent_bg=true
	var card := Card.new()
	root.add_child(card)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output_dir+"/cards"))
	for i in manifest.size():
		card.room=views[i]
		card.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png(output_dir+"/cards/"+manifest[i].room+".png")==OK)
	print("FULL WALL CARDS: %d default-orientation room thumbnails captured" % manifest.size())
	quit()
