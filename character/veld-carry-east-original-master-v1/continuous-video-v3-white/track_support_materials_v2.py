"""Correct misplaced heel landmarks; preserve original failed diagnostic."""
from pathlib import Path
P=Path(__file__).resolve().parent
original=(P/'track_support_materials.py').read_text(encoding='utf-8')
namespace={'__file__':str(P/'track_support_materials.py')}
exec(compile(original.split('\nwindows=[]')[0],str(P/'track_support_materials.py'),'exec'),namespace)
track=namespace['track'];json=namespace['json'];Image=namespace['Image'];ImageDraw=namespace['ImageDraw']
windows=[]
for start,end,anchor,toe,heel in [
    (19,25,21,(136,212,146,218),(131,207,137,214)),
    (38,44,40,(143,211,153,217),(138,205,144,212)),
    (56,62,58,(135,212,145,218),(130,207,136,214))]:
    pair={'frames':[start,end],'toeCap':track(anchor,toe,start,end),'ankleStrap':track(anchor,heel,start,end)}
    pair['toeAnkleImpliedStrideDifferencePixels']=abs(pair['toeCap']['suggested37FrameTravelPixels']-pair['ankleStrap']['suggested37FrameTravelPixels'])
    windows.append(pair)
report={'scope':'Corrected interior ankle strap material patch versus toe cap, three short flat-support windows only. Original failed heel tracking preserved. Not full heel/toe roll or gait contact acceptance.', 'candidatePeriodFrames':37,'windows':windows,'strideAccepted':False}
(P/'support-material-diagnostic-v2.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1400,680),'#202a30');draw=ImageDraw.Draw(board)
for w,pair in enumerate(windows):
    for k,i in enumerate(range(pair['frames'][0],pair['frames'][1]+1)):
        im=Image.open(P/'full-clip-frames'/f'{i:03d}.png').convert('RGBA').crop((95,195,170,230)).resize((180,84),Image.Resampling.NEAREST)
        xy=(k*200,w*220+35);board.paste(im,xy,im);draw.text((xy[0],xy[1]-20),f'raw{i}',fill='white')
        for key,col in [('toeCap','#70d7e0'),('ankleStrap','#f4cb75')]:
            row=pair[key]['rows'][k];bounds=pair[key]['templateNativeBounds']
            nx=row['nativeX']+(bounds[2]-bounds[0])/2;ny=row['rawY']*(212/1024)+46+(bounds[3]-bounds[1])/2
            cx=xy[0]+(nx-95)*2.4;cy=xy[1]+(ny-195)*2.4
            draw.ellipse((cx-3,cy-3,cx+3,cy+3),outline=col,width=2)
        draw.text((xy[0],xy[1]+96),f"toe {pair['toeCap']['rows'][k]['correlation']:.2f}",fill='#70d7e0')
        draw.text((xy[0],xy[1]+115),f"ankle {pair['ankleStrap']['rows'][k]['correlation']:.2f}",fill='#f4cb75')
board.save(P/'support-material-tracking-review-v2.png')
print(json.dumps({'windows':[{'frames':w['frames'],'toeStride':w['toeCap']['suggested37FrameTravelPixels'],'ankleStride':w['ankleStrap']['suggested37FrameTravelPixels'],'difference':w['toeAnkleImpliedStrideDifferencePixels'],'toeResidual':w['toeCap']['linearResidualSpanNativePixels'],'ankleResidual':w['ankleStrap']['linearResidualSpanNativePixels'],'minimumAnkleCorrelation':w['ankleStrap']['minimumCorrelation']} for w in windows],'strideAccepted':False}))
