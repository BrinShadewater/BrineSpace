"""Build review media from the longest continuous episode in a native walk trace."""
from pathlib import Path
import argparse
import json
from PIL import Image, ImageDraw


def main(folder):
    folder = Path(folder).resolve()
    records = json.loads((folder / 'walk-sequence.json').read_text())
    episodes = []
    for index, record in enumerate(records):
        if not episodes or episodes[-1]['episode'] != record['episode']:
            episodes.append({'episode': record['episode'], 'indices': []})
        episodes[-1]['indices'].append(index)
    if not episodes:
        raise ValueError('No native walk samples')
    chosen = max(episodes, key=lambda episode: len(episode['indices']))
    indices = chosen['indices']
    if len(indices) <= 6:
        raise ValueError('No reviewable continuous episode')
    frames = []
    for index in indices:
        path = (folder / records[index]['file']).resolve()
        if not path.is_relative_to(folder):
            raise ValueError('Capture path leaves review folder')
        with Image.open(path) as image:
            frames.append(image.convert('RGB'))
    if len({frame.size for frame in frames}) != 1:
        raise ValueError('Capture dimensions changed during episode')
    times = [records[index]['time'] for index in indices]
    intervals = [b-a for a,b in zip(times,times[1:])]
    if not intervals or min(intervals) <= 0:
        raise ValueError('Episode time must advance')
    # GIF delays have 10-ms resolution. Round cumulative timestamps so 30/60fps
    # captures do not silently play faster by truncating every individual delay.
    boundaries = [round((t-times[0])*100) for t in times]
    boundaries.append(round((times[-1]-times[0]+intervals[-1])*100))
    durations = [(b-a)*10 for a,b in zip(boundaries,boundaries[1:])]
    if min(durations)<=0:
        raise ValueError('Capture cadence exceeds GIF timing resolution')
    frames[0].save(folder / 'live-walk.gif', save_all=True,
                   append_images=frames[1:], duration=durations, loop=0)
    width,height = frames[0].size
    sheet = Image.new('RGB',(width*3,height+24),'#293b40')
    draw = ImageDraw.Draw(sheet)
    for column, local_index in enumerate([0,len(frames)//2,len(frames)-1]):
        source_index = indices[local_index]
        record = records[source_index]
        sheet.paste(frames[local_index],(column*width,24))
        draw.text((column*width+6,5),
                  f"episode {chosen['episode']} sample {source_index}: {record['state']} {record['direction']}",
                  fill='white')
    sheet.save(folder / 'live-walk-contact.png')
    # First/middle/last can hide a one-frame discontinuity at a state change.
    boundaries = [i for i in range(1, len(indices))
                  if (records[indices[i-1]]['state'], records[indices[i-1]]['direction'])
                  != (records[indices[i]]['state'], records[indices[i]]['direction'])]
    boundary_pages = []
    for offset in range(0, len(boundaries), 3):
        page_boundaries = boundaries[offset:offset+3]
        contact = Image.new('RGB', (width*2, (height+24)*len(page_boundaries)), '#293b40')
        labels = ImageDraw.Draw(contact)
        pairs = []
        for row, boundary in enumerate(page_boundaries):
            pair = [indices[boundary-1], indices[boundary]]
            pairs.append(pair)
            for column, local_index in enumerate([boundary-1, boundary]):
                record = records[indices[local_index]]
                top = row*(height+24)
                contact.paste(frames[local_index], (column*width, top+24))
                labels.text((column*width+6, top+5),
                            f"sample {indices[local_index]}: {record['state']} {record['direction']}", fill='white')
        filename = f'state-transition-{offset//3:02}.png'
        contact.save(folder / filename)
        boundary_pages.append({'file': filename, 'sourcePairs': pairs})
    report = {'status':'review_media_only', 'totalSamples':len(records),
              'gifDurationMs':sum(durations),'gifTimingQuantumMs':10,
              'episodes':[{'episode':e['episode'],'samples':len(e['indices'])} for e in episodes],
              'previewEpisode':chosen['episode'],'previewSamples':len(indices),
              'sourceIndices':indices,
              'stateTransitionPages':boundary_pages,
              'limits':['Preview contains only the longest continuous episode; all raw captures and trace records are retained.',
                        'GIF repeats the travel segment including its exit; this is not a seamless gait loop or proof of visual acceptance.']}
    (folder / 'live-walk-review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ['totalSamples','episodes','previewEpisode','previewSamples']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder')
    main(parser.parse_args().folder)
