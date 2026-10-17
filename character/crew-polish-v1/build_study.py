"""Package the Veld repaint for review; production catalogs remain independent."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
DIRS=['south','north','east','west']

def main():
    source=ROOT/'sources/veld-walk-v1.png'
    image=Image.open(source).convert('RGBA')
    assert image.size==(1536,1024)
    states=[]; records=[]
    # One transform per facing; retains each row's authored bob and foot travel.
    # No frame is individually normalized to its silhouette or lowest boot.
    scale=140/168
    east_source=Image.open(ROOT/'sources/veld-east-v2.png').convert('RGBA')
    for row,direction in enumerate(DIRS):
        files=[]
        for col in range(6):
            local_scale=scale
            if direction=='east':
                x=(col%3)*512;y=(col//3)*512
                tile=east_source.crop((x,y,x+512,y+512))
                local_scale=140/453
            else:
                tile=image.crop((col*256,row*256,(col+1)*256,(row+1)*256))
            a=np.array(tile);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
            tile=Image.fromarray(a)
            tile=tile.resize((round(tile.width*local_scale),round(tile.height*local_scale)),Image.Resampling.LANCZOS)
            tile.putalpha(tile.getchannel('A').point(lambda v:255 if v>=128 else 0))
            frame=Image.new('RGBA',(256,256))
            # Authoring sheet uses its original x92 axis; front/rear contact is y200,
            # side contact y193. Export profile is the existing 256 canvas at p128,224.
            at=(round(128-92*scale),round(224-(200 if row<2 else 193)*scale))
            if direction=='east':at=(round(128-260*local_scale),round(224-(496 if col<3 else 468)*local_scale))
            frame.alpha_composite(tile,at)
            path=ROOT/f'veld-study/frames/walk-{direction}/{col:03}.png'
            path.parent.mkdir(parents=True,exist_ok=True);frame.save(path)
            box=frame.getbbox()
            assert box and box[0]>0 and box[1]>0 and box[2]<256 and box[3]<256
            files.append(path.relative_to(ROOT/'veld-study').as_posix())
            records.append(dict(direction=direction,slot=col,box=box,offset=at,scale=local_scale,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        states.append(dict(id='walk-'+direction,frameFiles=files,
            frameDurationsMs=[170,130,150,170,130,150],loop=True))
    pack=dict(name='Veld painted walk study',frameWidth=256,frameHeight=256,
        pivot=[128,224],standingHeight=148,states=states,status='unselected study')
    (ROOT/'veld-study/manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
    (ROOT/'review/veld-study-registration.json').write_text(json.dumps(dict(
        sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        eastSourceSha256=hashlib.sha256((ROOT/'sources/veld-east-v2.png').read_bytes()).hexdigest(),scale=scale,
        records=records,limits=['Fixed registration is provisional; world-space contact and native playback not established.',
        'Repaint retains six poses; does not establish improved smoothness.']),indent=2)+'\n')
    board=Image.new('RGBA',(1536,4*310),'#242b2e');draw=ImageDraw.Draw(board)
    for row,s in enumerate(states):
        for col,path in enumerate(s['frameFiles']):
            im=Image.open(ROOT/'veld-study'/path)
            board.alpha_composite(im,(col*256,row*310+24))
        draw.text((12,row*310+8),'Veld / '+s['id']+' / unselected painted study',fill='white')
    board.save(ROOT/'review/veld-study-contact.png')
    print('Packaged 24 poses / four walk studies; alpha and bounds pass. Not installed.')

if __name__=='__main__':main()
