"""Trace which tracked asset files the BrineSpace runtime can actually reach.

Usage (from the repository root):
    python tools/live_asset_manifest.py

Roots are runtime code and data only: scripts/, rooms/, scenes/, brineui/,
brinecore-animation/ scripts and scenes, project.godot, export_presets.cfg and the
top-level character/*.json bindings. References are followed transitively through
JSON data (manifests, compositions, catalogs, registrations). A folder the code reads
with a runtime-built path or a directory listing counts every file inside it as
"dynamic"; JSON inside such folders is followed too. Tests, tools, docs and skills are
deliberately not roots: an asset only they mention is not live in the game.

Writes docs/ASSET_MANIFEST.md (the readable map) and
output/asset-manifest/live-asset-manifest.csv (every file with status and referrers).
"""
import collections
import csv
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_TOP = ('assets/', 'character/', 'rooms/', 'Brine icons/', 'brineui/',
             'mining-drone-animation/', 'brinecore-animation/')
CODE_EXT = ('.gd', '.gd.uid', '.gdshader', '.gdshader.uid', '.tscn', '.import', '.md', '.txt', '.py')
TOPS = r'(?:assets|character|rooms|Brine icons|brineui|mining-drone-animation|brinecore-animation)'
# Code references are followed too (a preloaded tools/*.gd or scripts/*.gd is runtime code).
REF_RE = re.compile(r'(?:res://)?((?:' + TOPS[3:-1] + r'|scripts|tools|scenes)/[A-Za-z0-9 _./\-]+)')
DYN_RE = re.compile(r'res://(' + TOPS + r'/[A-Za-z0-9_\-. ]+(?:/[A-Za-z0-9_\-. ]+)*/)[^"\']*(?:%s|%d|%03d|"\s*\+|"\s*%)')
FOLDER_RE = re.compile(r'res://(' + TOPS + r'/[A-Za-z0-9_\-. ]+(?:/[A-Za-z0-9_\-. ]+)*)/?"')
DIR_RE = re.compile(r'(?:get_files_at|get_directories_at|DirAccess\.open)\(\s*"res://([^"]+?)/?"')
REL_RE = re.compile(r'"([A-Za-z0-9_\-./ ]+\.(?:png|json|webp|jpg|wav|ogg|mp4))"')


def norm(path):
    return path.replace('\\', '/').rstrip('/').rstrip('.')


def is_root(path):
    if path.startswith(('scripts/', 'rooms/', 'scenes/', 'brinecore-animation/', 'brineui/')) and path.endswith(('.gd', '.tscn', '.gdshader')):
        return True
    if path in ('project.godot', 'export_presets.cfg'):
        return True
    return path.startswith('character/') and path.count('/') == 1 and path.endswith('.json')


def owner_of(ref):
    """Map a referencing file to a room / character / system key for the report."""
    match = re.match(r'rooms/[^/]+/(?:[^/]+/)?([a-z0-9_\-]+?)(?:_view|-composition-v\d+|_south_facing|_whole_view)?\.(gd|json)$', ref)
    if ref.startswith('rooms/') and match:
        name = match.group(1).replace('-', '_')
        if name in ('room_dressing', 'nursery', 'nursery_whole_view', 'full_wall_prop', 'decoration_props', 'riser_geometry', 'room_floor'):
            return 'system/room-rendering'
        return 'room/' + name
    if ref.startswith('character/'):
        parts = ref.split('/')
        return 'character/' + (parts[1] if len(parts) > 2 else parts[1].replace('.json', ''))
    if ref.startswith('scripts/'):
        stem = ref.split('/')[1].replace('.gd', '')
        for who in ('bill', 'veld', 'branforth', 'marsh', 'companion', 'architect', 'crew'):
            if stem.startswith(who):
                return 'character/' + who
        return 'system/' + stem
    if ref.startswith('scenes/'):
        return 'system/' + ref.split('/')[1].replace('.tscn', '')
    if ref.startswith('assets/'):
        return 'assets-data/' + ref.split('/')[1]
    return 'system/' + ref


