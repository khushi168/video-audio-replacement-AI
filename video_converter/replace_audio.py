import moviepy.editor as mp


def replace_audio(video_file, audio_file):
    video = mp.VideoFileClip(video_file)
    audio = mp.AudioFileClip(audio_file)
    final_video = video.set_audio(audio)
    output_path = "output_video.mp4"
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path
