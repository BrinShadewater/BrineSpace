from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=R/'character/bill-carry-start-south-v2'
s=(R/'character/bill-carry-start-north-v2/build_review.py').read_text(encoding='utf-8')
s=s.replace('bill-carry-north-gait-v2','bill-carry-south-gait-v3').replace('north','south').replace('North','South')
s=s.replace('The new South set is selected for new sessions. Existing saves retain their source version. Save/resume and interruptions pass the current station checks; natural routes and broader contact polish remain under review. <a href="version-continue.html" style="color:#adcddd">View station Continue comparisons</a>', 'This is a staged South candidate. Normal gameplay retains the prior South art. Compatible saved-source admission, interruptions, natural routes and broader contact/loop polish remain under review.')
(E/'build_review.py').write_text(s,encoding='utf-8')
print('Staged South motion page builder saved')
