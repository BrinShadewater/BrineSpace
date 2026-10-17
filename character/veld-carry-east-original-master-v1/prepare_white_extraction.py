from pathlib import Path
P=Path(__file__).resolve().parent;D=P/'continuous-video-v3-white'
script=(P/'continuous-video-v1/extract_source.py').read_text(encoding='utf-8')
script=script.replace('green=(values[:,:,1]>values[:,:,0]+40)&(values[:,:,1]>values[:,:,2]+40)&(values[:,:,1]>100)','green=(values.min(axis=2)>=238)&((values.max(axis=2)-values.min(axis=2))<12)')
script=script.replace("'candidateCycle':[32,64]","'candidateCycle':[]")
script=script.replace('only chroma/background alpha plus1rawpx global edge erosion','only white/background alpha plus1rawpx global edge erosion; enclosed background gaps preserved, no blanket hole fill')
(D/'extract_source.py').write_text(script,encoding='utf-8')
compare=(P/'continuous-video-v1/compare_masters.py').read_text(encoding='utf-8')
(D/'compare_masters.py').write_text(compare,encoding='utf-8')
print('Fixed-reference white alpha extraction prepared; no RGB grading/per-frame normalization.')
