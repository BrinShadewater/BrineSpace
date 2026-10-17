from pathlib import Path
P=Path(__file__).resolve().parent;old=P.parent/'standing-step-video-v1'
for name in ['review_raw.py','extract_source.py','audit_masters.py','package_review.py']:
 dest=P/name;assert not dest.exists()
 s=(old/name).read_text(encoding='utf-8')
 if name=='extract_source.py':
  s=s.replace("'fixedPlateSize':[768,1024]","'fixedPlateSize':reg['plateSize']")
  s=s.replace("rgb=np.array(Image.open(file).convert('RGB'));", "image=Image.open(file).convert('RGB');assert list(image.size)==reg['plateSize'], 'Output dimensions differ from frozen input plate; inspect mapping before extraction';rgb=np.array(image);")
 dest.write_text(s,encoding='utf-8')
print('Whole clip review prepared with explicit input/output dimension guard.')
