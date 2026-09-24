extends SceneTree
## Compact layout evidence; recovery slots deliberately carry no assigned identity.
func _init():
	var rows: Array=[]
	for seed_value in [32,73,118]:
		var site:=preload("res://scripts/site_generator.gd").generate(seed_value)
		var obstacles: Array=[]
		var deposits: Array=[]
		for cell in site.wrecks: obstacles.append({"x":cell.x,"y":cell.y,"kind":site.wrecks[cell].kind})
		for cell in site.sites: deposits.append({"x":cell.x,"y":cell.y,"kind":site.sites[cell].kind})
		rows.append({"seed":seed_value,"generation_usec":site.generation_usec,"obstacles":obstacles,"deposits":deposits})
	FileAccess.open("res://output/procedural-sites-2026-09-23/layouts.json",FileAccess.WRITE).store_string(JSON.stringify(rows,"  "))
	print("Three procedural layout previews saved")
	quit()
