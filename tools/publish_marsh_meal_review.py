"""Publish all eight source meal loops and actual full galley service captures."""
from pathlib import Path
import json,subprocess
import imageio_ffmpeg
from PIL import Image,ImageDraw
from publish_marsh_gesture_review import selected,registered,panel,save_webp

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-meal-review-2026-10-14'
OUT=BASE/'review'
CAP=ROOT/'output/marsh-meal-2026-10-14/after-native'

def main():
    OUT.mkdir(exist_ok=True)
    current=selected();prior=json.loads((BASE/'selected-before.json').read_text())
    cards=[]
    for key,old in prior.items():
        original=(ROOT/old['manifest'],old['metadata'],old['state'])
        frames=[]
        for i in range(6):
            canvas=Image.new('RGB',(600,294),'#26333c')
            canvas.paste(panel(registered(original,i)),(0,24))
            canvas.paste(panel(registered(current[key],i)),(300,24))
            draw=ImageDraw.Draw(canvas);draw.text((8,6),'Before',fill='white');draw.text((308,6),'Current',fill='white')
            frames.append(canvas)
        save_webp(frames,current[key][2]['frameDurationsMs'],OUT/(key+'.webp'))
        cards.append(f'<article><h3>{key}</h3><img src="{key}.webp"><p>Six holds · 900 ms source cycle</p></article>')
    report=json.loads((CAP/'report.json').read_text());assert report['failures']==0
    native=[];receipts=[]
    for case in sorted({s['direction'] for s in report['samples']}):
        samples=[s for s in report['samples'] if s['direction']==case]
        chronology=[];last=None
        with (OUT/(case+'-encode.log')).open('w') as log:
            proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-f','rawvideo','-pix_fmt','rgb24','-s','600x504','-r','25','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/(case+'.mp4'))],stdin=subprocess.PIPE,stdout=log,stderr=subprocess.STDOUT)
            for i,s in enumerate(samples):
                canvas=Image.new('RGB',(600,504),'#26333c');canvas.paste(Image.open(CAP/s['file']),(0,24))
                ImageDraw.Draw(canvas).text((8,6),s['key']+'/'+str(s['slot']),fill='white')
                proc.stdin.write(canvas.tobytes())
                if i==0:canvas.save(OUT/(case+'-poster.png'))
                tag=(s['key'],s['slot'])
                if tag!=last:chronology.append(s);last=tag
            proc.stdin.close();assert proc.wait()==0
        # First complete eating/drinking cycle plus actual final transitions.
        selected_samples=[];seen=set()
        for s in chronology:
            tag=(s['key'],s['slot'])
            if tag not in seen:selected_samples.append(s);seen.add(tag)
        selected_samples.extend(samples[-6:])
        board=Image.new('RGB',(1200,((len(selected_samples)+5)//6)*225),'#26333c')
        for i,s in enumerate(selected_samples):
            x=round(s['canvasPosition'][0]-s['region'][0]);y=round(s['canvasPosition'][1]-s['region'][1])
            left=max(0,min(400,x-100));top=max(0,min(280,y-140))
            board.paste(Image.open(CAP/s['file']).crop((left,top,left+200,top+200)),(i%6*200,i//6*225+25))
            ImageDraw.Draw(board).text((i%6*200+3,i//6*225+5),s['key']+'/'+str(s['slot']),fill='white')
        board.save(OUT/(case+'-holds.png'))
        native.append(f'<article><h3>{case}</h3><video controls loop muted preload="metadata" poster="{case}-poster.png" src="{case}.mp4"></video></article>')
        receipts.append({'case':case,'samples':len(samples),'fps':25,'selectedHolds':sorted(k+'/'+str(i) for k,i in seen)})
    html='''<!doctype html><meta charset="utf-8"><title>Marsh · eating and drinking</title><style>body{background:#142129;color:#dbe4e6;font:16px system-ui;margin:32px auto;max-width:1280px;padding:0 20px}h1,h2,h3{font-weight:550}p{max-width:990px;line-height:1.6}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(550px,1fr));gap:20px}article{background:#26333c;padding:14px;border-radius:10px}img,video{width:100%;image-rendering:pixelated}a{color:#a7d6cc}</style><h1>Marsh · eating and drinking</h1><p>South-facing bowl/spoon and mug poses now match the current ivory boots and suit. Exact current idle at both ends. Other directional drawings are retained. Each six-second meal completes seven bowl cycles; three-second drinking completes three cup cycles, ending empty-handed. Presentation follows the saved service timer.</p><h2>Actual galley playback</h2><p>Four default room rotations, reachable prescribed counter arrival, complete eating/drinking intervals and final idle. Other crew and world ticks are frozen. Native captures advance at 25 Hz; room rotation does not imply a particular character facing. This is controlled playback, not autonomous approach or a disk Continue test.</p><section>'''+''.join(native)+'''</section><h2>All directional source cycles · before / current</h2><p>900 ms source timing below. The controller fits complete cycles into the unchanged six/three-second service intervals. The small view shows a station-size reading aid.</p><section>'''+''.join(cards)+'''</section><p><a href="../../../docs/MARSH_MEAL_POLISH_2026-10-14.md">Evidence and handoff</a> · <a href="../../marsh-rest-review-2026-10-14/review/index.html">Seated and resting</a></p>'''
    html=html.replace('Four default room rotations, reachable prescribed counter arrival,', 'All four default galley contacts face north; the revised South drawings are shown in the source comparisons below. Four room rotations, reachable prescribed counter arrival,')
    (OUT/'index.html').write_text(html,encoding='utf-8')
    (OUT/'publication.json').write_text(json.dumps({'sourceStates':8,'sourceHolds':48,'native':receipts},indent=2)+'\n')
    print('Published eight source comparisons and four full native meal clips')

if __name__=='__main__':main()
