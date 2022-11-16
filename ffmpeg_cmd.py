import asyncio
from ffmpy3 import FFmpeg



def make_video(name):
    audio_name = "./music/" + name + ".mp3"
    video_name = "./video/" + name + ".mp4"
    image_name = "./images/p1.jpg"
    ff = FFmpeg (
        inputs = {image_name : ['-loop', '1', '-r', '30'], audio_name : None},
        outputs= {video_name : ['-c:v', 'libx264', '-c:a', 'copy','-b:v', '2M', '-s', '1920x1080', '-shortest', '-y']}
    )
    print(ff.cmd)
    ff.run()


if __name__ == "__main__":
    name = "七里香"
    make_video(name)



