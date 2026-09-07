"""Derive provisional deposit poses with separately authored release timing.

No new artwork is painted. Source pose reuse is explicit; locker contact still
requires runtime review before these candidates can be selected by gameplay.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parent
for actor in ['bill', 'veld', 'branforth']:
    version = {'bill': 'v4', 'veld': 'v1', 'branforth': 'v2'}[actor]
    pickup = ROOT / f'revisions/{actor}-pickup-helmet-east-{version}'
    target = ROOT / f'revisions/{actor}-deposit-helmet-east-v1'
    target.mkdir(exist_ok=True)
    source_manifest = json.loads((pickup / 'manifest.json').read_text(encoding='utf-8'))
    files = source_manifest['states'][0]['frameFiles']
    order = [5, 4, 3, 2, 1, 0]
    durations = [160, 200, 200, 260, 180, 160]
    release_frame = 4
    records = []
    contact = Image.new('RGB', (1104, 208), '#1d252a')
    for index, source_index in enumerate(order):
        source = pickup / files[source_index]
        frame = Image.open(source).convert('RGBA')
        assert frame.size == (92, 104)
        # Byte copies retain the exact source identity, including boundary poses.
        (target / f'frame_{index:03}.png').write_bytes(source.read_bytes())
        enlarged = frame.resize((184, 208), Image.Resampling.NEAREST)
        contact.paste(enlarged, (184 * index, 0), enlarged)
        records.append({'frame': index, 'source': source.relative_to(ROOT).as_posix(),
                        'sourcePose': source_index, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    removal_end = ROOT / f'pilot/{actor}-remove-helmet-east/frame_005.png'
    assert removal_end.read_bytes() == (target / 'frame_000.png').read_bytes(), actor
    contact.save(target / 'contact.png')
    manifest = {'status': 'derived_candidate_not_integrated', 'frameWidth': 92, 'frameHeight': 104,
                'pivot': [46, 98], 'states': [{'id': 'deposit-helmet-east', 'frameCount': 6,
                    'frameFiles': [f'frame_{i:03}.png' for i in range(6)],
                    'frameDurationsMs': durations, 'loop': False,
                    'events': [{'id': 'release-helmet-to-locker', 'frame': release_frame,
                                'timeMs': sum(durations[:release_frame])}]}],
                'derivation': 'Pickup pose images reused in reverse order; deposit timing and release marker authored separately. Marker is review metadata, not a runtime inventory event.'}
    (target / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (target / 'sources.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    (target / 'README.md').write_text(
        '# Provisional helmet deposit\n\n'
        'Rebuild with `python character/crew-underwater-v1/build_deposit_revision.py`. '
        'Six poses reuse the actor-specific pickup sequence in reverse order, with independent timing. '
        'The initial pose exactly matches the existing removal endpoint. '
        'The first empty-handed pose starts at 820 ms; the release marker is review metadata only.\n\n'
        'Not selected by runtime. Reversal does not prove a believable shelf interaction: '
        'the helmet must remain visible as a locker prop after hand release, and hand positions must '
        'meet the actual shelf. Pickup pose/proportion defects remain inherited. '
        'Review continuous motion, empty-hand withdrawal and inventory/save interruption semantics before integration.\n',
        encoding='utf-8')
    print(f'{actor}: six deposit poses, exact removal join, release at {sum(durations[:release_frame])} ms (candidate)')
