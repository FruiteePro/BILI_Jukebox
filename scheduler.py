import asyncio
import random
import time
import os
import logging
from bilibili_api import live
from threading import Thread, Lock

from wordpicker import analysis_danmuku, music_downloader
import utils
import globaler as gl
import ffmpeg_cmd

room = live.LiveDanmaku(room_display_id=gl.room_id)
lock = Lock()


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
    code, music_name = await analysis_danmuku(event)
    if code == -1:
        return 0
    gl.download_list.append(music_name)
    task = video_composer(music_name)
    asyncio.gather(task)


#添加一首 music
async def add_music(music_name):
    with lock:
        gl.called_list.append(music_name)


#音乐下载及封装
async def video_composer(music_name):
    download_code = await music_downloader(music_name)
    if download_code == -1:
        gl.download_list.remove(music_name)
        return -1
    video_compose_code, msg = await ffmpeg_cmd.make_video_2(music_name)
    if video_compose_code == -1:
        gl.download_list.remove(music_name)
        print("video composer error : " + str(msg))
        return -1
    print("video composer success")
    while gl.download_list[0] != music_name:
        await asyncio.sleep(10)
    await add_music(music_name)
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
    #asyncio.run(music_player())
    t1.join()


if __name__ == "__main__":
    setup()

