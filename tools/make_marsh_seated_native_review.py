"""Publish the selected player and staged live furniture review."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'output/marsh-animation-audit';OUT=ROOT/'character/marsh-run-carry-review-v1'
def main():
    paths=sorted((BASE/'seated-native').glob('frame-*.png'));assert len(paths)==92
    frames=[Image.open(p).convert('RGB') for p in paths]
    frames[0].save(OUT/'native-seated-player.gif',save_all=True,append_images=frames[1:],duration=50,loop=0)
    board=Image.new('RGB',(804,465*8),'#17212a');draw=ImageDraw.Draw(board)
    pack=json.loads((ROOT/'character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json').read_text());timing={s['id']:s['frameDurationsMs'] for s in pack['states']}
    for r,id in enumerate(('crew_lounge','observation_room')):
        for q in range(4):
            actions=['sit-down','sit-idle' if r==0 else 'read-seated','sit-rise'];frames=[];durations=[]
            direction='north' if r==0 else 'south'
            for a in actions:
                for i,ms in enumerate(timing[a+'-'+direction]):
                    path=BASE/'seated-rooms'/f'{id}-q{q}-{a}-{i:02}.png'
                    frames.append(Image.open(path).convert('RGB').crop((365,115,767,560)));durations.append(ms)
            frames[0].save(OUT/f'native-seated-{id}-q{q}.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
            for c,a in enumerate(actions[:2]):
                path=BASE/'seated-rooms'/f'{id}-q{q}-{a}-00.png';im=Image.open(path).convert('RGB').crop((365,115,767,560));y=(r*4+q)*465;board.paste(im,(c*402,y));draw.text((c*402+4,y+447),f'{id} q{q} {a}',fill='white')
    board.save(OUT/'native-seated-rooms-contact.png');print('Published 92 selected-player and 84 staged furniture captures')
if __name__=='__main__':main()
