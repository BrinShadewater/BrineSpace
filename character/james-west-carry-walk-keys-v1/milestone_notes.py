from pathlib import Path
import os,uuid,time,shutil

def insert_status(f, section, previous_header):
    entry=section.encode(); header=previous_header.encode()
    before=f.stat(); tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        with f.open('rb') as source,tmp.open('wb') as dest:
            pending=b''
            while True:
                chunk=source.read(1024*1024)
                pending+=chunk
                if entry.split(b'\n',1)[0] in pending:return
                at=pending.find(header)
                if at>=0:
                    dest.write(pending[:at]);dest.write(entry+b'\n');dest.write(pending[at:])
                    shutil.copyfileobj(source,dest,1024*1024)
                    break
                if not chunk:raise ValueError('Previous status header not found')
                keep=max(len(header),len(entry.split(b'\n',1)[0]))
                if len(pending)>keep:
                    dest.write(pending[:-keep]);pending=pending[-keep:]
        for attempt in range(5):
            after=f.stat()
            assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns)
            try:
                os.replace(tmp,f)
                break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()

def record_guides(root,section,previous_header):
    paths=[root/'docs/CURRENT_STATUS.md',root/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',root/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',root/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
    for f in paths:
        if f.name=='CURRENT_STATUS.md':
            insert_status(f,section,previous_header)
            continue
        old=f.read_bytes();entry=section.encode()
        if entry.split(b'\n',1)[0] in old:continue
        if f.name=='CURRENT_STATUS.md':
            at=old.index(previous_header.encode());new=old[:at]+entry+b'\n'+old[at:]
        else:new=old+b'\n'+entry
        tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
        try:
            for attempt in range(5):
                assert f.read_bytes()==old
                try:os.replace(tmp,f);break
                except PermissionError:
                    if attempt==4:raise
                    time.sleep(1)
        finally:
            if tmp.exists():tmp.unlink()
    return len(paths)
