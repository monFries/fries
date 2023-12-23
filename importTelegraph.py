import requests
import re
from bs4 import BeautifulSoup
import yaml


preferences = open("toys/preferences.yml")
dict_preferences = yaml.safe_load(preferences)
preferences.close()
dict_telepages = dict_preferences['telepages']

'''
dict_telepages = {
    'mis_canales': 'https://telegra.ph/my-07-27-5',

    'eventos': 'https://telegra.ph/eventos-07-24',
    'canales_extras': 'https://telegra.ph/canales-07-24-4',
}
'''

def importTG(telepage):
    try:
        string = ""
        contenido = ""

        page1 = requests.get(dict_telepages[telepage])
        soup1 = BeautifulSoup(page1.text, 'html.parser')

        if page1.status_code != 200:
            pass
        else:
            j = 0
            for content in soup1.find_all(['p', 'h3', 'h4', 'a']):
                if len(content.text.strip()) < 40 and not (content.text.startswith('http')):
                    title = content.text.strip()
                    j = 1
                elif len(content.text.strip()) == 40 and j == 1:
                    ids = content.text
                    string += str((title + "\n" + ids + "\n"))
                    j = 0
                elif content.text.startswith('http') and j == 1:
                    ids = content.text
                    string += str((title + "\n" + ids + "\n"))
                    j = 0

            contenido = ((string.replace(u'\xa0', u' ')).strip())

    except Exception as e:
        print("importTG : ERROR :", e)

    if contenido != "":
        print("importTG : INFO : canales importados de Telegraph")
    else:
        print("importTG : INFO : no hay canales en Telegraph")

    return contenido
