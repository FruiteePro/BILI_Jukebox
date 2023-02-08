import asyncio
import random
import time
import os
import logging
from bilibili_api import live
from threading import Thread, Lock
import time

import start

start.get_default_info()

import wordpicker
import utils
import globaler as gl
import ffmpeg_cmd



room = live.LiveDanmaku(room_display_id=gl.room_id)
lock = Lock()
time_last_pop = time.time()

#主播放循环
async def music_player():
    while True:
        try:
            code, selected_music = choose_music()
            _, duration = await ffmpeg_cmd.get_vidoe_info(selected_music)
            time_point1 = time.time()
            logging.info("playing " + selected_music + "  music_duration: " + str(duration) + " second")
            if not os.path.exists('./video/' + selected_music + '.flv'):
                logging.warning("No music:" + selected_music)
                continue
            await begin_live(selected_music)
            time_point2 = time.time()
            real_duration = time_point2 - time_point1

            while real_duration < 0.9 * float(duration):
                try:
                    time_point1 = time.time()
                    await ffmpeg_cmd.push_stream(selected_music, real_duration)
                    time_point2 = time.time()
                    real_duration = real_duration + time_point2 - time_point1
                except:
                    break
                
            logging.info("music real play time: " + str(real_duration))
            if code:
                with lock:
                    gl.called_list.pop(0)

            if code:
                utils.delete_music(selected_music)
        except Exception as e:
            logging.error(e)
            break

#开播
async def begin_live(music_name):
    try:
        logging.info("live start")
        await ffmpeg_cmd.start_live(music_name)
    except Exception as e:
        logging.error(e)


#点歌循环
@room.on('DANMU_MSG')
async def call_list(event):
    with lock:
        code, music_name, usr_info = await wordpicker.analysis_danmuku(event)
    if code == -1:
        return 0
    if gl.check_music_name(music_name):
        with lock:
            await wordpicker.double_music_fault(usr_info)
            gl.clean_fault_music(music_name)
            return 0
    with lock:
        gl.download_list.append(music_name)
    task = video_composer(music_name, usr_info)
    asyncio.gather(task)


#添加一首 music
async def add_music(music_name):
    with lock:
        gl.called_list.append(music_name)


#音乐下载及封装
async def video_composer(music_name, usr_info):
    download_code, real_music_name = await wordpicker.music_downloader(music_name)
    if download_code == -1:
        await wordpicker.download_fault(usr_info, music_name)
        with lock:
            gl.clean_fault_music(music_name)
        return -1
    with lock:
        await wordpicker.success_danmuku(usr_info, music_name)
    video_compose_code, msg = await ffmpeg_cmd.make_video_2(music_name, real_music_name)
    if video_compose_code == -1:
        with lock:
            gl.clean_fault_music(music_name)
        print("video composer error : " + str(msg))
        return -1
    print("video composer success")
    
    count = 0
    while gl.download_list[0] != music_name:
        await asyncio.sleep(10)
        if gl.download_list[1] == music_name:
            count += 1
            if count == 30:
                pop_fist_music()
                count = 0

    await add_music(music_name)
    with lock:
        gl.download_list.pop(0)
    


#选择下一个音乐
#返回选择的 music_name
def choose_music():
    #print(gl.called_list)
    if not gl.called_list:
        num = random.randint(0, len(gl.default_list)-1)
        return 0, gl.default_list[num]
    else:
        with lock:
            res = gl.called_list[0];
            return 1, res

#排除排队bug
def pop_fist_music():
    time_curr = time.time()
    if time_curr - time_last_pop > 300:
        with lock:
            gl.download_list.pop(0)
            time_last_pop = time_curr


async def tasks():
    #room = live.LiveDanmaku(gl.room_id)
    room_connect = room.connect()
    await asyncio.gather(room_connect)

def run_bili_loop():
    asyncio.run(tasks())
    #print("nice")

def setup():
    t1 = Thread(target=run_bili_loop, args=())
    t1.start()
    asyncio.run(music_player())
    t1.join()


if __name__ == "__main__":
    setup()

