
import utils
from WangyiyunMusicApi import music_download



#弹幕抓取
async def on_danmaku(event):
    # 收到弹幕
    text = event['data']['info'][1]
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
        return 1, name



#音乐下载
async def music_downloader(name):
    code, mess = music_download(name)
    print("downloading......")
    if code == -1 :
        print("failed download :" + mess)
    else :
        print("success download: " + mess)
    return code


if __name__ == "__main__":
    print("start")
    #asyncio.run(room.connect())

