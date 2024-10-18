# Example 1 - From microphone
# Example 2 - From an audio file

import os, time
import azure.cognitiveservices.speech as speech

base_url = os.environ['AI_MULTISERVICE_ENDPOINT']
key = os.environ['AI_MULTISERVICE_KEY']
region = os.environ['AI_MULTISERVICE_REGION']


def transcribe_from_microphone():
    # SpeechConfig, AudioConfig, SpeechRecognizer (client)

    speech_config = speech.SpeechConfig(subscription=key, region=region)
    speech_config.speech_recognition_language='en-US'

    audio_config = speech.audio.AudioConfig(use_default_microphone=True)

    client = speech.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    result = client.recognize_once()

    if result.reason == speech.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text
    
    elif result.reason == speech.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    
    elif result.reason == speech.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speech.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")



def transcribe_from_file():
    speech_config = speech.SpeechConfig(subscription=key, region=region)
    speech_config.speech_recognition_language='en-US'

    audio_config = speech.audio.AudioConfig(use_default_microphone=True)

    client = speech.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(event):
        print(f"CLOSING on {event}")
        client.stop_continuous_recognition()
        nonlocal done
        done = True

    results = []
    client.session_started.connect(lambda evt: print(f'SESSION STARTED: {evt}'))
    client.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    client.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    client.recognized.connect(lambda evt: results.append(evt.result))
    client.recognized.connect(lambda evt: print(f"RECOGNIZED: {evt}"))
    # client.recognizing.connect(lambda evt: print(f"RECOGNIZING: {evt}"))

    client.session_stopped.connect(stop_cb)
    client.canceled.connect(stop_cb)

    client.start_continuous_recognition()
    while not done:
        time.sleep(0.5)

    for speech_recognition_result in results:
        if speech_recognition_result.reason == speech.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
        
        elif speech_recognition_result.reason == speech.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        
        elif speech_recognition_result.reason == speech.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speech.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
    
    return results




if __name__ == "__main__":
    # text = transcribe_from_microphone()
    file = 'data/FightMilk.wav'
    transcribe_from_file()