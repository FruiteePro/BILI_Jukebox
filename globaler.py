default_list = []
called_list = []
download_list = []

room_id = 0
rtmp_addr = ""
live_code = ""

SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

usr_time = {}


def get_called_num():
    return len(called_list)

def check_music_name(name):
    if (name in called_list) or (name in download_list):
        return True
    return False

def clean_fault_music(name):
    if name in called_list:
        called_list.remove(name)
    if name in download_list:
        download_list.remove(name)

