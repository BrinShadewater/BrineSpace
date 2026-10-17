from pathlib import Path
p=Path(__file__).resolve().parent
for source,target in [('package-upper-v13.gd','package-upper-v14.gd'),('review_upper_v13.py','review_upper_v14.py')]:
    path=p/target;assert not path.exists(),target
    path.write_text((p/source).read_text().replace('v13','v14').replace('V13','V14'))
print('New independent V14 source package/review; preferred sources unchanged.')
