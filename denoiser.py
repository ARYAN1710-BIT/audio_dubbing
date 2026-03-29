import noisereduce as nr
import soundfile as sf

def denoise_audio(input_path: str, output_path: str = "output/clean_audio.wav") -> str:
    data, rate = sf.read(input_path)
    reduced = nr.reduce_noise(y=data, sr=rate, stationary=False)
    sf.write(output_path, reduced, rate)
    print(f"[Denoiser] ✅ Clean audio saved to {output_path}")
    return output_path