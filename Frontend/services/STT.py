from google.cloud import speech
import os, io

GOOGLE_CREDENTIALS_PATH = "credentials/google_stt.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH

def transcribe_audio(audio_path):
    client = speech.SpeechClient()

    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # ✅ MUST match recorder
        language_code="en-IN",    # ✅ Or change to "hi-IN", "ta-IN" etc.
        enable_automatic_punctuation=True,
        model="latest_long",      # ✅ better accuracy
        use_enhanced=True         # ✅ use enhanced model
    )

    response = client.recognize(config=config, audio=audio)
    print(response)

    for result in response.results:
        return result.alternatives[0].transcript

    return ""
