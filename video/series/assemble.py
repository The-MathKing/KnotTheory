"""Concatenate one episode's scenes into out/E01_<title>.mp4 with chapter markers.
Usage: python assemble.py E01 [E02 ...]   (QUALITY=l for the preview renders)"""
import re, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
QUAL = '480p15' if os.environ.get('QUALITY') == 'l' else '1080p30'

def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode().strip())

def assemble(ep):
    script = os.path.join(HERE, 'scripts', ep + '.md')
    ep_title = None; titles = {}
    for line in open(script, encoding='utf-8'):
        m = re.match(r'^# (.*)$', line)
        if m and ep_title is None: ep_title = m.group(1).strip()
        m = re.match(r'^## (E\d\dS\d\d) — (.*)$', line)
        if m: titles[m.group(1)] = m.group(2).strip()
    clips = []
    for sid in sorted(titles):
        p = os.path.join(HERE, 'media', 'videos', ep.lower(), QUAL, sid + '.mp4')
        if not os.path.exists(p): raise SystemExit(f'missing {p}')
        clips.append((sid, p))
    t = 0.0; chapters = []
    with open(os.path.join(HERE, 'media', f'concat_{ep}.txt'), 'w') as f:
        for sid, p in clips: f.write(f"file '{p}'\n")
    for sid, p in clips:
        d = dur(p); chapters.append((sid, titles[sid], t, t + d)); t += d
    with open(os.path.join(HERE, 'media', f'chapters_{ep}.txt'), 'w') as f:
        f.write(f';FFMETADATA1\ntitle={ep_title}\n')
        for sid, name, a, b in chapters:
            f.write(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(a*1000)}\nEND={int(b*1000)}\ntitle={name}\n')
    slug = re.sub(r'[^A-Za-z0-9]+', '_', ep_title.split('—', 1)[-1]).strip('_')
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    out = os.path.join(HERE, 'out', f'{ep}_{slug}.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(HERE, 'media', f'concat_{ep}.txt'),
                    '-i', os.path.join(HERE, 'media', f'chapters_{ep}.txt'), '-map_metadata', '1', '-c', 'copy', out], check=True)
    print('wrote', out, 'minutes', round(t/60, 1))
    for sid, name, a, b in chapters:
        print(f'  {int(a)//60:02d}:{int(a)%60:02d}  {sid}  {name}')

if __name__ == '__main__':
    for ep in sys.argv[1:]: assemble(ep)
