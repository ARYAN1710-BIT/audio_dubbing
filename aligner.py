import librosa
import soundfile as sf
import numpy as np

def align_and_merge(segments: list, original_audio: str,
                    output_path: str = "output/dubbed.wav") -> str:
    original, sr = sf.read(original_audio)
    dubbed = np.zeros(len(original))

    for seg in segments:
        if "tts_path" not in seg:
            continue
        tts_audio, _ = librosa.load(seg["tts_path"], sr=sr)
        target_len = int((seg["end"] - seg["start"]) * sr)

        if len(tts_audio) == 0 or target_len == 0:
            continue

        rate = len(tts_audio) / target_len
        stretched = librosa.effects.time_stretch(tts_audio, rate=rate)

        start_sample = int(seg["start"] * sr)
        end_sample   = start_sample + min(len(stretched), target_len)
        dubbed[start_sample:end_sample] = stretched[:end_sample - start_sample]

    sf.write(output_path, dubbed, sr)
    print(f"[Aligner] ✅ Final dubbed audio: {output_path}")
    return output_path