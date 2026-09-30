#!/usr/bin/env bash
# Rebuild simple-enough-to-trust.mp4 from source.
# Needs: python3 (pip: piper-tts imageio-ffmpeg numpy), node + playwright (Chromium).
# VOICE_DIR must hold en_US-lessac-high.onnx(.json) from huggingface.co/rhasspy/piper-voices.
set -euo pipefail
cd "$(dirname "$0")"
FFMPEG=$(python3 -c "import imageio_ffmpeg as i; print(i.get_ffmpeg_exe())"); export FFMPEG
TMP=$(mktemp -d)
if [ -n "${VOICE_DIR:-}" ]; then   # regenerate voiceover clips (otherwise reuse audio/s*.wav)
  python3 - <<PY
import json, subprocess
for k, t in json.load(open('src/vo.json')):
    subprocess.run(['python3', '-m', 'piper', '-m', '$VOICE_DIR/en_US-lessac-high.onnx', '--length-scale', '0.86',
                    '--sentence-silence', '0.15', '-f', f'audio/{k}.wav'], input=t.encode(), check=True, capture_output=True)
PY
fi
python3 src/timing.py
python3 src/audio.py
for p in 0 1 2 3; do node src/capture.js video "$TMP/part$p.mp4" 30 $p 4 & done; wait
printf "file '%s'\n" "$TMP"/part{0,1,2,3}.mp4 > "$TMP/list.txt"
"$FFMPEG" -y -v error -f concat -safe 0 -i "$TMP/list.txt" -i audio/mix.wav -c:v copy -c:a aac -b:a 192k \
  -movflags +faststart -shortest simple-enough-to-trust.mp4
echo "wrote simple-enough-to-trust.mp4"
