import requests
from bs4 import BeautifulSoup



def importPreferences():
    try:
        page = requests.get('https://raw.githubusercontent.com/epScraper/preferences/main/preferences.yml')
        soup = BeautifulSoup(page.text, 'html.parser')

        if page.status_code == 200:
            print("importPreferences : INFO : preferences imported")
        else:
            print("importPreferences : INFO : no preferences")
            return

    except Exception as e:
        print("importPreferences : ERROR :", e)
        return

    with open("toys/preferences.yml", "w") as p:
        p.write(soup.text)
        print("importPreferences : OK : preferences exported to disc")
        p.close()

importPreferences()
