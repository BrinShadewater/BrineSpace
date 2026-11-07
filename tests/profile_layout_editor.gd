extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
var result: Dictionary={}
func _init() -> void: call_deferred("run")
func measure(label: String, action: Callable, count:=20) -> void:
	var values: Array=[]
	for i in range(count):
		var start:=Time.get_ticks_usec(); action.call(); values.append((Time.get_ticks_usec()-start)/1000.0)
	values.sort(); result[label]={"median_ms":values[count/2],"p95_ms":values[mini(count-1,int(count*0.95))]}
func run() -> void:
	Store.path="res://output/layout-editor/performance-isolated.json"; Store.loaded=true; Store.data={}
	if FileAccess.file_exists(Store.path+".recovery.json"): DirAccess.remove_absolute(ProjectSettings.globalize_path(Store.path+".recovery.json"))
	var started:=Time.get_ticks_usec()
	var e=Editor.open(root)
	result.open_ms=(Time.get_ticks_usec()-started)/1000.0
	await process_frame
	e.layer=0; e.selected="sample_cooler"; e.refresh()
	measure("authored_positions",func(): Store.authored_positions(e.entries[0].asset,0),100)
	measure("validation",e.issues)
	measure("refresh",e.refresh)
	measure("tray",e.rebuild_library)
	e.free_placement.button_pressed=true
	for i in range(40): e.draft["library/common-analog_clock#"+str(i)]=[-150+i%8*35,40+i/8*25]
	e.refresh()
	measure("populated_refresh",e.refresh)
	measure("drag_update",func(): e.draft[e.selected][0]+=0.01; e.refresh(true))
	if DisplayServer.get_name()!="headless":
		measure("drag_render",func(): e.draft[e.selected][0]+=0.01; e.refresh(true); RenderingServer.force_draw())
	for i in range(150): e.history.append(e.draft.duplicate(true))
	e.dirty=true
	measure("recovery",e.write_recovery,6)
	var label:="baseline"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--label="): label=arg.trim_prefix("--label=")
	var f:=FileAccess.open("res://output/layout-editor/performance-"+label+".json",FileAccess.WRITE); f.store_string(JSON.stringify(result,"  ")); f.close()
	print("PROFILE "+JSON.stringify(result))
	e.close_editor(); await process_frame; quit()
