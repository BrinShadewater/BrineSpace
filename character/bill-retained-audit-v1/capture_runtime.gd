extends SceneTree

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_major_bill_animations()
	var player = grid.human_water_player
	var tracks := []
	for variant in ["bare","helmet"]:
		var rows: Dictionary = player.frames if variant == "bare" else player.equipment_frames["diving-helmet"]
		var timings: Dictionary = player.timing if variant == "bare" else player.equipment_timing["diving-helmet"]
		for key in rows:
			var prefix = str(key).split("-")[0]
			if prefix in ["walk","interact","kneel","repair","stand"]: continue
			if prefix == "idle" and not str(key).begins_with("idle-east"): continue
			var files := []
			for i in range(rows[key].size()):
				var rel := "frames/%s/%s/%03d.png" % [variant,key,i]
				var full := "res://character/bill-retained-audit-v1/"+rel
				DirAccess.make_dir_recursive_absolute(full.get_base_dir())
				assert(rows[key][i].get_image().save_png(full)==OK)
				files.append(rel)
			var pivot: Vector2 = rows[key][0].get_meta("crew_pivot")
			tracks.append({"key":key,"variant":variant,"files":files,"durations":timings[key].durations,"pivot":[pivot.x,pivot.y],"width":rows[key][0].get_width(),"height":rows[key][0].get_height()})
	var f := FileAccess.open("res://character/bill-retained-audit-v1/runtime-tracks.json",FileAccess.WRITE)
	f.store_string(JSON.stringify(tracks,"  ")+"\n")
	print("BILL RETAINED AUDIT: %d actual loaded tracks" % tracks.size())
	grid.free()
	quit()
