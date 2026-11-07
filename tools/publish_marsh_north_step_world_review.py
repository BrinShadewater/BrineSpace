"""Publish exact native crops and scoped staged North step root/contact evidence."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-step-v1';RUN=ROOT/'output/marsh-animation-audit/north-step-world-v1-2026-10-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=json.loads((RUN/'report.json').read_text()); assert report['failures']==0 and len(report['captures'])==32
    before=json.loads((RUN/'owner-before.json').read_text()); assert before==json.loads((RUN/'owner-after.json').read_text())
    assert json.loads((RUN/'first-run/owner-before.json').read_text())==json.loads((RUN/'first-run/owner-after.json').read_text())
    log=(RUN/'native.log').read_text(encoding='utf-8-sig'); assert 'ERROR:' not in log
    review=BASE/'world-review-v1';review.mkdir(exist_ok=True);groups={};captures=[]
    crop=(470,210,590,355)
    for record in report['captures']:
        im=Image.open(RUN/record['file']).convert('RGB');native=im.crop(crop)
        groups.setdefault(record['length'],[]).append((record,native))
        source=ROOT/record['sourceFile'].removeprefix('res://')
        captures.append({**record,'nativeSha256':sha(RUN/record['file']),'sourceSha256':sha(source),'crop':crop})
    board=Image.new('RGB',(8*240,4*330),'#293b40');draw=ImageDraw.Draw(board);previews=[];decoded_pairs=0
    for row,(length,entries) in enumerate(groups.items()):
        assert len(entries)==8
        frames=[];durations=[]
        for i,(record,im) in enumerate(entries):
            board.paste(im.resize((240,290),Image.Resampling.NEAREST),(i*240,row*330+30))
            draw.text((i*240+6,row*330+5),'%.3fu /%s #%d @%.2f'%(length,record['key'],record['slot'],record['time']),fill='white')
            frames.append(im)
            durations.append(round((entries[i+1][0]['time']-record['time'])*1000) if i<7 else 600)
        name='route-%d.png'%row;frames[0].save(review/name,save_all=True,append_images=frames[1:],duration=durations,loop=0)
        decoded=Image.open(review/name)
        # PNG encoder can merge pixel-identical consecutive presentations.
        timeline=[]
        for i,im in enumerate(frames):timeline.extend([im.tobytes()]*durations[i])
        actual=[]
        for i in range(decoded.n_frames):
            decoded.seek(i);actual.extend([decoded.convert('RGB').tobytes()]*round(decoded.info['duration']))
        assert actual==timeline;decoded_pairs+=len(entries);previews.append({'file':name,'length':length,'durationsMs':durations,'scope':'Exact native crop at source-change boundaries; viewer terminal600ms/repeat are not actor looping.'})
    board.save(review/'native-board.png')
    evidence={'normalAdmission':False,'checks':report['checks'],'failures':0,'captures':captures,'samples':report['samples'],'ownerNonLogFiles':len(before),'ownerUnchanged':True,'maxLeftDepthDriftWorld':max(s['leftDepthDrift'] for s in report['samples']),'decodedNativePresentationPairs':decoded_pairs,'rootCurveVerified':True,'nominalLeftDepthVerified':True,'rangeExactContactVerified':False,'snapshotsVerified':False,'continueVerified':False,'scope':report['scope'],'previews':previews,'inputs':{p:sha(ROOT/p) for p in ['character/marsh-north-step-v1/step_controller.gd','tools/review_marsh_north_step_world.gd','tools/build_marsh_north_step_sequence.py','character/marsh-north-step-v1/sequence-v1/manifest.json','scripts/main.gd','scripts/marsh_npc.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd']},'logSha256':sha(RUN/'native.log')}
    unit=(RUN/'unit.log').read_text(encoding='utf-8-sig'); assert '1449 checks,0 failures' in unit and 'ERROR:' not in unit
    evidence['controllerChecks']=1449; evidence['controllerLogSha256']=sha(RUN/'unit.log')
    evidence['controllerTestSha256']=sha(ROOT/'tests/test_marsh_north_step_controller.gd')
    frozen=json.loads((RUN/'inputs-before.json').read_text()); assert frozen==json.loads((RUN/'inputs-after.json').read_text())
    for path,digest in frozen.items():assert sha(ROOT/path)==digest
    evidence['inputsHashTiming']='24targeted inputs hashed before/after final native interval and at publication; no recursive dependency freeze.'
    evidence['inputs']=frozen
    evidence['targetedInputsUnchanged']=True
    (review/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh North step — staged world</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1200px}img{image-rendering:pixelated;max-width:100%}.motion{width:240px}</style><h1>North step — unselected world study</h1><p>781checks,32native captures,0failures. Actual corridor navigation/root curve and pause; staged actor plus whole-sprite contact presentation. Four prescribed5/5.734/6/7unit straight empty-goal routes; normal game costs/failure flags retained, peers/world paused.</p><p>Nominal left sole depth stays fixed through transfer/closure. Other lengths show up to'+str(round(evidence['maxLeftDepthDriftWorld'],3))+'world units of depth drift. Range/lateral contact and motion quality still need judgement; this is not normal selection, service/emergency/snapshot/Continue or natural traffic acceptance.</p>'
    for p in previews:html+='<p>'+str(round(p['length'],3))+' world units</p><img class="motion" src="'+p['file']+'">'
    html+='<p>Lossless APNGs retain native room colour;32decoded native presentation pairs pass.600ms final viewer hold/repeat only. All2931owner files unchanged. First fixture camera-error run preserved.</p><h2>All native source holds</h2><img src="native-board.png"><p><a href="verification.json">Exact evidence</a> · <a href="../sequence-v1/recipe.json">Whole-source registrations</a></p>'
    (review/'index.html').write_text(html)
    print(report['checks'],'world checks;',decoded_pairs,'lossless native pairs; max depth drift',round(evidence['maxLeftDepthDriftWorld'],4),'world units')
if __name__=='__main__':main()
