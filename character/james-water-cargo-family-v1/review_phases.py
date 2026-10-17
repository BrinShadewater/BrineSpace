from pathlib import Path
from PIL import Image,ImageDraw
import sys
P=Path(__file__).resolve().parent
installed='--installed' in sys.argv
for mode in ['helmet']:
 board=Image.new('RGB',(8*230,4*255),'#303b40');dr=ImageDraw.Draw(board)
 for row,d in enumerate(['east','south','west','north']):
  labels=[mode+'-salvage-'+d+'-000']+[mode+'-pickup-'+d+'-'+str(i).zfill(3) for i in range(6)]+[mode+'-carry-'+d+'-000']
  for col,label in enumerate(labels):
   im=Image.open(P/('installed-phase-captures' if installed else 'route-captures')/(label+'.png')).convert('RGB');sc=min(225/im.width,225/im.height);im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.BILINEAR);at=(col*230,row*255+28);board.paste(im,at);dr.text((at[0]+3,row*255+5),label,fill='white')
 board.save(P/('native-'+('installed-' if installed else '')+'phase-'+mode+'.png'))
print('Controlled helmet exterior phase contact board / 32 captures')
