import os
from modules.extractor   import extract_audio
from modules.denoiser    import denoise_audio
from modules.diarizer    import diarize
from modules.transcriber import transcribe
from modules.translator  import translate
from modules.tts         import generate_tts
from modules.aligner     import align_and_merge

# ── Config — fill these in ─────────────────────────────────
INPUT_FILE  = "input/sample.mp4"       # your test video/audio
TARGET_LANG = "es"                     # target language (es=Spanish, fr=French, hi=Hindi etc.)
HF_TOKEN    = "hf_YOUR_TOKEN_HERE"     # huggingface.co token
os.environ["ELEVENLABS_API_KEY"] = "YOUR_ELEVENLABS_KEY"
DEVICE      = "cpu"
# ───────────────────────────────────────────────────────────
HF_TOKEN = "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"  
os.environ["ELEVENLABS_API_KEY"] = "sk_d72760faf8b9ba98fe89bb88d0087989cfd672b853b0ea7e"# ← paste here
def main():
    print("\n=== 🎙️ Audio Dubbing Pipeline ===\n")

    print("Step 1: Extracting audio...")
    raw_audio = extract_audio(INPUT_FILE)

    print("\nStep 2: Denoising audio...")
    clean_audio = denoise_audio(raw_audio)

    print("\nStep 3: Speaker diarization...")
    diarization = diarize(clean_audio, HF_TOKEN)

    print("\nStep 4: Transcribing speech...")
    segments = transcribe(clean_audio, diarization, device=DEVICE)

    print("\nStep 5: Translating text...")
    segments = translate(segments, target_lang=TARGET_LANG)

    print("\nStep 6: Generating dubbed voices...")
    segments = generate_tts(segments)

    print("\nStep 7: Aligning & merging audio...")
    final = align_and_merge(segments, clean_audio)

    print(f"\n✅ Done! Dubbed audio saved to: {final}")

if __name__ == "__main__":
    main()