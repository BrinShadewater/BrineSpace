from pathlib import Path
import hashlib,json,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
e=json.loads((P/'native-evidence.json').read_bytes());rows=e['records']
# Verify the stationary foot on whole views before using this fixed screenshot crop.
FOOT=(486,362)
def crop(r):
    p=P.parents[1]/r['path'].removeprefix('res://')
    return Image.open(p).convert('RGB').crop((FOOT[0]-75,FOOT[1]-115,FOOT[0]+75,FOOT[1]+20))
boards=[]
for page in range(math.ceil(len(rows)/48)):
    b=Image.new('RGB',(1200,6*165),'#303b40');d=ImageDraw.Draw(b)
    for n,r in enumerate(rows[page*48:(page+1)*48]):
        x=n%8*150;y=n//8*165;b.paste(crop(r),(x,y+20))
        d.text((x+3,y+3),r['label'].removeprefix('actual-'),fill='white')
        d.text((x+3,y+151),f"{r['work']:.3f}s / sparks {r['sparks']}",fill='white')
    name=f'native-page{page}.png';b.save(P/name);boards.append(name)
ordinary=[r for r in rows if r['label'].startswith('actual-')]
images=[]
for r in ordinary:
    b=Image.new('RGB',(300,292),'#303b40');b.paste(crop(r).resize((300,270),Image.Resampling.NEAREST),(0,22))
    ImageDraw.Draw(b).text((6,4),r['key']+f" #{r['index']} / pose order",fill='white');images.append(b)
images[0].save(P/'native-source-order.gif',save_all=True,append_images=images[1:],duration=50,loop=0,disposal=2)
manifest=json.loads((P.parents[1]/'character/james-torch-material-residue-v2/bare-manifest.json').read_bytes())
clips={s['id']:s for s in manifest['states']}
source_images=[]
source_board=Image.new('RGB',(920,math.ceil(len(ordinary)/5)*204),'#303b40');sd=ImageDraw.Draw(source_board)
for n,r in enumerate(ordinary):
    reference=clips[r['key']]['frameFiles'][r['index']]
    source=Image.open(P.parents[1]/reference.removeprefix('res://')).convert('RGBA')
    assert hashlib.sha256(source.tobytes().hex().encode()).hexdigest()==r['sourceHash']
    source_board.paste(source,(n%5*184,n//5*204+20),source);sd.text((n%5*184+4,n//5*204+3),r['key']+f" #{r['index']}",fill='white')
    b=Image.new('RGB',(600,240),'#303b40');d=ImageDraw.Draw(b)
    d.text((8,8),'James hull repair / selected whole poses / simplified timing',fill='white')
    for x,height in [(90,148),(270,82),(420,54),(540,27)]:
        scale=height/148;im=source.resize((round(184*scale),round(184*scale)),Image.Resampling.LANCZOS)
        b.paste(im,(round(x-92*scale),round(212-172*scale)),im);d.text((x-15,223),f'{height}px',fill='white')
    source_images.append(b)
source_board.save(P/'selected-source-review.png')
source_images[0].save(P/'selected-source-order.gif',save_all=True,append_images=source_images[1:],duration=50,loop=0,disposal=2)
inventory={r['path']:hashlib.sha256((P.parents[1]/r['path'].removeprefix('res://')).read_bytes()).hexdigest() for r in rows}
(P/'review-evidence.json').write_text(json.dumps({'boards':boards,'captures':len(rows),'ordinarySourceCaptures':len(ordinary),'cleanSelectedSourceMatches':len(ordinary),'cleanSourceBoard':'selected-source-review.png','cleanPreview':'selected-source-order.gif','fixedCropFoot':FOOT,'nativeHashes':inventory,'scope':'Unique selected source-slot views plus actual before/after fresh Continue phases and completion, fixed native screenshot crop. Repeated held-loop occurrences are not individually captured. GIF uses50ms/captured pose and first occurrence per selected source; not continuous real-time overlay/gameplay footage. Clean preview uses exactly the selected sources whose RGBA hashes match native captures; no environment overlays.'},indent=2)+'\n')
print(json.dumps({'boards':boards,'captures':len(rows),'ordinary':len(ordinary)}))
