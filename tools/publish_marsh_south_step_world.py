"""Publish bounded native South step motion and actor-only restoration evidence."""
from pathlib import Path
import hashlib,json,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-step-v1'
RUN=ROOT/'output/marsh-animation-audit/south-step-world-v1-2026-10-02'
OUT=BASE/'world-review-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    report=read(RUN/'report.json');assert report['checks']==874 and report['failures']==0
    assert len(report['captures'])==44 and report['stagedActorRestores']==6
    frozen=read(RUN/'inputs-before.json');assert frozen==read(RUN/'inputs-after.json')
    for path,digest in frozen.items():assert sha(ROOT/path)==digest
    owner=read(RUN/'owner-before.json');assert owner==read(RUN/'owner-after.json')
    log=(RUN/'godot.log').read_text(encoding='utf-8-sig');assert 'ERROR:' not in log
    unit=ROOT/'output/marsh-animation-audit/south-step-controller-v1-2026-10-02'
    unitlog=(unit/'godot.log').read_text(encoding='utf-8-sig')
    assert '1526 checks,0 failures' in unitlog and 'ERROR:' not in unitlog
    assert read(unit/'owner-before.json')==read(unit/'owner-after.json')
    OUT.mkdir(exist_ok=True);crop=(415,200,525,325)
    records=[];route_board=Image.new('RGB',(8*220,4*280),'#293b40');draw=ImageDraw.Draw(route_board)
    restore_board=Image.new('RGB',(2*220,6*280),'#293b40');restore_draw=ImageDraw.Draw(restore_board)
    previews=[];groups=[]
    for index,row in enumerate(report['captures']):
        native=RUN/row['file'];source=RUN/row['sourceFile']
        canonical=BASE/'candidate-05'/f"{row['slot']:03d}.png" if row['key']=='walk-step-south' else ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png'
        assert Image.open(source).convert('RGBA').tobytes()==Image.open(canonical).convert('RGBA').tobytes()
        im=Image.open(native).convert('RGB');assert im.size==(1600,900)
        tile=im.crop(crop)
        records.append(dict(row,crop=crop,nativeSha256=sha(native),sourceSha256=sha(source),canonicalSha256=sha(canonical)))
        if index<32:
            y,x=divmod(index,8);route_board.paste(tile.resize((220,250),Image.Resampling.NEAREST),(220*x,280*y+25))
            draw.text((220*x+4,280*y+4),row['label']+' /'+str(row['slot']),fill='white')
            if x==0:groups.append([])
            groups[-1].append((row,tile))
        else:
            y,x=divmod(index-32,2);restore_board.paste(tile.resize((220,250),Image.Resampling.NEAREST),(220*x,280*y+25))
            restore_draw.text((220*x+4,280*y+4),row['label']+' /'+str(row['slot']),fill='white')
    for index,entries in enumerate(groups):
        times=[float(re.search(r't([\d.]+)$',row['label']).group(1)) for row,im in entries]
        durations=[round((times[i+1]-times[i])*1000) for i in range(7)]+[600]
        frames=[im for row,im in entries];name=f'route-{index}.png'
        frames[0].save(OUT/name,save_all=True,append_images=frames[1:],duration=durations,loop=0)
        decoded=Image.open(OUT/name);expected=[];actual=[]
        for frame,duration in zip(frames,durations):expected.extend([frame.tobytes()]*duration)
        for frame_index in range(decoded.n_frames):
            decoded.seek(frame_index);actual.extend([decoded.convert('RGB').tobytes()]*round(decoded.info['duration']))
        assert actual==expected
        previews.append({'file':name,'durationsMs':durations,'scope':'Native source-change boundary crop. Final600ms and repeat are viewer behavior only.'})
    route_board.save(OUT/'native-board.png');restore_board.save(OUT/'restore-board.png')
    lateral=[]
    for length in sorted({row['length'] for row in report['samples']}):
        rows=[row for row in report['samples'] if row['length']==length and row['active']]
        right=[row['rightContact'][0] for row in rows if row['slot']<4]
        left=[row['leftContact'][0] for row in rows if row['slot']>=4]
        lateral.append({'length':length,'rightSupportLateralRangeWorld':max(right)-min(right),'leftSupportLateralRangeWorld':max(left)-min(left)})
    evidence={'normalAdmission':False,'worldChecks':874,'controllerChecks':1526,'failures':0,'engineErrors':0,'exitCodes':[0,0],'captures':records,'samples':report['samples'],'stagedActorRestores':6,'rootCurveVerified':True,'supportDepthVerified':True,'lateralSupportRanges':lateral,'targetedInputs':frozen,'inputsStable':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'visualReview':'pending','previews':previews,'nativeLogSha256':sha(RUN/'godot.log'),'controllerLogSha256':sha(unit/'godot.log'),'unitInputFreeze':'No pre-run source inventory for controller-only interval; native interval freezes same controller/test plus runtime/source inputs before and after. Owner fingerprints bracket both intervals.','scope':report['scope'],'fullRunSave':False,'titleContinue':False,'limits':['Mixed widths/face/arms/material details remain provisional.','Closing right boot ends3.5dense inward; supporting-foot centroid quantization remains.','Prescribed ordinary empty-goal routes with peers paused; natural traffic and real service/emergency priorities remain unproven.']}
    (OUT/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='''<!doctype html><meta charset="utf-8"><title>Marsh South step staged world</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1400px}img{image-rendering:pixelated;max-width:100%}.motion{width:220px}</style><h1>South short-step staged physical study</h1><p>1526 controller checks;874 native world checks;44 exact source/native pairs;six actor-only binary restores;zero failures.100 targeted native inputs and2931 owner files unchanged. Normal catalog stays unselected.</p><p>Four prescribed5/5.734/6/7world-unit routes use actual furnished Cold Store navigation and normal grid playback. Root advances during reach while whole-sprite offset holds support; left support depth stays fixed during plant/closure. Small lateral contact shifts and broader reach/identity joins remain visible. Peers paused. This does not prove natural traffic, service/emergency priorities, full RunSave or Title Continue.</p>'''
    for preview in previews:html+='<img class="motion" src="'+preview['file']+'">'
    html+='<p>Lossless native boundary animations;600ms terminal viewer hold/repeat only. No temporal interpolation added.</p><h2>All native source holds</h2><img src="native-board.png"><h2>Before/after staged actor restores</h2><img src="restore-board.png"><p><a href="verification.json">Exact evidence and contact samples</a></p>'
    (OUT/'index.html').write_text(html,encoding='utf-8')
    print(json.dumps({'checks':[1526,874],'pairs':44,'restores':6,'inputsStable':len(frozen),'ownerUnchanged':len(owner),'lateralRanges':lateral}))
if __name__=='__main__':main()
