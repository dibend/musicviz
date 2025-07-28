# MusicViz

Welcome to **MusicViz**, the tiny tool that turns any song into a snazzy waveform video. Feed it an audio file and out pops an MP4 of dancing squiggles. Perfect for your next social post or quick demo.

## Features

- 🌀 Generates a waveform frame for every slice of your track using `librosa`.
- 🎥 Stitches frames into a video with `ffmpeg`.
- ⚡ Supports up to 60 seconds of audio by default to keep things speedy.
- 🧹 Cleans up after itself so your drive stays tidy.

## Quick Start

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

### Conda setup (Windows/macOS/Linux)

Prefer using Anaconda or Miniconda? Create an environment and install everything
with the same commands on any platform:

```bash
conda create -n musicviz python=3.10
conda activate musicviz
conda install -c conda-forge ffmpeg
pip install -r requirements.txt
```

2. **Run the visualizer**

```bash
python app.py path/to/input.mp3 output_video.mp4
```

You'll see progress bars as frames are created, then `ffmpeg` will assemble them into `output_video.mp4`.

## How It Works

`app.py` loads your audio, normalizes it, and splits it into small chunks. For each chunk, a waveform image is drawn with Matplotlib. Once all frames are ready, `ffmpeg` glues them together with the original audio track so everything stays in sync.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

Enjoy making music videos! 🎶
