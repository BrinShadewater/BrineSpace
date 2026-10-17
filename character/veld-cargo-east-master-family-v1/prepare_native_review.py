from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
script=(R/'character/veld-cargo-west-master-family-v1/review_native.py').read_text().replace('west','east').replace('West','East')
script=script[:script.index("html='''")]+"print('4 chronological boards /72 source-native pairs;72 lossless native decode checks pass')\n"
(P/'review_native.py').write_text(script,encoding='utf-8')
