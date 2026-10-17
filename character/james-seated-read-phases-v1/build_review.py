from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent
e=json.loads((P/'validate-evidence.json').read_text());assert e['failures']==0
for room in ['crew_lounge','observation_room']:
    roi=(330,235,435,390) if room=='crew_lounge' else (630,230,790,390)
    for mode in [0,1]:
        records=[r for r in e['records'] if r['room']==room and r['mode']==mode]
        board=Image.new('RGB',(6*320,((len(records)+5)//6)*344),'#202a30');d=ImageDraw.Draw(board)
        frames=[];durations=[]
        for i,t in enumerate(records):
            im=Image.open(P/'controller-native'/Path(t['capture']).name).convert('RGB').crop(roi)
            crop=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);x=i%6*320;y=i//6*344;board.paste(crop,(x,y+24));d.text((x+3,y+3),t['key']+' '+str(t['index'])+' @'+str(round(t['simTime'],2)),fill='white')
            frames.append(crop);durations.append(round(((records[i+1]['simTime'] if i+1<len(records) else t['simTime']+.1)-t['simTime'])*1000))
        board.save(P/(room+'-'+str(mode)+'-chronological.png'))
        # Native controller frame-change capture playback, exact recorded simulation intervals.
        frames[0].save(P/(room+'-'+str(mode)+'-controller.gif'),save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
        for page in range((len(records)+17)//18):
            board.crop((0,page*3*344,1920,min(board.height,(page+1)*3*344))).save(P/(room+'-'+str(mode)+'-page'+str(page)+'.png'))
print('All172 native chronological captures on page boards; controller interval GIFs, no continuous60Hz claim.')
