
import utils
import logging
from bilibili_api import live, Credential, Danmaku
import time

from WangyiyunMusicApi import music_download
import globaler as gl


credential = Credential(sessdata=gl.SESSDATA, bili_jct=gl.BILI_JCT, buvid3=gl.BUVID3)
room = live.LiveRoom(gl.room_id, credential)

#弹幕抓取
async def on_danmaku(event):
    # 收到弹幕
    text = event['data']['info'][1]
    usr_info = {
        'uid': event['data']['info'][2][0],
        'usr_name': event['data']['info'][2][1]
    }
    print(text)
    return text, usr_info


#弹幕解析
#@room.on('DANMU_MSG')
async def analysis_danmuku(event):  
    text, usr_info = await on_danmaku(event)
    code, name = utils.get_danmuku_result(text)
    if code == -1 :
        return -1, 'error', usr_info
        
    sig = await check_valid(usr_info, name)
    if not sig:
        return -1, 'error', usr_info
    return 1, name, usr_info


#判断冷却时间
async def check_valid(usr_info, music_name):
    uid = usr_info['uid']
    usr_name = usr_info['usr_name']
    time_curr = time.time()
    if uid in gl.usr_time:
        if time_curr - gl.usr_time[uid] < 30:
            text = usr_name + "的冷却还有" + str(int(30 - time_curr + gl.usr_time[uid])) + "秒哦=v="
            danmuku = Danmaku(text=text)
            await room.send_danmaku(danmuku)
            return False
    return True


#点歌成功弹幕
async def success_danmuku(usr_info, music_name):
    uid = usr_info['uid']
    usr_name = usr_info['usr_name']
    time_curr = time.time()
    text = "歌曲" + music_name + "在下载啦～"
    danmuku = Danmaku(text=text)
    await room.send_danmaku(danmuku)
    gl.usr_time[uid] = time_curr


#重复点歌失败
async def double_music_fault(usr_info):
    uid = usr_info['uid']
    usr_name = usr_info['usr_name']
    text = usr_name + "点的歌曲已经在列表中了OvO"
    danmuku = Danmaku(text=text)
    await room.send_danmaku(danmuku)

#下载失败弹幕
async def download_fault(usr_info, music_name):
    uid = usr_info['uid']
    usr_name = usr_info['usr_name']
    text = "歌曲" + music_name + "下载失败了T_T"
    danmuku = Danmaku(text=text)
    await room.send_danmaku(danmuku)

#循环弹幕

#音乐下载
async def music_downloader(name):
    code, mess = music_download(name)
    print("downloading......")
    if code == -1 :
        print("failed download :" + mess)
    else :
        print("success download: " + mess)
    return code, mess


if __name__ == "__main__":
    logging.info("start")
    #asyncio.run(room.connect())

