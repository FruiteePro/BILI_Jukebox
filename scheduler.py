import asyncio
import os
import random
import time
from bilibili_api import live
from threading import Thread, Lock

from wordpicker import analysis_danmuku
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
            print("playing " + selected_music + "  music_duration: " + str(duration) + " second")
            await begin_live(selected_music)
            time_point2 = time.time()
            real_duration = time_point2 - time_point1

            while real_duration < 0.9 * float(duration):
                time_point1 = time.time()
                await ffmpeg_cmd.push_stream(selected_music, real_duration)
                time_point2 = time.time()
                real_duration = real_duration + time_point2 - time_point1
                
            print("music real play time: " + str(real_duration))
            with lock:
                gl.called_list.pop(0)

            if code:
                utils.delete_music(selected_music)
        except Exception as e:
            print(e)

#开播
async def begin_live(music_name):
    try:
        print("live start")
        await ffmpeg_cmd.start_live(music_name)
    except Exception as e:
        print(e)


#点歌循环
@room.on('DANMU_MSG')
async def call_list(event):
    code, music_name = await analysis_danmuku(event)
    if code == -1:
        return 0
    code, msg = await ffmpeg_cmd.make_video(music_name)
    if code == -1:
        return 0
    print(msg)
    await add_music(music_name)

#添加一首 music
async def add_music(music_name):
    with lock:
        gl.called_list.append(music_name)


#选择下一个音乐
#返回选择的 music_name
def choose_music():
    print(gl.called_list)
    if not gl.called_list:
        num = random.randint(0, len(gl.defult_list)-1)
        return 0, gl.defult_list[num]
    else:
        with lock:
            res = gl.called_list[0];
            return 1, res


async def tasks():
    room_connect = room.connect()
    await asyncio.gather(room_connect)

def run_bili_cycle():
    asyncio.run(tasks())
    print("nice")


def setup():
    t1 = Thread(target=run_bili_cycle, args=())
    t1.start()
    asyncio.run(music_player())
    t1.join()


if __name__ == "__main__":
    setup()

