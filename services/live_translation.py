from Speech.text_to_speech import text_to_speech
from Speech.translate_speech import translate_from_microphone

target_language = 'es'
translations = translate_from_microphone(target_language=target_language)

result = text_to_speech(text=translations[target_language], language=target_language)
print(result)

