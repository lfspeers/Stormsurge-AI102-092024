import azure.cognitiveservices.speech as speech
import os


key = os.environ['AI_MULTISERVICE_KEY']
region = os.environ['AI_MULTISERVICE_REGION']

def translate_from_microphone(target_language, source_language='en-US'):

    translation_config = speech.translation.SpeechTranslationConfig(subscription=key, region=region, voice_name='de-DE-KlausNeural')
    translation_config.speech_recognition_language = source_language
    translation_config.add_target_language(target_language)
    translation_config.set_speech_synthesis_output_format(speech.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm)

    # For auto-recognition of input/source language
    auto_detect_source_language_config = speech.languageconfig.AutoDetectSourceLanguageConfig(['en-US', 'es-MX', 'de-DE'])

    audio_config = speech.audio.AudioConfig(use_default_microphone=True)

    client = speech.translation.TranslationRecognizer(translation_config=translation_config,
                                                      auto_detect_source_language_config=auto_detect_source_language_config,
                                                      audio_config=audio_config)
    

    print('Please speak into your microphone.')
    result = client.recognize_once()

    if result.reason == speech.ResultReason.TranslatedSpeech:
        print("Recognized: {}".format(result.text))
        print("""Translated into '{}': {}""".format(
            target_language, 
            result.translations[target_language]))
        return result.translations
    
    elif result.reason == speech.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    
    elif result.reason == speech.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speech.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


if __name__ == '__main__':
    result = translate_from_microphone(target_language='de')
