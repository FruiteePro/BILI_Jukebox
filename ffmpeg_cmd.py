import asyncio
from ffmpy3 import FFmpeg, FFprobe
import subprocess
import json
import os

import globaler as gl

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
        ff.run_async()
        await ff.wait()
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

        return 1, duration


    except Exception as e:
        print(e)
        return -1, e


#获取音乐信息
async def get_music_info(name):
    try:
        video_name = "./music/" + name + ".mp3"
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

        return 1, duration

    except Exception as e:
        print(e)
        return -1, e

    

#开始推流
#这里使用一个命名管道来进行推流
async def start_live(name):
    try:
        video_name = './video/' + name + '.flv'
        live_addr = gl.rtmp_addr + gl.live_code
        ff = FFmpeg (
            global_options = [
                '-v', 'quiet'
            ],
            inputs = {
                video_name : ['-re']
            },
            outputs = {
                #"rtmp://rtmp地址/你的直播码" : [
                live_addr : [
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-b:a', '192k',
                    '-f', 'flv'
                ]
            }   
        )
        print(ff.cmd)
        await ff.run_async()
        await ff.wait()
    except Exception as e:
        print(e)


#断点推流
async def push_stream(name, time):
    try:
        time = int(time)
        video_name = './video/' + name + '.flv'
        live_addr = gl.rtmp_addr + gl.live_code
        ff = FFmpeg (
            global_options = [
                '-v', 'quiet'
            ],
            inputs = {
                video_name : [
                    '-ss', str(time),
                    '-re'
                ]
            },
            outputs = {
                live_addr : [
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-b:a', '192k',
                    '-f', 'flv'
                ]
            }   
        )
        print(ff.cmd)
        await ff.run_async()
        await ff.wait()
    except Exception as e:
        print(e)



if __name__ == "__main__":
    asyncio.run (start_live())




