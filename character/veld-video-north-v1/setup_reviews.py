from pathlib import Path
P=Path(__file__).resolve().parent.parent
base=P/'veld-video-east-v1'
for d in ['north','south']:
 p=P/f'veld-video-{d}-v1'
 (p/'review.py').write_text((base/'review.py').read_text())
 s=(base/'build_loop.py').read_text().replace('east',d)
 s=s.replace(f"P.parent/'veld-side-foundation-v1/{d}-standing.png'",f"P.parent/'veld-animation-pilot-v12/frames/idle-{d}/000.png'")
 (p/'build_loop.py').write_text(s)
