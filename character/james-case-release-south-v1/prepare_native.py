from pathlib import Path
P=Path(__file__).resolve().parent
for name in ['native-world.gd','native-indexed.gd']:
    source=(P.parent/'james-case-release-north-v1'/name).read_text()
    source=source.replace('james-case-release-north-v1','james-case-release-south-v1').replace('North','South').replace('for rotation in [3]','for rotation in [1]')
    source=source.replace('james_case_release.direction="south"','james_case_release.direction="diagonal"')
    source=source.replace('Other directions retain selected older cancellation. Not every East source index/gears/invalidation/traffic proof.','East/West/North have separate selected release packs. Not every South source index/gears/invalidation/traffic proof.')
    (P/name).write_text(source)
for pack in ['james-case-release-east-v1','james-case-release-west-v1','james-case-release-north-v1']:
    for path in (P.parent/pack).glob('*.gd'):
        old=path.read_bytes();new=old.replace(b'james_case_release.direction="south"',b'james_case_release.direction="diagonal"')
        if new!=old:path.write_bytes(new)
print('South native fixtures prepared; invalid direction uses diagonal now all four facings are supported.')