def main():
    os.chdir(ROOT)
    tracked = [t for t in subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.split('\n') if t]
    tset = set(tracked)
    live, dyn_folders = set(), set()
    refby = collections.defaultdict(set)
    visited = set()
    queue = [t for t in tracked if is_root(t)]

    def scan(path):
        try:
            text = open(path, encoding='utf-8', errors='ignore').read()
        except OSError:
            return
        for m in DYN_RE.finditer(text):
            dyn_folders.add(norm(m.group(1)))
        for m in FOLDER_RE.finditer(text):
            folder = norm(m.group(1))
            if folder not in tset:
                dyn_folders.add(folder)
        for m in DIR_RE.finditer(text):
            dyn_folders.add(norm(m.group(1)))
        for m in REF_RE.finditer(text):
            target = norm(m.group(1))
            if target in tset:
                live.add(target)
                refby[target].add(path)
                if target.endswith(('.json', '.gd', '.tscn')):
                    queue.append(target)
        if path.endswith('.json'):
            base = os.path.dirname(path)
            for m in REL_RE.finditer(text):
                rel = norm(os.path.normpath(os.path.join(base, m.group(1))))
                if rel in tset and rel not in live:
                    live.add(rel)
                    refby[rel].add(path)
                    if rel.endswith('.json'):
                        queue.append(rel)

    def drain():
        while queue:
            path = queue.pop()
            if path in visited or path not in tset:
                continue
            visited.add(path)
            scan(path)

    drain()
    # JSON inside wholesale-loaded folders is parsed at runtime too; follow it until stable.
    while True:
        added = 0
        for t in tracked:
            if t not in visited and t.endswith('.json') and any(t.startswith(d + '/') for d in dyn_folders):
                queue.append(t)
                added += 1
        if not added:
            break
        drain()

    dyn_live = {t for t in tracked if any(t.startswith(d + '/') for d in dyn_folders)}
    rows = []
    folder_status = collections.defaultdict(collections.Counter)
    by_owner = collections.defaultdict(lambda: collections.defaultdict(int))
    status = collections.Counter()
    for t in tracked:
        if not t.startswith(ASSET_TOP) or t.endswith(CODE_EXT) or is_root(t):
            continue
        state = 'live' if t in live else ('dynamic' if t in dyn_live else 'unreferenced')
        folder = '/'.join(t.split('/')[:2])
        status[state] += 1
        folder_status[folder][state] += 1
        rows.append((t, state, ';'.join(sorted(refby.get(t, [])))))
        if state == 'live':
            for ref in refby[t]:
                by_owner[owner_of(ref)][folder] += 1

    out_dir = os.path.join('output', 'asset-manifest')
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'live-asset-manifest.csv'), 'w', encoding='utf-8', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(['path', 'status', 'referenced_by'])
        writer.writerows(sorted(rows))

    lines = ['# BrineSpace asset manifest', '',
             'Generated by `python tools/live_asset_manifest.py`; do not edit by hand. It traces `res://`',
             'references from runtime code (scripts/, rooms/, scenes/, character bindings) transitively through',
             'JSON data. Tests, tools, docs and skills are not roots: an asset only they mention is not live.',
             '', '| Status | Files | Meaning |', '|---|---|---|',
             f"| live | {status['live']} | reached by an exact path from runtime code or data |",
             f"| dynamic | {status['dynamic']} | inside a folder the code reads with a built path or directory listing |",
             f"| unreferenced | {status['unreferenced']} | nothing in the runtime points at it (provenance, superseded versions, sources) |",
             '', '## Live assets by owner', '',
             'Which asset folders each room, character or system loads. Moves must keep these pairs intact.', '']
    for owner in sorted(by_owner):
        lines.append(f'### {owner}')
        for folder, count in sorted(by_owner[owner].items(), key=lambda kv: -kv[1]):
            lines.append(f'- `{folder}` — {count} file(s)')
        lines.append('')
    lines += ['## Folder status', '',
              'Every second-level folder under the asset tops. A folder with zero live and zero dynamic files is',
              'an `archive/` candidate once tests no longer read it; a dynamic-only folder is loaded wholesale',
              'and must move as a unit.', '',
              '| Folder | live | dynamic | unreferenced |', '|---|---:|---:|---:|']
    for folder in sorted(folder_status):
        c = folder_status[folder]
        lines.append(f"| `{folder}` | {c['live']} | {c['dynamic']} | {c['unreferenced']} |")
    with open(os.path.join('docs', 'ASSET_MANIFEST.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines) + '\n')

    print(f"asset files: {len(rows)}  live={status['live']} dynamic={status['dynamic']} unreferenced={status['unreferenced']}")
    print(f"dynamic folders: {len(dyn_folders)}; fully unreferenced folders: "
          f"{sum(1 for c in folder_status.values() if c['live'] == 0 and c['dynamic'] == 0)} of {len(folder_status)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
