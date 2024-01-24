from flask import Flask, render_template, request, jsonify
import azure.cognitiveservices.speech as speechsdk
import random
import os

app = Flask(__name__)

AZURE_VOICES = [
    "en-US-DavisNeural",
    "en-US-TonyNeural",
    "en-US-JasonNeural",
    "en-US-GuyNeural",
    "en-US-JaneNeural",
    "en-US-NancyNeural",
    "en-US-JennyNeural",
    "en-US-AriaNeural",
]

AZURE_VOICE_STYLES = [
    # Currently using the 9 of the 11 available voice styles
    # Note that certain styles aren't available on all voices
    "angry",
    "cheerful",
    "excited",
    "hopeful",
    "sad",
    "shouting",
    "terrified",
    "unfriendly",
    "whispering"
]
def playText(name, text):
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

@app.route('/', methods=['GET', 'POST'])
def slash():
    return render_template('index.html')

@app.route('/messenger', methods=['GET', 'POST'])
def messenger():
    return render_template('messenger.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    name = request.args.get('name')
    message = request.args.get('message')
    playText(name, message)
    return jsonify(success=True), 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
