import asyncio
from ffmpy3 import FFmpeg
from ffmpy3 import FFprobe
import subprocess
import json
import time



#音频和图片合成视频
def make_video(name):
    audio_name = "./music/" + name + ".mp3"
    video_name = "./video/" + name + ".mp4"
    image_name = "./images/p3.jpg"
    ff = FFmpeg (
        global_options = [
            '-v', 'quiet'
        ],
        inputs = {
            image_name : [
                '-loop', '1', 
                '-r', '30'
            ], 
            audio_name : None
        },
        outputs = {
            video_name : [
                '-c:v', 'libx264', 
                '-c:a', 'ac3',
                '-b:v', '2M', 
                '-b:a', '192k',
                '-s', '1920x1080', 
                '-shortest', 
                '-y'
            ]
        }
    )
    print(ff.cmd)
    ff.run()

#获取视频信息
def get_vidoe_info(name):
    video_name = "./video/" + name + ".mp4"
    ff = FFprobe (
        inputs = {
            video_name : None
        },
        global_options = [
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams', '-show_format'
        ]
    )
    print (ff.cmd)
    stdout, stderr = ff.run(stdout=subprocess.PIPE)
    info = json.loads(stdout.decode('utf-8'))
    duration = info['format']['duration']

    print(info)
    


if __name__ == "__main__":
    name = "七里香"
    time1 = time.time()
    make_video(name)
    time2 = time.time()
    print(time2 - time1)
    #get_vidoe_info(name)



