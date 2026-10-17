from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'package-upper-v15.gd').read_text().replace('v15','v16').replace('V15','V16').replace('frames-v9/bare/002.png','frames-v9/helmet/002.png').replace('upper-v16-bare.png','upper-v16-helmet.png')
review=(p/'review_upper_v15.py').read_text().replace('v15','v16').replace('V15','V16').replace('frames-v9/bare/','frames-v9/helmet/').replace('upper-v16-bare.png','upper-v16-helmet.png')
for name,text in [('package-upper-v16.gd',source),('review_upper_v16.py',review)]:
    path=p/name;assert not path.exists();path.write_text(text)
print('Helmet counterpart package/review prepared without changing selected banks.')
