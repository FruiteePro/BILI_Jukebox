import asyncio
import os
import random
import time
from bilibili_api import live

from wordpicker import analysis_danmuku
import utils
import globaler as gl
import ffmpeg_cmd

room = live.LiveDanmaku(gl.room_id)


#主播放循环
async def music_player():
    while True:
        try:
            code, selected_music = choose_music()
            #gl.playing = selected_music
            duration = ffmpeg_cmd.get_vidoe_info(selected_music)
            time_point1 = time.time()
            print("playing " + selected_music + "  music_duration: " + duration + " s")
            await begin_live(selected_music)
            #await write_fifo(selected_music)

            if code:
                utils.delete_music(selected_music)
            time_point2 = time.time()
            real_duration = time_point2 - time_point1
            print("music real play time: " + real_duration)
            print
            #await asyncio.sleep(10)
        except Exception as e:
            print(e)

#开播
async def begin_live(music_name):
    try:
        print("live start")
        await ffmpeg_cmd.start_live(music_name)
        # code, get_duration =  await ffmpeg_cmd.get_vidoe_info(gl.playing)
        # if code == 1:
        #     duration = get_duration
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
    #######################################BUG
    # ret = os.fork()
    # if ret == 0:
    #     write_fifo()
    #     return
    # else:
    #     return
    asyncio.gather(write_fifo())
    



#video 写入 fifo
async def write_fifo():
    if gl.called_list:
        video_name = gl.called_list[0]
        fifo_path = './fifo/' + gl.pipe_name
        print("23")
        with open(fifo_path, 'w') as wf:
            wf.write(video_name)
            gl.called_list.pop(0)
        #with open(fifo_path, os.O_SYNC | os.O_CREAT | os.O_RDWR | os.O_NONBLOCK) as wf:
        # wf = os.open(fifo_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
        # os.write(wf, video_name.encode())
        # gl.called_list.pop(0)
        # os.close(wf)
    #print(content)
    #wf = os.open(fifo_path, os.O_SYNC | os.O_CREAT | os.O_RDWR | os.O_NONBLOCK)


#添加一首 music
async def add_music(music_name):
    gl.called_list.append(music_name)


#选择下一个音乐
#返回选择的 music_name
def choose_music():
    update_call_list()
    print(gl.called_list)
    if not gl.called_list:
        num = random.randint(0, len(gl.defult_list)-1)
        return 0, gl.defult_list[num]
    else:
        res = gl.called_list[0];
        gl.called_list.pop(0)
        return 1, res

#更新call_list
def update_call_list():
    fifo_path = './fifo/' + gl.pipe_name
    rf = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
    buffer = os.read(rf, 1024)
    os.close(rf)
    if len(buffer) == 0:
        return -1
    else:
        muisc_names = utils.str_2_name(buffer)
        gl.called_list.extend(muisc_names)
        return 1
            

async def tasks():
    #name_trans = write_fifo()
    room_connect = room.connect()
    await asyncio.gather(room_connect)



def setup():
    ret = os.fork()
    if ret == 0:
        asyncio.run(tasks())
    else:
        asyncio.run(music_player())


if __name__ == "__main__":
    name = "push"

    #asyncio.run(setup())
    utils.creat_FIFO(name)
    setup()
    #ffmpeg_cmd.start_live
