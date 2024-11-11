import utils as u
from importTelegraph import *
from ipfs_scraper import get_acelinks_ipfs
from mixer import mix_listas

#from tools import *
#from getElcano import *
#from getElcanoWeb import *
# Push from terminal from a second user
# git config --local credential.helper ""

check = 0
channels_dict = []

def export_messages():


        #channel_dict = dict()  # {channel_id: channel_name}
        cleansed_content = ""
        #all_channels = u.dict_epgs + '\n\n' + '#EXTINF:-1 tvg-logo="https://telegra.ph/file/c96c897856acfd7ed5671.png", elcano by Lucas' + '\n' + 'https://www.dropbox.com/scl/fi/4kcyvcbz0as0lgrkr23rl/canal_off.mp4?rlkey=vrgvew6phshrgfdg4xwjxcllt&st=qnagguh4&dl=1' + '\n'
        all_channels = u.dict_epgs + '\n\n'

        
        events = importTG('eventos')
        cleansed_content = cleanse_events(events)
        channel_dict = update_channel_dict(cleansed_content)
        all_channels += export_channels(channel_dict)

        extras = importTG('canales_extras')
        cleansed_content = cleanse_general(extras)

        elcano = read_cached_elcano()
        cleansed_content += cleanse_general(elcano)

        misCanales = importTG('mis_canales')
        cleansed_content += cleanse_misCanales(misCanales)
        channel_dict = update_channel_dict(cleansed_content)
        all_channels += export_channels(channel_dict)

        '''
        electroperra = import_ep()
        if electroperra is not None:
            cleansed_content = cleanse_electro(electroperra)
            channel_dict = update_channel_dict(cleansed_content)
            all_channels += export_channels(channel_dict)

        elPlan = import_elPlan()
        if elPlan is not None:
            cleansed_content = cleanse_elPlan(elPlan)
            channel_dict = update_channel_dict(cleansed_content)
            all_channels += export_channels(channel_dict)
        '''
    
        write_channel_lists(all_channels)

def read_cached_elcano():
    with open('toys/cachedList.txt', 'r') as cachedlist:
        contenido = cachedlist.read()
        cachedlist.close()
        print("read_cached_elcano: INFO: returning elcano cacheado")
        return (contenido)


