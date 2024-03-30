import yaml
dict_canales = {}
dict_nombres ={}

preferences = open("toys/preferences.yml")
dict_preferences = yaml.safe_load(preferences)
preferences.close()

dict_nombres = dict_preferences['nombres']
dict_canales = dict_preferences['canales']
dict_epgs = dict_preferences['epgs']
group_title_order = dict_preferences['group_title_order']
#group_title_order = ["Eventos", "DAZN F1", "LaLiga", "M+ Champions", "Mis canales", "DAZN", "M+ Deportes", "M+ LaLiga Hypermotion", "Otros deportes", "electroperra", "Otros"]

def correct_channel_name(channel_name):
    for key in dict_nombres:
        if dict_nombres[key]['name'] in channel_name:
            channel_name = channel_name.replace(dict_nombres[key]['name'], dict_nombres[key]['replace'])
            return channel_name.strip()

    return channel_name.strip()


def get_channel_list(channel_dict):

    channel_list = []
    logo = ''

    #for channel_id, channel_name in channel_dict.items():
    for channel in channel_dict:
        channel_name = channel['name']
        channel_id = channel['id']

        if channel_name.startswith("eventos"):
            channel_name = channel_name[7:]
            group_title = 'Eventos'
            tvg_id = 'OTROS'
            logo = 'https://telegra.ph/file/c96c897856acfd7ed5671.png'

        elif channel_name.startswith("miscana"):
            channel_name = channel_name[7:]
            group_title = 'Mis canales'
            tvg_id = 'OTROS'
            logo = 'https://telegra.ph/file/c96c897856acfd7ed5671.png'

        elif channel_name.startswith("ep"):
            channel_name = channel_name
            group_title = 'UHD'
            tvg_id = 'OTROS'
            logo = 'https://telegra.ph/file/c96c897856acfd7ed5671.png'

        else:
            for key in dict_canales:
                if channel_name == dict_canales[key]['channel_name']:
                    group_title = dict_canales[key]['group_title']
                    tvg_id = dict_canales[key]['tvg_id']
                    logo = dict_canales[key]['logo']
                    break
                else:
                    channel_name = channel_name
                    group_title = 'Otros deportes'
                    tvg_id = 'nil'
                    logo = 'https://telegra.ph/file/c96c897856acfd7ed5671.png'

        identif = (channel_id[0:4])
        if identif == 'http':
            identif = ''

        channel_info = {"group_title": group_title,
                        "tvg_id": tvg_id,
                        "logo": logo,
                        "channel_id": channel_id,
                        "channel_name": channel_name + "  " + identif}

        channel_list.append(channel_info)

    return channel_list
