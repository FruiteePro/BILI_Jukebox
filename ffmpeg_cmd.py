import asyncio
from ffmpy3 import FFmpeg
from ffmpy3 import FFprobe
import subprocess
import json
import time
import os

import globaler as gl
import utils

#音频和图片合成视频
async def make_video(name):
    try:
        print("video generating......")
        audio_name = "./music/" + name + ".mp3"
        video_name = "./video/" + name + ".flv"
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
                    '-c:a', 'aac',
                    '-b:v', '2M', 
                    '-b:a', '192k',
                    '-s', '1920x1080', 
                    '-f', 'flv',
                    '-shortest', 
                    '-y'
                ]
            }
        )
        print(ff.cmd)
        await ff.run_async()
        return 1, "success"
    except Exception as e:
        return -1, e

#获取视频信息
async def get_vidoe_info(name):
    try:
        video_name = "./video/" + name + ".flv"
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
        #print(info)
        return 1, duration
        # if isinstance(duration, ):
        #     return 1, duration
        # else:
        #     return -1, "error"

    except Exception as e:
        return -1, e

    

#开始推流
#这里使用一个命名管道来进行推流
async def start_live(name):
    pipi_path = './fifo/' + gl.pipe_name
    video_name = './video/' + name + '.flv'
    live_addr = "\"" + gl.rtmp_addr + gl.live_code + "\""
    if not os.path.exists(pipi_path):
        print('ERROR! No push FIFO!')
    ff = FFmpeg (
        global_options = [
            '-v', 'quiet'
        ],
        inputs = {
            video_name : ['-re']
        },
        outputs = {
            #"rtmp://rtmp地址/你的直播码" : [
            "" : [
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-f', 'flv'
            ]
        }   
    )
    #print(ff.cmd)
    #ff.run()
    print(ff.cmd + ' ' + live_addr)
    #os.system(ff.cmd + " " + live_addr + " &")
    os.system(ff.cmd + " " + live_addr)




if __name__ == "__main__":
    name = "七里香"
    fifo_name = 'push'
    #time1 = time.time()
    #make_video(name)
    #time2 = time.time()
    #print(time2 - time1)
    #get_vidoe_info(name)
    asyncio.run (start_live())




