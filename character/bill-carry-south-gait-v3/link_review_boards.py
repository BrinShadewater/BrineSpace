from pathlib import Path
P=Path(__file__).resolve().parent;E=P.parent/'bill-carry-start-south-v2'
marker='Compatible saved-source admission, interruptions, natural routes and broader contact/loop polish remain under review.'
links=' Compare directional masters: <a style="color:#adcddd" href="../bill-carry-south-gait-v3/bare-cross-family-review.png">bare</a> / <a style="color:#adcddd" href="../bill-carry-south-gait-v3/helmet-cross-family-review.png">helmet</a>.'
for name in ['index.html','build_review.py']:
 p=E/name;s=p.read_text(encoding='utf-8')
 if links not in s:p.write_text(s.replace(marker,marker+links),encoding='utf-8')
