"""Publish measured source holds and real social/impact native clips locally."""
from pathlib import Path
import json
import subprocess
import imageio_ffmpeg
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-gestures-review-2026-10-14'
OUT=BASE/'review'
EVIDENCE=ROOT/'output/marsh-gestures-2026-10-14'


def resolve(parent,f):return ROOT/f[6:] if f.startswith('res://') else (parent/f).resolve()


def selected():
    c=ROOT/'character/marsh-v2/catalog.json';result={}
    for rel in json.loads(c.read_text())['body']:
        p=(c.parent/rel).resolve();m=json.loads(p.read_text())
        for s in m['states']:result[s['id']]=(p,m,s)
    return result


def registered(record,slot):
    p,m,s=record;im=Image.open(resolve(p.parent,s['frameFiles'][slot])).convert('RGBA')
    out=Image.new('RGBA',(184,237));offset=(92-round(m['pivot'][0]),172-round(m['pivot'][1]))
    bounds=im.getbbox()
    assert bounds[0]+offset[0]>=0 and bounds[1]+offset[1]>=0 and bounds[2]+offset[0]<=184 and bounds[3]+offset[1]<=237
    out.paste(im,offset);return out


def panel(im):
    out=Image.new('RGB',(300,270),'#26333c');out.paste(im,(0,12),im)
    small=im.resize((81,104),Image.Resampling.NEAREST);out.paste(small,(202,115),small)
    ImageDraw.Draw(out).text((202,235),'0.44x',fill='white');return out


def save_webp(frames,durations,path):
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,loop=0,lossless=True)


