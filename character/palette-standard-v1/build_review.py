"""Build a same-clock before/after palette viewer from selected manifests."""
from standardize import ROOT,REPO,read,write,CAST

def main():
    frozen=read(ROOT/'baseline.json');mapped=read(ROOT/'mapping.json')['files'];result={}
    for actor,info in frozen['inventory']['actors'].items():
        timing={};current_files={}
        if actor in CAST:
            root=REPO/'character'/CAST[actor];catalog=read(root/'catalog.json')
            manifests=[root/f for f in catalog['body']]
        else:
            root=REPO/'character'/('margot-polish-v1' if actor=='margot' else 'robot-polish-v1')
            manifests=[root/'manifest.json' if actor=='margot' else root/actor/'manifest.json']
        for path in manifests:
            for state in read(path)['states']:
                timing[state['id']]=state['frameDurationsMs']
                frame_root=path.parent if actor in CAST else root
                current_files[state['id']]=[(frame_root/f).resolve().relative_to(REPO).as_posix() for f in state['frameFiles']]
        result[actor]={key:dict(pivot=s['pivot'],height=s['height'],durations=timing[key],
            before=['originals/'+mapped[f]['originalSha256']+'.png' for f in current_files[key]],
            after=['../../'+f for f in current_files[key]]) for key,s in info['states'].items()}
    write(ROOT/'review/view.json',result)
    print('Review state count:',sum(len(s) for s in result.values()))
if __name__=='__main__':main()
