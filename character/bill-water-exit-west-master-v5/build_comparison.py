from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parent
density=148/956
master=Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGBA').crop((870,0,1230,1024))
master=master.resize((round(master.width*density),round(master.height*density)),Image.Resampling.LANCZOS)
canvas=Image.new('RGBA',(352,320));canvas.alpha_composite(master,(140,66))
board=Image.new('RGB',(1760,720),'#182932');d=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
 items=[('Original master / original density',canvas),('Swimmer',Image.open(P/g/'frames/swim-land-west/000.png').convert('RGBA')),('Previous lowering hands',Image.open(R/'bill-water-exit-west-master-v4'/g/'frames/swim-land-west/001.png').convert('RGBA')),('Corrected lowering hands',Image.open(P/g/'frames/swim-land-west/001.png').convert('RGBA')),('Next elbow support',Image.open(P/g/'frames/swim-land-west/002.png').convert('RGBA'))]
 for col,(title,im) in enumerate(items):
  board.paste(im,(col*352,row*360+25),im);d.text((col*352+3,row*360+4),g+' / '+title,fill='white')
board.save(P/'master-comparison.png');board.crop((352,0,1760,720)).save(P/'prior-comparison.png')
