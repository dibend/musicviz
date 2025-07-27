import sys
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import subprocess
from tqdm import tqdm

def generate_frames(audio_path, tmp_dir, fps=30, max_duration=60):
    y, sr = librosa.load(audio_path, duration=max_duration)
    y = y / np.max(np.abs(y))  # Normalize
    total_frames = int(librosa.get_duration(y=y, sr=sr) * fps)
    samples_per_frame = int(sr / fps)

    os.makedirs(tmp_dir, exist_ok=True)

    for i in tqdm(range(total_frames), desc="Generating frames"):
        start = i * samples_per_frame
        end = start + samples_per_frame * 2
        snippet = y[start:end]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(snippet, color='blue')
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
    if len(sys.argv) != 3:
        print("Usage: python music_visualizer.py <input_audio> <output_video.mp4>")
        sys.exit(1)

    audio_path = sys.argv[1]
    output_path = sys.argv[2]
    tmp_dir = "frames_temp"
    fps = 30

    total_frames = generate_frames(audio_path, tmp_dir, fps=fps)
    make_video_with_ffmpeg(tmp_dir, audio_path, output_path, fps)
    cleanup(tmp_dir)
    print(f"✅ Video saved to: {output_path}")

if __name__ == "__main__":
    main()

