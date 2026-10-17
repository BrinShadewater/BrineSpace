"""Publish native paid construction captures; no source or runtime mutation."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'output/marsh-animation-audit/welding-native';OUT=ROOT/'character/marsh-run-carry-review-v1'
CROPS={0:(496,280,636,420),1:(482,270,622,410),2:(498,262,638,402),3:(512,270,652,410)}
def main():
    board=Image.new('RGB',(280*4,300*4),'#17212a');draw=ImageDraw.Draw(board)
    for side,direction in enumerate(('north','east','south','west')):
        paths=[BASE/f'side-{side}-torch-draw-{i:02}.png' for i in range(6)]
        paths += [BASE/f'side-{side}-frame-{i:02}.png' for i in range(36)]
        paths += [BASE/f'side-{side}-torch-stow-{i:02}.png' for i in range(6)]
        frames=[Image.open(p).convert('RGB').crop(CROPS[side]).resize((280,280),Image.Resampling.NEAREST) for p in paths]
        durations=[87]*6+[50]*36+[87]*6
        frames[0].save(OUT/f'native-welding-{direction}.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
        for col,index in enumerate((0,5,18,47)):
            board.paste(frames[index],(col*280,side*300));draw.text((col*280+4,side*300+282),direction+' '+['idle','ready','work','stowed'][col],fill='white')
    board.save(OUT/'native-welding-contact.png');print('Published 192 native construction captures in four facings')
if __name__=='__main__':main()
