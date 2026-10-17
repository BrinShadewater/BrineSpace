import hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw
P = Path(__file__).resolve().parent
e = json.loads((P/'native-evidence.json').read_bytes())
rows = e['actualCaptures']
b = Image.new('RGB',(1260,610),(45,55,60));d = ImageDraw.Draw(b)
for n,r in enumerate(rows):
    # Fixed foot measured in the actual1600x900 screenshot. The fixture's
    # transform estimate double-applied viewport stretch; preserve it as raw
    # diagnostic data, never use it to crop or infer body scale.
    im = Image.open(P/'native'/r['path']);x,y = (486,362)
    crop = im.crop((round(x)-65,round(y)-110,round(x)+65,round(y)+25))
    xx = n%9*140;yy = n//9*200
    b.paste(crop,(xx,yy+25));d.text((xx+3,yy+166),f"north #{r['index']} / {r['progress']:.2f}s",fill='white')
b.save(P/'actual-repair-review.png')
for gear in ['bare','helmet']:
    for phase in ['before','corrected']:
        b = Image.new('RGB',(1000,420),(45,55,60))
        for n,direction in enumerate(['north','east','south','west']):
            im = Image.open(P/'native'/f'{gear}-{direction}-{phase}.png').crop((0,0,1000,420))
            b.paste(im.resize((500,210)),((n%2)*500,(n//2)*210))
        b.save(P/f'{gear}-native-{phase}-comparison.png')
files = list((P/'native').glob('*.png'))
(P/'visual-evidence.json').write_text(json.dumps({'actualNativeViews':len(rows),'prescribedNativeViews':16,'sourceBoards':8,'sourceRefs':448,'actualReviewFixedFoot':[486,362],'cropScope':'Fixed screenshot-measured foot for all27 views. Raw fixture footViewport estimate double-applies stretch and is not used for scale/contact evidence. No per-pose recentering.','nativeHashes':{str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Prepared final actual source board and four native comparison boards.')
