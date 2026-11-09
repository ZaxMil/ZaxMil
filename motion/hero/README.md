# ZaxMil Profile Hero — HyperFrames Motion Source

This is the editable, **original** motion composition used to generate the animated header in the profile README.

- Engine: [HyperFrames](https://github.com/heygen-com/hyperframes), seekable HTML-to-video renderer.
- Composition: [index.html](index.html)
- Static skyline source artwork: [assets/hero.svg](assets/hero.svg)
- Approved developer avatar: [assets/zax-avatar.webp](assets/zax-avatar.webp)
- Local animation script: [vendor/gsap.min.js](vendor/gsap.min.js), GSAP © GreenSock (see https://gsap.com/community/standard-license/).
- Output: [renders/zaxmil-hero.mp4](renders/zaxmil-hero.mp4).
- Embed: [../../assets/hero-motion.gif](../../assets/hero-motion.gif).

The profile README embeds an optimized GIF because GitHub README markdown does not autoplay MP4 videos or execute custom JavaScript. The MP4 is a portable preview; the composition is the editable source. For full-interaction sites, host the web composition separately.

## Regenerate

Requirements: Node.js 22+, ffmpeg, Chromium (installed by HyperFrames). In this directory:

~~~sh
npx --yes hyperframes browser ensure
npx --yes hyperframes lint
npx --yes hyperframes render --output renders/zaxmil-hero.mp4 --fps 24 --quality standard --workers 1

ffmpeg -y -i renders/zaxmil-hero.mp4 \
  -filter_complex "[0:v]fps=15,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle" \
  ../../assets/hero-motion.gif
~~~

The animation uses a finite, paused GSAP timeline with a four-second loop. No outbound API calls, telemetry from the composition, or paid video models are required.

If motion is uncomfortable, the full static alternative is at [../../assets/hero-poster.png](../../assets/hero-poster.png).
