from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent
packs=[json.loads((P/(m+'-manifest.json')).read_bytes()) for m in ['bare','helmet']]
states=[next(s for s in p['states'] if s['id']=='inspect-east') for p in packs]
frames=[]
for i in range(141):
    board=Image.new('RGB',(736,230),'#303b40');draw=ImageDraw.Draw(board)
    for mode,state in enumerate(states):
        for column,index in enumerate([0,i]):
            im=Image.open(P/state['frameFiles'][index]).convert('RGBA')
            x=mode*368+column*184
            board.paste(im,(x,34),im)
            draw.text((x+8,8),['bare','helmet'][mode]+' / '+('master' if column==0 else 'tablet'),fill='white')
    frames.append(board)
durations=states[0]['frameDurationsMs']
frames[0].save(P/'paired-material-review.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False)
(P/'preview-scope.json').write_text(json.dumps({'sourceSlotsPerGear':141,'durationMs':sum(durations),'scope':'Constructed selected-source-clock paired GIF with exact idle master. Not continuous native station video.'},indent=2))
print('Paired complete-source-clock review exported.')
