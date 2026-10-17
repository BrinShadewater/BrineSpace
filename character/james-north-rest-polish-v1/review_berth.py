from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
for mode in ['bare','helmet']:
    folder=P/('retained-berth' if mode=='bare' else 'retained-berth-helmet')/'branforth/seating-room'
    board=Image.new('RGB',(1620,630),'#303b40');d=ImageDraw.Draw(board)
    for row,action in enumerate(['lie-down','sleep','get-up']):
        for col in range(6):
            im=Image.open(folder/f'{action}-{col:02}.png').convert('RGB')
            board.paste(im.crop((330,123,600,300)),(col*270,row*210+25))
            d.text((col*270+4,row*210+5),mode+' '+action+' '+str(col),fill='white')
    board.save(P/('native-berth-'+mode+'-contact.png'))
print('36 actual selected retained-berth poses packaged for paired visual review')
