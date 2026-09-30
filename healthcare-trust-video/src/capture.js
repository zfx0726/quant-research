// Usage: node capture.js stills <t1,t2,...> <outdir>
//        node capture.js video <out.mp4> [fps] [part] [parts]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const FFMPEG = process.env.FFMPEG || 'ffmpeg';
(async () => {
  const [mode, a1, a2, a3, a4] = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => { console.error('PAGE ERROR', e); process.exit(1); });
  await page.goto('file://' + path.join(__dirname, 'index.html'));
  await page.evaluate(() => window.ready);
  const shot = async t => { await page.evaluate(t => window.render(t), t);
    return page.screenshot({ type: 'jpeg', quality: 94, clip: { x: 0, y: 0, width: 1920, height: 1080 } }); };
  if (mode === 'stills') {
    for (const t of a1.split(',').map(Number)) require('fs').writeFileSync(`${a2}/f_${t.toFixed(2)}.jpg`, await shot(t));
  } else {
    const fps = +(a2 || 30), part = +(a3 || 0), parts = +(a4 || 1), N = 60 * fps;
    const f0 = Math.floor(N * part / parts), f1 = Math.floor(N * (part + 1) / parts);
    const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', a1], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = f0; f < f1; f++) {
      const buf = await shot(f / fps);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (f % 150 === 0) console.log(`part ${part}: frame ${f}/${f1}`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
