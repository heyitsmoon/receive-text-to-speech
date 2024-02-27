import azure.cognitiveservices.speech as speechsdk
import requests
import json
import time
import random 
import os

AZURE_VOICES = [
    #"en-US-DavisNeural",
    # "en-US-TonyNeural",
    # "en-US-JasonNeural",
    # "en-US-GuyNeural",
     "en-US-JaneNeural",
    # "en-US-NancyNeural",
    #"en-US-JennyNeural",
    # "en-US-AriaNeural",
]

AZURE_VOICE_STYLES = [
    # Currently using the 9 of the 11 available voice styles
    # Note that certain styles aren't available on all voices
    # "angry",
    # "cheerful",
    # "excited",
    # "hopeful",
    # "sad",
    # "shouting",
    "terrified",
    # "unfriendly",
    # "whispering"
]
def play_text(name, text):
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get('SPEECH_KEY'), 
        region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = random.choice(AZURE_VOICES)

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.

    voice_style = random.choice(AZURE_VOICE_STYLES)
    voice_name = random.choice(AZURE_VOICES)

    ssml_text = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xmlns:emo='http://www.w3.org/2009/10/emotionml' xml:lang='en-US'><voice name='{voice_name}'><mstts:express-as style='{voice_style}'>{name}: {text}</mstts:express-as></voice></speak>"

    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(
                    cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


def main():


    url = "http://127.0.0.1:5000/login_curl"
    payload = {"username": "me", "password":"password"}
    #curl -X POST -d "username=me&password=password" https://127.0.0.1:5000/login_curl
    response = requests.post(url, data=payload)
    
    json_data = json.loads(response.text)

    access_token = json_data["access_token"]
    
    while(True): 
        print("waiting a minute")
        time.sleep(60)


        url_messages = "http://127.0.0.1:5000/curl_messages"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url_messages, headers=headers)
        messages = response.text.split("\n")

            


        for message in messages:
            message_parts = message.split("|")
            if len(message_parts) > 1:
                identifier = message_parts[0].strip()
                name = message_parts[2]
                message_text = message_parts[3]
                play_text(name, message_text)
                url_delete = f"http://127.0.0.1:5000/clear_message_id/{identifier}"
                response = requests.get(url_delete, headers=headers)





    
if __name__ == "__main__":
    main()