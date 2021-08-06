#!/home/hvianna/anaconda3/bin/python

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_nav(tg_dataframe):
    '''
    BLA BLA BLA


    '''


    search = pd.DataFrame(tg_dataframe)
    my_urls = search['URL']

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}

    nev_extracted = []
    for consulta in my_urls:

        try:
            with requests.Session() as s:

                s.trust_env = False

                # Finding the authentication needed to gain access to Pegasus Module
                r = s.get(consulta, headers=headers)

                # Extracting the complete url with all the parameter
                soup = BeautifulSoup(r.content, 'html.parser')
                x = soup.find('div', class_="dadosCotas")
                nev_extracted.append(x.text)

            s.close()

        except:
            nev_extracted.append('nao_encontrada')
            continue

    search['INFO'] = nev_extracted
    return search
