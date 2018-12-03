
import pytube
link = "https://www.youtube.com/watch?v=PTpgUmIWPis"
yt = pytube.YouTube(link)
print('Video')
all_videos = yt.streams.all()

videos = yt.streams.filter(only_video=True).all()
for x in videos:
	print(x)

print('Audio')
#to get only audio use
audio = yt.streams.filter(only_audio=True).all()
for x in audio:
	print(x)
#audio_download = yt.streams.filter(only_audio=True).first()
#audio_download.download('C:\\Users\\cgarc\\Desktop\\cst205\\final_project\\yt_vids')

#stream = yt.streams.first()
#stream.download('C:\\Users\\cgarc\\Desktop\\cst205\\final_project\\yt_vids')
