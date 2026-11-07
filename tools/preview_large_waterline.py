"""Package stepped native water-depth captures without resizing pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'output/large-waterline-v1'
IDS = ['hydroponics_farm', 'storage_depot', 'moonbay', 'tidal_power_plant']
frames = []
font = ImageFont.load_default(size=15)
for stage in range(5):
    board = Image.new('RGB', (870, 948), '#09171d')
    draw = ImageDraw.Draw(board)
    for i, room in enumerate(IDS):
        at = ((i % 2) * 435, (i // 2) * 474)
        draw.text((at[0] + 12, at[1] + 4), room.replace('_', ' '), font=font, fill='#b0c2c0')
        crop = Image.open(OUT / f'{room}-q0-s{stage}.png').convert('RGB').crop((350, 130, 785, 580))
        board.paste(crop, (at[0], at[1] + 24))
    frames.append(board)
swatches = Image.new('RGB', (870, 948 * len(frames)))
for i, frame in enumerate(frames):
    swatches.paste(frame, (0, i * 948))
palette = swatches.quantize(colors=256)
indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
indexed[0].save(OUT / 'large-room-water-depths-v1.gif', save_all=True, append_images=indexed[1:], duration=[900, 800, 900, 1000, 1100], loop=0, optimize=False)
frames[2].save(OUT / 'large-room-waterlines-v1.png')
print('Four large-room types, five native depth stages; fixed palette, no pixel resizing')
