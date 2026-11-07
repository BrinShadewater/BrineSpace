extends SceneTree
const Wet=preload("res://rooms/doors/door_water.gd")
const Door=preload("res://rooms/doors/department_door.gd")
func _init():
	for path in [get_script().resource_path,"res://tests/test_wet_door_integration.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var file:=FileAccess.open(path+".uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));file.close()
	var state:=Wet.advance({},9,1.0)
	assert(state.closing_until<0)
	state=Wet.advance(state,6,1.1)
	assert(state.closing_until>1.1)
	var held:=Wet.advance(state,6,1.1)
	assert(held==state,"Paused visual clock preserves closing effect")
	state=Wet.advance(state,7,1.2)
	assert(state.closing_until<0,"Opening cancels closing signal")
	state=Wet.advance(state,0,1.3)
	assert(state.closing_until>1.3)
	state=Wet.advance(state,0,2.0)
	assert(state.closing_until<2.0,"Closed warning expires")
	state=Wet.advance(state,0,0.0)
	assert(state.closing_until<0,"Restored clock does not replay a closure")
	for variant in Door.VARIANTS:
		for vertical in [false,true]:
			var previous:=INF
			for frame in range(10):
				var area:=0.0
				for part in Door.parts(frame,vertical,variant):
					if part.get("leaf",false) or part.get("front_leaf",false): area+=part.rect.get_area()
				assert(area<=previous,"Opening skins retract monotonically")
				previous=area
			assert(previous==0,"Fully open aperture contains no leaves")
	print("DOOR POLISH LOGIC PASS: closing/hold/open/expiry/restore and 100 aperture states")
	quit()
