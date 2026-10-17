from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;o=p/'water-stop-bridge-v340';dest=p/'water-motion-review-v341';dest.mkdir(exist_ok=True)
bank=json.loads((o/'playback-bank.json').read_bytes());assert len(bank)==96
images={}
for row in bank.values():
    for f in row:
        if f['src'] not in images:
            im=Image.open(o/f['src']).convert('RGBA');assert hashlib.sha256(im.tobytes()).hexdigest()==f['hash'];images[f['src']]=im
types=['swim-stop-phase','swim-restart-phase','swim-stop-resume'];media=[]
def paint(canvas,f,x,y,height):
    scale=height/f['height'];im=images[f['src']];im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
    canvas.paste(im,(round(x-f['pivot'][0]*scale),round(y-f['pivot'][1]*scale)),im)
for direction in ['west','east','north','south']:
    for typ in types:
        rows=[bank[gear+'/'+typ+'-'+str(phase)+'-'+direction] for gear in ['bare','diving-helmet'] for phase in range(1,5)]
        boundaries={0}
        for row in rows:
            t=0
            for f in row:t+=f['duration'];boundaries.add(t)
        boundaries=sorted(boundaries);boundaries.append(boundaries[-1]+700)
        frames=[];durations=[]
        for t,end in zip(boundaries,boundaries[1:]):
            board=Image.new('RGB',(1024,700),(48,59,64));draw=ImageDraw.Draw(board)
            draw.text((5,5),f'{direction} / {typ} / {t}ms / exact staged poses, no actor physics',fill='white')
            for n,row in enumerate(rows):
                cursor=t;f=row[-1]
                for candidate in row:
                    if cursor<candidate['duration']:f=candidate;break
                    cursor-=candidate['duration']
                x=(n%4)*256;y=(n//4)*330+30
                draw.text((x+5,y),f'{"bare" if n<4 else "helmet"} entry{n%4+1} pose{f["slot"]}',fill='white')
                for height,anchor,level in [(148,128,145),(82,50,275),(54,150,275),(27,224,275)]:
                    paint(board,f,x+anchor,y+level,height);draw.text((x+anchor-15,y+level+30),str(height)+'px',fill='white')
            frames.append(board);durations.append(end-t)
        name=direction+'-'+typ+'.png';frames[0].save(dest/name,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0);media.append(name)
strips=[]
for direction in ['west','east','north','south']:
    for gear in ['bare','diving-helmet']:
        board=Image.new('RGB',(1500,2160),(48,59,64));draw=ImageDraw.Draw(board)
        for ti,typ in enumerate(types):
            for phase in range(1,5):
                y=(ti*4+phase-1)*180;row=bank[gear+'/'+typ+'-'+str(phase)+'-'+direction]
                draw.text((5,y+3),f'{gear} {direction} {typ} {phase} /82px /'+','.join(str(int(f['duration'])) for f in row),fill='white')
                for slot,f in enumerate(row):paint(board,f,slot*150+75,y+90,82)
        name=gear+'-'+direction+'-all-poses.png';board.save(dest/name);strips.append(name)
report={'rows':len(bank),'slots':sum(len(v) for v in bank.values()),'uniquePixels':len(images),'animatedBoards':media,'staticBoards':strips,'normalChanged':False,'fullMotionActuallyViewed':False,'scope':'Exact exported staged row clocks, whole-canvas uniform registration at four ruler sizes. APNG loops include terminal hold; no actor collision or save route simulation.'}
(dest/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'Built {len(media)} APNG boards from {len(bank)} rows/{report["slots"]} exact slots/{len(images)} unique images.')
