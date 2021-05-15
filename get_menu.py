from requests import get
import urllib.request
from bs4 import BeautifulSoup
from io import BytesIO
import pathlib
from datetime import datetime

import pdfplumber

def save_menu(menu):
    with open("menu.pdf",'wb') as f:
        f.write(menu)
    

menu_file = pathlib.Path('menu.pdf')
if menu_file.exists():
    if datetime.fromtimestamp(menu_file.stat().st_mtime).date() == datetime.now().date():
        pdf = pdfplumber.open("menu.pdf")
    else:
        id = BeautifulSoup(get("https://www.lycee-louis-lachenal.fr/fr/menus").content,"html.parser").iframe["src"][32:-8]
        menu = urllib.request.urlopen(f"https://drive.google.com/u/0/uc?id={id}&export=download").read()
        save_menu(menu)
        pdf = pdfplumber.open(BytesIO(menu))

else:
    id = BeautifulSoup(get("https://www.lycee-louis-lachenal.fr/fr/menus").content,"html.parser").iframe["src"][32:-8]
    menu = urllib.request.urlopen(f"https://drive.google.com/u/0/uc?id={id}&export=download").read()
    save_menu(menu)
    pdf = pdfplumber.open(BytesIO(menu))
    

page = pdf.pages[0]

lundi = (36,29,192,340)
mardi = (191,29,348,340)
mercredi = (347,29,504,340)
jeudi = (503,29,667,340)
vendredi = (666,29,831,340)

def get_all(days):
    ret = {}
    for day in days:
        info = page.within_bbox(day).extract_text().replace("   "," ").replace("  "," ").replace("","")

        ret[info[:info.index("\n")]] = info[info.index("\n")+1:]
    return ret

if __name__ == '__main__':
    print(get_all([lundi,mardi,mercredi,jeudi,vendredi]))
