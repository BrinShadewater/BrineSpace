"""Compose existing authored/candidate poses into simulation-timed locker clips."""
from pathlib import Path
import json
import hashlib

ROOT = Path(__file__).resolve().parent
for actor in ['bill', 'veld', 'branforth']:
    pickup = {'bill': 'v4', 'veld': 'v1', 'branforth': 'v2'}[actor]
    for action, sources in {
        'equip-helmet': [f'revisions/{actor}-pickup-helmet-east-{pickup}', f'pilot/{actor}-equip-helmet-east'],
        'remove-helmet': [f'pilot/{actor}-remove-helmet-east', f'revisions/{actor}-deposit-helmet-east-v1'],
    }.items():
        target = ROOT / f'locker/{actor}-{action}-east'
        target.mkdir(parents=True, exist_ok=True)
        files, durations, events, provenance = [], [], [], []
        elapsed = 0
        for relative in sources:
            source = ROOT / relative
            manifest = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
            assert [manifest['frameWidth'], manifest['frameHeight'], manifest['pivot']] == [92, 104, [46, 98]]
            clip = manifest['states'][0]
            for event in clip.get('events', []):
                events.append({**event, 'frame': event['frame'] + len(files), 'timeMs': event['timeMs'] + elapsed})
            for file in clip['frameFiles']:
                path = source / file
                files.append('../../' + relative + '/' + file)
                provenance.append({'source': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            durations.extend(clip['frameDurationsMs'])
            elapsed += sum(clip['frameDurationsMs'])
        # The shared boundary image must not inherit two full independent holds.
        assert provenance[5]['sha256'] == provenance[6]['sha256']
        original_join = durations[5:7]
        durations[5:7] = [80, 100] if action == 'equip-helmet' else [120, 100]
        for event in events:
            event['timeMs'] = sum(durations[:event['frame']])
        elapsed = sum(durations)
        data = {'status': 'integrated_provisional_locker_sequence', 'frameWidth': 92, 'frameHeight': 104, 'pivot': [46, 98],
                'states': [{'id': action + '-east', 'frameCount': len(files), 'frameFiles': files,
                            'frameDurationsMs': durations, 'loop': False, 'events': events}],
                'sources': provenance,
                'joinTiming': {'frames': [5, 6], 'sourceDurationsMs': original_join, 'composedDurationsMs': durations[5:7], 'reason': 'One shared held pose, not two sequential full holds.'},
                'limitations': 'Candidate pose joins and shelf attachment alignment require visual refinement. Shelf visibility follows handoff markers; equipment commits at whole-action completion and cancellation keeps prior equipment.'}
        if action == 'equip-helmet':
            data['states'][0]['events'].append({'id': 'take-helmet-from-locker', 'frame': 2, 'timeMs': sum(durations[:2])})
        (target / 'manifest.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        print(f'{actor} {action}: {len(files)} frames, {elapsed} ms')
