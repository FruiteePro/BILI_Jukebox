# BILI_Jukebox
A jukebox on bilibili live

这是一个在哔哩哔哩直播平台运行的直播点歌机

## 运行环境：

ffmpeg

python 3.10.5

ffmpy3 0.2.4

bilibili_api 14.2.0

还有什么别的可能忘了，报错再装也行。

### 快速使用：

将仓库 git clone 到目录中，进入仓库。

输入命令：

```shell
python ./start.py
```

按照提示输入哔哩哔哩直播的直播间号，rtmp地址和直播码等等。SESSDATA，BILI_JCT和BUVID3的配置请参考[bilibili_api的开发文档](https://bili.moyu.moe/#/get-credential)。

待完成初始化后，```ctrl+c``` 关掉程序。

修改 ```conf/config.yaml``` ，配置默认歌单。在 ```images``` 文件夹中放入默认直播封面。

在哔哩哔哩开启直播，并再次执行start文件。

然后就可以在直播间发癫了（笑。

## 特别鸣谢：

没这两个爹会死：

	[Bilibili_api](https://bili.moyu.moe/#/)

	[ffmpy](https://ffmpy-zh.readthedocs.io/zh/latest/)

还有有空帮我找bug的朋友们：

	BLHSSSG

	FireV0dka
    
	一只罗白

## 后记：

这个点歌机其实就是写着玩的，其实并不太好用，但好歹是能用。

这大概是俺第一个从头到尾自己搞的小玩意，写的代码实在是烂，要是吵到您的眼睛了真是对不起orz（下次还敢。
