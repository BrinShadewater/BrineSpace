extends SceneTree
## Trim and export directly from newly authored high-resolution transparent masters.
const GROUPS := [
	{"path":"res://brineui/badge-icons-v3/atlases/resources.png", "cols":4, "rows":3, "ids":["metal","power","oxygen","water","food","data","biomass","rare_minerals","integrity","crew","corruption","archived_data"]},
	{"path":"res://brineui/badge-icons-v3/atlases/hazards-actions.png", "cols":4, "rows":3, "ids":["anomaly","orbit","fire","freeze","sensor","repair","scrap","assign_workplace","focus_room","doors_open","doors_closed","hull_intact"]},
	{"path":"res://brineui/badge-icons-v3/atlases/draft-crew.png", "cols":4, "rows":4, "ids":["fan","row","show_hand","hide_hand","frame_on","frame_off","reroll","health","fatigue","hunger","activity","assigned_room","idle","working","unassigned","resting"]},
	{"path":"res://brineui/badge-icons-v3/atlases/navigation-utility.png", "cols":5, "rows":4, "ids":["archive","diagnostics","journal","menu","settings","search","filter","close","back","expand","collapse","locked","unlocked","pause","play","confirm","cancel","info","warning","help"]},
]
func _initialize() -> void:
	var report: Array = []
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://brineui/badge-icons-v3/icons"))
	for group in GROUPS:
		var image := Image.new()
		if image.load(group.path) != OK:
			push_error("Missing atlas: " + group.path)
			quit(1)
			return
		for index in range(group.ids.size()):
			var cell := Rect2i(roundi((index % int(group.cols))*float(image.get_width())/group.cols), roundi((index/int(group.cols))*float(image.get_height())/group.rows), roundi(float(image.get_width())/group.cols), roundi(float(image.get_height())/group.rows))
			# Authored rows are not perfectly uniform: cut in their actual transparent gutters.
			var bands: Array = []
			if group.path == "res://brineui/badge-icons-v3/atlases/hazards-actions.png": bands = [[0,432],[438,736],[738,image.get_height()]]
			if group.path == "res://brineui/badge-icons-v3/atlases/draft-crew.png": bands = [[0,282],[285,522],[525,740],[742,image.get_height()]]
			if group.path == "res://brineui/badge-icons-v3/atlases/navigation-utility.png": bands = [[0,326],[330,575],[580,833],[840,image.get_height()]]
			if not bands.is_empty():
				var band: Array = bands[index/int(group.cols)]
				cell.position.y = band[0]
				cell.size.y = band[1]-band[0]
			var source := image.get_region(cell.intersection(Rect2i(Vector2i.ZERO,image.get_size())))
			var bounds := source.get_used_rect()
			if bounds.size.x < 16 or bounds.size.y < 16:
				push_error("Empty glyph: " + str(group.ids[index]))
				quit(1)
				return
			var icon := source.get_region(bounds)
			var ratio := minf(1.0,224.0/maxf(icon.get_width(),icon.get_height()))
			icon.resize(maxi(1,roundi(icon.get_width()*ratio)),maxi(1,roundi(icon.get_height()*ratio)),Image.INTERPOLATE_LANCZOS)
			var output := Image.create(256,256,false,Image.FORMAT_RGBA8)
			output.fill(Color.TRANSPARENT)
			output.blit_rect(icon,Rect2i(Vector2i.ZERO,icon.get_size()),(Vector2i(256,256)-icon.get_size())/2)
			var id: String = group.ids[index]
			var destination: String = preload("res://scripts/ui_badge_icons.gd").PATHS[id]
			# Preserve the accepted v2 Archived Data cartridge instead of the old chip symbol.
			if id != "archived_data" and output.save_png(destination) != OK:
				push_error("Unable to save: " + destination)
				quit(1)
				return
			report.append({"id":id,"source":group.path,"bounds":str(bounds),"scale":ratio,"export":destination})
	var file := FileAccess.open("res://output/ui-badge-icons-2026-10-03/slicing.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t"))
	print("BADGE ICONS: %d source cells checked, 59 new 256px exports; no source upscaling" % report.size())
	quit()
