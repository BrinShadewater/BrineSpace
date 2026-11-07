"""Review retained cargo/turn/water clips without modifying selected artwork."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageDraw
import imageio_ffmpeg
from publish_marsh_gesture_review import selected,resolve,save_webp

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-remaining-review-2026-10-14'
OUT=BASE/'review'
EVIDENCE=ROOT/'output/marsh-remaining-2026-10-14'

def registered(record,slot):
    p,m,s=record;im=Image.open(resolve(p.parent,s['frameFiles'][slot])).convert('RGBA')
    out=Image.new('RGBA',(224,237));offset=(112-round(m['pivot'][0]),172-round(m['pivot'][1]))
    box=im.getbbox()
    assert box[0]+offset[0]>=0 and box[1]+offset[1]>=0 and box[2]+offset[0]<=224 and box[3]+offset[1]<=237
    out.paste(im,offset);return out

def panel(im):
    out=Image.new('RGB',(350,265),'#26333c');out.paste(im,(0,16),im)
    small=im.resize((99,104),Image.Resampling.NEAREST);out.paste(small,(245,115),small)
    return out

def main():
    OUT.mkdir(exist_ok=True);d=selected();prior=json.loads((BASE/'selected-before.json').read_text())
    groups={'Cargo swimming and return':[],'Carrying turns':[],'Water reactions':[],'Retained compatibility clips':[]}
    hashes=0;joins=0
    for key,old in prior.items():
        p,m,s=d[key]
        assert s==old['state'] and {k:v for k,v in m.items() if k!='states'}==old['metadata']
        for i,f in enumerate(s['frameFiles']):
            assert hashlib.sha256(resolve(p.parent,f).read_bytes()).hexdigest()==old['files'][i]['sha256'];hashes+=1
        images=[panel(registered(d[key],i)) for i in range(len(s['frameFiles']))]
        save_webp(images,s['frameDurationsMs'],OUT/(key+'.webp'))
        group='Cargo swimming and return' if key.startswith(('swim-pickup-','swim-carry-','cargo-drain-')) else 'Carrying turns' if key.startswith('carry-turn-') else 'Retained compatibility clips' if key.startswith(('equip-helmet-','remove-helmet-','recover-air-')) else 'Water reactions'
        kind='Loop' if s['loop'] else 'Finite action · viewer replay'
        groups[group].append(f'<article><h3>{key}</h3><img loading="lazy" src="{key}.webp"><p>{kind} · {len(images)} holds · {sum(s["frameDurationsMs"]):g} ms</p></article>')
    for direction in ['east','west','north','south']:
        for a,i,b,j in [('swim-pickup-'+direction,0,'idle-'+direction,0),('swim-pickup-'+direction,-1,'swim-carry-'+direction,0),('cargo-drain-'+direction,0,'swim-carry-'+direction,0),('cargo-drain-'+direction,-1,'carry-'+direction,0)]:
            assert registered(d[a],i).tobytes()==registered(d[b],j).tobytes();joins+=1
    for key in prior:
        if key.startswith(('carry-turn-','swim-carry-turn-')):
            family='swim-carry' if key.startswith('swim-') else 'carry';a,b=key.split('-')[-2:]
            assert registered(d[key],0).tobytes()==registered(d[family+'-'+a],0).tobytes()
            assert registered(d[key],-1).tobytes()==registered(d[family+'-'+b],0).tobytes();joins+=2
    chains=[]
    for direction in ['east','west','north','south']:
        frames=[];durations=[]
        for key,repeats in [('swim-pickup-'+direction,1),('swim-carry-'+direction,2),('cargo-drain-'+direction,1),('carry-'+direction,2),('cargo-unload-'+direction,1),('idle-'+direction,1)]:
            p,m,s=d[key]
            for repeat in range(repeats):
                frames.extend(panel(registered(d[key],i)) for i in range(len(s['frameFiles'])));durations.extend(s['frameDurationsMs'])
        save_webp(frames,durations,OUT/('chain-'+direction+'.webp'))
        chains.append(f'<article><h3>{direction} · complete cargo source chain</h3><img src="chain-{direction}.webp"></article>')
    captures=sorted((EVIDENCE/'loaded-turns').glob('frame-*.png'))
    assert len(captures)==108
    with (EVIDENCE/'native-encode.log').open('w') as log:
        proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-framerate','24','-i',str(EVIDENCE/'loaded-turns/frame-%03d.png'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'native-loaded-turns.mp4')],stdout=log,stderr=subprocess.STDOUT);assert proc.wait()==0
    Image.open(captures[8]).save(OUT/'native-loaded-turns-poster.png')
    board=Image.new('RGB',(960*2,460*6),'#26333c')
    for i,n in enumerate([0,5,12,23,24,29,36,47,48,53,60,71]):board.paste(Image.open(captures[n]),((i%2)*960,(i//2)*460))
    board.save(OUT/'native-turn-holds.png')
    native='''<h2>Native cargo turn selection</h2><p>Current game player selects all 12 directed cargo swimming turns and all 76 turn holds, then plays the four loaded loops. The turn grid advances each column through normalized progress; columns can have different source durations. Use individual source clips for authored timing. This is sampled native player playback, not real-time FPS evidence.</p><video controls muted loop preload="metadata" poster="native-loaded-turns-poster.png" src="native-loaded-turns.mp4"></video>'''
    expedition=json.loads((EVIDENCE/'expedition/report.json').read_text())
    assert expedition['failures']==0 and len(expedition['journeys'])==1
    journey=expedition['journeys'][0]
    assert len(journey['phases'])==12 and len(journey['pickup_frames'])==6 and len(journey['drain_frames'])==5 and len(journey['unload_frames'])==4
    native+='<h2>In-game cargo delivery check</h2><p>The actual rotation-zero expedition passes dispatch, all 12 phases, six pickup poses, loaded return turns, five drainage poses, four unload poses and one delivery credit. Loaded and draining checkpoints restore through the game save reader. This is one controlled journey; it does not certify every route or rotation.</p>'
    sections=''
    for title,cards in groups.items():
        note='<p>Marsh is a sealed android: normal play does not select helmet equip/removal, air recovery or low-air distress. These legacy clips stay retained for compatibility; no oxygen or helmet behavior is enabled.</p>' if title=='Retained compatibility clips' else ''
        if title=='Water reactions':note='<p>Treading and water shutdown retain their current drawings. Low-air distress is a retained diagnostic clip; Marsh does not need oxygen and does not enter it through normal breathing behavior.</p>'
        sections+=f'<details><summary>{title} · {len(cards)} clips</summary>{note}<section>'+''.join(cards)+'</section></details>'
    html='''<!doctype html><meta charset="utf-8"><title>Marsh · remaining animation review</title><style>body{background:#142129;color:#dbe4e6;font:16px system-ui;margin:32px auto;max-width:1280px;padding:0 20px}h1,h2,h3{font-weight:550}p{max-width:1000px;line-height:1.6}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}article{background:#26333c;padding:12px;border-radius:10px}img{width:350px;max-width:100%;image-rendering:pixelated}video{max-width:100%;width:960px}summary{font-size:22px;cursor:pointer;margin:25px 0}a{color:#a7d6cc}</style><h1>Marsh · remaining animations</h1><p>Review of cargo swimming, dry and underwater turns, treading and water shutdown. These existing drawings and timings are retained: 64 pickup, return and turn endpoints already match their adjoining poses exactly. No additional artwork changes were needed in this pass.</p><h2>Pickup → loaded swimming → drain → carry → unload</h2><p>Source sequences use current selected frames and authored timing; viewer replay is separate from a completed in-game delivery.</p><section>'''+''.join(chains)+'</section>'+native+sections+'''<p><a href="../../../docs/MARSH_REMAINING_REVIEW_2026-10-14.md">Evidence and handoff</a> · <a href="../../marsh-meal-review-2026-10-14/review/index.html">Accepted eating and drinking</a></p>'''
    (OUT/'index.html').write_text(html,encoding='utf-8')
    (OUT/'publication.json').write_text(json.dumps({'sourceStates':len(prior),'sourceHolds':hashes,'exactJoins':joins,'nativeCaptures':len(captures),'expedition':{k:v for k,v in journey.items() if k!='captures'},'artworkChanged':False},indent=2)+'\n')
    print(f'{len(prior)} clips / {hashes} unchanged holds; {joins} exact joins; four chains and108 native captures')

if __name__=='__main__':main()