def cleanse_events(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'

    #if re.search(channel_id_regex, message_content):
    for i, row in enumerate(rows):
        if re.search(channel_id_regex, row) or row.startswith("http"):
            if i > 0:
                cleansed_content += "eventos" + rows[i - 1] + "\n" + row + "\n"
            else:
                cleansed_content += "eventos" + "Canal" + "\n" + row + "\n"

    return cleansed_content


def cleanse_misCanales(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'

    #if re.search(channel_id_regex, message_content):
    for i, row in enumerate(rows):
        if re.search(channel_id_regex, row) or row.startswith("http"):
            if i > 0:
                cleansed_content += "miscana" + rows[i - 1] + "\n" + row + "\n"
            else:
                cleansed_content += "miscana" + "Canal" + "\n" + row + "\n"

    return cleansed_content


def cleanse_general(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'
    
    #if re.search(channel_id_regex, message_content):
    for i, row in enumerate(rows):
        if re.search(channel_id_regex, row) or row.startswith("http"):
            if i > 0:
              cleansed_content += rows[i-1] + "\n" + row + "\n"
            else:
              cleansed_content += "Canal" + "\n" + row + "\n"

    return cleansed_content

'''
def cleanse_electro(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'

    if re.search(channel_id_regex, message_content):
        for i, row in enumerate(rows):
            if re.search(channel_id_regex, row) or row.startswith("http"):
                if i > 0:
                    cleansed_content += "electro" + rows[i - 1] + "\n" + row + "\n"
                else:
                    cleansed_content += "electro" + " Canal" + "\n" + row + "\n"

    return cleansed_content

def cleanse_elPlan(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'

    if re.search(channel_id_regex, message_content):
        for i, row in enumerate(rows):
            if re.search(channel_id_regex, row) or row.startswith("http"):
                if i > 0:
                    cleansed_content += "elPlan_" + rows[i - 1] + "\n" + row + "\n"
                else:
                    cleansed_content += "elPlan_" + " Canal" + "\n" + row + "\n"

    return cleansed_content
'''

'''
def update_channel_dict(message_content):

    channel_dict = dict()
    rows = message_content.split("\n")
    
    for i, row in enumerate(rows):
        if i % 2 == 1:
            channel_id = row
            channel_name = rows[i-1]
            channel_name = u.correct_channel_name(channel_name)  
            channel_dict[channel_id] = channel_name

    return channel_dict

'''
def update_channel_dict(message_content):

    global check
    channel_dict = dict()
    rows = message_content.split("\n")
    for i, row in enumerate(rows):
        if i % 2 == 1:
            channel_id = row
            channel_name = rows[i-1]
            check += 1
            channel_name = u.correct_channel_name(channel_name)

            channel_dict = {
                "index": check,
                "name": channel_name,
                "id": channel_id
            }
            channels_dict.append(channel_dict)

    #print(channels_dict)
    return channels_dict


def export_channels(channel_dict):

    channel_list = u.get_channel_list(channel_dict)
    channels = ""

    channel_pattern = '#EXTINF:-1 group-title="GROUPTITLE" tvg-id="TVGID" tvg-logo="LOGO", CHANNELTITLE\nacestream://CHANNELID\n'
    channel_pattern_http = '#EXTINF:-1 group-title="GROUPTITLE" tvg-id="TVGID" tvg-logo="LOGO", CHANNELTITLE\nCHANNELID\n'


    for group_title in u.group_title_order:
        for channel_info in channel_list:
            if channel_info["group_title"] == group_title:
                if "http" in channel_info["channel_id"]:
                    ch_pattern = channel_pattern_http
                else:
                    ch_pattern = channel_pattern
                channel = ch_pattern.replace("GROUPTITLE", channel_info["group_title"]) \
                                               .replace("TVGID", channel_info["tvg_id"]) \
                                               .replace("LOGO", channel_info["logo"]) \
                                               .replace("CHANNELID", channel_info["channel_id"]) \
                                               .replace("CHANNELTITLE", channel_info["channel_name"])
                channels += channel

    return channels


def write_channel_lists(all_channels):

    if all_channels != "":
        
        all_channels_kodi = all_channels.replace("acestream://", "plugin://script.module.horus?action=play&id=")
        all_channels_get = all_channels.replace("acestream://", "http://127.0.0.1:6878/ace/getstream?id=")
        all_channels_int = all_channels.replace("acestream://", "http://192.168.1.90:8008/ace/getstream?id=")
        #all_channels_rasp = all_channels.replace("acestream://", "http://<ipraspberry>:6878/ace/getstream?id=")

        with open("base.txt", "w") as f:
            f.write(all_channels)
            print("exportChannels : OK : list exported")
            f.close()

        with open("kodi.txt", "w") as k:
            k.write(all_channels_kodi)
            print("exportChannels : OK : kodi list exported")
            k.close()

        with open("get.txt", "w") as g:
            g.write(all_channels_get)
            print("exportChannels : OK : get list exported")
            g.close()
            
        with open("int.txt", "w") as int:
            int.write(all_channels_int)
            print("exportChannels : OK : int list exported")
            int.close()

        '''
        with open("rasp.txt", "w") as rasp:
            rasp.write(all_channels_rasp)
            print("exportChannels : OK : rasp list exported")
            rasp.close()
        '''
            
    else:
        print("exportChannels : ERROR : list is empty")
        

if __name__ == "__main__":
    #scraper()
    #getCachedList()
    get_acelinks_ipfs()
    mix_listas()

    #asyncio.run(main())
    export_messages()

