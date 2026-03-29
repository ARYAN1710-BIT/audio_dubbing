from deep_translator import GoogleTranslator

def translate(segments: list, target_lang: str = "es") -> list:
    translator = GoogleTranslator(source="auto", target=target_lang)
    for seg in segments:
        original = seg["text"]
        seg["translated"] = translator.translate(original)
        print(f"[Translator] \"{original}\" → \"{seg['translated']}\"")
    return segments