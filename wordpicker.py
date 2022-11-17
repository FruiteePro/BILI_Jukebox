from bilibili_api import live
import json
import asyncio

import globaler as gl
import utils
from WangyiyunMusicApi import music_download


#room = live.LiveDanmaku(21282223)


#弹幕抓取
async def on_danmaku(event):
    # 收到弹幕
    text = event['data']['info'][1]
    #print(json.dumps(event, indent=2))
    print(text)
    return text


#弹幕解析
#@room.on('DANMU_MSG')
async def analysis_danmuku(event):  
    text = await on_danmaku(event)
    code, name = utils.get_danmuku_result(text)
    if code == -1 :
        return -1, 'error'
    else : 
        ifsucc = await music_downloader(name)
        if ifsucc == -1 :
            return -1, 'error'
        else :
            print("呦西")
            #放入播放队列
            return 1, name



#音乐下载
async def music_downloader(name):
    code, mess = music_download(name)
    print("downloading......")
    if code == -1 :
        print(mess)
    else :
        print("success download: " + mess)
    return code


# async def test():
#     while True:
#         await sleepd()
        

# async def sleepd():
#     await asyncio.sleep(1)
#     print("11111111/2")

# async def main():
#     task1 = room.connect()
#     task2 = test()
#     await asyncio.gather(task1, task2)

if __name__ == "__main__":
    print("start")
    #asyncio.run(room.connect())



