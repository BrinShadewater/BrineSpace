"""Assemble review media from the layered cryopod native fixture's captures."""
from pathlib import Path
from PIL import Image, ImageDraw
import argparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/cryo-layered-v1'
ACTORS = ['bill', 'veld', 'branforth']
THAW = sorted([3.3 + i * .22 for i in range(26)] + [6.0])
EXIT = [8.8 + i * .029 for i in range(41)]

def panel(actor, label):
    image = Image.open(OUT / f'{actor}-{label}.png').convert('RGB')
    return image.crop((10,15,105,175)).resize((190,320), Image.Resampling.NEAREST)

def build():
    falling='fall-recovery' in OUT.name or 'fall-landing' in OUT.name
    thaw=[3.3+i*.3 for i in range(8)] if falling else THAW
    exit=[5.4+i*.06 for i in range(77)] if falling else EXIT
    sequence = [(f'{t:.2f}', 300 if falling else 220) for t in thaw]
    sequence += [(f'{t:.2f}', 60 if falling else 30) for t in exit]
    sequence += [('released', 1400)]
    frames=[]
    for label, _ in sequence:
        image=Image.new('RGB',(570,350),(23,30,36))
        draw=ImageDraw.Draw(image)
        for index, actor in enumerate(ACTORS):
            image.paste(panel(actor,label),(index*190,30))
            draw.text((index*190+8,8),actor.title(),fill='white')
        frames.append(image)
    frames[0].save(OUT/'thaw-and-exit.gif',save_all=True,append_images=frames[1:],
        duration=[ms for _,ms in sequence],loop=0,disposal=2)
    contact=Image.new('RGB',(950,1050),(23,30,36))
    for row, actor in enumerate(ACTORS):
        for column, label in enumerate(['3.30','7.44','8.40','9.30','released'] if falling else ['3.30','6.00','8.80','9.50','released']):
            contact.paste(panel(actor,label),(column*190,row*350+30))
            ImageDraw.Draw(contact).text((column*190+5,row*350+8),actor+' '+label,fill='white')
    contact.save(OUT/'contact.png')
    print(f'Built native review GIF: {len(frames)} samples, three actors; contact sheet.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=OUT)
    OUT=parser.parse_args().output.resolve()
    build()
