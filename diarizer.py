from pyannote.audio import Pipeline
import soundfile as sf
import torch

def diarize(audio_path: str, hf_token: str) -> list:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token  # try this instead of token=
    )

    data, sample_rate = sf.read(audio_path)
    waveform = torch.tensor(data).float()
    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)
    else:
        waveform = waveform.T

    audio = {"waveform": waveform, "sample_rate": sample_rate}
    diarization = pipeline(audio)

    segments = []

    # Handle both old and new pyannote output formats
    try:
        # pyannote v3 Annotation object
        for segment, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                "speaker": speaker,
                "start": round(segment.start, 3),
                "end":   round(segment.end, 3)
            })
    except AttributeError:
        # pyannote v4 DiarizeOutput object
        for turn in diarization:
            segments.append({
                "speaker": str(turn.speaker),
                "start": round(turn.start, 3),
                "end":   round(turn.end, 3)
            })
        
    for s in segments:
        print(f"[Diarizer] {s['speaker']}: {s['start']}s → {s['end']}s")

    return segments