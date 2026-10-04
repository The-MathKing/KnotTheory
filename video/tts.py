"""Generate one WAV per script beat with Kokoro. Caches by text hash so edits
re-render only the beats that changed. Writes audio/durations.json."""
import re, json, hashlib, sys, os
import soundfile as sf
import numpy as np

SCRIPT = 'SCRIPT.md'
OUT = 'audio'
VOICE = 'af_heart'
SPEED = 1.0
SR = 24000

def parse(path):
    scenes = {}
    cur = None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^## (S\d\d)\b', line)
        if m:
            cur = m.group(1); scenes[cur] = []; continue
        m = re.match(r'^(\d+)\.\s+(.*\S)\s*$', line)
        if m and cur:
            scenes[cur].append(m.group(2))
    return scenes

def main(only=None):
    scenes = parse(SCRIPT)
    os.makedirs(OUT, exist_ok=True)
    meta_path = os.path.join(OUT, 'durations.json')
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    pipe = None
    for sc, beats in scenes.items():
        if only and sc not in only: continue
        for i, text in enumerate(beats, 1):
            key = f'{sc}_{i:02d}'
            h = hashlib.sha1(text.encode()).hexdigest()[:12]
            wav = os.path.join(OUT, key + '.wav')
            if os.path.exists(wav) and meta.get(key, {}).get('hash') == h:
                continue
            if pipe is None:
                from kokoro import KPipeline
                pipe = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
            chunks = [a for _, _, a in pipe(text, voice=VOICE, speed=SPEED)]
            audio = np.concatenate([np.asarray(c) for c in chunks])
            # 0.35 s of silence at the end so beats don't run together
            audio = np.concatenate([audio, np.zeros(int(0.35 * SR))])
            sf.write(wav, audio, SR)
            meta[key] = {'hash': h, 'dur': round(len(audio) / SR, 3), 'text': text}
            print(key, meta[key]['dur'], flush=True)
            json.dump(meta, open(meta_path, 'w'), indent=1)
    total = sum(v['dur'] for k, v in meta.items() if k in {f'{s}_{i:02d}' for s, b in scenes.items() for i in range(1, len(b)+1)})
    print('TOTAL narration (s):', round(total), 'min:', round(total/60, 1))

if __name__ == '__main__':
    main(set(sys.argv[1:]) or None)
