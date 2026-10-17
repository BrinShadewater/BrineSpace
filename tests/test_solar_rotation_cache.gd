extends SceneTree
const Solar = preload("res://rooms/full-wall-v1/solar_array_view.gd")
const Store = preload("res://scripts/room_layout_store.gd")
class Painter extends Node2D:
	var room
	var q := 0
	var mode := 0
	var mask := 0
	var running := true
	var clock := 0.5
	func _draw():
		var sides := []
		for side in range(4):
			if mask & (1 << side): sides.append(side)
		room.configure_embedded(q,sides,running,clock,[0] if mask & 1 else [])
		room.shell_pass = mode
		room.render_into(self,Vector2(256,256),1.0,mode==3,true)
var checks := 0
var failures := 0
func check(ok: bool,label: String):
	checks += 1
	if not ok: failures += 1; push_error(label)
func _init(): call_deferred("run")
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	if DisplayServer.get_name()=="headless": quit(2); return
	var views := []
	var captures := []
	var painters := []
	for index in range(2):
		var view=Solar.new(); view.embedded=true; root.add_child(view); view.hide()
		view.retain_rotation_setup=index==1
		views.append(view)
		var capture=SubViewport.new(); capture.size=Vector2i(512,512); capture.transparent_bg=true
		capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(capture);captures.append(capture)
		var painter=Painter.new();painter.room=view;capture.add_child(painter);painters.append(painter)
	Store.prime()
	var original: Dictionary=Store.data.duplicate(true)
	for edit in range(5):
		if edit>0:
			Store.data=original.duplicate(true)
			Store.data[Store.key("thermal-control-wall",1)]={"full_wall_thermal-control-wall":null} if edit==1 else {}
			if edit>=3:
				Store.data[Store.key("thermal-control-wall",1)]={"full_wall_thermal-control-wall":[-140,-130],"size/full_wall_thermal-control-wall":[0.8,0.9],"flip/full_wall_thermal-control-wall":[true,false]}
			if edit==4:
				Store.data[Store.key("thermal-control-wall",1)]["full_wall_thermal-control-wall"]=[-120,-110]
			else:
				Store.revision+=1;Store.geometry_revision+=1
		for pass_index in range(4):
			for q in range(4):
				for painter in painters:
					painter.q=q;painter.mode=pass_index;painter.mask=(q+pass_index*3)%16
					painter.running=pass_index%2==0;painter.clock=0.5+pass_index;painter.queue_redraw()
				await frame()
				check(not captures[0].get_texture().get_image().is_invisible(),"Reference contains rendered art")
				check(captures[0].get_texture().get_image().get_data()==captures[1].get_texture().get_image().get_data(),"Exact solar pixels edit%d pass%d q%d"%[edit,pass_index,q])
				check(views[0].props==views[1].props,"Exact props after rotation/edit")
				check(views[0].dressing.profile==views[1].dressing.profile,"Exact dressing after rotation/edit")
				check(views[0].edges==views[1].edges,"Exact door/open/omitted edges")
	# Compare two cached views after deliberately mutating active working data.
	views[0].retain_rotation_setup=true
	for q in [0,1,2,3,0,1]:
		for painter in painters:painter.q=q;painter.queue_redraw()
		await frame()
	for view in views:
		view.props[0]["probe_mutation"]=true
		view.dressing.profile["probe_mutation"]=true
		view.layout[0]["probe_mutation"]=true
	for q in [2,1,3,1,3]:
		for painter in painters:painter.q=q;painter.queue_redraw()
		await frame()
		check(not views[1].props[0].has("probe_mutation"),"Working props restore original snapshot")
		check(not views[1].layout[0].has("probe_mutation"),"Working layout restores original snapshot")
		check(not views[1].dressing.profile.has("probe_mutation"),"Working profile restores original snapshot")
		check(views[0].props==views[1].props,"Mutation restores canonical props")
		check(views[0].layout==views[1].layout,"Mutation restores canonical layout")
		check(views[0].dressing.profile==views[1].dressing.profile,"Mutation restores canonical profile")
		check(captures[0].get_texture().get_image().get_data()==captures[1].get_texture().get_image().get_data(),"Mutation recovery pixels")
	# Edits can arrive without changing the currently configured quarter.
	Store.data=original.duplicate(true)
	Store.data[Store.key("thermal-control-wall",3)]={"full_wall_thermal-control-wall":null}
	Store.revision+=1;Store.geometry_revision+=1
	for painter in painters: painter.queue_redraw()
	await frame()
	check(captures[0].get_texture().get_image().get_data()==captures[1].get_texture().get_image().get_data(),"Same-quarter deletion preserves current renderer")
	check(views[0].props==views[1].props,"Same-quarter deletion props")
	check(views[1].rotation_setup_hits>=30,"Reused rotation snapshots exercised")
	check(views[1].rotation_setups.size()==4,"Cache bounded to four rotations")
	views[1].set_meta("layout_editor_preview",true)
	views[1].configure_embedded(0,[],false,0.0)
	check(views[1].rotation_setups.is_empty(),"Studio clears runtime snapshots")
	print("SOLAR CACHE ","PASS" if failures==0 else "FAIL"," checks=",checks," failures=",failures)
	for view in views:view.queue_free()
	for capture in captures:capture.queue_free()
	await process_frame
	quit(0 if failures==0 else 1)
