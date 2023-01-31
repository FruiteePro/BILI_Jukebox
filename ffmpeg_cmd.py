import asyncio
from ffmpy3 import FFmpeg, FFprobe
import subprocess
import json
import logging
import os

import globaler as gl
import utils

#改变图片格式
async def trans_image(name):
    try:
        image = "./images/" + name + ".jpg"
        new_image = "./images/" + name + ".jpg"
        ff = FFmpeg (
            global_options = [
                '-v', 'quiet'
            ],
            inputs = {
                image : [

                ]
            },
            outputs = {
                new_image : [
                    '-vf', 'crop=w=1920:h=1080',
                    '-y'
                ]
            }
        )
        logging.debug(ff.cmd)
        await ff.run_async()
        await ff.wait()
        return 1, "success"
    except Exception as e:
        return -1, e

#合成封面视频
async def make_image_video(name):
    try:
        image = './images/' + name + '.jpg'
        out_video = './video/' + name + '.flv'
        ff = FFmpeg(
            global_options = [
                '-v', 'quiet'
            ],
            inputs = {
                image : [
                    '-loop', '1', 
                    '-r', '30'
                ], 
            },
            outputs = {
                out_video : [
                    '-c:v', 'libx264', 
                    '-b:v', '3M', 
                    '-t', '600',
                    '-f', 'flv',
                    '-s', '1920x1080',
                    '-y'
                ]
            }
        )
        logging.debug(ff.cmd)
        await ff.run_async()
        await ff.wait()
    except Exception as e:
        logging.error(e)


#生成视频文字
async def make_default_video(name):
    try:
        image_video = "./images/" + name + ".jpg"
        new_image_video = "./image_video/" + name + ".flv"
        ff = FFmpeg (
            global_options = [
                '-v', 'quiet'
            ],
            inputs = {
                image_video : [
                    '-loop', '1', 
                    '-r', '30'
                ]
            },
            outputs = {
                new_image_video : [
                    '-c:v', 'libx264', 
                    '-b:v', '5M', 
                    '-t', '600',
                    '-f', 'flv',
                    '-s', '1920x1080',
                    '-vf', 'drawtext=fontcolor=white:fontsize=50:fontfile=./font/SmileySans-Oblique.ttf:text=\'BILI-Jukebox 点歌机\n\n点歌可发送弹幕 点歌-[歌名]\nPS：不用加方括号（目前只支持网易云哦）\':x=30:y=30, drawtext=fontcolor=white:fontsize=50:fontfile=SmileySans-Oblique.tff:text=\'当前播放歌曲：\n\n待播歌曲数：\n \n接下来播放：\':x=30:y=300, drawtext=fontcolor=white:fontsize=50:fontfile=SmileySans-Oblique.tff:text=\'播放进度\: \':x=1400:y=30',
                    '-y'
                ]
            }
        )
        logging.debug(ff.cmd)
        await ff.run_async()
        await ff.wait()
        return 1, "success"
    except Exception as e:
        return -1, e


#音频和图片合成视频
async def make_video(name):
    try:
        logging.info("video generating......")
        audio_name = "./music/" + name + ".mp3"
        video_name = "./video/" + name + ".flv"
        image_name = "./images/p4.jpg"


        k, duration = await get_music_info(name=name)
        if k == -1 :
            duration = 0

        duration = float(duration)
        mm = int(duration / 60)
        ss = int(duration % 60) + 1
        music_num = gl.get_called_num()
        if music_num > 0:
            next_music = gl.called_list[0]
        else:
            next_music = "列表是空的哦～"

        text1 = 'drawtext=fontcolor=white:fontsize=50:fontfile=./font/SmileySans-Oblique.ttf:text=\'%{pts\:gmtime\:0\:%M\\\\\\:%S}/' + str(mm) + '\:' + str(ss) + '\':x=1600:y=35,'
        text2 = 'drawtext=fontcolor=white:fontsize=50:fontfile=./font/SmileySans-Oblique.ttf:text=\'' + str(name) + '\':x=300:y=300,'
        text3 = 'drawtext=fontcolor=white:fontsize=50:fontfile=./font/SmileySans-Oblique.ttf:text=\'' + str(music_num) + '\':x=260:y=405,'
        text4 = 'drawtext=fontcolor=white:fontsize=50:fontfile=./font/SmileySans-Oblique.ttf:text=\'' + str(next_music) + '\':x=260:y=500'


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
                    '-b:v', '5M', 
                    '-b:a', '192k',
                    '-s', '1920x1080', 
                    '-vf', text1 + text2 + text3 + text4,
                    '-f', 'flv',
                    '-shortest', 
                    '-y'
                ]
            }
        )
        logging.debug(ff.cmd)
        await ff.run_async()
        await ff.wait()
        return 1, "success"
    except Exception as e:
        return -1, e

#通过替换音频来合成视频（似乎会快那么一点点
async def make_video_2(name):
    try:
        logging.info("video generating......")
        audio_name = "./music/" + name + ".mp3"
        video_name = "./video/" + name + ".flv"
        image_video_name = "./image_video/" + utils.select_image()

        k, duration = await get_music_info(name=name)
        if k == -1 :
            duration = 0

        duration = float(duration)
        mm = int(duration / 60)
        ss = int(duration % 60) + 1
        music_num = gl.get_called_num()
        if music_num > 0:
            next_music = gl.called_list[0]
        else:
            next_music = "列表是空的哦～"

        text1 = 'drawtext=fontcolor=white:fontsize=50:fontfile=./font/SmileySans-Oblique.ttf:text=\'%{pts\:gmtime\:0\:%M\\\\\\:%S}/' + str(mm) + '\:' + str(ss) + '\':x=1600:y=35,'
        text2 = 'drawtext=fontcolor=white:fontsize=50:fontfile=./font/SmileySans-Oblique.ttf:text=\'' + str(name) + '\':x=300:y=300,'
        text3 = 'drawtext=fontcolor=white:fontsize=50:fontfile=./font/SmileySans-Oblique.ttf:text=\'' + str(music_num) + '\':x=260:y=405,'
        text4 = 'drawtext=fontcolor=white:fontsize=50:fontfile=./font/SmileySans-Oblique.ttf:text=\'' + str(next_music) + '\':x=260:y=500'


        ff = FFmpeg (
            global_options = [
                '-v', 'quiet'
            ],
            inputs = {
                image_video_name : None, 
                audio_name : None
            },
            outputs = {
                video_name : [
                    '-c:v', 'libx264', 
                    '-c:a', 'aac',
                    '-s', '1920x1080', 
                    '-vf', text1 + text2 + text3 + text4,
                    '-f', 'flv',
                    '-shortest', 
                    '-y'
                ]
            }
        )
        logging.debug(ff.cmd)
        await ff.run_async()
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
        logging.debug(ff.cmd)
        stdout, stderr = ff.run(stdout=subprocess.PIPE)
        info = json.loads(stdout.decode('utf-8'))
        duration = info['format']['duration']

        return 1, duration


    except Exception as e:
        logging.error(e)
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
        logging.debug (ff.cmd)
        stdout, stderr = ff.run(stdout=subprocess.PIPE)
        info = json.loads(stdout.decode('utf-8'))
        duration = info['format']['duration']

        return 1, duration

    except Exception as e:
        logging.error(e)
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
        logging.debug(ff.cmd)
        await ff.run_async()
        await ff.wait()
    except Exception as e:
        logging.error(e)


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
        logging.debug(ff.cmd)
        await ff.run_async()
        await ff.wait()
    except Exception as e:
        logging.error(e)



if __name__ == "__main__":
    asyncio.run (start_live())




