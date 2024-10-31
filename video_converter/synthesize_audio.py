from google.oauth2 import service_account
from google.cloud import texttospeech


def synthesize_audio(text):
    # Path to your service account key file
    credentials = service_account.Credentials.from_service_account_file(
        r"C:\Users\HP\Downloads\analog-figure-440119-j9-e5de0180b5fa.json")

    # Initialize the Text-to-Speech client with the loaded credentials
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    input_text = texttospeech.SynthesisInput(text=text)

    # Configure the voice parameters (you can adjust these as needed)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Set the audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )

    # Perform the text-to-speech synthesis
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Save the output audio to a file
    output_audio_path = "output_audio.mp3"
    with open(output_audio_path, "wb") as out:
        out.write(response.audio_content)

    return output_audio_path
