"""Rebuild review candidates from preserved generated sources; no provider calls.

Owner handoff explicitly requests a reproducible local bake. This performs canvas
registration, uniform species scaling, grayscale conversion for tintable tissue,
and deterministic simple glint overlays. It does not repaint source anatomy.
"""
from pathlib import Path
import hashlib
import json
import math
from PIL import Image, ImageDraw, ImageOps, ImageFont
import numpy as np

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT / 'review'
REVIEW.mkdir(exist_ok=True)
FILES = []

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, im, **meta):
    path = ROOT / name
    im.save(path)
    FILES.append(dict(path=name, dimensions=list(im.size), sha256=digest(path),
                      alpha_extrema=list(im.getchannel('A').getextrema()), **meta))
    return im

def gray(im):
    out = ImageOps.grayscale(im).convert('RGBA')
    out.putalpha(im.getchannel('A'))
    return out

def source(name):
    return Image.open(ROOT / 'sources' / (name + '.png')).convert('RGBA')

def point_glow(im, at, radius, strength=1):
    # Straight-alpha near-white falloff, no black RGB fringe.
    px = im.load()
    x0, y0 = at
    for y in range(max(0, int(y0-radius)), min(im.height, int(y0+radius)+1)):
        for x in range(max(0, int(x0-radius)), min(im.width, int(x0+radius)+1)):
            d = math.hypot(x-x0, y-y0)/radius
            if d < 1:
                a = round(255 * strength * (1-d)**2)
                if a > px[x,y][3]:
                    px[x,y] = (248, 253, 255, a)

def atlas(name, src, grid, cell, scale, pivots, target, fps):
    cols, rows = grid
    frames = []
    sheet = Image.new('RGBA', (cols*cell[0], rows*cell[1]))
    core = Image.new('RGBA', sheet.size)
    registration = []
    # Select one source pose. Deterministic periodic deformation avoids model-
    # generated anatomy/scale changes between independent atlas panels.
    for i in range(cols*rows):
        col, row = i % cols, i // cols
        box = (0, 0, round(src.width/cols), round(src.height/rows))
        frame = gray(src.crop(box))
        frame = frame.resize((round(frame.width*scale), round(frame.height*scale)), Image.Resampling.LANCZOS)
        pivot = pivots[0]
        offset = (round(target[0]-pivot[0]*scale), round(target[1]-pivot[1]*scale))
        registered = Image.new('RGBA', cell)
        registered.alpha_composite(frame, offset)
        overlay = Image.new('RGBA',cell)
        point_glow(overlay,target,15 if name=='lantern' else 7,.72)
        if name == 'lantern':
            alpha=np.array(registered.getchannel('A'))
            for left,right in [(65,115),(115,143),(143,167),(167,195),(195,255)]:
                ys,xs=np.where(alpha[220:,left:right]>80)
                if len(ys):
                    lowest=int(ys.max()); xx=float(np.median(xs[ys==lowest]))+left
                    point_glow(overlay,(xx,lowest+220),5,.6)
        phase=i*math.tau/8
        yy,xx=np.mgrid[0:cell[1],0:cell[0]]
        if name=='lantern':
            tail=np.clip((yy-target[1])/230,0,1)
            dx=8*tail*np.sin(phase+tail*3)
            breath=1+.025*math.sin(phase)
            sx=(xx-target[0])/breath+target[0]-dx
            sy=(yy-target[1])/breath+target[1]
        else:
            tail=np.clip((target[0]-xx)/580,0,1)
            sx=xx
            sy=yy+6*tail*np.sin(phase+tail*6)
        # PIL mesh performs bilinear sampling; shared inverse coordinates keep
        # tissue and white glints attached through every periodic phase.
        mesh=[]
        for y in range(0,cell[1],16):
            for x in range(0,cell[0],16):
                x1=min(x+16,cell[0]); y1=min(y+16,cell[1])
                quad=[]
                for qx,qy in [(x,y),(x,y1-1),(x1-1,y1-1),(x1-1,y)]:
                    quad.extend([float(sx[qy,qx]),float(sy[qy,qx])])
                mesh.append(((x,y,x1,y1),tuple(quad)))
        registered=registered.transform(cell,Image.Transform.MESH,mesh,Image.Resampling.BILINEAR)
        overlay=overlay.transform(cell,Image.Transform.MESH,mesh,Image.Resampling.BILINEAR)
        frames.append(registered)
        sheet.alpha_composite(registered, (col*cell[0],row*cell[1]))
        core.alpha_composite(overlay,(col*cell[0],row*cell[1]))
        registration.append(dict(frame=i, source_box=box, source_pivot=pivot, offset=list(offset)))
    body_name = 'lantern-bell-body.png' if name=='lantern' else 'ribbon-swimmer.png'
    core_name = 'lantern-bell-core.png' if name=='lantern' else 'ribbon-head.png'
    meta = dict(cell=list(cell), grid=list(grid), frames=8, fps=fps, pivot=list(target),
                tintable=True, registration=registration, source_scale=scale)
    save(body_name,sheet,**meta)
    save(core_name,core,cell=list(cell),grid=list(grid),frames=8,fps=fps,pivot=list(target),tintable=False)
    return frames

