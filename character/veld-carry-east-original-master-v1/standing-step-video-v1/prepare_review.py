from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'continuous-video-v3-white/review_raw.py').read_text(encoding='utf-8')
(P/'review_raw.py').write_text(s,encoding='utf-8')
s=(P.parent/'continuous-video-v3-white/extract_source.py').read_text(encoding='utf-8')
old=s[s.index("reg=json.loads("):s.index("files=sorted(")]
new="reg=json.loads((P/'input-record.json').read_text(encoding='utf-8'));scale=reg['sourceScale'];native_size=tuple(reg['nativeSize']);offset=tuple(reg['fixedOffset']);ref_out=Image.open(P/'registered-reference.png').convert('RGBA')\n"
s=s.replace(old,new).replace('All141 raw frames','All raw frames').replace('Loop/contact/native/controller acceptance pending.','Finite start/stop/endpoint/contact/native/controller acceptance pending.')
(P/'extract_source.py').write_text(s,encoding='utf-8')
print('Raw chronology and input-frozen entire-source extraction prepared.')
