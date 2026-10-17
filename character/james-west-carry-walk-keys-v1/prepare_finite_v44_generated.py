from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'finite-handoff-v44';out.mkdir(exist_ok=True)
refs={m:[r/('character/james-carry-'+('headcaps' if m=='bare' else 'authored-helmet')+'-v1/frames/004.png'),p/'coherent-turn-v40'/(m+'-candidate.png'),p/'whole-belt-admission-v35'/(m+'-candidate.png')] for m in ['bare','helmet']}
clock=[70,70,70]
for mode,files in refs.items():
    paths=['res://'+f.relative_to(r).as_posix() for f in files]
    states=[dict(id='carry-prepare-west',frameCount=3,frameFiles=paths,frameDurationsMs=clock,loop=False),dict(id='carry-unprepare-west',frameCount=3,frameFiles=list(reversed(paths)),frameDurationsMs=list(reversed(clock)),loop=False,derivedFrom='Explicit reverse of preparation study, not case unloading.')]
    pack=dict(name='James coherent carrying preparation study '+mode,frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,status='staged_motion_review_pending',states=states,scope='V40 coherent turn anatomy; three finite preparation sources then distance walk0. No normal adoption.')
    (out/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
frames=[]
for i in range(3):
    im=Image.new('RGBA',(512,282),(48,59,63,255));draw=ImageDraw.Draw(im)
    for col,mode in enumerate(refs):
        im.alpha_composite(Image.open(refs[mode][i]).convert('RGBA'),(col*256,26));draw.text((col*256+4,7),mode+' / preparation '+str(i),fill='white')
    frames.append(im)
frames[0].save(out/'paired-prepare.apng',save_all=True,append_images=frames[1:],duration=clock,loop=0,disposal=0,blend=0)
with Image.open(out/'paired-prepare.apng') as im:
    assert im.n_frames==3
    for i,f in enumerate(frames):im.seek(i);assert im.convert('RGBA').tobytes()==f.tobytes() and im.info['duration']==clock[i]
walk=json.loads((p/'master-head-review-v16/bare-manifest.json').read_bytes())['states'][0]['frameDurationsMs'];journey=frames[:3];jclock=clock[:3]+walk
for i in range(49):
    im=Image.new('RGBA',(512,282),(48,59,63,255));draw=ImageDraw.Draw(im)
    for col,mode in enumerate(refs):
        im.alpha_composite(Image.open(p/'master-head-review-v16'/(mode+'-%03d.png'%i)).convert('RGBA'),(col*256,26));draw.text((col*256+4,7),mode+' / original walk '+str(i),fill='white')
    journey.append(im)
journey[0].save(out/'paired-start-and-walk.apng',save_all=True,append_images=journey[1:],duration=jclock,loop=0,disposal=0,blend=0)
with Image.open(out/'paired-start-and-walk.apng') as im:
    assert im.n_frames==52
    for i,f in enumerate(journey):im.seek(i);assert im.convert('RGBA').tobytes()==f.tobytes() and im.info['duration']==jclock[i]
program=(p/'finite-bridge-v36/native_probe.gd').read_text(encoding='utf-8').replace('finite-bridge-v36','finite-handoff-v44')
prefix,body=program.split('func _init()',1)
body=body.replace('range(4)','range(3)').replace('size()==4','size()==3').replace('Four authored slots','Three authored slots').replace('-.25)','-.21)').replace('250ms','210ms').replace('.251','.211').replace('[3-i]','[2-i]').replace('eight paired','six paired').replace('four-pose','three-pose').replace('    ','\t')
program=prefix+'func _init()'+body
extra="""	# At210ms hand off to distance-driven walk0, rather than replaying its40ms.
	player.load_manifest("res://character/james-west-carry-walk-keys-v1/master-head-review-v16/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/james-west-carry-walk-keys-v1/master-head-review-v16/helmet-manifest.json"),"Walking pair appended")
	check(absf(player.cycle_seconds("carry-prepare-west")+player.cycle_seconds("carry-west")-1.89)<.000001,"Runtime study equals1890ms source preview")
	var handoff_samples:=0
	for equipment in ["","diving-helmet"]:
		var row: Array=player.frames["carry-west"] if equipment.is_empty() else player.equipment_frames[equipment]["carry-west"]
		check(player.frame("carry","west",.21,Vector2.ZERO,equipment)==row[0],"Walk0 begins at210ms")
		var elapsed:=0.0
		for slot in range(49):
			var distance: float=.1796875*(elapsed+.000001)/1.68
			var tex: Texture2D=player.frame("carry","west",.21+elapsed+.000001,Vector2(-distance,0),equipment)
			check(tex==row[slot],"Exact chronological distance source after handoff")
			if slot==1:check(absf(.21+elapsed-.25)<.000001,"Walk1 begins at250ms without duplicate walk0")
			handoff_samples+=1
			elapsed+=float(player.timing["carry-west"].durations[slot])/1000.0
"""
program=program.replace('\tvar uid_path:=',extra+'\tvar uid_path:=')
program=program.replace('"captures":captures,','"captures":captures,"handoffSourceSamples":handoff_samples,"handoffMs":210,"journeyMs":1890,')
program=program.replace('\t','    ')
(out/'native_probe.gd').write_text(program,encoding='utf-8')
files=[f for bank in refs.values() for f in bank]+[out/(m+'-manifest.json') for m in refs]+[Path(__file__),out/'native_probe.gd',r/'scripts/grid_canvas.gd',r/'character/ACTIVE_ASSETS.json']
(out/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},sourcePoses=3,preparationMs=210,walkSourceFrames=49,walkMs=sum(walk),journeyFrames=52,journeyMs=sum(jclock),previewDecodedExact=True,normalChanged=False),indent=2)+'\n')
print('V44 three-source210ms study and exact52-frame1890ms chronology prepared; native program included in frozen inputs.')
