import whisperx

def transcribe(audio_path: str, segments: list, device: str = "cpu") -> list:
    model = whisperx.load_model("base", device=device, compute_type="int8")
    result = model.transcribe(audio_path, batch_size=8)

    align_model, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    result = whisperx.align(
        result["segments"], align_model, metadata, audio_path, device
    )

    enriched = []
    for seg in result["segments"]:
        speaker = "UNKNOWN"
        for d in segments:
            if d["start"] <= seg["start"] <= d["end"]:
                speaker = d["speaker"]
                break
        enriched.append({
            "speaker": speaker,
            "start":   seg["start"],
            "end":     seg["end"],
            "text":    seg["text"].strip()
        })
        print(f"[Transcriber] {speaker}: \"{seg['text'].strip()}\"")
    return enriched