"""Concatenate the rendered scenes into one MP4 with chapter markers."""
import re, os, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {'partA': range(1, 9), 'partB': range(9, 17), 'partC': range(17, 25), 'partD': range(25, 32)}
QUAL = '1080p30'
titles = {}
for line in open(os.path.join(HERE, 'SCRIPT.md'), encoding='utf-8'):
    m = re.match(r'^## (S\d\d) — (.*)$', line)
    if m: titles[m.group(1)] = m.group(2).strip()
clips = []
for part, rng in FILES.items():
    for i in rng:
        sid = f'S{i:02d}'
        p = os.path.join(HERE, 'media', 'videos', part, QUAL, sid + '.mp4')
        if not os.path.exists(p): raise SystemExit(f'missing {p}')
        clips.append((sid, p))
def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode().strip())
norm = []
t = 0.0; chapters = []
for sid, p in clips:
    norm.append((sid, p))
    d = dur(p); chapters.append((sid, titles.get(sid, sid), t, t + d)); t += d
with open(os.path.join(HERE, 'media', 'concat.txt'), 'w') as f:
    for sid, p in norm: f.write(f"file '{p}'\n")
with open(os.path.join(HERE, 'media', 'chapters.txt'), 'w') as f:
    f.write(';FFMETADATA1\ntitle=Where Optimal Networks Stop Existing\n')
    for sid, name, a, b in chapters:
        f.write(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(a*1000)}\nEND={int(b*1000)}\ntitle={name}\n')
out = os.path.join(HERE, 'Where_Optimal_Networks_Stop_Existing.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(HERE, 'media', 'concat.txt'),
                '-i', os.path.join(HERE, 'media', 'chapters.txt'), '-map_metadata', '1', '-c', 'copy', out], check=True)
print('wrote', out, 'total minutes', round(t/60, 1))
for sid, name, a, b in chapters:
    print(f'{int(a)//60:02d}:{int(a)%60:02d}  {sid}  {name}')
