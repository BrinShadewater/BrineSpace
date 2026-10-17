from pathlib import Path
import json
P=Path(__file__).resolve().parent
assert not (P/'anatomy-config.json').exists(), 'Preserve reviewed config; edit deliberately'
configs={}
for d,source_ruler in [('east',70),('south',72),('west',60),('north',62)]:
    folder=P.parent/('james-death-'+d+'-v1')
    heads=json.loads((folder/'head-candidates.json').read_text())['heads']
    if d=='north':heads[6]=[89,85];heads[7]=[92,78]
    if d=='south':
        for i,point in {1:[98,38],2:[110,49],3:[83,73],4:[52,82],5:[50,83],9:[112,177],10:[119,178],11:[120,184]}.items():heads[i]=point
    skull=22 if d=='north' else 25
    lean=18 if d=='north' else 13
    ground_angles={'east':[0,-12,-15,-15,-25,-30],'west':[0,12,15,15,30,30],'south':[0,0,0,0,45,45],'north':[0,0,0,0,0,0]}[d]
    water_angles={'east':[0,0,0,-8,-15,-20],'west':[0,0,0,8,15,20],'south':[0,0,0,0,0,0],'north':[0,0,0,0,0,0]}[d]
    configs[d]={'heads':heads}
    for action,donors,angles in [('death-ground',[0,lean,lean,6,6,6],ground_angles),('death-water',[6]*6,water_angles)]:
        configs[d][action]={'scale':skull/source_ruler,'ruler':f'{source_ruler}px reviewed full cranium against{skull}px selected skull; one anatomical scale per action row, not silhouette normalization','helmetDonors':donors,'helmetAngles':angles}
(P/'anatomy-config.json').write_text(json.dumps(configs,indent=2)+'\n')
print('Prepared fixed anatomical audition and manually reviewed axial cranial proxies')
