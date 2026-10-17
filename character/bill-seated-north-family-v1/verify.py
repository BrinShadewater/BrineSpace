from pathlib import Path
import json, hashlib
P = Path(__file__).resolve().parent
ROOT = P.parent.parent

def main():
    bindings = json.loads((P/'source-bindings.json').read_text())
    checks = []
    def check(ok, label):
        checks.append({'passed': bool(ok), 'check': label})
    for name, digest in bindings['sha256'].items():
        path = ROOT/name.removeprefix('res://')
        check(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest, 'Source binding '+name)
    registry = json.loads((P.parent/'ACTIVE_ASSETS.json').read_text())
    loader = (ROOT/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
    expected = {'sit-down-north', 'sit-rise-north', 'sit-idle-north', 'read-seated-north', 'read-seated-enter-north', 'read-seated-exit-north'}
    for gear, section in [('bare','actionOverrides'),('helmet','equipmentOverrides')]:
        manifest = json.loads((P/(gear+'-manifest.json')).read_text())
        check(registry[section]['bill-north-sitting-family'] == f'character/bill-seated-north-family-v1/{gear}-manifest.json', gear+' selected registry')
        check(f'res://character/bill-seated-north-family-v1/{gear}-manifest.json' in loader, gear+' normal loader')
        check(manifest['pivot'] == [128,224] and manifest['standingHeight'] == 148, gear+' figure plane')
        check({s['id'] for s in manifest['states']} == expected, gear+' action coverage')
        by_id = {s['id']:s for s in manifest['states']}
        for state in manifest['states']:
            check(len(state['frameFiles']) == 6 and all(f.startswith('res://') for f in state['frameFiles']), state['id']+' whole paths')
            duration = 960 if state['loop'] else (480 if 'read-seated-' in state['id'] else 800)
            check(sum(state['frameDurationsMs']) == duration, state['id']+' timing')
        enter, exit = by_id['read-seated-enter-north'], by_id['read-seated-exit-north']
        check(exit['frameFiles'] == enter['frameFiles'][::-1], gear+' reversed tablet poses')
        check(exit['frameDurationsMs'][0] == 60, gear+' cached first-slot contract')
    result = {'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks}
    (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':result['passed'],'checks':len(checks)}))
    return 0 if result['passed'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
