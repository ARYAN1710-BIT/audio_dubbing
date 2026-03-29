import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))

VOICE_MAP = {
    "SPEAKER_00": "21m00Tcm4TlvDq8ikWAM",
    "SPEAKER_01": "AZnzlk1XvdvUeBnXmlld",
}

def generate_tts(segments: list, output_dir: str = "output/tts") -> list:
    os.makedirs(output_dir, exist_ok=True)
    for i, seg in enumerate(segments):
        voice_id = VOICE_MAP.get(seg["speaker"], "21m00Tcm4TlvDq8ikWAM")
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=seg["translated"],
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
        )
        path = f"{output_dir}/seg_{i:03d}.mp3"
        with open(path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        seg["tts_path"] = path
        print(f"[TTS] ✅ Segment {i} saved: {path}")
    return segments