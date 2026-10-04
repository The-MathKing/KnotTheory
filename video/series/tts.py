"""Generate one WAV per script beat with Kokoro, for every scripts/E??.md.
Beats are keyed <scene>_<NN> by the number written in the script (which runs
through the whole episode), matching the hold()/beat() indices in the scenes.
Caches by text hash. Writes audio/durations.json. Usage: python tts.py [E01 E02 ...]"""
import re, json, hashlib, sys, os, glob
import soundfile as sf
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'audio'); VOICE = 'af_heart'; SPEED = 1.0; SR = 24000

def parse_all(only=None):
    scenes = {}
    for path in sorted(glob.glob(os.path.join(HERE, 'scripts', 'E*.md'))):
        ep = os.path.basename(path)[:3]
        if only and ep not in only: continue
        cur = None
        for line in open(path, encoding='utf-8'):
            m = re.match(r'^## (E\d\dS\d\d)\b', line)
            if m:
                cur = m.group(1); scenes[cur] = []; continue
            m = re.match(r'^(\d+)\.\s+(.*\S)\s*$', line)
            if m and cur:
                scenes[cur].append((int(m.group(1)), m.group(2)))
    return scenes

def main(only=None):
    scenes = parse_all(only)
    os.makedirs(OUT, exist_ok=True)
    meta_path = os.path.join(OUT, 'durations.json')
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    pipe = None
    for sc, beats in scenes.items():
        for i, text in beats:
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
            audio = np.concatenate([audio, np.zeros(int(0.35 * SR))])
            sf.write(wav, audio, SR)
            meta[key] = {'hash': h, 'dur': round(len(audio) / SR, 3), 'text': text}
            print(key, meta[key]['dur'], flush=True)
            json.dump(meta, open(meta_path, 'w'), indent=1)
    by_ep = {}
    for sc, beats in scenes.items():
        for i, _ in beats:
            by_ep[sc[:3]] = by_ep.get(sc[:3], 0) + meta.get(f'{sc}_{i:02d}', {}).get('dur', 0)
    for ep, t in sorted(by_ep.items()):
        print(ep, 'narration min:', round(t/60, 1))
    print('TOTAL min:', round(sum(by_ep.values())/60, 1))

if __name__ == '__main__':
    main(set(sys.argv[1:]) or None)
