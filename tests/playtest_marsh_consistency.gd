extends SceneTree
## Native selected-player review; does not simulate a maintenance room assignment.
class Review extends Node2D:
    var textures: Array=[]
    var state: String=""
    var labels: Array=[]
    func _draw() -> void:
        draw_rect(Rect2(0,0,960,460),Color("293b40"))
        for col in range(textures.size()):
            var texture: Texture2D=textures[col]
            if texture==null:continue
            var x: float=120+col*240
            draw_string(ThemeDB.fallback_font,Vector2(x-80,26),str(labels[col])+" / "+state,HORIZONTAL_ALIGNMENT_LEFT,-1,16)
            draw_string(ThemeDB.fallback_font,Vector2(x-75,54),"Source / station scale",HORIZONTAL_ALIGNMENT_LEFT,-1,14)
            for row in range(2):
                var scale: float=1.0 if row==0 else 65.28/float(texture.get_meta("crew_standing_height"))
                var anchor:=Vector2(x,210 if row==0 else 402)
                draw_line(anchor-Vector2(100,0),anchor+Vector2(100,0),Color("839597"))
                draw_texture_rect(texture,Rect2(anchor-texture.get_meta("crew_pivot")*scale,texture.get_size()*scale),false)
func review_seconds(player,key: String,spec: Dictionary) -> float:
    if key.begins_with("idle-"):return .5
    return player.cycle_seconds(key)*(2 if spec.loop else 1)+(.8 if key.begins_with("death-") else 0.0)
func _init() -> void:call_deferred("run")
func run() -> void:
    if DisplayServer.get_name()=="headless":quit(2);return
    root.size=Vector2i(960,460);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
    var output: String="res://output/marsh-animation-audit/consistency-native/"
    DirAccess.make_dir_recursive_absolute(output)
    var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
    var player=grid.marsh_player
    var contract: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-consistency-review-v1/runtime-contract.json"))
    var groups: Array=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-consistency-review-v1/groups.json"))
    var failures:=0
    var checked:=0
    for key in contract.states:
        var spec: Dictionary=contract.states[key]
        if not player.frames.has(key) or player.frames[key].size()!=spec.files.size():failures+=1;push_error("Missing review state: "+key);continue
        var elapsed:=0.0
        for slot in range(spec.files.size()):
            var image:=Image.new();image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+str(spec.files[slot])))
            var texture: Texture2D=player.frame_at_elapsed(key,elapsed+.001)
            if texture==null or texture.get_image().get_data()!=image.get_data():failures+=1;push_error("Review frame differs: %s / %d"%[key,slot])
            elapsed+=float(spec.durations[slot])/1000.0;checked+=1
    var view:=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
    var captures:=0
    for group_index in range(groups.size()):
        var group: Dictionary=groups[group_index]
        for sample in range(16):
            view.textures=[];view.labels=[];view.state=group.title
            for column in group.columns:
                view.labels.append(column.label)
                var length:=0.0
                for key in column.keys:length+=review_seconds(player,key,contract.states[key])
                var cursor: float=length*float(sample)/16.0
                var selected_key: String=column.keys.back()
                for key in column.keys:
                    var duration: float=review_seconds(player,key,contract.states[key])
                    if cursor<duration:selected_key=key;break
                    cursor-=duration
                if contract.states[selected_key].loop:cursor=fposmod(cursor,player.cycle_seconds(selected_key))
                view.textures.append(player.frame_at_elapsed(selected_key,cursor+.001))
            view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
            root.get_texture().get_image().save_png(output+"group-%02d-%02d.png"%[group_index,sample]);captures+=1
    grid.free()
    print("MARSH CONSISTENCY NATIVE: %d states, %d source/elapsed checks, %d captures, %d failures"%[contract.states.size(),checked,captures,failures])
    quit(1 if failures else 0)
