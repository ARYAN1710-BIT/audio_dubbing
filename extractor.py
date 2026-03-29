import ffmpeg
import os

# Tell Python exactly where FFmpeg is
os.environ["PATH"] += os.pathsep + r"C:\Users\HP\Downloads\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin"

def extract_audio(input_path: str, output_path: str = "output/raw_audio.wav") -> str:
    os.makedirs("output", exist_ok=True)
    (
        ffmpeg
        .input(input_path)
        .output(output_path, ac=1, ar=16000, format='wav')
        .overwrite_output()
        .run(quiet=True)
    )
    print(f"[Extractor]  Audio saved to {output_path}")
    return output_path