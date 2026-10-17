"""Publish current source rest clips and nine native furniture lifecycles locally."""
from pathlib import Path
import json,subprocess
import imageio_ffmpeg
from PIL import Image,ImageDraw
from publish_marsh_gesture_review import selected,registered,panel,save_webp,resolve

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-rest-review-2026-10-14'
OUT=BASE/'review'
EVIDENCE=ROOT/'output/marsh-rest-2026-10-14'


def main():
    current=selected();prior=json.loads((BASE/'selected-before.json').read_text());cards=[];source_pairs=[]
    for key,old in prior.items():
        record=current[key];state=record[2]
        images=[panel(registered(record,i)) for i in range(len(state['frameFiles']))]
        save_webp(images,state['frameDurationsMs'],OUT/(key+'.webp'))
        cards.append(f'<article><h3>{key}</h3><img loading="lazy" src="{key}.webp"><small>{len(images)} holds · authored source timing</small></article>')
        if key in ['sit-down-south','sit-idle-south','read-seated-south','sit-rise-south']:
            original=(ROOT/old['manifest'],old['metadata'],old['state']);frames=[]
            for i in range(len(state['frameFiles'])):
                canvas=Image.new('RGB',(600,294),'#26333c');canvas.paste(panel(registered(original,i)),(0,24));canvas.paste(images[i],(300,24));draw=ImageDraw.Draw(canvas);draw.text((8,6),'Before',fill='white');draw.text((308,6),'Revised',fill='white');frames.append(canvas)
            save_webp(frames,state['frameDurationsMs'],OUT/(key+'-comparison.webp'))
            source_pairs.append(f'<article><h3>{key}</h3><img src="{key}-comparison.webp"></article>')
    before=json.loads((EVIDENCE/'before-native/report.json').read_text());after=json.loads((EVIDENCE/'after-native/report.json').read_text())
    assert before['failures']==after['failures']==0
    cases=sorted({s['direction'] for s in after['samples']},key=lambda k:(not k.startswith('observation'),not k.startswith('crew_hab'),k))
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe();native=[];retained=[];receipts=[];changed_sources=0;changed_cases=set()
    for case in cases:
        samples=[s for s in after['samples'] if s['direction']==case];original=[s for s in before['samples'] if s['direction']==case];assert len(samples)==len(original)
        paired=case.startswith('observation');width=1200 if paired else 600
        chronology=[];last=None;selected_holds=set()
        video=OUT/(case+'.mp4')
        with (OUT/(case+'-encode.log')).open('w') as log:
            proc=subprocess.Popen([ffmpeg,'-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x504','-r','25','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE,stdout=log,stderr=subprocess.STDOUT)
            for i,s in enumerate(samples):
                old=original[i]
                for field in ['key','slot','stage','timer','foot','offset','headAlignment','canvasPosition','playerPhase','actionElapsed']:
                    assert s[field]==old[field],(case,i,field,s[field],old[field])
                # Before must actually be the frozen selected source, not another
                # old state accidentally loaded by an aggregate manifest.
                key=s['key'];expected=prior.get(key)
                record=(ROOT/expected['manifest'],expected['metadata'],expected['state']) if expected else current[key]
                p,m,state=record;expected_path=resolve(p.parent,state['frameFiles'][s['slot']])
                old_source=Image.open(EVIDENCE/'before-native'/('source-'+old['file'])).convert('RGBA')
                assert old_source.tobytes()==Image.open(expected_path).convert('RGBA').tobytes(),(case,i,'before selection')
                new_source=Image.open(EVIDENCE/'after-native'/('source-'+s['file'])).convert('RGBA')
                if old_source.tobytes()!=new_source.tobytes():changed_sources+=1;changed_cases.add(case)
                canvas=Image.new('RGB',(width,504),'#26333c');draw=ImageDraw.Draw(canvas)
                if paired:canvas.paste(Image.open(EVIDENCE/'before-native'/old['file']),(0,24));draw.text((8,6),'Before',fill='white')
                canvas.paste(Image.open(EVIDENCE/'after-native'/s['file']),(width-600,24));draw.text((width-592,6),'Selected / '+s['key']+'/'+str(s['slot']),fill='white');proc.stdin.write(canvas.tobytes())
                if i==0:canvas.save(OUT/(case+'-poster.png'))
                tag=(s['key'],s['slot']);selected_holds.add(tag)
                if tag!=last:chronology.append(s);last=tag
            proc.stdin.close();assert proc.wait()==0
        board=Image.new('RGB',(6*200,((len(chronology)+5)//6)*225),'#26333c')
        for i,s in enumerate(chronology):
            x=round(s['canvasPosition'][0]-s['region'][0]);y=round(s['canvasPosition'][1]-s['region'][1]);left=max(0,min(400,x-100));top=max(0,min(280,y-140))
            im=Image.open(EVIDENCE/'after-native'/s['file']);board.paste(im.crop((left,top,left+200,top+200)),(i%6*200,i//6*225+25));ImageDraw.Draw(board).text((i%6*200+3,i//6*225+5),s['key']+'/'+str(s['slot']),fill='white')
        board.save(OUT/(case+'-chronology.png'))
        card=f'<article><h3>{case}'+(' · before / revised' if paired else '')+f'</h3><video controls loop muted preload="metadata" poster="{case}-poster.png" src="{case}.mp4"></video></article>'
        (native if paired else retained).append(card);receipts.append(dict(case=case,frames=len(samples),fps=25,pairedMovementAndPoseClockSamples=len(samples),holds=sorted(k+'/'+str(slot) for k,slot in selected_holds)))
    html='''<!doctype html><meta charset="utf-8"><title>Marsh · seated and resting</title><style>body{background:#142129;color:#dbe4e6;font:16px system-ui;margin:32px auto;max-width:1360px;padding:0 20px}h1,h2,h3{font-weight:550}p{max-width:990px;line-height:1.6}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}article{background:#26333c;padding:14px;border-radius:9px}img,video{width:100%;image-rendering:pixelated}small{color:#aebec5}a{color:#9bddc7}summary{cursor:pointer;padding:18px 0}</style><h1>Marsh · seated and resting</h1><p>South sitting and reading now match his current ivory suit and boots. Seven complete drawings cover lowering, seated breathing and tablet reading; standing endpoints reuse exact current idle. Sit-down and stand-up share their poses in reverse. Generic south lie-down / get-up standing joins are corrected too. The accepted bunk and other directions stay selected.</p><h2>South seated sources · before / revised</h2><section>'''+''.join(source_pairs)+'''</section><h2>On the reading chairs</h2><p>Actual arrival, sitting, reading and rising at reachable observation-room furniture, four room rotations. These contacts face south. Physical foot, registered offsets and pose clocks match the before recordings. Videos use 25 Hz simulation; the long held reading interval is shortened to 1.2 seconds.</p><section>'''+''.join(native)+'''</section><h2>Current lounge and bunk · retained</h2><p>Actual north-facing lounge lifecycle in four rotations and east-facing station-prop bunk entry, rest and exit. These retain their current artwork and choreography. Held rest is shortened to 1.2 seconds. Room rotations do not imply four actor facings.</p><section>'''+''.join(retained)+'''</section><details><summary>All 34 seated / rest source clips · 120 holds</summary><p>Full source-size and small reading aids. Compatibility berth and generic rest clips are included as source reviews; only the current station-prop bunk is in the native bunk video. Source replays are viewer loops, not automatic in-game rest restarts.</p><section>'''+''.join(cards)+'''</section></details><p><a href="../../marsh-gestures-review-2026-10-14/review/index.html">Accepted gestures</a> · <a href="../../../docs/MARSH_REST_POLISH_2026-10-14.md">Evidence and handoff</a></p>'''
    (OUT/'index.html').write_text(html,encoding='utf-8')
    (OUT/'publication.json').write_text(json.dumps(dict(sourceStates=34,sourceHolds=120,native=receipts,changedNativeSources=changed_sources,changedNativeCases=sorted(changed_cases),beforeFrozenSourcesExact=True),indent=2)+'\n')
    print('Published34 source clips +4 source comparisons and9 native furniture movies;',changed_sources,'changed south reading samples')
    if (EVIDENCE/'corner-native/report.json').exists():
        from publish_marsh_lounge_contacts import main as publish_contacts
        publish_contacts()


if __name__=='__main__':main()
