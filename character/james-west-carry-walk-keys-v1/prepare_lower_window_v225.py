from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'lower-window-v225';out.mkdir(exist_ok=True)
ledger=json.loads((p/'material-repair-progress.json').read_bytes())
def source_for(i,mode):
    return p/({40:'lower-material-phase40-v222',41:'lower-material-phase41-v223',42:'lower-material-phase42-v224'}[i])/(mode+'-head-protected.png') if i in [40,41,42] else r/ledger['states'][i]['candidateSources'][mode]['file']
baseline=json.loads((p/'master-head-review-v16/bare-manifest.json').read_bytes())['states'][0]
studies=[('local',[39,40,41,42,43])];sources=[]
for mode in ['bare','helmet']:
    states=[]
    for label,indices in studies:
        fs=[source_for(i,mode) for i in indices];sources+=fs
        states.append(dict(id='carry-'+label+'-review-west',frameCount=len(fs),frameFiles=['res://'+f.relative_to(r).as_posix() for f in fs],frameDurationsMs=[baseline['frameDurationsMs'][i] for i in indices],loop=False,sourceIndices=indices))
    (out/(mode+'-manifest.json')).write_text(json.dumps(dict(frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_two_consecutive_window_studies',states=states,scope='Lower finish phase39..43 source window only; not full49source motion or normal selection.'),indent=2)+'\n')
for label,indices in studies:
    board=Image.new('RGBA',(256*len(indices),560),(47,58,63,255));draw=ImageDraw.Draw(board);paired=[]
    for col,i in enumerate(indices):
        pair=Image.new('RGBA',(512,256))
        for row,mode in enumerate(['bare','helmet']):
            im=Image.open(source_for(i,mode)).convert('RGBA');board.alpha_composite(im,(col*256,row*280+24));draw.text((col*256+4,row*280+5),mode+' pose'+str(i),fill='white');pair.alpha_composite(im,(row*256,0))
        paired.append(pair)
    board.save(out/(label+'-source-review.png'));clock=[baseline['frameDurationsMs'][i] for i in indices]
    paired[0].save(out/(label+'-paired.apng'),save_all=True,append_images=paired[1:],duration=clock,loop=0,disposal=0,blend=0)
    with Image.open(out/(label+'-paired.apng')) as decoded:
        assert decoded.n_frames==len(indices)
        for j in range(len(indices)):
            decoded.seek(j);assert decoded.info['duration']==clock[j] and np.array_equal(np.asarray(decoded.convert('RGBA')),np.asarray(paired[j]))
program=(p/'middle-window-v63/native_probe.gd').read_text().split('func _init()',1)[0].replace('middle-window-v63','lower-window-v225').replace('carry-review-west','carry-middle-review-west').replace('consecutive middle-stride source study','staged carrying window source study')
program+='''func _init() -> void:
    print("JAMES EXTENDED WINDOWS BOOT")
    call_deferred("run")
func run() -> void:
    var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\\\","/")
    check(OS.get_user_data_dir().replace("\\\\","/").to_lower()==expected.to_lower(),"Scratch profile isolation")
    if failures or DisplayServer.get_name()=="headless":quit(2);return
    var player=load("res://scripts/crew_sprite_player.gd").new()
    player.load_manifest(BODY)
    check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired candidate loaded")
    for mode in range(2):
        var gear: String="" if mode==0 else "diving-helmet"
        var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BODY if mode==0 else HELMET))
        var rows: Dictionary=player.frames if mode==0 else player.equipment_frames[gear]
        for state in manifest.states:
            check(rows[state.id].size()==state.frameCount,"Exact window source count")
            var elapsed:=0.0
            for i in range(state.frameCount):
                var source:=Image.load_from_file(ProjectSettings.globalize_path(state.frameFiles[i]))
                var tex: Texture2D=rows[state.id][i]
                var hold:=float(state.frameDurationsMs[i])/1000.0
                check(tex.get_image().get_data()==source.get_data(),"Exact source pixels")
                check(tex.get_meta("crew_pivot")==Vector2(128,224),"Fixed physical pivot")
                check(tex.get_meta("crew_standing_height")==148.0,"Declared148 ruler")
                for offset in [.000001,hold*.5,hold-.000001]:
                    check(player.frame_at_elapsed(state.id,elapsed+offset,gear).get_image().get_data()==source.get_data(),"Exact original clock interval")
                elapsed+=hold
            check(absf(player.cycle_seconds(state.id,gear)-elapsed)<.000001,"Actual source window duration")
            check(player.frame_at_elapsed(state.id,elapsed+.001,gear).get_image().get_data()==rows[state.id][-1].get_image().get_data(),"Finite endpoint clamps")
    root.size=Vector2i(1200,320);root.content_scale_size=Vector2i.ZERO
    var board:=Board.new();board.player=player;root.add_child(board)
    DirAccess.make_dir_recursive_absolute(OUT)
    var captures:=0
    var states: Array=JSON.parse_string(FileAccess.get_file_as_string(BODY)).states
    for state in states:
        var elapsed:=0.0
        for i in range(state.frameCount):
            board.key=state.id;board.elapsed=elapsed+float(state.frameDurationsMs[i])/2000.0;board.queue_redraw()
            await process_frame
            await RenderingServer.frame_post_draw
            check(root.get_texture().get_image().save_png(OUT.path_join(state.id+"-%03d.png"%i))==OK,"Paired four-size capture")
            captures+=1;elapsed+=float(state.frameDurationsMs[i])/1000.0
    var uid_path:="res://character/james-west-carry-walk-keys-v1/lower-window-v225/native_probe.gd.uid"
    if not FileAccess.file_exists(uid_path):
        var uid_file:=FileAccess.open(uid_path,FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    var file:=FileAccess.open("res://character/james-west-carry-walk-keys-v1/lower-window-v225/native-evidence.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"Isolated consecutive middle/seam source windows, paired exact sources/clocks/rulers/pivots. Not full49 walking cycle/controller/rooms/Continue."},"  "))
    print("JAMES EXTENDED WINDOWS: %d checks, %d failures, %d captures"%[checks,failures,captures])
    quit(1 if failures else 0)
'''
(out/'native_probe.gd').write_text(program,encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
frozen=sources+[out/'native_probe.gd',out/'bare-manifest.json',out/'helmet-manifest.json',r/'scripts/crew_sprite_player.gd',r/'scripts/grid_canvas.gd',r/'character/ACTIVE_ASSETS.json']
(out/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():sha(f) for f in frozen},studies=[dict(label=l,indices=ii,clock=[baseline['frameDurationsMs'][i] for i in ii]) for l,ii in studies],decodedApngExact=True,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
print(json.dumps(dict(sourceWindows=[dict(label=l,indices=ii,clock=[baseline['frameDurationsMs'][i] for i in ii]) for l,ii in studies],pairedSources=10)))
