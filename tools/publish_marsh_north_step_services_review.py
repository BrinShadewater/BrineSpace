"""Bind the staged service review to its native interval and submitted pixels."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/north-step-services-v1-2026-10-02'
DEST=ROOT/'character/marsh-north-step-v1/service-review-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=json.loads((RUN/'report.json').read_text())
    assert report['checks']==900 and report['failures']==0 and len(report['captures'])==128
    assert report['stagedActorRestores']==36
    owner=json.loads((RUN/'owner-before.json').read_text())
    assert owner==json.loads((RUN/'owner-after.json').read_text())
    frozen=json.loads((RUN/'inputs-before.json').read_text())
    assert frozen==json.loads((RUN/'inputs-after.json').read_text())
    for p,d in frozen.items():assert sha(ROOT/p)==d,p
    for name in ['unit.log','native.log']:
        log=(RUN/name).read_text(encoding='utf-8-sig');assert 'ERROR:' not in log
        if name=='unit.log':assert '1521 checks,0 failures' in log
    DEST.mkdir(exist_ok=True);groups={};captures=[];crop=(400,200,550,355)
    for r in report['captures']:
        native=Image.open(RUN/r['file']).convert('RGB').crop(crop)
        source=Image.open(RUN/r['sourceFile']).convert('RGBA')
        if r['key']=='walk-step-north':
            expected=Image.open(ROOT/'character/marsh-north-step-v1/sequence-v1'/('%03d.png'%r['slot'])).convert('RGBA')
            assert source.size==expected.size and source.tobytes()==expected.tobytes()
        groups.setdefault((r['work'],r['kind'],r['phase']),[]).append((r,native,source))
        captures.append({**r,'nativeSha256':sha(RUN/r['file']),'submittedSourceSha256':sha(RUN/r['sourceFile']),'crop':crop})
    available=[v for k,v in groups.items() if k[1]=='available']
    cancelled=[v for k,v in groups.items() if k[1]!='available']
    assert len(available)==4 and len(cancelled)==32
    boards=[];previews=[];pairs=0
    for label,rows,cols in [('available',available,8),('cancelled-a',cancelled[:16],3),('cancelled-b',cancelled[16:],3)]:
        board=Image.new('RGB',(cols*360,len(rows)*250),'#293b40');draw=ImageDraw.Draw(board)
        for y,entries in enumerate(rows):
            assert len(entries)==cols
            for x,(r,native,source) in enumerate(entries):
                board.paste(native,(x*360,y*250+40))
                # Submitted texture at 1:1 pixel scale. No anatomy resizing.
                matte=Image.new('RGBA',source.size,'#293b40');matte.alpha_composite(source)
                board.paste(matte.convert('RGB'),(x*360+160,y*250+40))
                draw.text((x*360+4,y*250+3),f"{r['work']} {r['kind']} {r['phase']:.2f}",fill='white')
                draw.text((x*360+4,y*250+19),f"{r['moment']} / {r['key']} #{r['slot']}",fill='white')
        name=label+'-board.png';board.save(DEST/name);boards.append(name)
        if label.startswith('cancelled'):
            for start in (0,8):board.crop((0,start*250,1080,(start+8)*250)).save(DEST/(label+'-'+str(start)+'.png'))
    for entries in available:
        frames=[e[1] for e in entries]
        times=[e[0]['clock'] if e[0]['clock']>=0 else .84 for e in entries]
        durations=[round((times[i+1]-times[i])*1000) for i in range(7)]+[600]
        name=entries[0][0]['work']+'.png'
        frames[0].save(DEST/name,save_all=True,append_images=frames[1:],duration=durations,loop=0)
        decoded=Image.open(DEST/name);expected=[];actual=[]
        for frame,ms in zip(frames,durations):expected.extend([frame.tobytes()]*ms)
        for i in range(decoded.n_frames):
            decoded.seek(i);actual.extend([decoded.convert('RGB').tobytes()]*round(decoded.info['duration']))
        assert actual==expected;pairs+=len(frames)
        previews.append({'file':name,'durationsMs':durations})
    evidence={'normalAdmission':False,'controllerChecks':1521,'nativeChecks':900,'failures':0,'cases':36,'stagedActorRestores':36,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'targetedInputs':frozen,'targetedInputsUnchanged':True,'inputsHashTiming':'24 targeted inputs frozen before/after native interval and publication; not recursive world dependency freeze.','captures':captures,'losslessNativeMotionPairs':pairs,'previews':previews,'scope':report['scope'],'normalRunSaveVerified':False,'titleContinueVerified':False,'safetyTrafficVerified':False,'logs':{n:sha(RUN/n) for n in ['unit.log','native.log']}}
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh North step service study</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1300px}img{max-width:100%;image-rendering:pixelated}.motion{width:300px}</style><h1>North short step: staged service study</h1><p>1521 controller checks;900 native checks,36 service cases,128 captures and36 binary actor restores;0 failures. Four ordinary goals arrive once, or cancel after actual room power/suspension changes at four clip phases. Cancelled work never revives. Ongoing walking cannot restart the idle-entry clip.</p><p>Unselected actor/renderer study in an actual furnished cold store. Normal failure flags retained; prescribed routes and paused peers/world. Actor-only binary restore preserves the entire snapshot and submitted pixels. Normal RunSave disk/title Continue, safety and traffic remain unverified.24 targeted input hashes and2931 owner files stayed unchanged.</p>'
    for p in previews:html+='<p>'+p['file'].removesuffix('.png')+'</p><img class="motion" src="'+p['file']+'">'
    html+='<p>Four lossless native motion previews,32 decoded presentation pairs. Measured source-change timing;600ms terminal viewer hold/repeat only. Cancellation boards are discrete before/after/finished comparisons. Every cell pairs an unscaled native crop with the exact submitted texture on a matte, also unscaled.</p>'
    for b in boards:html+='<h2>'+b.removesuffix('-board.png')+'</h2><img src="'+b+'">'
    html+='<p><a href="verification.json">Bound evidence</a> · <a href="../sequence-v1/recipe.json">Source registrations</a></p>'
    (DEST/'index.html').write_text(html)
    print('900 native /1521 controller checks;128 source/native pairs;32 lossless motion pairs;36 actor restores')
if __name__=='__main__':main()

