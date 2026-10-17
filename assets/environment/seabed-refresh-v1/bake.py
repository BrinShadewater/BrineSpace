"""Rebuild calibrated runtime sprites from immutable generated masters."""
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent
SOURCES = {'basalt-outcrop': 'basalt-outcrop-v2.png',
           'wreck-timbers': 'wreck-timbers-v1.png',
           'ribbon-kelp': 'ribbon-kelp-v1.png'}
def bake():
    (ROOT/'runtime').mkdir(exist_ok=True)
    for identity, source in SOURCES.items():
        image = Image.open(ROOT/source).convert('RGBA')
        # Trim only transparent margins; preserve all source color and alpha.
        image = image.crop(image.getchannel('A').getbbox())
        height = round(512*image.height/image.width)
        image.resize((512,height),Image.Resampling.LANCZOS).save(ROOT/'runtime'/f'{identity}.png')
if __name__ == '__main__': bake()
