from bs4 import BeautifulSoup

import pandas as pd
import requests

def get_nav(tg_dataframe):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}

    search = pd.DataFrame(tg_dataframe)
    my_urls = search['URL']

    nev_extracted = []
    for consulta in my_urls:
        try:
            with requests.Session() as s:
                s.trust_env = False

                r = s.get(consulta, headers=headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                x = soup.find('div', class_="dadosCotas")
                nev_extracted.append(x.text)

            s.close()

        except:
            nev_extracted.append('nao_encontrada')
            continue

    search['INFO'] = nev_extracted
    return search
