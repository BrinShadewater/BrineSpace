from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
import json
P=Path(__file__).resolve().parent;R=P.parent
review=json.loads((P/"review.json").read_text());density=148/956
master=Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGBA').crop((870,0,1230,1024))
master=master.resize((round(master.width*density),round(master.height*density)),Image.Resampling.LANCZOS)
canvas=Image.new('RGBA',(352,320));ma=np.array(master);my=int(np.where(ma[:,:,3]>180)[0].max())+1;canvas.alpha_composite(master,(140,224-my))
# Same-sheet neutral is West/left-facing calibration, not a selected idle.
sheet=Image.open(P/'sources/reach-calibrated-v1.png').convert('RGBA');sa=np.array(sheet);neutral=np.zeros_like(sa);neutral[0:1010,10:360]=sa[0:1010,10:360];calib=review['frames'][0]['calibration'];scale=calib['oneWholeSourceScale'];ni=Image.fromarray(neutral).resize((round(sheet.width*scale),round(sheet.height*scale)),Image.Resampling.LANCZOS);na=np.array(ni);yy,xx=np.where(na[:,:,3]>180);neutralCanvas=Image.new('RGBA',(352,320));neutralCanvas.alpha_composite(ni,(160-round((xx.min()+xx.max())/2),224-int(yy.max())-1))
board=Image.new('RGB',(2112,720),'#182932');d=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
 items=[('Original West master',canvas),('Neutral / West / calibration only',neutralCanvas),('Earlier oversized Reach',Image.open(R/'bill-swim-west-calibrated-v5'/g/'frames/swim-west/005.png').convert('RGBA')),('Calibrated Recover',Image.open(P/g/'frames/swim-west/004.png').convert('RGBA')),('Calibrated Reach',Image.open(P/g/'frames/swim-west/005.png').convert('RGBA')),('Calibrated Glide',Image.open(P/g/'frames/swim-west/006.png').convert('RGBA'))]
 for col,(title,im) in enumerate(items):
  board.paste(im,(col*352,row*360+25),im);d.text((col*352+3,row*360+4),g+' / '+title,fill='white')
board.save(P/'master-comparison.png');board.crop((352,0,2112,720)).save(P/'prior-comparison.png')
