"""Lay out VO clips on the 60s timeline and emit timing.js for the renderer."""
import json, re, wave
vo = json.load(open('src/vo.json'))
GAP = {'s6': 0.6, 's7': 0.45, 's10': 0.5}
t, scenes = 0.25, []
for k, text in vo:
    t += GAP.get(k, 0.3) if scenes else 0
    w = wave.open(f'audio/{k}.wav'); d = w.getnframes() / w.getframerate()
    # captions: split on sentence/colon boundaries, time ∝ characters
    parts = []
    for sent in [p.strip() for p in re.split(r'(?<=[.:])\s+', text) if p.strip()]:
        if len(sent) <= 62: parts.append(sent); continue
        cur = ''
        for ch in re.split(r'(?<=,)\s+', sent):  # break long sentences at commas
            if cur and len(cur) + len(ch) > 62: parts.append(cur); cur = ch
            else: cur = (cur + ' ' + ch).strip()
        parts.append(cur)
    merged = []
    for p in parts:  # fold tiny fragments ("One:") into the next caption
        if merged and len(merged[-1]) < 8: merged[-1] += ' ' + p
        else: merged.append(p)
    parts = merged
    n = sum(len(p) for p in parts); c = t; caps = []
    for p in parts:
        dd = d * len(p) / n; caps.append([round(c, 3), round(c + dd, 3), p]); c += dd
    scenes.append({'id': k, 'start': round(t, 3), 'dur': round(d, 3), 'caps': caps})
    t += d
print('VO ends at', round(t, 2))
open('src/timing.js', 'w').write('window.TIMING=' + json.dumps({'total': 60, 'scenes': scenes}, indent=1) + ';\n')
