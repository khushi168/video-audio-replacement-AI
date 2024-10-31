import os
import streamlit as st
from transcribe_audio import transcribe_audio
from correct_transcription import correct_transcription
from synthesize_audio import synthesize_audio
from replace_audio import replace_audio

st.title("Video Audio Replacement with AI")

# Upload video file
uploaded_video = st.file_uploader("Upload Video File", type=["mp4", "mov", "avi"])

if uploaded_video:
    # Get the uploaded file name and create a temp path
    uploaded_file_path = os.path.join("temp_video", uploaded_video.name)

    # Create the temp_video directory if it doesn't exist
    os.makedirs("temp_video", exist_ok=True)

    # Save the uploaded video file to the temp path
    with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_video.getbuffer())

    st.write("Transcribing audio...")
    transcription = transcribe_audio(uploaded_file_path)  # Pass the temp path
    st.write("Transcription completed.")

    st.write("Correcting transcription using GPT-4o...")
    corrected_text = correct_transcription(transcription)

    # Check if corrected_text is valid
    if corrected_text:
        st.write("Corrected Text:", corrected_text)  # Optional: Display the corrected text
        st.write("Synthesizing corrected audio...")
        synthesized_audio = synthesize_audio(corrected_text)

        st.write("Replacing audio in video...")
        output_video = replace_audio(uploaded_file_path, synthesized_audio)  # Pass the temp path

        st.video(output_video)  # Display the output video
        st.success("Audio replaced successfully!")
    else:
        st.error("Error: The corrected text is empty. Cannot synthesize audio.")
