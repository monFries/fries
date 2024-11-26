import sys
from bs4 import BeautifulSoup
from torpy.http.requests import TorRequests
import requests


def scraper():
    lista = ""
    print('scraper : INFO : requesting elcano...', flush=True)

    #try:
    with TorRequests() as tor_requests:
        with tor_requests.get_session() as sess:
            grab = sess.get('https://elcano.top')
            print(grab)
    #except:
        #print("scraper : INFO : torpy linea 22 could not access elcano")
        #sys.exit(1)

    soup = BeautifulSoup(grab.text, 'html.parser')
    for enlace in soup.find_all('a'):
        acelink = enlace.get('href')
        canal = enlace.text

        if not str(acelink).startswith("acestream://") or canal == "aquÃ­":
            pass
        else:
            link = str(acelink).replace("acestream://", "")
            lista += str((canal + "\n" + link + "\n"))
            contenido = ((lista.replace(u'\xa0', u' ')).strip())

    if contenido != "":
        print("scraper : OK : channels retrieved")
        write_cache(contenido)
    else:
        print("scraper : INFO : could not access elcano")
    

def write_cache(contenido):

    with open("toys/cachedList.txt", "wb") as cachedlist:
        cachedlist.write(contenido.encode('latin1'))
        cachedlist.close()
        print("scraper : INFO : elcano cached")




#scraper()

