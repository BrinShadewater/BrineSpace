"""Compare the saved video before keying/resizing; do not repair frames."""
from pathlib import Path
import subprocess,json
import imageio.v2 as iio
import imageio_ffmpeg
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
indices=[80,81,82,83,84,85]
reader=iio.get_reader(P/'source.mp4')
frames={i:reader.get_data(i) for i in indices};reader.close()
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(P/'source.mp4'),'-vf','select=between(n\\,80\\,85)','-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-']
run=subprocess.run(cmd,capture_output=True,check=True)
direct=np.frombuffer(run.stdout,np.uint8).reshape(-1,768,768,3)
board=Image.new('RGB',(768,552),'#303b40');draw=ImageDraw.Draw(board);rows=[]
for j,i in enumerate(indices):
    a=frames[i];b=direct[j];at=(j%3*256,j//3*276)
    board.paste(Image.fromarray(a).resize((256,256)),(at[0],at[1]+20));draw.text((at[0]+5,at[1]+3),str(i),fill='white')
    rows.append({'sourceFrame':i,'backgroundMedian':np.median(a[0:100,0:100,:],axis=(0,1)).tolist(),'independentInvocationMaxRgbDifference':int(np.abs(a.astype(int)-b.astype(int)).max())})
board.save(P/'raw-flash-detail.png')
report={'scope':'Raw RGB before foreground mask, resampling or grade. Separate FFmpeg invocation and imageio use the same bundled decoder, not independent decoder implementations.','rows':rows,'ffmpegExit':run.returncode,'sourceModified':False}
(P/'raw-flash-evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
