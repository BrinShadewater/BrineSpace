extends SceneTree
var checks:=0
var failures:=0
const OUT:="res://character/james-helmet-turn-dip-v1/cadence"
func check(ok:bool,why:String)->void:
    checks+=1
    if not ok:
        failures+=1
        push_error(why)
class Board extends Node2D:
    var textures:Array=[]
    var label_text:=""
    func _draw()->void:
        draw_rect(Rect2(0,0,1200,320),Color("303b40"))
        draw_string(ThemeDB.fallback_font,Vector2(12,24),label_text,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
        for mode in range(2):
            for size_index in range(4):
                var height:float=[148.0,82.0,54.0,27.0][size_index]
                var scale:float=height/148.0
                var at:=Vector2(100+size_index*150+mode*600,265)
                var tex:Texture2D=textures[mode]
                draw_texture_rect(tex,Rect2(at-Vector2(128,224)*scale,tex.get_size()*scale),false)
                draw_line(at-Vector2(40,0),at+Vector2(40,0),Color("536469"))
func _init()->void:
    call_deferred("run")
func run()->void:
    var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
    check(OS.get_user_data_dir().replace("\\","/").to_lower()==expected.to_lower(),"Scratch profile")
    if DisplayServer.get_name()=="headless":quit(2);return
    var grids:Array=[]
    var players:Array=[]
    for mode in range(2):
        var grid=load("res://scripts/grid_canvas.gd").new()
        grid._load_replacement_crew_animations()
        grids.append(grid)
        players.append(grid.branforth_player)
    root.size=Vector2i(1200,320)
    root.content_scale_size=Vector2i.ZERO
    var board:=Board.new()
    root.add_child(board)
    DirAccess.make_dir_recursive_absolute(OUT)
    var report:={"cases":[],"scope":"Normal factory/player frame dispatch at prescribed20ms simulation samples. Fixed world root while turning, short walking departure. No actual actor scheduler/room/priority/continuous-watched acceptance."}
    var captures:=0
    for pair in [["south","west"],["west","south"],["east","west"],["west","east"]]:
        var key:String="carry-turn-"+pair[0]+"-"+pair[1]
        var duration:float=players[0].cycle_seconds(key)
        var records:Array=[]
        var previous_hashes:Array=["",""]
        for mode in range(2):
            var player=players[mode]
            var gear:String="" if mode==0 else "diving-helmet"
            player.current_key=""
            player.motion.clear()
            player.frame("carry",pair[0],0.0,Vector2.ZERO,gear,true)
            player.frame("carry",pair[0],0.2,Vector2(.05,0),gear,true)
            # Trigger the turn at the declared origin before epsilon sampling.
            # Otherwise motion.started includes the first sample's epsilon.
            var first:Texture2D=player.frame("carry",pair[1],.3,Vector2(.06,0),gear,true)
            check(first==player.frame_at_elapsed(key,0.0,gear),"Turn starts at authored frame0")
        var steps:=int(round(duration/.02))+7
        for step in range(steps):
            var elapsed:float=step*.02+.0001
            var textures:Array=[]
            var hashes:Array=[]
            var indices:Array=[]
            var pos:=Vector2(.06,0) if elapsed<duration else Vector2(.06+(elapsed-duration)*.2,0)
            for mode in range(2):
                var player=players[mode]
                var gear:String="" if mode==0 else "diving-helmet"
                var tex:Texture2D=player.frame("carry",pair[1],.3+elapsed,pos,gear,true)
                check(tex!=null,"Normal frame returned")
                textures.append(tex)
                var rows:Dictionary=player.frames if mode==0 else player.equipment_frames[gear]
                var row:Array=rows[key] if elapsed<duration else rows["carry-"+pair[1]]
                var index:=-1
                for i in range(row.size()):
                    if tex==row[i]:index=i;break
                check(index>=0,"Actual source belongs to finite turn or destination carry")
                if elapsed<duration:
                    var authored:Texture2D=player.frame_at_elapsed(key,elapsed,gear)
                    check(tex.get_image().get_data()==authored.get_image().get_data(),"Dispatch clock matches authored turn")
                    check(str(player.motion.clip)==key,"Finite turn remains active")
                else:
                    check(str(player.motion.clip).is_empty(),"Finite turn clears at departure")
                    if step==int(round(duration/.02)):
                        check(index==0,"Departure starts destination gait0")
                indices.append(index)
                var hasher:=HashingContext.new()
                hasher.start(HashingContext.HASH_SHA256)
                hasher.update(tex.get_image().get_data())
                hashes.append(hasher.finish().hex_encode())
            var record:={"step":step,"elapsed":elapsed,"indices":indices,"rgbaSha256":hashes,"positionCells":[pos.x,pos.y]}
            if hashes!=previous_hashes or step==int(round(duration/.02))-1:
                board.textures=textures
                board.label_text="James normal turn dispatch / "+key+" / %.4fs"%elapsed
                board.queue_redraw()
                await process_frame
                await RenderingServer.frame_post_draw
                var name:String=key+"-%03d.png"%step
                check(root.get_texture().get_image().save_png(OUT.path_join(name))==OK,"Native cadence capture")
                record["capture"]=name
                captures+=1
            records.append(record)
            previous_hashes=hashes
        report.cases.append({"key":key,"duration":duration,"samples":records})
    report["checks"]=checks
    report["failures"]=failures
    report["captures"]=captures
    var file:=FileAccess.open(OUT.path_join("evidence.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"  "))
    for grid in grids:grid.free()
    print("JAMES NORMAL CADENCE: %d checks, %d failures, %d paired captures"%[checks,failures,captures])
    quit(1 if failures else 0)
