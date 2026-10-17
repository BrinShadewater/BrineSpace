from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageSequence
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'motion_rise_v5-evidence.json').read_bytes())
inputs=json.loads((p/'motion_rise_v5-inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
case=Image.open(p/'floor-case-west-v6.png').convert('RGBA')
decoded=0
for mode in ['bare','helmet']:
    records=[c for c in data['results'] if c.get('label','').startswith(mode+'-')]
    motion=next(c for c in data['results'] if c.get('motion') and c['mode']==mode)
    assert len(records)==45
    pages=[];frames=[];worlds=[]
    for i,c in enumerate(records):
        assert c['height']==148
        if i:assert abs(c['time']-records[i-1]['time']-.02)<1e-8
        source=Image.open(r/c['source'].removeprefix('res://')).convert('RGBA')
        delta=[round((c['foot'][j]-motion['fixedFoot'][j])/(65.28/148)) for j in range(2)]
        composite=Image.new('RGBA',(320,256),(48,59,64,255))
        if c['enabled']:composite.alpha_composite(case,(32,0))
        pivot=c['pivot'];composite.alpha_composite(source,(32+round(128-pivot[0])+delta[0],round(224-pivot[1])+delta[1]))
        world=Image.open(r/c['world'].removeprefix('res://')).convert('RGB');worlds.append(world)
        frame=Image.new('RGB',(max(320,world.width),286+world.height),'#303b40');draw=ImageDraw.Draw(frame)
        draw.text((6,6),mode+' sample%02d / %.3fs'%(i,c['time']-records[0]['time']),fill='white')
        frame.paste(composite.convert('RGB'),((frame.width-320)//2,26))
        frame.paste(world,((frame.width-world.width)//2,286))
        frames.append(frame)
    for start in [0,15,30]:
        board=Image.new('RGB',(5*320,3*410),'#303b40');draw=ImageDraw.Draw(board)
        for slot,c in enumerate(records[start:start+15]):
            i=start+slot;x=(slot%5)*320;y=(slot//5)*410
            draw.text((x+4,y+4),'%02d / %.3fs / %s'%(i,c['time']-records[0]['time'],'prop' if c['enabled'] else 'embedded' if c['embedded'] else 'held'),fill='white')
            # Presentation crops from already registered composite, source retained.
            board.paste(frames[i].crop(((frames[i].width-320)//2,26,(frames[i].width+320)//2,282)),(x,y+20))
            world=worlds[i].copy();world.thumbnail((310,125),Image.Resampling.NEAREST)
            board.paste(world,(x+(320-world.width)//2,y+280))
        board.save(p/(mode+'-motion-rise-v5-%02d-review.png'%start))
    # 45actual samples/20ms; final source is shown20ms plus600ms viewer-only hold.
    durations=[20]*44+[620]
    for label,images in [('registered',frames),('native',worlds)]:
        path=p/(mode+'-motion-rise-v5-'+label+'.png')
        images[0].save(path,save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0,optimize=False)
        replay=Image.open(path)
        for index,decoded_frame in enumerate(ImageSequence.Iterator(replay)):
            assert decoded_frame.convert('RGB').tobytes()==images[index].tobytes()
            assert abs(decoded_frame.info['duration']-durations[index])<.1
            decoded+=1
        assert replay.n_frames==45
(p/'motion-rise-v5-review.json').write_text(json.dumps({'selected':False,'visualReviewPending':True,'nativeSourceWorldPairs':90,'losslessApngDecodedChecks':decoded,'targetedInputsUnchanged':len(inputs),'sampleSeconds':.02,'viewerOnlyTerminalHoldMilliseconds':600,'loopSemantics':'Viewer reset repeats finite excerpt; actor motion is not authored looping.','registration':'Upper registered source/prop composite at fixed physical contact; lower actual fixed-camera native pixels. Native-only APNG contains original room pixels without resampling or palette conversion.','scope':data['scope']},indent=2)+'\n')
print('Six45sample review boards;4losslessAPNGs;'+str(decoded)+' decoded RGB/duration checks;'+str(len(inputs))+'targeted hashes unchanged.')
