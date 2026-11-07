"""Inspect effective Marsh artwork and motion; metrics flag review, not acceptance."""
from pathlib import Path
import json, hashlib, argparse
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-quality-pass-v2'

def main():
    global OUT
    parser=argparse.ArgumentParser();parser.add_argument('--output')
    args=parser.parse_args()
    if args.output:OUT=ROOT/args.output
    OUT.mkdir(exist_ok=True)
    contract=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())
    states=contract['states'];images={};rows=[]
    for key,s in states.items():
        frames=[];geometry=[];tone=[]
        for f,h in zip(s['files'],s['hashes']):
            assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h, f
            im=images.setdefault(f,Image.open(ROOT/f).convert('RGBA'))
            # Register arbitrary canvases onto one common foot anchor.
            layer=Image.new('RGBA',(384,384));layer.paste(im,(192-round(s['pivot'][0]),320-round(s['pivot'][1])))
            a=np.asarray(layer);frames.append(a)
            box=im.getbbox();geometry.append({'bounds':box,'opaquePixels':int((a[:,:,3]>0).sum()),'edgeContact':box[0]==0 or box[1]==0 or box[2]==im.width or box[3]==im.height})
            rgb=a[:,:,:3].astype(float);mask=(a[:,:,3]>0)&(rgb[:,:,0]>=rgb[:,:,1])&(rgb[:,:,0]-rgb[:,:,1]<25)&(rgb[:,:,0]-rgb[:,:,2]>12)&(rgb[:,:,0]-rgb[:,:,2]<65)&(rgb.mean(2)>105)&(rgb.mean(2)<230)
            tone.append(float(np.median(rgb.mean(2)[mask])) if mask.any() else None)
        pairs=list(zip(frames,frames[1:]))+([(frames[-1],frames[0])] if s['loop'] else [])
        changes=[]
        for a,b in pairs:
            visible=(a[:,:,3]>0)|(b[:,:,3]>0)
            changes.append(float(np.abs(a.astype(float)-b.astype(float)).mean(2)[visible].mean()))
        internal=changes[:-1] if s['loop'] else changes
        median=float(np.median(internal)) if internal else 0
        row={'key':key,'slots':len(frames),'loop':s['loop'],'durations':s['durations'],'standingHeight':s['standingHeight'],'pixelsPerWorldUnit':s['standingHeight']/65.28,'geometry':geometry,'ivoryMedianByPose':tone,'registeredChange':changes,'seamRatio':changes[-1]/median if s['loop'] and median else 0,'duplicatePairs':[i for i,(a,b) in enumerate(pairs) if np.array_equal(a,b)]}
        rows.append(row)
        tiles=[]
        for a in frames:
            im=Image.fromarray(a).crop((64,128,320,384));bg=Image.new('RGB',im.size,'#293b40');bg.paste(im,(0,0),im);tiles.append(bg)
        # Every pose retained, with exact authored timing. No interpolated art.
        tiles[0].save(OUT/(key+'.gif'),save_all=True,append_images=tiles[1:],duration=s['durations'],loop=0)
    # Four facings together; all slots, split into six-frame columns.
    families=sorted({k.rsplit('-',1)[0] for k in states if k.rsplit('-',1)[-1] in ('north','south','east','west')})
    for family in families:
        keys=[family+'-'+d for d in ('south','north','east','west') if family+'-'+d in states]
        n=max(len(states[k]['files']) for k in keys);segments=(n+5)//6
        # Swimming transition boots can extend below their registration pivot.
        # Fit all artwork instead of clipping it into a fixed standing-height row.
        extent=[]
        for key in keys:
            s=states[key]
            for f in s['files']:
                b=images[f].getbbox();extent.append((b[0]-s['pivot'][0],b[1]-s['pivot'][1],b[2]-s['pivot'][0],b[3]-s['pivot'][1]))
        above=max(-b[1] for b in extent);below=max(0,max(b[3] for b in extent))
        cell_width=max(192,round(max(-b[0] for b in extent)+max(b[2] for b in extent)+20))
        cell_height=round(above+below+40);anchor_y=round(above+25)
        board=Image.new('RGB',(cell_width*6,len(keys)*segments*cell_height),'#293b40');draw=ImageDraw.Draw(board)
        for direction,key in enumerate(keys):
            s=states[key]
            for slot,f in enumerate(s['files']):
                x=slot%6*cell_width;y=(direction*segments+slot//6)*cell_height
                im=images[f];board.paste(im,(x+cell_width//2-round(s['pivot'][0]),y+anchor_y-round(s['pivot'][1])),im)
                draw.text((x+3,y+3),key+' '+str(slot)+' / '+str(s['durations'][slot])+'ms',fill='white')
        board.save(OUT/(family+'-contact.png'))
    report={'states':len(states),'slots':sum(len(s['files']) for s in states.values()),'uniquePaths':len(images),'rows':rows,'limits':'Registered pixel changes and ivory masks are review flags, not motion/anatomy certificates. GIFs use authored timings; gameplay locomotion uses distance cadence.'}
    (OUT/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
    if not (OUT/'baseline-contract.json').exists():
        (OUT/'baseline-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
    print('Current contract:',report['states'],'states /',report['slots'],'slots;',len(families),'complete-pose boards')
    print('Loop seam review:',[(r['key'],round(r['seamRatio'],2)) for r in sorted(rows,key=lambda r:r['seamRatio'],reverse=True)[:12]])
    print('Canvas edge contacts:',[(r['key'],[i for i,g in enumerate(r['geometry']) if g['edgeContact']]) for r in rows if any(g['edgeContact'] for g in r['geometry'])])
if __name__=='__main__':main()
