import os
import urllib.request
import re

#音乐下载
def download(url, name):
    path = os.path.join(os.getcwd(), 'music')
    if not os.path.exists(path):
        os.mkdir(path=path)
    
    file_path, _ = urllib.request.urlretrieve(url=url, filename=os.path.join(path, f'{name}.mp3'))
    print(file_path)
    
#处理弹幕
def get_danmuku_result(str):
    ret = re.match("^点歌-[\S]*", str)
    if ret:
        name = re.findall(r"^点歌-(.+)", str)
        print(name)
        format_name = name[0].replace(" ", "_")
        return 1, format_name
    else:
        return -1, "NULL"

#处理 FIFO 传来的 bytes
def str_2_name(buffer):
    ret = re.findall(r"/(.*?)/", buffer)
    return ret

#创建FIFO
def creat_FIFO(name):
    if not os.path.exists('./fifo/'):
        os.mkdir('./fifo/')
    path = './fifo/' + name
    if not os.path.exists(path):
        os.mkfifo(path)

#删除FIFO
def delete_FIFO(name):
    path = './fifo/' + name
    os.remove(path)

#删除音乐文件
def delete_music(name):
    video_path = './video/' + name + '.flv'
    music_path = './music/' + name + '.mp3'
    os.remove(video_path)
    os.remove(music_path)