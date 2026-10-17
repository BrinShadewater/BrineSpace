"""Read-only density/palette diagnostics and honest common-scale review boards.

Metrics flag review candidates; neither colour statistics nor edge contrast
certifies style, anatomical consistency or animation quality.
"""
from pathlib import Path
import json,csv,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import binary_erosion
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OUT=ROOT/'review/style';OUT.mkdir(parents=True,exist_ok=True)
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
SMALL=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
CAST={'bill':'major-bill-v3','veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2','marsh':'marsh-v2'}

def catalog(folder):
    root=REPO/'character'/folder;cat=json.loads((root/'catalog.json').read_text());states={}
    for name in cat['body']:
        path=root/name;pack=json.loads(path.read_text())
        for s in pack['states']:states[s['id']]=(path,pack,s)
    return states

def diagnostic(path,height):
    im=Image.open(path).convert('RGBA');a=np.array(im);mask=a[:,:,3]>127
    rgb=a[:,:,:3].astype(float);light=rgb@np.array([.2126,.7152,.0722])
    interior=binary_erosion(mask,iterations=2)
    chroma=rgb.max(2)-rgb.min(2)
    neutral=interior&(chroma<30)&(light>25)&(light<180)
    blue=interior&(rgb[:,:,2]>rgb[:,:,0]+8)&(rgb[:,:,2]>rgb[:,:,1]+2)&(light>30)
    pair=interior[:,1:]&interior[:,:-1]
    contrast=np.abs(np.diff(light,axis=1))[pair]
    return dict(width=im.width,height=im.height,bounds=list(im.getbbox()),standingHeight=height,
        pixelsPerWorldUnit=round(height/65.28,4),partialAlpha=int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum()),
        opaquePixels=int(mask.sum()),neutralMedianRGB=np.round(np.median(rgb[neutral],axis=0),1).tolist() if neutral.any() else None,
        blueMedianRGB=np.round(np.median(rgb[blue],axis=0),1).tolist() if blue.any() else None,
        interiorContrast=round(float(np.mean(contrast)),2) if len(contrast) else None)

def draw_actor(board,source,x,foot,k):
    path,pack,state=source;im=Image.open(path.parent/state['frameFiles'][0]).convert('RGBA')
    scale=k*148/pack.get('standingHeight',74)
    if scale!=1:im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
    pivot=pack.get('pivot',[46,86]);board.alpha_composite(im,(round(x-pivot[0]*scale),round(foot-pivot[1]*scale)))

def main():
    packs={who:catalog(folder) for who,folder in CAST.items()}
    path=ROOT/'veld-painted-v2/manifest.json';data=json.loads(path.read_text())
    packs['veld-candidate']={s['id']:(path,data,s) for s in data['states']}
    if '--boards-only' in sys.argv:
        cached=json.loads((OUT/'metrics.json').read_text());records=cached['states'];summaries=cached['packs']
    else:
        records=[];summaries={}
        for who,states in packs.items():
            count=0;density=set();alpha=0;dimensions=set()
            for key,(path,pack,state) in states.items():
                frames=[diagnostic(path.parent/f,pack.get('standingHeight',74)) for f in state['frameFiles']]
                count+=len(frames);density.update(f['pixelsPerWorldUnit'] for f in frames);alpha+=sum(f['partialAlpha'] for f in frames)
                dimensions.update((f['width'],f['height']) for f in frames)
                heights=[f['bounds'][3]-f['bounds'][1] for f in frames]
                records.append(dict(actor=who,state=key,frames=frames,frameCount=len(frames),silhouetteHeightRange=[min(heights),max(heights)],
                    interiorContrastMedian=round(float(np.median([f['interiorContrast'] for f in frames])),2)))
            summaries[who]=dict(states=len(states),frameReferences=count,pixelsPerWorldUnit=sorted(density),canvasSizes=sorted(dimensions),partialAlphaPixels=alpha)
        report=dict(scope='All current crew body catalogs plus Veld candidate; not equipment or runtime-composed states',
            interpretation='Colour masks include multiple materials. Contrast is not a blur score. Pose height is not anatomical scale. Visual review is required.',packs=summaries,states=records)
        (OUT/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')
        with (OUT/'states.csv').open('w',newline='') as f:
            writer=csv.writer(f);writer.writerow(['actor','state','frames','min silhouette height','max silhouette height','median interior contrast','first-frame neutral RGB','first-frame blue RGB'])
            for r in records:writer.writerow([r['actor'],r['state'],r['frameCount'],*r['silhouetteHeightRange'],r['interiorContrastMedian'],r['frames'][0]['neutralMedianRGB'],r['frames'][0]['blueMedianRGB']])
    # Equal source-density ruler, never normalize crouches/swimming to standing height.
    keys=['idle-south','walk-south','walk-east','repair-west','swim-east']
    board=Image.new('RGBA',(1250,1700),'#242b2e');d=ImageDraw.Draw(board)
    d.text((20,15),'CREW STYLE AUDIT / shared 148px standing-height ruler / 1x export scale',font=FONT,fill='white')
    for row,(who,states) in enumerate(packs.items()):
        for col,key in enumerate(keys):
            x=col*250+125;y=85+row*325
            d.text((col*250+12,y-26),who+' / '+key,font=SMALL,fill='#dce3e1')
            if key in states:draw_actor(board,states[key],x,y+162,1)
            else:d.text((col*250+30,y+90),'Not repainted',font=SMALL,fill='#bd9a75')
            d.line((col*250+25,y+164,col*250+225,y+164),fill='#536469')
            if key in states:draw_actor(board,states[key],x,y+260,65.28/148)
    board.save(OUT/'cast-density.png')
    # Candidate palette and paired old/new action rows at the same source scale.
    keys=['idle','walk','kneel','repair','stand'];board=Image.new('RGBA',(1500,1180),'#e0dfd7');d=ImageDraw.Draw(board)
    d.text((15,12),'VELD / current left, candidate right / fixed scale / light-background edge review',font=FONT,fill='#242b2e')
    for row,direction in enumerate(['east','west','south','north']):
        for col,kind in enumerate(keys):
            key=kind+'-'+direction;x=col*300+100;y=row*280+52
            d.text((col*300+10,y),key,font=SMALL,fill='#242b2e')
            for j,who in enumerate(['veld','veld-candidate']):
                draw_actor(board,packs[who][key],x+j*130,y+185,1)
                metric=next(r for r in records if r['actor']==who and r['state']==key)['frames'][0]
                for n,field in enumerate(['neutralMedianRGB','blueMedianRGB']):
                    color=metric[field]
                    if color:d.rectangle((x-25+j*130+n*28,y+207,x-2+j*130+n*28,y+225),fill=tuple(round(v) for v in color))
            d.text((col*300+14,y+235),'current | candidate; neutral / blue samples',font=SMALL,fill='#454c4e')
    board.save(OUT/'veld-materials.png')
    print(json.dumps(summaries))
if __name__=='__main__':main()
