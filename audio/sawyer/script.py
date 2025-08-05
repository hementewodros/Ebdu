import moviepy
paths = [r"audio\sawyer\13-1.mp4", r"audio\sawyer\14-1.mp4", r"audio\sawyer\15-1.mp4", r"audio\sawyer\17-1.mp4"]
for path in paths:
    video = moviepy.VideoFileClip(path)
    video.audio.write_audiofile(path.replace(".mp4", ".mp3"))
    video.close()
