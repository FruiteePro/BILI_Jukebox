import imp
import os
import urllib.request
import re


def download(url, name):
    path = os.path.join(os.getcwd(), 'music')
    if not os.path.exists(path):
        os.mkdir(path=path)
    
    file_path, _ = urllib.request.urlretrieve(url=url, filename=os.path.join(path, f'{name}.mp3'))
    print(file_path)
    

def get_danmuku_result(str):
    ret = re.match("^点歌-[\S]*", str)
    if ret:
        return 1, ret.group()
    else:
        return -1, "NULL"