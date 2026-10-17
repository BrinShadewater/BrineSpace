from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'middle-window-v60';out.mkdir(exist_ok=True)
folders=[p/'master-material-phase23-v58',p/'case-grip-material-phase24-v57',p/'master-material-phase25-v59'];clock=[40,40,40];frames=[]
for mode in ['bare','helmet']:
    fs=[folder/(mode+('-candidate.png' if i==1 else '-head-protected.png')) for i,folder in enumerate(folders)]
    paths=['res://'+f.relative_to(r).as_posix() for f in fs];frames+=fs
    manifest=dict(frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_three_consecutive_pose_study',states=[dict(id='carry-review-west',frameCount=3,frameFiles=paths,frameDurationsMs=clock,loop=False)],scope='Source poses23/24/25,120ms middle window only; not full walk.')
    (out/(mode+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
paired=[];board=Image.new('RGBA',(768,560),(47,58,63,255));draw=ImageDraw.Draw(board)
for i in range(3):
    im=Image.new('RGBA',(512,256));im.alpha_composite(Image.open(frames[i]).convert('RGBA'));im.alpha_composite(Image.open(frames[i+3]).convert('RGBA'),(256,0));paired.append(im)
    for row in range(2):
        board.alpha_composite(Image.open(frames[i+row*3]).convert('RGBA'),(i*256,row*280+24));draw.text((i*256+5,row*280+5),('bare' if row==0 else 'helmet')+' pose'+str(i+23),fill='white')
board.save(out/'consecutive-source-review.png')
paired[0].save(out/'paired-middle-window.apng',save_all=True,append_images=paired[1:],duration=clock,loop=0,disposal=0,blend=0)
with Image.open(out/'paired-middle-window.apng') as decoded:
    assert decoded.n_frames==3
    for i in range(3):
        decoded.seek(i);assert decoded.info['duration']==40 and np.array_equal(np.asarray(decoded.convert('RGBA')),np.asarray(paired[i]))
program=(p/'finite-handoff-v44/native_probe.gd').read_text().split('func _init()',1)[0]
program=program.replace('finite-handoff-v44','middle-window-v60').replace('carry-prepare-west','carry-review-west').replace('staged finite carrying preparation','consecutive middle-stride source study')
program+='''func _init() -> void:
    print("JAMES MIDDLE WINDOW BOOT")
    call_deferred("run")
func run() -> void:
    var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\\\","/")
    check(OS.get_user_data_dir().replace("\\\\","/").to_lower()==expected.to_lower(),"Scratch profile isolation")
    if failures or DisplayServer.get_name()=="headless":quit(2);return
    var player=load("res://scripts/crew_sprite_player.gd").new()
    player.load_manifest(BODY)
    check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired candidate load")
    for mode in range(2):
        var gear: String="" if mode==0 else "diving-helmet"
        var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BODY if mode==0 else HELMET))
        var rows: Dictionary=player.frames if mode==0 else player.equipment_frames[gear]
        check(rows["carry-review-west"].size()==3,"Three consecutive source slots")
        check(absf(player.cycle_seconds("carry-review-west",gear)-.12)<.000001,"Original120ms window")
        var state: Dictionary=manifest.states[0]
        for i in range(3):
            var source:=Image.load_from_file(ProjectSettings.globalize_path(state.frameFiles[i]))
            var tex: Texture2D=rows[state.id][i]
            check(tex.get_image().get_data()==source.get_data(),"Exact source pixels")
            check(tex.get_meta("crew_pivot")==Vector2(128,224),"Fixed physical pivot")
            check(tex.get_meta("crew_standing_height")==148.0,"Declared148 ruler")
            for offset in [.000001,.02,.039999]:
                check(player.frame_at_elapsed(state.id,i*.04+offset,gear).get_image().get_data()==source.get_data(),"Exact original clock interval")
        check(player.frame_at_elapsed(state.id,.121,gear).get_image().get_data()==rows[state.id][-1].get_image().get_data(),"Finite window endpoint")
    root.size=Vector2i(1200,320);root.content_scale_size=Vector2i.ZERO
    var board:=Board.new();board.player=player;root.add_child(board)
    DirAccess.make_dir_recursive_absolute(OUT)
    var captures:=0
    for i in range(3):
        board.elapsed=i*.04+.02;board.queue_redraw()
        await process_frame
        await RenderingServer.frame_post_draw
        check(root.get_texture().get_image().save_png(OUT.path_join("middle-%03d.png"%i))==OK,"Four-size paired capture")
        captures+=1
    var uid_path:="res://character/james-west-carry-walk-keys-v1/middle-window-v60/native_probe.gd.uid"
    if not FileAccess.file_exists(uid_path):
        var uid_file:=FileAccess.open(uid_path,FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    var file:=FileAccess.open("res://character/james-west-carry-walk-keys-v1/middle-window-v60/native-evidence.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"windowMs":120,"scope":"Isolated consecutive staged poses23/24/25, paired exact sources/clocks/rulers/pivots. Not full walk/controller/room/Continue."},"  "))
    print("JAMES MIDDLE WINDOW: %d checks, %d failures, %d captures"%[checks,failures,captures])
    quit(1 if failures else 0)
'''
(out/'native_probe.gd').write_text(program,encoding='utf-8')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
frozen=frames+[out/'native_probe.gd',out/'bare-manifest.json',out/'helmet-manifest.json',r/'scripts/crew_sprite_player.gd',r/'scripts/grid_canvas.gd',r/'character/ACTIVE_ASSETS.json']
(out/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():sha(f) for f in frozen},indices=[23,24,25],clock=clock,decodedApngExact=True,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
print('Consecutive120ms source window and native fixture prepared; exact APNG decode passed.')
