"""Voiceover: Kokoro-82M neural TTS (Apache-2.0), voice af_heart, natural pace -> audio/s*.wav (24 kHz)."""
import json, os, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
VOICE_DIR = os.environ['VOICE_DIR']  # holds kokoro-v1.0.onnx + voices-v1.0.bin
VOICE, SPEED = os.environ.get('VOICE', 'af_heart'), float(os.environ.get('SPEED', '1.0'))
k = Kokoro(f'{VOICE_DIR}/kokoro-v1.0.onnx', f'{VOICE_DIR}/voices-v1.0.bin')
tot = 0
for key, text in json.load(open('src/vo.json')):
    audio, sr = k.create(text, voice=VOICE, speed=SPEED, lang='en-us')
    # trim leading/trailing silence, keep a short natural tail
    idx = np.where(np.abs(audio) > 0.01)[0]
    audio = audio[max(0, idx[0] - int(.03 * sr)): idx[-1] + int(.12 * sr)]
    sf.write(f'audio/{key}.wav', audio, sr, subtype='PCM_16')
    tot += len(audio) / sr; print(key, round(len(audio) / sr, 2))
print('total speech', round(tot, 2))
