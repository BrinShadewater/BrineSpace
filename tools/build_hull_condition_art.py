"""Package selected immutable painted sources; no painting or colour grading."""
import hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'assets/environment/hull-condition-v2'
GENERATED=Path('C:/Users/Alex/.codex/generated_images/01a0f098-dc3b-7e11-9f28-021676820905')
SELECTED=[('hairline','exec-3acfc433-49b6-48d0-ae07-1c40950fa3f9.png',32),('split','exec-ca02f519-0d2f-4567-ad80-97a2f776ec5d.png',34),('rupture','exec-36c2c449-547d-4657-8486-c841aa886586.png',37),('patch','exec-1878c195-d3c8-41dc-9eb5-655df8471a37.png',29),('weld','exec-6060b31c-d80a-4eae-9c28-ab9aea0452e1.png',32)]
def build():
    ledger_path=PACK/'source-ledger.json'
    expected={item['source']:item['sha256'] for item in json.loads(ledger_path.read_text())['selected']} if ledger_path.exists() else {}
    for source,digest in expected.items():
        assert hashlib.sha256((PACK/source).read_bytes()).hexdigest()==digest, 'Immutable source drift: '+source
    (PACK/'sources').mkdir(parents=True,exist_ok=True)
    (PACK/'runtime').mkdir(exist_ok=True)
    atlas=Image.new('RGBA',(768,512));ledger=[]
    for index,(name,filename,height) in enumerate(SELECTED):
        dest=PACK/'sources'/(name+'-v1.png')
        if not dest.exists():shutil.copy2(GENERATED/filename,dest)
        im=Image.open(dest).convert('RGBA')
        bounds=im.getchannel('A').point(lambda a:255 if a>=8 else 0).getbbox()
        assert bounds and im.getchannel('A').getextrema()[0]==0
        # Crop transparent margins, isotropic resampling only. Source alpha/RGB retained.
        art=im.crop(bounds);factor=height*(256/48)/art.height
        art=art.resize((round(art.width*factor),round(art.height*factor)),Image.Resampling.LANCZOS)
        tile=Image.new('RGBA',(256,256));pivot_y=213-art.height/2 if name=='patch' else 149
        offset=(128-art.width//2,round(pivot_y-art.height/2))
        tile.alpha_composite(art,offset);atlas.alpha_composite(tile,((index%3)*256,(index//3)*256))
        tile.save(PACK/'runtime'/(name+'-256.png'))
        ledger.append(dict(id=name,source='sources/'+dest.name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),dimensions=im.size,alpha_bounds=bounds,runtime_size=art.size,offset=offset,height_world=height))
    atlas.save(PACK/'runtime/hull-256.png')
    ledger_path.write_text(json.dumps(dict(selected=ledger,tile_size=256,world_tile_size=48,unused_slot=5,processing='alpha>=8 bounds; isotropic Lanczos; preserved RGB/alpha; registered margins only'),indent=2))
    board=Image.new('RGBA',(768,548),'#527279');board.alpha_composite(atlas,(0,36));draw=ImageDraw.Draw(board)
    for i,(name,_,_) in enumerate(SELECTED):draw.text(((i%3)*256+8,(i//3)*256+38),name,fill='white')
    out=ROOT/'output/hull-condition-v2';out.mkdir(exist_ok=True);board.convert('RGB').save(out/'source-contact.png')
    print('Packaged 5 alpha decals; 256px tiles at 48 world units')
if __name__=='__main__':build()