lantern = atlas('lantern',source('lantern'),(4,2),(320,480),.70,
    [(181,200),(181,207),(181,211),(181,204),(181,190),(181,192),(181,193),(181,195)],(160,160),6)
ribbon = atlas('ribbon',source('ribbon'),(1,8),(640,96),.50,
    [(1113,118),(1113,111),(1113,119),(1113,108),(1113,102),(1113,117),(1113,113),(1113,118)],(604,48),10)

def fit(name, src, dimensions, pivot):
    # One aspect-preserving scale per component; transparent canvas, no stretch.
    if name == 'tidewalker-body.png':
        src=src.crop(src.getchannel('A').getbbox())
    im = ImageOps.contain(src, (dimensions[0]-16,dimensions[1]-16), Image.Resampling.LANCZOS)
    out = Image.new('RGBA',dimensions)
    out.alpha_composite(im,((dimensions[0]-im.width)//2,(dimensions[1]-im.height)//2))
    return save(name,out,pivot=list(pivot),frames=1,fps=0,tintable=False)

body = fit('tidewalker-body.png',source('tidewalker-matte-v2'),(1600,420),(800,210))
fin = fit('tidewalker-fin.png',source('fin'),(320,256),(299,18))
sail = fit('tidewalker-sail.png',source('sail'),(160,160),(80,148))
# Body-pixel registration corresponds to current code coordinates. 13 cells maps
# to 1600 pixels (123.0769 pixels/cell); this is a handoff scale exception.
body_bounds=body.getchannel('A').getbbox()
px_per_cell = (body_bounds[2]-body_bounds[0])/13
lights = Image.new('RGBA',body.size)
positions=[]
for i in range(26):
    lx=5.3-i*.42
    ly=(.55 if i%2==0 else -.45)*(.4+.6*math.cos(lx*.16))
    at=(round(800+lx*px_per_cell),round(210+ly*px_per_cell))
    silhouette=np.array(body.getchannel('A'))[:,at[0]]
    ys=np.where(silhouette>100)[0]
    if len(ys):
        want=(ys.min()+ys.max())*.5+(.55 if i%2==0 else -.45)*(ys.max()-ys.min())*.5
        at=(at[0],int(ys[np.argmin(abs(ys-want))]))
    positions.append(list(at))
    point_glow(lights,at,9)
save('tidewalker-lights.png',lights,pivot=[800,210],light_positions=positions,tintable=True,
     light_region_size=[20,20],frames=1,fps=0)

concepts=source('concepts')
for species,box in [('glass-choir',(0,0,800,887)),('veil-kite',(800,0,1774,887))]:
    pose=ImageOps.contain(concepts.crop(box),(224,224),Image.Resampling.LANCZOS)
    tissue=gray(pose)
    core=pose.copy()
    luminance=np.array(ImageOps.grayscale(pose))
    a=np.array(pose.getchannel('A'))
    core.putalpha(Image.fromarray((a.astype(float)*np.clip((luminance.astype(float)-185)/70,0,1)).astype('uint8')))
    tissue_sheet=Image.new('RGBA',(1024,512)); core_sheet=Image.new('RGBA',tissue_sheet.size)
    for i in range(8):
        # Solid registration; slow bank/rotation is performed by runtime clock.
        at=(i%4*256+(256-pose.width)//2,i//4*256+(256-pose.height)//2)
        tissue_sheet.alpha_composite(tissue,at); core_sheet.alpha_composite(core,at)
    save(species+'-body.png',tissue_sheet,cell=[256,256],grid=[4,2],frames=8,fps=6,pivot=[128,128],tintable=True)
    save(species+'-core.png',core_sheet,cell=[256,256],grid=[4,2],frames=8,fps=6,pivot=[128,128],tintable=False)
alpha=np.array(body.getchannel('A'))
def rim_y(x,side):
    ys=np.where(alpha[:,x]>100)[0]
    return int(ys.min()+4 if side<0 else ys.max()-4)
fin_roots=[[round(800+(2.6-i*3.1)*px_per_cell),rim_y(round(800+(2.6-i*3.1)*px_per_cell),side)]
           for i in range(3) for side in [-1,1]]
sail_roots=[[round(800+(4.2-i*1.35)*px_per_cell),rim_y(round(800+(4.2-i*1.35)*px_per_cell),-1)] for i in range(7)]
manifest=dict(schema=1,status='installed sea-life pack',world_units_per_cell=384,
              owner_accepted=True,runtime_wired=True,
              acceptance_scope='Owner approved continuation from first-pass direction; integrated motion is a new review milestone.',
              tidewalker=dict(body_pivot=[800,210],pixels_per_cell=px_per_cell,
                  fin_roots=fin_roots,
                  sail_roots=sail_roots,
                  light_positions=positions),
              limitations=['Small-creature motion is derived from a single registered source pose with periodic deformation.',
                  'Lantern tip glints follow the same deformation as tissue.',
                  'Matte-v2 tidewalker removes baked dot chains; original source retained as rejected material treatment.',
                  'Fin and sail roots are registered inside the actual body silhouette.',
                  'Tidewalker density is 384/pixels_per_cell world units per active art pixel; no invented upscaled detail.',
                  'No playable release export; integrated owner review remains separate from continuation approval.'],
              files=FILES,sources=[dict(path='sources/'+p.name,sha256=digest(p),dimensions=list(Image.open(p).size))
                                  for p in sorted((ROOT/'sources').glob('*.png'))])
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

try:
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
    small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
except OSError:
    font=small=ImageFont.load_default()
board=Image.new('RGBA',(1500,1320),(16,30,38,255))
d=ImageDraw.Draw(board)
d.text((30,18),'BRINESPACE / SEA LIFE V1 / FIRST-PASS REVIEW',font=font,fill='#dce8e8')
d.text((30,50),'Candidate art only. Layer separation, motion and runtime review remain open.',font=small,fill='#a7bbc3')
def preview(im,box,tint=None,bg=None):
    x,y,w,h=box
    if bg: d.rectangle((x,y,x+w,y+h),fill=bg)
    im=ImageOps.contain(im,(w,h),Image.Resampling.LANCZOS)
    if tint:
        rgb=Image.new('RGBA',im.size,tint)
        rgb=__import__('PIL.ImageChops',fromlist=['multiply']).multiply(im,rgb)
        im=rgb
    board.alpha_composite(im,(x+(w-im.width)//2,y+(h-im.height)//2))
for i in range(4):
    preview(lantern[i],(30+i*205,105,180,290),(64,242,217,255))
d.text((30,400),'Lantern bell / 8 phases / 320 x 480 / 6 fps / tintable',font=small,fill='#c0d5d9')
preview(lantern[0],(910,105,180,290),None,'#c4c3b7')
preview(lantern[0],(1160,105,180,290),None,'#642b53')
d.text((910,400),'Alpha checks: light and contrasting grounds',font=small,fill='#c0d5d9')
for i in range(3): preview(ribbon[i],(30,445+i*57,780,55),(153,255,158,255))
d.text((30,625),'Ribbon swimmer / 8 phases / 640 x 96 / 10 fps',font=small,fill='#c0d5d9')
preview(body,(30,665,1120,260))
preview(fin,(1160,665,145,130));preview(sail,(1310,665,150,140))
d.text((30,940),'Tidewalker / body, fin, sail and 26-dot overlay / attachment review pending',font=small,fill='#c0d5d9')
preview(concepts.crop((0,0,800,887)),(45,995,300,260))
preview(concepts.crop((800,0,1774,887)),(770,995,330,260))
d.text((355,1010),'GLASS CHOIR',font=font,fill='#cbeae6')
d.text((355,1050),'Filter-feeder / 0.35 cells',font=small,fill='#a7bbc3')
d.text((355,1080),'Three chambers; drifts and slowly rotates.',font=small,fill='#a7bbc3')
d.text((1110,1010),'VEIL KITE',font=font,fill='#cbeae6')
d.text((1110,1050),'Solitary glider / 0.9 cells',font=small,fill='#a7bbc3')
d.text((1110,1080),'Folded membrane; banks with the current.',font=small,fill='#a7bbc3')
board.convert('RGB').save(REVIEW/'contact-sheet.jpg',quality=94)
print('Baked',len(FILES),'candidate PNGs; seven sources preserved; review/contact-sheet.jpg')
