"""Build a conservative, explicit dependency manifest for Windows Game exports.
Exact references are followed; dynamic path prefixes retain their directory contents.
Nothing is deleted. JSON-relative frame paths and imported-resource dependencies remain covered.
"""
from pathlib import Path
import argparse, hashlib, json, re, subprocess, os
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'assets/runtime-release.json'
EXTENSIONS = {'.gd','.tscn','.tres','.gdshader','.shader','.png','.jpg','.jpeg','.webp','.svg','.ogg','.wav','.mp3','.json','.cfg','.ttf','.otf'}
TEXT = {'.gd','.tscn','.tres','.gdshader','.shader','.json','.cfg','.godot'}
STRINGS = re.compile(r'["\']([^"\'\n]+)["\']')
def collect(root=ROOT, read_root=None):
    root=root.resolve()
    selected, pending, reasons = set(), [], {}
    walked=set()
    def descendants(directory):
        relative=os.path.relpath(directory,root).replace('\\','/')
        if relative.split('/')[0] in {'.godot','.git','output','outputs','builds','asset_backups','skills'}: return
        key=str(directory)
        if key in walked:return
        walked.add(key)
        for folder, dirs, files in os.walk(directory,followlinks=False):
            dirs[:]=[x for x in dirs if not x.startswith('.') and x not in {'output','outputs','builds','asset_backups','skills'}]
            for name in files:yield Path(folder)/name
    seen_refs=set()
    def add(path, reason):
        if any(tag in reason for tag in [": dynamic", ": formatted"]) and path.suffix.lower() in {".gd"}: return
        absolute=Path(os.path.abspath(path))
        if not absolute.is_relative_to(root):return
        rel=absolute.relative_to(root).as_posix()
        if rel in selected:return
        if path.suffix.lower() not in EXTENSIONS and rel not in {'project.godot','NOTICE.md'}:return
        path=path.resolve()
        if not path.is_relative_to(root) or not path.is_file():return
        rel=path.relative_to(root).as_posix()
        if rel in {'assets/runtime-release.json','build_info.json'} or rel.startswith(('.godot/','.git/','output/','outputs/','builds/')): return
        if path.suffix.lower() not in EXTENSIONS and rel not in {'project.godot','NOTICE.md'}: return
        if rel not in selected: selected.add(rel);pending.append(path);reasons[rel]=reason
    def reference(value, owner):
        key=(value, "" if value.startswith("res://") else str(owner.parent))
        if key in seen_refs: return
        seen_refs.add(key)
        if not value or value == 'res://' or '\\' in value or '://' in value and not value.startswith('res://'): return
        if value.startswith('res://'): candidates=[root/value[6:]]
        else: candidates=[owner.parent/value,root/value]
        for p in candidates:
            if '%' in str(p):
                pattern=re.sub(r'%[-0-9.]*[sdf]', '*',str(p))
                # Glob only under the project. Static prefixes can include nested generated frame directories.
                import glob
                for match in glob.glob(pattern):
                    m=Path(match)
                    if m.is_dir():
                        for f in descendants(m): add(f,owner.relative_to(root).as_posix()+': formatted directory')
                    else: add(m,owner.relative_to(root).as_posix())
            elif p.is_file(): add(p,owner.relative_to(root).as_posix())
            elif value.startswith('res://'):
                if p.is_dir():
                    for f in descendants(p): add(f,owner.relative_to(root).as_posix()+': dynamic directory')
                elif p.parent.is_dir():
                    # String concatenation, e.g. "res://rooms/foo/panel-" + variant + ".png".
                    for f in p.parent.glob(p.name+'*'):
                        if f.is_dir():
                            for child in descendants(f): add(child,owner.relative_to(root).as_posix()+': dynamic prefix')
                        else: add(f,owner.relative_to(root).as_posix()+': dynamic prefix')
    add(root/'project.godot','entry');add(root/'scenes/title_screen.tscn','entry');add(root/'NOTICE.md','rights')
    # Runtime room/prop selection enumerates this directory rather than naming every JSON.
    while pending:
        p=pending.pop()
        if p.suffix.lower() not in TEXT: continue
        if p.relative_to(root).as_posix().startswith('addons/'):
            # Exporter tooling, not runtime code: its begins_with("res://rooms")
            # prefix TEST is not a dependency, yet reading it as one pulled the
            # entire rooms/ tree (~540 MB of sources) into every release.
            continue
        read_path=(read_root/p.relative_to(root)) if read_root is not None and (read_root/p.relative_to(root)).is_file() else p
        text=read_path.read_text(encoding='utf-8-sig',errors='replace')
        if p.name=='project.godot':
            text='\n'.join(line for line in text.splitlines() if not line.startswith('run/main_scene.'))
        for value in STRINGS.findall(text):
            if value.startswith('res://') or Path(value).suffix.lower() in EXTENSIONS:
                reference(value,p)
        if p.suffix=='.gd':
            match=re.search(r'^extends\s+["\']([^"\']+)',text,re.M)
            if match: reference(match[1],p)
    return selected,reasons

def main():
    selected,reasons=collect()
    for name in ['addons/brine_raw_export/plugin.gd','export_presets.cfg']:
        selected.add(name); reasons[name]='build configuration'
    rows=[]; aggregate=hashlib.sha256()
    settings=(ROOT/'export_presets.cfg').read_text(encoding='utf-8-sig')
    settings=re.sub(r'^export_files=.*$', '', settings, flags=re.M)
    aggregate.update(settings.replace('\r\n','\n').encode('utf-8'))
    for name in sorted(selected):
        p=ROOT/name
        if name=='export_presets.cfg': continue
        data=p.read_bytes()
        if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'} and data.startswith(b'version https://git-lfs.github.com/spec/'):
            raise RuntimeError('Fetch the LFS artwork before exporting: '+name)
        digest=hashlib.sha256(data).hexdigest()
        rows.append({'path':'res://'+name,'bytes':p.stat().st_size,'sha256':digest,'reason':reasons[name]})
        aggregate.update((name+'\0'+digest+'\n').encode())
    source_id=aggregate.hexdigest()
    manifest={'schema':1,'source_sha256':source_id,'files':rows}
    MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip())
    info={'build_id':'brinespace-'+source_id[:16],'source_sha256':source_id,'git_commit':commit,'working_tree_modified':dirty,'file_count':len(rows),'source_bytes':sum(x['bytes'] for x in rows)}
    (ROOT/'build_info.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    # The selected-resource preset allows Godot to follow its own imported dependencies.
    resources=[x['path'] for x in rows if Path(x['path']).suffix in {'.gd','.tscn','.tres','.gdshader','.shader','.ogg','.wav','.mp3','.ttf','.otf'}]
    p=ROOT/'export_presets.cfg';s=p.read_text()
    start=s.index('[preset.3]');end=s.index('[preset.3.options]',start)
    block=s[start:end]
    block=re.sub(r'export_filter="[^"]+"','export_filter="selected_resources"',block)
    block=re.sub(r'include_filter="[^"]*"','include_filter=""',block)
    block=re.sub(r'exclude_filter="[^"]*"','exclude_filter="output/*,outputs/*,builds/*,asset_backups/*,skills/*,.git/*,tests/*,docs/*"',block)
    block=re.sub(r'^export_files=.*\n','',block,flags=re.M)
    block=block.replace('export_filter="selected_resources"','export_filter="selected_resources"\nexport_files=PackedStringArray('+','.join(json.dumps(x) for x in resources)+')')
    p.write_text(s[:start]+block+s[end:],encoding='utf-8')
    print(json.dumps(info))
if __name__=='__main__': main()
