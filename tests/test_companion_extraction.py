"""Run with project Python; isolates the white-key regression."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_companion_cleanup import clean

image=Image.new('RGBA',(32,32),'white')
draw=ImageDraw.Draw(image)
draw.rectangle((8,8,23,23),fill='black')
draw.rectangle((10,10,21,21),fill='white')
result=clean(image,True)
assert result.getpixel((0,0))[3]==0, 'Exterior background must be transparent'
assert result.getpixel((15,15))==(255,255,255,255), 'Interior white panels must survive'
assert result.getpixel((8,8))[3]==255, 'Dark silhouette must survive'
print('Companion extraction PASS')
