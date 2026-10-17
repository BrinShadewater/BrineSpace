from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'package-upper-v14.gd').read_text().replace('v14','v15').replace('V14','V15')
source=source.replace('upper-body-intermediate-v15-raw.png','upper-crop-v15/raw.png')
source=source.replace('raw.resize(256,256,Image.INTERPOLATE_LANCZOS)','raw.resize(80,80,Image.INTERPOLATE_LANCZOS)')
source=source.replace('frame.blit_rect(raw,region,region.position)','frame.blit_rect(raw,Rect2i(region.position-Vector2i(96,56),region.size),region.position)')
source=source.replace('256.0/1254.0','80.0/1254.0')
source=source.replace('"translation":[0,0]','"translation":[96,56]')
source=source.replace('Coherent generated upper-body region','Generated enlarged upper-body reference crop, restored at its original crop origin')
for name,text in [('package-upper-v15.gd',source),('review_upper_v15.py',(p/'review_upper_v14.py').read_text().replace('v14','v15').replace('V14','V15').replace("'upper-body-intermediate-v15-raw.png'","'upper-crop-v15/raw.png'").replace('character/james-cargo-return-bridges-v1/upper-body-intermediate-v15-raw.png','character/james-cargo-return-bridges-v1/upper-crop-v15/raw.png'))]:
    path=p/name;assert not path.exists();path.write_text(text)
print('V15 native crop-origin package and independent source review prepared.')
