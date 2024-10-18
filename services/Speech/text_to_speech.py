import azure.cognitiveservices.speech as speech
import os

base_url = os.environ['AI_MULTISERVICE_ENDPOINT']
key = os.environ['AI_MULTISERVICE_KEY']
region = os.environ['AI_MULTISERVICE_REGION']


def text_to_speech(text, language='en'):

    speech_config = speech.SpeechConfig(subscription=key, region=region)
    audio_config = speech.audio.AudioOutputConfig(use_default_speaker=True)

    voices = {
        'en': 'en-US-EmmaMultilingualNeural',
        'es': 'es-MX-LucianoNeural',
        'de': 'de-DE-KatjaNeural'
    }

    speech_config.speech_synthesis_voice_name = voices[language]

    speech_synthesizer = speech.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text(text)

    if result.reason == speech.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
        print(result.reason)
        print(result.audio_duration)   
        # result.properties # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.propertyid?view=azure-python
    elif result.reason == speech.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speech.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    return result


if __name__ == "__main__":
    text = "Sally sells sea shells at the sea shore."
    result = text_to_speech(text)
    print(result)