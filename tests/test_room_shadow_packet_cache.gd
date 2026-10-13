extends SceneTree
const Lighting=preload("res://rooms/whole-room/room_lighting.gd")
const Scope=preload("res://scripts/session_art_cache.gd")
var failures:=0
var checks:=0
class Sample extends Node2D:
	var phase:=0
	func _draw():
		if phase==0:
			for i in 128:Lighting.draw_equipment_shadows(self,[{"rect":Rect2(-30,-20,60,40)}],float(i)/127.0)
		elif phase==1:
			Lighting.draw_equipment_shadows(self,[{"rect":Rect2(-29.5,-20,60,40)}],1.0)
		else:
			for i in 140:Lighting.draw_equipment_shadows(self,[{"rect":Rect2(-70+i*.25,-20,60,40)}],1.0)
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func contact_cache_aliases():
	var saved:Dictionary=Lighting._contact_boxes
	Lighting._contact_boxes={}
	var pairs=[
		[Color(.015,.025,.03,.025001),Color(.015,.025,.03,.025101),.01,.49],
		[Color(.015,.025,.03,.060001),Color(.015,.025,.03,.060101),.51,1.49],
		[Color(-.2,.025,1.2,-.1),Color(0,.025,1,0),3.7,3.7],
		[Color(1.3,-1,.03,2),Color(1,0,.03,1),9.5,10.0]]
	for pair in pairs:
		check(pair[0].to_html()==pair[1].to_html() and int(round(pair[2]))==int(round(pair[3])),"Fixture exercises the same legacy colour/radius bucket")
		var first:StyleBoxFlat=Lighting._contact_box(pair[0],pair[2])
		var later:StyleBoxFlat=Lighting._contact_box(pair[1],pair[3])
		check(is_same(first,later),"Same bucket retains the original StyleBox identity")
		check(first.bg_color==pair[0],"First unquantized colour remains authoritative")
		check(first.corner_radius_top_left==int(round(pair[2])),"Rounded contact silhouette remains unchanged")
	var lower:StyleBoxFlat=Lighting._contact_box(Color(.015,.025,.03,.4),.49)
	var upper:StyleBoxFlat=Lighting._contact_box(Color(.015,.025,.03,.4),.51)
	check(not is_same(lower,upper),"Radius rounding boundary keeps distinct silhouettes")
	Lighting._contact_boxes=saved
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\","/").simplify_path()
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--profile="):expected=arg.trim_prefix("--profile=")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/").simplify_path()!=expected:quit(2);return
	preload("res://tools/release_benchmark.gd").configure_test_window(root)
	root.set_disable_input(true)
	contact_cache_aliases()
	Lighting.clear_room_shadow_packets()
	var sample:=Sample.new();root.add_child(sample)
	await frame()
	check(Lighting.room_shadow_packets.size()==1,"128 light levels reuse one geometry")
	check(Lighting.room_shadow_packet_misses==1 and Lighting.room_shadow_packet_hits>=127,"Fades update palettes instead of rebuilding geometry")
	check(Lighting.room_shadow_palette_updates>=128,"Every changing palette is applied")
	var retained_points:PackedVector2Array=Lighting.room_shadow_packets.values()[0].points.duplicate()
	Lighting.room_shadow_packet_bytes=Lighting.ROOM_SHADOW_PACKET_BYTES-1
	sample.phase=1;sample.queue_redraw();await frame()
	check(Lighting.room_shadow_packets.size()==1,"Byte budget evicts old buffers before admitting a new plan")
	check(Lighting.room_shadow_packet_bytes<Lighting.ROOM_SHADOW_PACKET_BYTES,"Buffer accounting remains bounded")
	check(Lighting.room_shadow_packets.values()[0].points!=retained_points,"Moved footprints invalidate geometry")
	sample.phase=2;sample.queue_redraw();await frame()
	check(Lighting.room_shadow_packets.size()<=128,"Continuous editing cannot retain every position")
	check(Lighting.room_shadow_packet_bytes<=Lighting.ROOM_SHADOW_PACKET_BYTES,"Editing respects buffer budget")
	sample.queue_free();await frame()
	check(Scope.owners.is_empty(),"Fixture has no unrelated drawing owners")
	var first:=Node2D.new();root.add_child(first);Scope.retain(first)
	var second:=Node2D.new();root.add_child(second);Scope.retain(second)
	var held:int=Lighting.room_shadow_packets.size()
	first.queue_free();await frame()
	check(Lighting.room_shadow_packets.size()==held,"Overlapping owners preserve live geometry")
	second.queue_free();await frame()
	check(Lighting.room_shadow_packets.is_empty() and Lighting.room_shadow_packet_bytes==0,"Final owner releases geometry and palette buffers")
	FileAccess.open("user://packet-cache-result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("ROOM SHADOW CACHE ",checks," checks, ",failures," failures")
	quit(0 if failures==0 else 1)
