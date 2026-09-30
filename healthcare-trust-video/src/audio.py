"""Score + SFX + voiceover mix, all synthesized/rendered locally -> audio/mix.wav (48 kHz stereo)."""
import json, subprocess, numpy as np, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR, T = 48000, 60.0
N = int(SR * T)
rs = np.random.default_rng(3)
tl = json.loads(open('src/timing.js').read().split('=', 1)[1].rstrip().rstrip(';'))
SC = {s['id']: s for s in tl['scenes']}
TXT = {s['id']: ' '.join(c[2] for c in s['caps']) for s in tl['scenes']}
def wt(i, sub): s = SC[i]; return s['start'] + s['dur'] * TXT[i].index(sub) / len(TXT[i])
FLIP = wt('s6', 'So let')

def load(path):
    raw = subprocess.run([FF, '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)
def place(buf, x, t0, g=1.0):
    i = int(t0 * SR); x = x[:max(0, len(buf) - i)]; buf[i:i + len(x)] += g * x
def env(n, a, r):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na); e[n - nr:] = np.minimum(e[n - nr:], np.linspace(1, 0, nr)); return e
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def lp(x, fc):  # one-pole lowpass (vectorized via FFT filter)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); return np.fft.irfft(X / (1 + 1j * f / fc), len(x))

t = np.arange(N) / SR
music = np.zeros((N, 2))

# --- pads: minor & uneasy before the flip, open major after ---
def pad(notes, t0, t1, bright, amp=.06):
    n = int((t1 - t0) * SR); tt = np.arange(n) / SR; out = np.zeros((n, 2))
    for m in notes:
        for ch, det in ((0, -1), (1, 1)):
            f0 = midi(m) * (1 + det * .0025)
            v = sum(np.sin(2 * np.pi * f0 * h * tt + rs.uniform(0, 6)) / h ** (1.6 - .4 * bright) for h in range(1, 7))
            out[:, ch] += v
    out *= amp / len(notes) * (1 + .15 * np.sin(2 * np.pi * .25 * tt))[:, None]
    out *= env(n, .8, .9)[:, None]; return out
dark = [[45, 57, 60, 64], [41, 57, 60, 65], [38, 57, 62, 65], [40, 56, 59, 64]]     # Am  F  Dm  E
light = [[48, 60, 64, 67, 71], [41, 60, 65, 69, 72], [43, 62, 67, 71, 74], [45, 60, 64, 69, 76]]  # Cmaj7 F G Am(add)
bar = 60 / 76 * 4
c = 0.0; i = 0
while c < FLIP:
    e = min(c + bar + .8, FLIP + .6); x = pad(dark[i % 4], c, e, 0, .07); j = int(c * SR); music[j:j + len(x)] += x; c += bar; i += 1
bar2 = 60 / 100 * 4; c = FLIP; i = 0
while c < T:
    e = min(c + bar2 + .8, T); x = pad(light[i % 4], c, e, 1, .06); j = int(c * SR); music[j:j + len(x)] += x[:N - j]; c += bar2; i += 1

# --- heartbeat under the problem half, slowly quickening ---
def thump(f=55, d=.18):
    n = int(d * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * (f * tt + 40 * (1 - np.exp(-tt * 30)) / 30)) * np.exp(-tt * 22)
c = 2.9
while c < FLIP - .6:
    for off, g in ((0, .35), (.22, .22)):
        place(music[:, 0], thump(), c + off, g); place(music[:, 1], thump(), c + off, g)
    c += 60 / (62 + 18 * c / FLIP)

# --- plucked arpeggio + soft kick after the flip ---
def pluck(f, d=.5):
    n = int(d * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + .3 * np.sin(4 * np.pi * f * tt) + .1 * np.sin(6 * np.pi * f * tt)) * np.exp(-tt * 7)
arp = [[72, 76, 79, 83], [72, 77, 81, 84], [74, 79, 83, 86], [72, 76, 81, 88]]
step = 60 / 100 / 2; k = 0; c = FLIP + bar2 / 2
while c < T - .8:
    ch = arp[int((c - FLIP) / bar2) % 4]; f = midi(ch[k % 4] - 12)
    pan = .5 + .35 * np.sin(k * .9)
    p = pluck(f); place(music[:, 0], p, c, .05 * (1 - pan)); place(music[:, 1], p, c, .05 * pan)
    if k % 4 == 0 and c > SC['s7']['start']:
        place(music[:, 0], thump(48, .25), c, .28); place(music[:, 1], thump(48, .25), c, .28)
    c += step; k += 1

# --- SFX ---
sfx = np.zeros(N)
def noise_sweep(d, f0, f1, g):
    n = int(d * SR); x = rs.standard_normal(n); out = np.zeros(n); fc = np.geomspace(f0, f1, n)
    y = 0.0; a = 1 - np.exp(-2 * np.pi * fc / SR)
    for i2 in range(n): y += a[i2] * (x[i2] - y); out[i2] = y
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 2 * g
def hit(g=1.0):
    n = int(.5 * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * (70 * tt + 90 * (1 - np.exp(-tt * 25)) / 25)) * np.exp(-tt * 9)
    snap = rs.standard_normal(n) * np.exp(-tt * 45) * .5
    return (body + snap) * g
def chime(f, g=.12):
    n = int(1.6 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + .4 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 3)) * np.exp(-tt * 2.2) * g
