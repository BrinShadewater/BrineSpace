from pathlib import Path
P=Path(__file__).resolve().parent;D=P/'continuous-video-v3-white'
script=(P/'continuous-video-v1/review_raw.py').read_text(encoding='utf-8')
script=script.replace('green=(a[:,:,1]>a[:,:,0]+40)&(a[:,:,1]>a[:,:,2]+40)&(a[:,:,1]>100)','green=(a.min(axis=2)>=238)&((a.max(axis=2)-a.min(axis=2))<12)')
script=script.replace('green segmentation diagnostic only','white segmentation diagnostic only')
(D/'review_raw.py').write_text(script,encoding='utf-8')
print('White-background raw chronology reviewer prepared; no alpha or RGB artwork changes.')
