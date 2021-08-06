#!/home/hvianna/anaconda3/bin/python

import pandas as pd
import requests
from bs4 import BeautifulSoup


def links_bny(name_output):
    '''
    Descrever função

    '''

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}

    with requests.Session() as s:

        s.trust_env = False

        # Accessing the BNY web site and making the
        # post request form to each one of the asset management
        # Finding the authentication needed to gain access to Pegasus Module

        main_page = 'https://servicosfinanceiros.bnymellon.com/AppPages/investimentfunds/funds.aspx'
        r = s.get(main_page, headers=headers)

        busca = {
            "__EVENTTARGET": [],
            "__EVENTARGUMENT": [],
            "__VIEWSTATE": [],
            "__VIEWSTATEGENERATOR": [],
            "__EVENTVALIDATION": [],
            "ctl00$ContentPlaceHolder$txtNomeFundo": "",
            "ctl00$ContentPlaceHolder$ibtOk.x": "21",
            "ctl00$ContentPlaceHolder$ibtOk.y": "24",
            "ctl00$ContentPlaceHolder$ddlGestor": [],
            "ctl00$ContentPlaceHolder$ddlTipoFundo": ""}

        soup = BeautifulSoup(r.content, 'html.parser')
        div_tags = soup.find_all('input')

        busca['__EVENTTARGET'].append(div_tags[0]['value'])
        busca['__EVENTARGUMENT'].append(div_tags[1]['value'])
        busca['__EVENTVALIDATION'].append(div_tags[4]['value'])
        busca['__VIEWSTATE'].append(div_tags[2]['value'])
        busca['__VIEWSTATEGENERATOR'].append(div_tags[3]['value'])

        # Getting a list all the Asset management
        # in BNY web site

        inicial_list = {'ASSET': [], 'ID_CONSULTA': []}

        x = soup.find_all('option')
        for i in x:
            conteudo_asset = i.contents[0]
            id_asset = i.attrs['value']

            if len(id_asset) == 0: continue
            if 'Fundo de Investimento' in conteudo_asset: continue
            if 'Fundo Mútuo' in conteudo_asset: continue
            if 'FUNCINE' in conteudo_asset: continue
            if 'Clube de Investimento' in conteudo_asset:
                continue

            else:
                inicial_list['ASSET'].append(conteudo_asset)
                inicial_list['ID_CONSULTA'].append(id_asset)

        # Consulting each on each one of the IDs
        # to get all the funds on the website

        my_pages = []
        controle = {'TOTAL': []}
        list_2 = {'FUNDOS': [], 'CNPJ': [], 'URL': []}

        key_list = list(inicial_list.keys())
        val_list = list(inicial_list.values())

        gestores = val_list[0]
        gestores_ids = val_list[1]

        my_size = len(gestores_ids)
        controler = 0

        for asset_id in gestores_ids:

            try:

                # EXTRACT INFORMATION (FROM FIRST PAGE)
                #    - NOME
                #    - CNPJ
                #    - ITEM

                mult_page = {
                    "__EVENTTARGET": 'ctl00$ContentPlaceHolder$grvFundos',
                    "__EVENTARGUMENT": [],
                    "__VIEWSTATE": [],
                    "__VIEWSTATEGENERATOR": [],
                    "__EVENTVALIDATION": [],
                    "ctl00$ContentPlaceHolder$txtNomeFundo": "",
                    "ctl00$ContentPlaceHolder$ddlGestor": [],
                    "ctl00$ContentPlaceHolder$ddlTipoFundo": ""}

                mult_page['ctl00$ContentPlaceHolder$ddlGestor'].clear()
                mult_page['ctl00$ContentPlaceHolder$ddlGestor'].append(asset_id)

                busca['ctl00$ContentPlaceHolder$ddlGestor'].clear()
                busca['ctl00$ContentPlaceHolder$ddlGestor'].append(asset_id)

                r = s.post(main_page, data=busca, headers=headers)

                #############################################################
                # In case that asset has more than one page
                # We need those informations to make "n" page extraction

                soup2 = BeautifulSoup(r.content, 'html.parser')
                div_tags2 = soup2.find_all('input')

                mult_page['__VIEWSTATE'].append(div_tags2[2]['value'])
                mult_page['__VIEWSTATEGENERATOR'].append(div_tags2[3]['value'])
                mult_page['__EVENTVALIDATION'].append(div_tags2[4]['value'])
                #############################################################

                soup = BeautifulSoup(r.content, 'html.parser')

                tags = soup.find_all('a')
                for tag in tags:

                    try:
                        narrow_it = tag.contents[0]
                        fund_url = tag.get('href', None)

                        if 'Fundos Administrados' in narrow_it: continue
                        if 'Agentes Autônomos' in narrow_it: continue
                        if 'Documentos Relacionados' in narrow_it: continue
                        if 'Acesso Restrito' in narrow_it: continue
                        if 'Política de Privacidade' in narrow_it: continue
                        if 'Cookies' in narrow_it: continue

                        if 'fund.aspx' in fund_url:
                            list_2['URL'].append(
                                f'https://servicosfinanceiros.bnymellon.com/AppPages/investimentfunds/{fund_url}')

                        if len(narrow_it) == 0:
                            continue

                        if len(narrow_it) > 3:
                            list_2['FUNDOS'].append(narrow_it)
                            controle['TOTAL'].append(narrow_it)

                        if len(narrow_it) < 2:
                            my_pages.append(narrow_it)

                    except:
                        continue

                tags_02 = soup.find_all('span', class_='mellon-text0')
                for goal in tags_02:
                    try:

                        narrow_it_02 = goal.contents[0]

                        if len(narrow_it_02) == 18:
                            if "Ltda" in narrow_it_02: continue
                            if "S.A" in narrow_it_02: continue
                            if "LTDA" in narrow_it_02:
                                continue

                            else:
                                narrow_it_02.split('-')
                                list_2['CNPJ'].append(narrow_it_02)

                    except:
                        continue

                #############################################################
                # EXTRACTING INFO FROM THOSE ASSETS WHO HAD
                # MORE THAN 1 PAGE

                for page in my_pages:

                    next_page = f'Page${page}'
                    mult_page['__EVENTARGUMENT'].clear()
                    mult_page['__EVENTARGUMENT'].append(next_page)

                    next_page = s.post(main_page, data=mult_page, headers=headers)
                    soup_add = BeautifulSoup(next_page.content, 'html.parser')

                    tags = soup_add.find_all('a')
                    for tag in tags:

                        try:
                            narrow_it = tag.contents[0]
                            fund_url = tag.get('href', None)

                            if 'Fundos Administrados' in narrow_it: continue
                            if 'Agentes Autônomos' in narrow_it: continue
                            if 'Documentos Relacionados' in narrow_it: continue
                            if 'Acesso Restrito' in narrow_it: continue
                            if 'Política de Privacidade' in narrow_it: continue
                            if 'Cookies' in narrow_it: continue

                            if 'fund.aspx' in fund_url:
                                list_2['URL'].append(
                                    f'https://servicosfinanceiros.bnymellon.com/AppPages/investimentfunds/{fund_url}')

                            if len(narrow_it) == 0:
                                continue

                            if len(narrow_it) > 3:
                                list_2['FUNDOS'].append(narrow_it)
                                controle['TOTAL'].append(narrow_it)

                        except:
                            continue

                    tags_02 = soup_add.find_all('span', class_='mellon-text0')
                    for goal in tags_02:

                        try:
                            narrow_it_02 = goal.contents[0]

                            if len(narrow_it_02) == 18:
                                if "Ltda" in narrow_it_02: continue
                                if "S.A" in narrow_it_02: continue
                                if "LTDA" in narrow_it_02:
                                    continue

                                else:
                                    narrow_it_02.split('-')
                                    list_2['CNPJ'].append(narrow_it_02)

                        except:
                            continue

                #############################################################

                controler += 1

                controle['TOTAL'].clear()
                my_pages.clear()
                print(my_size - controler)

            except:
                controler += 1
                print(my_size - controler)
                pass

    s.close()

    df = pd.DataFrame(list_2)
    df.to_excel(name_output, index=False)
    print('Informações extraídas com sucesso')