# envelopes falling
tEnv = wt('s1', 'Then')
for i2 in range(7): place(sfx, noise_sweep(.18, 3000, 600, .10), tEnv + .1 + i2 * .13 + .3)
# bills landing
for ph in ('A hospital', 'A doctor', 'A lab', 'And a letter'): place(sfx, noise_sweep(.3, 400, 3000, .12), wt('s2', ph) - .1)
place(sfx, hit(.55), wt('s2', 'this is not') + .15)                 # THIS IS NOT A BILL
place(sfx, hit(.35), wt('s4', 'One in five') + .95)                 # DENIED
for s in ('s3', 's4', 's5', 's7', 's8', 's9', 's10'):                # scene whooshes
    place(sfx, noise_sweep(.55, 300, 5000, .09), SC[s]['start'] - .5)
place(sfx, noise_sweep(1.6, 200, 9000, .16), FLIP - 1.3)             # riser into the redesign
place(sfx, chime(midi(84), .16), FLIP + .2)
for i2, ph in enumerate(('Automate', 'screen', 'and never')): place(sfx, chime(midi(79 + 3 * i2), .08), wt('s9', ph) + .4)
for i2, ph in enumerate(('A price', 'A bill', 'A system')): place(sfx, chime(midi(72 + [0, 4, 7][i2]), .09), wt('s10', ph))
place(sfx, chime(midi(84), .12), wt('s10', 'A system') + .85)

# --- voiceover ---
vo = np.zeros(N)
for s in tl['scenes']: place(vo, load(f"audio/{s['id']}.wav"), s['start'])
vo = lp(vo, 9000); vo = vo / np.max(np.abs(vo)) * .85
# sidechain duck the music under VO
e = np.convolve(np.abs(vo), np.ones(int(.05 * SR)) / int(.05 * SR), 'same')
duck = 1 - .55 * np.clip(e / .05, 0, 1)
duck = np.convolve(duck, np.ones(int(.25 * SR)) / int(.25 * SR), 'same')
music[:, 0] = lp(music[:, 0], 7000) * duck; music[:, 1] = lp(music[:, 1], 7000) * duck
mix = music * 1.0 + (vo + sfx)[:, None] * np.array([1, 1])
mix *= env(N, .05, 1.2)[:, None]
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
pcm = (np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes()
subprocess.run([FF, '-y', '-v', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11', '-ar', str(SR), 'audio/mix.wav'], input=pcm, check=True)
print('mix written; flip at', round(FLIP, 2))
