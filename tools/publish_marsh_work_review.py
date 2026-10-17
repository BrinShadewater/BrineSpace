"""Local source review and bounded native torch playback for the October14 pass."""
from pathlib import Path
import json
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-work-review-2026-10-14'
OUT = BASE / 'review'
EVIDENCE = ROOT / 'output/marsh-work-2026-10-14'


def selected():
    path = ROOT / 'character/marsh-v2/catalog.json'
    result = {}
    for rel in json.loads(path.read_text())['body']:
        p = (path.parent / rel).resolve()
        m = json.loads(p.read_text())
        for s in m['states']: result[s['id']] = (p,m,s)
    return result


def registered(p,m,s,slot):
    f = s['frameFiles'][slot]
    path = ROOT / f[6:] if f.startswith('res://') else p.parent / f
    im = Image.open(path).convert('RGBA')
    out = Image.new('RGBA',(184,237))
    out.paste(im,(92-round(m['pivot'][0]),172-round(m['pivot'][1])))
    return out


def preview(frames,durations,path):
    # Fixed registered source at full density plus station-size reading aid.
    outputs=[]
    for im in frames:
        canvas=Image.new('RGB',(300,270),'#26333c')
        canvas.paste(im,(0,12),im)
        small=im.resize((81,104),Image.Resampling.NEAREST)
        canvas.paste(small,(202,115),small)
        ImageDraw.Draw(canvas).text((202,235),'0.44x',fill='white')
        outputs.append(canvas)
    outputs[0].save(path,save_all=True,append_images=outputs[1:],duration=durations,loop=0,lossless=True)


