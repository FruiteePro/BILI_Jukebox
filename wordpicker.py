from bilibili_api import live
import json
import asyncio
import utils
from WangyiyunMusicApi import music_download

#room = live.LiveDanmaku(21282223)
room = live.LiveDanmaku(6)

#弹幕抓取

async def on_danmaku(event):
    # 收到弹幕
    text = event['data']['info'][1]
    #print(json.dumps(event, indent=2))
    print(text)
    return text


#弹幕解析
@room.on('DANMU_MSG')
async def analysis_danmuku(event):
    text = await on_danmaku(event)
    code, name = utils.get_danmuku_result(text)
    if code == -1 :
        return 0
    else : 
        ifsucc = await music_download(name)
        if ifsucc == -1 :
            return 0
        else :
            print("呦西")
            #放入播放队列


#音乐下载
async def music_download(name):
    code, mess = music_download(name)
    if code == -1 :
        print(mess)
    else :
        print("success download" + mess)
    return code




if __name__ == "__main__":
    asyncio.run(room.connect())



