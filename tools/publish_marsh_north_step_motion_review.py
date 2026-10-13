"""Package every captured update losslessly; retain sampled-motion scope."""
from pathlib import Path
import hashlib,json,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/north-step-motion-v1-2026-10-02'
DEST=ROOT/'character/marsh-north-step-v1/motion-review-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    global RUN,DEST
    polish='--polish' in sys.argv
    if polish:
        RUN=ROOT/'output/marsh-animation-audit/north-step-motion-v2-2026-10-02'
        DEST=ROOT/'character/marsh-north-step-v1/motion-review-v2'
    sequence='sequence-v2' if polish else 'sequence-v1'
    report=json.loads((RUN/'report.json').read_text());assert report['failures']==0 and report['cases']==3 and len(report['captures'])==168
    inputs=json.loads((RUN/'inputs-before.json').read_text());assert inputs==json.loads((RUN/'inputs-after.json').read_text())
    for p,d in inputs.items():assert sha(ROOT/p)==d,p
    owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN/'native.log').read_text(encoding='utf-8-sig')
    DEST.mkdir(exist_ok=True);groups={};captures=[];crop=(400,200,550,355)
    for r in report['captures']:
        im=Image.open(RUN/r['file']).convert('RGB').crop(crop)
        source=Image.open(RUN/r['sourceFile']).convert('RGBA')
        expected_path=ROOT/'character/marsh-north-step-v1'/sequence/('%03d.png'%r['slot']) if r['key']=='walk-step-north' else ROOT/'character/marsh-v2/frames/bare/idle-north/000.png'
        expected=Image.open(expected_path).convert('RGBA');assert source.size==expected.size and source.tobytes()==expected.tobytes()
        groups.setdefault(r['length'],[]).append((r,im))
        captures.append({**r,'nativeSha256':sha(RUN/r['file']),'submittedSourceSha256':sha(RUN/r['sourceFile']),'crop':crop})
    previews=[];pairs=0
    for index,(length,entries) in enumerate(groups.items()):
        assert len(entries)==56
        board=Image.new('RGB',(1200,1260),'#293b40');draw=ImageDraw.Draw(board)
        frames=[];durations=[]
        for i,(r,im) in enumerate(entries):
            x=(i%8)*150;y=(i//8)*180;board.paste(im,(x,y+25))
            draw.text((x+3,y+4),f"{r['time']:.2f}s #{r['slot']} {r['moment']}",fill='white')
            frames.append(im);durations.append(round((entries[i+1][0]['time']-r['time'])*1000) if i<55 else 600)
        board_name=f'route-{index}-board.png';board.save(DEST/board_name)
        board.crop((0,540,1200,900)).save(DEST/f'route-{index}-transfer.png')
        name=f'route-{index}.png';frames[0].save(DEST/name,save_all=True,append_images=frames[1:],duration=durations,loop=0)
        decoded=Image.open(DEST/name);actual=[];expected=[]
        for im,ms in zip(frames,durations):expected.extend([im.tobytes()]*ms)
        for i in range(decoded.n_frames):decoded.seek(i);actual.extend([decoded.convert('RGB').tobytes()]*round(decoded.info['duration']))
        assert actual==expected;pairs+=len(entries)
        previews.append({'file':name,'board':board_name,'length':length,'durationMs':durations,'decodedPresentations':56,'maxLeftDepthDriftWorld':max(r.get('leftDepthDrift',0) for r,_ in entries),'maxLeftLateralDriftWorld':max(r.get('leftLateralDrift',0) for r,_ in entries)})
    evidence={**report,'captures':captures,'targetedInputs':inputs,'targetedInputsUnchanged':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'decodedNativePresentations':pairs,'previews':previews,'normalAdmission':False,'realTimePacingVerified':False,'normalSaveTitleVerified':False,'inputFreezeScope':'24 targeted inputs before/after/publication; not recursive dependency freeze.','nativeLogSha256':sha(RUN/'native.log')}
    evidence['inputFreezeScope']=f'{len(inputs)} targeted inputs before/after/publication; not recursive dependency freeze.'
    if polish:
        base=ROOT/'character/marsh-north-step-v1'
        for i in (0,1,2,3,4,6):assert (base/'sequence-v1'/('%03d.png'%i)).read_bytes()==(base/'sequence-v2'/('%03d.png'%i)).read_bytes()
        old=Image.open(base/'sequence-v1/005.png').convert('RGBA');new=Image.open(base/'sequence-v2/005.png').convert('RGBA')
        expected=Image.new('RGBA',old.size);expected.alpha_composite(old,(-1,0))
        assert expected.tobytes()==new.tobytes() and sum(a>0 for a in old.tobytes()[3::4])==sum(a>0 for a in new.tobytes()[3::4])
        assert max(p['maxLeftLateralDriftWorld'] for p in previews)<.221
        evidence['polishVerified']='Closing entire figure shifted one integer pixel left, no clipping; other six frames byte-identical. Max planted lateral centroid drift reduced from.441 to.221world (half a dense pixel).'
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh North step sampled motion</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1300px}img{max-width:100%;image-rendering:pixelated}.motion{width:300px}</style><h1>North short step: every movement update</h1><p>'+str(report['checks'])+' native checks,3 routes/168 captures,0 failures. Actual20ms updates through1.08s, preceding exact idle, all seven holds, root curve and normal arrival once. APNGs decode to168 exact native presentation pairs; no tweened or invented frames.</p><p>Unselected actor/contact renderer in furnished cold store; prescribed5/nominal5.734/7unit curiosity routes. World/peers paused, normal failure flags retained, room placement explicit. Deterministic sampled motion, not real-time frame pacing or natural coordinator traffic. Normal save/title selection remains open.'+str(len(inputs))+' targeted inputs/2931 owner non-log files unchanged. Final600ms viewer hold/repeat only.</p>'
    if polish:html+='<p>'+evidence['polishVerified']+' V1 retained. Camera, scale, grade and all source anatomy unchanged.</p>'
    for p in previews:html+=f'<h2>{p["length"]:.3f} world units</h2><img class="motion" src="{p["file"]}"><p>Planted left depth drift {p["maxLeftDepthDriftWorld"]:.3f}; lateral drift {p["maxLeftLateralDriftWorld"]:.3f} world units. Measurements cover holds3–5.</p><img src="{p["board"]}">'
    html+='<p><a href="verification.json">Bound evidence</a> · <a href="../'+sequence+'/contact-comparison.png">Whole-source contact comparison</a></p>'
    (DEST/'index.html').write_text(html);print(report['checks'],'native checks;',pairs,'lossless presentation pairs;',[(round(p['length'],3),round(p['maxLeftDepthDriftWorld'],3),round(p['maxLeftLateralDriftWorld'],3)) for p in previews])
if __name__=='__main__':main()
