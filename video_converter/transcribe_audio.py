import os
import io
from google.oauth2 import service_account
from google.cloud import speech
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def transcribe_audio(video_file_path):
    # Load Google Cloud credentials directly from the JSON key file
    credentials = service_account.Credentials.from_service_account_file(
        r"C:\Users\HP\Downloads\analog-figure-440119-j9-e5de0180b5fa.json"
    )

    # Initialize the Speech-to-Text client with the loaded credentials
    client = speech.SpeechClient(credentials=credentials)

    try:
        # Step 1: Extract audio from the video file
        with VideoFileClip(video_file_path) as video:
            audio = video.audio
            audio_file_path = "temp_audio.wav"
            audio.write_audiofile(audio_file_path, codec='pcm_s16le')  # Writes audio in the correct format

        # Step 2: Load the audio file using pydub
        audio_segment = AudioSegment.from_wav(audio_file_path)

        # Step 3: Split audio into smaller chunks
        chunk_length_ms = 60000  # 1 minute chunks
        chunks = [audio_segment[i:i + chunk_length_ms] for i in range(0, len(audio_segment), chunk_length_ms)]

        transcription = ""

        # Step 4: Process each chunk
        for index, chunk in enumerate(chunks):
            chunk_file_path = f"temp_audio_chunk_{index}.wav"
            chunk.export(chunk_file_path, format="wav")  # Export the chunk as a wav file

            with io.open(chunk_file_path, "rb") as audio_file:
                audio_content = audio_file.read()

            # Configure the transcription request
            audio_obj = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                language_code="en-US",
                enable_automatic_punctuation=True
            )

            # Perform the transcription
            response = client.recognize(config=config, audio=audio_obj)
            transcription += " ".join([result.alternatives[0].transcript for result in response.results]) + " "

            # Cleanup chunk file
            os.remove(chunk_file_path)

        # Cleanup main audio file
        os.remove(audio_file_path)  # Remove the temporary audio file

        return transcription.strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
