from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent
for d in ['east','west']:
 im=Image.open(P/'endpoints/bare'/('idle-'+d+'.png')).convert('RGBA');im=im.crop(im.getbbox());im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(P.parent/('james-air-'+d+'-v1')/'selected-idle-profile-reference.png')
