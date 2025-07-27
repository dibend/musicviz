import sys
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import subprocess
from tqdm import tqdm
import argparse

def generate_frames(audio_path, tmp_dir, line_color="blue", bg_color="white", fps=30):
    y, sr = librosa.load(audio_path)
    y = y / np.max(np.abs(y))  # Normalize
    total_frames = int(librosa.get_duration(y=y, sr=sr) * fps)
    samples_per_frame = int(sr / fps)

    os.makedirs(tmp_dir, exist_ok=True)

    for i in tqdm(range(total_frames), desc="Generating frames"):
        start = i * samples_per_frame
        end = start + samples_per_frame * 2
        snippet = y[start:end]

        fig, ax = plt.subplots(figsize=(10, 4), facecolor=bg_color)
        ax.plot(snippet, color=line_color)
        ax.set_facecolor(bg_color)
        ax.set_xlim([0, len(snippet)])
        ax.set_ylim([-1, 1])
        ax.axis('off')
        plt.tight_layout()
        
        frame_path = os.path.join(tmp_dir, f"frame_{i:05d}.png")
        fig.savefig(frame_path)
        plt.close(fig)

    return total_frames

def make_video_with_ffmpeg(tmp_dir, audio_path, output_path, fps):
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", os.path.join(tmp_dir, "frame_%05d.png"),
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    subprocess.run(cmd, check=True)

def cleanup(tmp_dir):
    for f in os.listdir(tmp_dir):
        if f.endswith('.png'):
            os.remove(os.path.join(tmp_dir, f))
    os.rmdir(tmp_dir)

def main():
    parser = argparse.ArgumentParser(description="Generate a simple music visualization video")
    parser.add_argument("input_audio", help="Path to the input audio file")
    parser.add_argument("output_video", help="Path to save the output video")
    parser.add_argument("--line-color", default="blue", dest="line_color",
                        help="Line color for the waveform (name or hex)")
    parser.add_argument("--bg-color", default="white", dest="bg_color",
                        help="Background color (name or hex)")
    args = parser.parse_args()

    audio_path = args.input_audio
    output_path = args.output_video
    line_color = args.line_color
    bg_color = args.bg_color

    tmp_dir = "frames_temp"
    fps = 30

    total_frames = generate_frames(audio_path, tmp_dir,
                                   line_color=line_color,
                                   bg_color=bg_color,
                                   fps=fps)
    make_video_with_ffmpeg(tmp_dir, audio_path, output_path, fps)
    cleanup(tmp_dir)
    print(f"✅ Video saved to: {output_path}")

if __name__ == "__main__":
    main()

