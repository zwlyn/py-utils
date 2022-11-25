# -*- encoding: utf-8 -*-
import os
import re
from moviepy.editor import VideoFileClip

PROXY = "socks5://127.0.0.1:10001"

def mp4ToMp3(mp4File):
    video = VideoFileClip(mp4File)
    audio = video.audio
    basename = os.path.basename(mp4File)
    audio.write_audiofile('{filename}.mp3'.format(filename=basename))

def mp4ToWav(mp4File):
    video = VideoFileClip(mp4File)
    audio = video.audio
    basename = os.path.basename(mp4File)
    audio.write_audiofile('{filename}.wav'.format(filename=basename))

def youtubToMp4(url):
    command = 'youtube-dl.exe --proxy {proxy} "{url}"'.format(proxy=PROXY, url=url)
    popen = Popen()
    res = popen(command)
    if str(res[0]) == "0":
        filename = re.findall(r"\[download\] (.*\.mp4)", res[1])[0]
        print("SUCCESS: 下载成功 ", filename)
        mp4ToWav(filename)
    else:
        print("ERROR: 下载失败，返回码：{reason}".format(reason=res))