def main():
    current=selected();before=json.loads((BASE/'selected-before.json').read_text())
    endpoints=Image.new('RGB',(552,416),'#26333c')
    for row,(key,slot) in enumerate([('torch-draw-south',0),('torch-stow-south',5)]):
        old=before[key]
        prior=(ROOT/old['manifest'],old['metadata'],old['state'])
        for col,(record,index,label) in enumerate([(prior,slot,'Before / '+key),(current[key],slot,'Installed'),(current['idle-south'],0,'Current idle')]):
            pose=registered(*record,index)
            endpoints.paste(pose,(col*184,row*208+24),pose)
            ImageDraw.Draw(endpoints).text((col*184+3,row*208+4),label,fill='white')
    endpoints.save(OUT/'south-torch-endpoints.png')
    cards=[]
    for key,prior in before.items():
        p,m,s=current[key]
        frames=[registered(p,m,s,i) for i in range(len(s['frameFiles']))]
        preview(frames,s['frameDurationsMs'],OUT/(key+'.webp'))
        cards.append(f'<article><h3>{key}</h3><img loading="lazy" src="{key}.webp"><small>{len(frames)} holds · source timing</small></article>')
    cargo=[]
    for direction in ['east','west','north','south']:
        frames=[];durations=[]
        for action,repeats in [('idle',1),('pickup',1),('carry',2),('unload',1),('idle',1)]:
            p,m,s=current[action+'-'+direction]
            for repeat in range(repeats):
                slots=[0] if action=='idle' else range(len(s['frameFiles']))
                for slot in slots:
                    frames.append(registered(p,m,s,slot));durations.append(350 if action=='idle' else s['frameDurationsMs'][slot])
        preview(frames,durations,OUT/('cargo-chain-'+direction+'.webp'))
        cargo.append(f'<article><h3>{direction}</h3><img src="cargo-chain-{direction}.webp"></article>')
    previous=json.loads((EVIDENCE/'before-native/report.json').read_text())
    after=json.loads((EVIDENCE/'after-native/report.json').read_text())
    assert previous['failures']==after['failures']==0
    native=[];receipts=[]
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    for direction in ['south','east','west','north']:
        samples=[s for s in after['samples'] if s['direction']==direction]
        prior=[s for s in previous['samples'] if s['direction']==direction]
        width=800 if prior else 400
        video=OUT/('native-'+direction+'.mp4')
        with (OUT/('native-'+direction+'-encode.log')).open('w') as log:
            proc=subprocess.Popen([ffmpeg,'-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x424','-r','60','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE,stdout=log,stderr=subprocess.STDOUT)
            chronology=[];last=None
            for i,s in enumerate(samples):
                canvas=Image.new('RGB',(width,424),'#26333c');draw=ImageDraw.Draw(canvas)
                if prior:
                    canvas.paste(Image.open(EVIDENCE/'before-native'/prior[i]['file']),(0,24));draw.text((8,6),'Before',fill='white')
                    for field in ['foot','canvasPosition','key','slot','playerPhase','paused']:
                        assert s[field]==prior[i][field],(i,field)
                canvas.paste(Image.open(EVIDENCE/'after-native'/s['file']),(width-400,24));draw.text((width-392,6),'Installed / '+s['key']+'/'+str(s['slot']),fill='white')
                if i==0:canvas.save(OUT/('native-'+direction+'-poster.png'))
                proc.stdin.write(canvas.tobytes())
                key=(s['key'],s['slot'])
                if key!=last:chronology.append((s,canvas));last=key
            proc.stdin.close();assert proc.wait()==0
        board=Image.new('RGB',(6*200,((len(chronology)+5)//6)*220),'#26333c')
        for i,(s,canvas) in enumerate(chronology):
            x=round(s['canvasPosition'][0]-s['region'][0]);y=round(s['canvasPosition'][1]-s['region'][1])
            frame=Image.open(EVIDENCE/'after-native'/s['file'])
            region=(x-100,y-150,x+100,y+30)
            assert min(region)>=0 and region[2]<=400 and region[3]<=400
            board.paste(frame.crop(region),(i%6*200,i//6*220+25))
            ImageDraw.Draw(board).text((i%6*200+4,i//6*220+5),s['key']+'/'+str(s['slot']),fill='white')
        board.save(OUT/('native-'+direction+'-chronology.png'))
        receipts.append(dict(direction=direction,frames=len(samples),fps=60,paired=bool(prior)))
        native.append(f'<article><h3>{direction}'+(' · before / installed' if prior else '')+f'</h3><video controls loop muted preload="metadata" poster="native-{direction}-poster.png" src="native-{direction}.mp4"></video></article>')
    (OUT/'publication.json').write_text(json.dumps(dict(sourceStates=len(cards),sourceHolds=sum(len(s['files']) for s in before.values()),native=receipts,scope=after['scope']),indent=2)+'\n')
    html='''<!doctype html><meta charset="utf-8"><title>Marsh · cargo and work polish</title><style>body{background:#142129;color:#dbe4e6;font:16px system-ui;margin:32px auto;max-width:1280px;padding:0 20px}h1,h2,h3{font-weight:550}p{max-width:900px;line-height:1.6}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}article{background:#26333c;padding:14px;border-radius:9px}img,video{width:100%;image-rendering:pixelated}small{color:#aebec5}a{color:#9bddc7}summary{cursor:pointer;padding:18px 0}</style><h1>Marsh · cargo and work polish</h1><p>The accepted east-run fix stays selected. This pass corrects the south torch sequence's standing entry and exit: both now use his current idle body. The kneeling descent, torch grip, welding movement and rise remain intact.</p><h2>In the station</h2><p>South is paired before / installed at the same 60 Hz clock. Other directions show the current selection. Native room rendering with prescribed construction timers; this captures the visual handoffs, not autonomous job completion.</p><section>'''+''.join(native)+'''</section><h2>Pickup → carrying → unloading</h2><p>All four cargo grips and standing endpoints reviewed; retained. Source sequences below use their authored timing. The carrying root stays fixed for comparison; walking travel is supplied by the game.</p><section>'''+''.join(cargo)+'''</section><details><summary>All 44 cargo / work source clips · 232 holds</summary><section>'''+''.join(cards)+'''</section></details><p><a href="../../marsh-east-run-smooth-v1/review/index.html">Accepted east run</a> · <a href="../../../docs/MARSH_WORK_POLISH_2026-10-14.md">Evidence and handoff</a></p>'''
    html=html.replace('<h2>In the station</h2>','<details><summary>Standing endpoint comparison</summary><img style="max-width:700px" src="south-torch-endpoints.png"></details><h2>In the station</h2>')
    html=html.replace('The kneeling descent, torch grip, welding movement and rise remain intact.','The kneeling descent, torch grip, welding movement and rise remain intact. Sparks now follow the authored torch tip in every working pose instead of floating at an older body-size offset. Actual construction continues to place sparks at the doorway, as designed.')
    (OUT/'index.html').write_text(html,encoding='utf-8')
    print('Published44 source clips,4 cargo sequences and4 native videos; south204samples paired')


if __name__=='__main__': main()
