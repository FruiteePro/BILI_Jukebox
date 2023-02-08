import scheduler
import ffmpeg_cmd
import globaler as gl
from WangyiyunMusicApi import music_download
import utils

from bilibili_api import live
import zipfile
import wget
import asyncio
import logging
import yaml
import os



def get_default_info():
    try:
        yaml_path = "./conf/config.yaml"
        room_id = 0
        rtmp_addr = ""
        live_code = ""
        SESSDATA = ""
        BILI_JCT = ""
        BUVID3 = ""
        default_list = ['2:23 AM', '七里香']

        if not os.path.exists("./music"):
            os.mkdir("./music")
        if not os.path.exists("./images"):
            os.mkdir("./images")
        if not os.path.exists("./video"):
            os.mkdir("./video")
        if not os.path.exists("./image_video"):
            os.mkdir("./image_video")
        if not os.path.exists("./conf"):
            os.mkdir("./conf")
        if not os.path.exists("./font"):
            os.mkdir("./font")
        
        logging.info("Dir loaded successfully.")

        if not os.path.exists("./font/SmileySans-Oblique.ttf"):
            try:
                logging.info("Font can not find. Start to download...")
                url = "https://github.com/atelier-anchor/smiley-sans/releases/download/v1.1.1/smiley-sans-v1.1.1.zip"
                wget.download(url, "SmilySans.zip")
                zip_file = zipfile.ZipFile("SmilySans.zip")
                zip_extract = zip_file.extractall("./font")
                zip_extract.close()

            except Exception as e:
                logging.error(e)
        
        logging.info("Font loaded successfully.")

        if not os.path.exists(yaml_path):
            logging.info("yaml file can not be found. Start to create...")
            room_id = input("room id:")
            rtmp_addr = input("rtmp addr:")
            live_code = input("live code:")
            SESSDATA = input("SESSDATA:")
            BILI_JCT = input("BILI_JCT:")
            BUVID3 = input("BUVID3:")

            yaml_data = {
                "room_id": room_id,
                "rtmp_addr": rtmp_addr,
                "live_code": live_code,
                "default_list": default_list,
                "SESSDATA": SESSDATA,
                "BILI_JCT": BILI_JCT,
                "BUVID3": BUVID3
            }
            with open(yaml_path,"w") as f:
                yaml.safe_dump(data=yaml_data, stream=f)
            logging.info("yaml file created successfully.")

            gl.room_id = room_id
            gl.rtmp_addr = rtmp_addr
            gl.live_code = live_code
            gl.default_list = default_list
            gl.SESSDATA = SESSDATA
            gl.BILI_JCT = BILI_JCT
            gl.BUVID3 = BUVID3

            logging.info("yaml file loaded successfully")

        else:
            with open(yaml_path, 'r') as f:
                yaml_data = yaml.safe_load(f.read()) 

                gl.room_id = int(yaml_data["room_id"])
                gl.rtmp_addr = yaml_data["rtmp_addr"]
                gl.live_code = yaml_data["live_code"]
                gl.default_list = yaml_data["default_list"]
                gl.SESSDATA = yaml_data["SESSDATA"]
                gl.BILI_JCT = yaml_data["BILI_JCT"]
                gl.BUVID3 = yaml_data["BUVID3"]

                logging.info("yaml file loaded successfully")

    except Exception as e:
        logging.error(e)
    
    

async def initialization():
    # initialize images
    for file in os.listdir("./images/"):
        if file.endswith(".jpg"):
            image_name = file.split('.')[0]
            logging.debug(image_name)
            await ffmpeg_cmd.trans_image(image_name)
            image_video_path = "./image_video/" + image_name + ".flv"
            if not os.path.exists(image_video_path):
                await ffmpeg_cmd.make_default_video(image_name)

    # initialize default musics
    remove_list = []
    for music in gl.default_list:
        video_path = "./video/" + music + ".flv"
        music_path = "./music/" + music + ".mp3"
        if not os.path.exists(video_path):
            code_num = 1
            if not os.path.exists(music_path):
                code_num, mess = music_download(music)

            if code_num == 1:
                code_num, _ = await ffmpeg_cmd.make_video_2(music, music)
            
            if code_num == -1:
                logging.warning("music {} initialize failed".format(music))
                remove_list.append(music)
                continue
    for item in remove_list:
        gl.default_list.remove(item)
    
    
 

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(initialization())
    logging.info("Please start your Live.")
    sig = input("If Live is start? [y/n]")
    if sig == 'y' or sig == 'Y':
        scheduler.setup()
    else:
        logging.info("Please run again when you start your Live.")