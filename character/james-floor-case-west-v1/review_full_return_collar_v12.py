from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageSequence

p=Path(__file__).resolve().parent
r=p.parents[1]
d=json.loads((p/'full_return_collar_v12-evidence.json').read_bytes())
inputs=json.loads((p/'full_return_collar_v12-inputs.json').read_bytes())
assert d['failures']==0
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
case=Image.open(p/'floor-case-west-v7.png').convert('RGBA')
out=p/'full-return-collar-v12-review'
out.mkdir(exist_ok=True)
decoded=0
for mode in ['bare','helmet']:
    rows=[x for x in d['results'] if x.get('label','').startswith(mode+'-')]
    motion=next(x for x in d['results'] if x.get('mode')==mode)
    frames=[]
    worlds=[]
    for i,c in enumerate(rows):
        source=Image.open(r/c['source'].removeprefix('res://')).convert('RGBA')
        assert c['height']==148
        delta=[round((c['foot'][j]-motion['fixedFoot'][j])/(65.28/148)) for j in range(2)]
        frame=Image.new('RGBA',(384,256),'#303b40')
        if c['enabled']:frame.alpha_composite(case,(64,0))
        frame.alpha_composite(source,(64+round(128-c['pivot'][0])+delta[0],round(224-c['pivot'][1])+delta[1]))
        frames.append(frame.convert('RGB'))
        worlds.append(Image.open(r/c['world'].removeprefix('res://')).convert('RGB'))
    for start in range(0,len(rows),12):
        board=Image.new('RGB',(4*384,3*410),'#303b40')
        draw=ImageDraw.Draw(board)
        for slot,c in enumerate(rows[start:start+12]):
            i=start+slot;x=slot%4*384;y=slot//4*410
            draw.text((x+4,y+4),'%02d %.3fs %s'%(i,c['time']-rows[0]['time'],c['rowId']),fill='white')
            board.paste(frames[i],(x,y+20))
            world=worlds[i].copy();world.thumbnail((380,125),Image.Resampling.NEAREST)
            board.paste(world,(x+(384-world.width)//2,y+280))
        board.save(out/('%s-%02d.png'%(mode,start)))
    durations=[round(1000*(rows[i+1]['time']-c['time'])) for i,c in enumerate(rows[:-1])]+[620]
    assert all(x>0 for x in durations)
    for name,images in [('registered',frames),('native',worlds)]:
        path=out/(mode+'-'+name+'.png')
        images[0].save(path,save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0,optimize=False)
        expected=[];holds=[]
        for im,hold in zip(images,durations):
            if expected and expected[-1].tobytes()==im.tobytes():holds[-1]+=hold
            else:expected.append(im);holds.append(hold)
        replay=Image.open(path)
        assert replay.n_frames==len(expected)
        for i,f in enumerate(ImageSequence.Iterator(replay)):
            assert f.convert('RGB').tobytes()==expected[i].tobytes()
            assert abs(f.info['duration']-holds[i])<.1
            decoded+=1
report={'nativeChecks':d['checks'],'nativeFailures':d['failures'],'pairs':sum('source' in x for x in d['results']),'inputHashes':len(inputs),'decodedRgbAndDurationChecks':decoded,'visualReviewPending':True,'timing':'Unequal source-change intervals preserve actual capture timestamps; last frame620ms viewer-only hold. Actor updates20ms.','scope':'Full prescribed East-to-West carry return, V9 bridge, revised West unload/rise, then first departure. Both gears. Not natural scheduling, normal installation or title Continue.','evidenceScopeCorrection':'Native evidence retains an obsolete no-full-V9 phrase; actual row coverage includes all admitted V9 bridge rows. This does not establish full master or smoothness acceptance.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