def main():
    d=selected();prior=json.loads((BASE/'selected-before.json').read_text());cards=[]
    for key,old in prior.items():
        record=d[key];s=record[2]
        frames=[panel(registered(record,i)) for i in range(len(s['frameFiles']))]
        save_webp(frames,s['frameDurationsMs'],OUT/(key+'.webp'))
        cards.append(f'<article><h3>{key}</h3><img loading="lazy" src="{key}.webp"><small>{len(frames)} holds · authored source timing</small></article>')
    key='crew-chat-south';old=prior[key];before=(ROOT/old['manifest'],old['metadata'],old['state'])
    frames=[]
    for i in range(8):
        canvas=Image.new('RGB',(600,294),'#26333c');canvas.paste(panel(registered(before,i)),(0,24));canvas.paste(panel(registered(d[key],i)),(300,24));draw=ImageDraw.Draw(canvas);draw.text((8,6),'Before',fill='white');draw.text((308,6),'Revised',fill='white');frames.append(canvas)
    save_webp(frames,d[key][2]['frameDurationsMs'],OUT/'south-chat-before-after.webp')
    old_native=json.loads((EVIDENCE/'before-native/report.json').read_text());new_native=json.loads((EVIDENCE/'after-native/report.json').read_text())
    assert old_native['failures']==new_native['failures']==0
    cases=sorted({s['direction'] for s in new_native['samples']},key=lambda k:(not k.startswith('chat-'),not k.endswith('south'),k))
    native=[];injury=[];receipts=[];ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    for case in cases:
        samples=[s for s in new_native['samples'] if s['direction']==case];old=[s for s in old_native['samples'] if s['direction']==case]
        assert len(samples)==len(old)
        for a,b in zip(samples,old):
            for field in ['key','slot','foot','canvasPosition','playerPhase','actionElapsed']:
                assert a[field]==b[field],(case,a['index'],field,a[field],b[field])
        paired=case=='chat-south';width=800 if paired else 400
        movie=OUT/('native-'+case+'.mp4');chronology=[];last=None
        with (OUT/('native-'+case+'-encode.log')).open('w') as log:
            proc=subprocess.Popen([ffmpeg,'-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x424','-r','30','-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],stdin=subprocess.PIPE,stdout=log,stderr=subprocess.STDOUT)
            for i,s in enumerate(samples):
                canvas=Image.new('RGB',(width,424),'#26333c');draw=ImageDraw.Draw(canvas)
                if paired:canvas.paste(Image.open(EVIDENCE/'before-native'/old[i]['file']),(0,24));draw.text((8,6),'Before',fill='white')
                canvas.paste(Image.open(EVIDENCE/'after-native'/s['file']),(width-400,24));draw.text((width-392,6),'Selected / '+s['key']+'/'+str(s['slot']),fill='white')
                proc.stdin.write(canvas.tobytes())
                if i==0:canvas.save(OUT/('native-'+case+'-poster.png'))
                tag=(s['key'],s['slot'])
                if tag!=last:chronology.append(s);last=tag
            proc.stdin.close();assert proc.wait()==0
        board=Image.new('RGB',(6*200,((len(chronology)+5)//6)*220),'#26333c')
        for i,s in enumerate(chronology):
            x=round(s['canvasPosition'][0]-s['region'][0]);y=round(s['canvasPosition'][1]-s['region'][1]);region=(x-100,y-145,x+100,y+45)
            assert min(region)>=0 and region[2]<=400 and region[3]<=400
            im=Image.open(EVIDENCE/'after-native'/s['file']);board.paste(im.crop(region),(i%6*200,i//6*220+25));ImageDraw.Draw(board).text((i%6*200+3,i//6*220+5),s['key']+'/'+str(s['slot']),fill='white')
        board.save(OUT/('native-'+case+'-chronology.png'))
        card=f'<article><h3>{case}'+(' · before / revised' if paired else '')+f'</h3><video controls loop muted preload="metadata" poster="native-{case}-poster.png" src="native-{case}.mp4"></video></article>'
        (native if case.startswith('chat-') else injury).append(card)
        receipts.append(dict(case=case,frames=len(samples),fps=30,pairedMovementAndPoseClockSamples=len(samples),comparisonVideo=paired))
    html='''<!doctype html><meta charset="utf-8"><title>Marsh · gestures and reactions</title><style>body{background:#142129;color:#dbe4e6;font:16px system-ui;margin:32px auto;max-width:1280px;padding:0 20px}h1,h2,h3{font-weight:550}p{max-width:960px;line-height:1.6}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}article{background:#26333c;padding:14px;border-radius:9px}img,video{width:100%;image-rendering:pixelated}small{color:#aebec5}a{color:#9bddc7}summary{cursor:pointer;padding:18px 0}</style><h1>Marsh · gestures and reactions</h1><p>The accepted swimming, locomotion and welding changes stay selected. South-facing conversation now has four matching complete gesture drawings, with current ivory boot panels, suit, face and planted stance. The four neutral holds use the exact current idle. Original 1.1-second gesture timing and social rules stay intact.</p><h2>South conversation source comparison</h2><img style="max-width:900px" src="south-chat-before-after.webp"><h2>Real conversations in the lounge</h2><p>Marsh faces an actual partner and takes his normal speaking turn. South is paired before / revised. These 30 Hz native clips skip the three-second listening wait. All four directions also passed disk save/Continue and pause checks.</p><section>'''+''.join(native)+'''</section><h2>Physical impact and recovery · retained</h2><p>Reviewed in all four directions through the normal nonfatal impact controller. The current fall, white synthetic fluid, rise and return-to-idle poses are retained.</p><section>'''+''.join(injury)+'''</section><details><summary>40 reviewed gesture / reaction / everyday source clips · 208 holds</summary><p>Source previews replay for comparison. Finite death states hold their final pose in game. Meal and tablet sources are shown unchanged; this pass revises south conversation only.</p><section>'''+''.join(cards)+'''</section></details><p><a href="../../marsh-work-review-2026-10-14/review/index.html">Accepted cargo/work pass</a> · <a href="../../../docs/MARSH_GESTURE_POLISH_2026-10-14.md">Evidence and handoff</a></p>'''
    (OUT/'index.html').write_text(html,encoding='utf-8')
    (OUT/'publication.json').write_text(json.dumps(dict(sourceStates=len(prior),sourceHolds=sum(len(v['files']) for v in prior.values()),native=receipts),indent=2)+'\n')
    print('Published40 source clips/208 holds,8 native videos and full-body south comparison')


if __name__=='__main__':main()
