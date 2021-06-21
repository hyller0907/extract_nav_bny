import pandas as pd
import requests
from bs4 import BeautifulSoup
from easygui import *
from tkinter import *
import tkinter as tk
from tkinter import filedialog


# !jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10

def GET_NEV(df):
    search = pd.DataFrame(df)
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


# message / information to be displayed on the screen
message = "WARNING: Gostaria de atualizar a lista existente dos fundos, disponíveis no site da BNY MELLON ?"

# title of the window
title = "Security Warning"

# creating a continue cancel box
output = ccbox(message, title)

# if user pressed continue
if output:

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}

    with requests.Session() as s:

        s.trust_env = False

        '''
        Accessing the BNY web site and making the
        post request form to each one of the asset management

        '''

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

        '''
        Getting a list all the Asset management
        in BNY web site    
        '''

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

        '''
        Consulting each on each one of the IDs
        to get all the funds on the website
        '''

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
                '''
                EXTRACT INFORMATION (FROM FIRST PAGE)
                    - NOME
                    - CNPJ
                    - ITEM
                '''

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
    df.to_excel('EXTRACTED_BNY.xlsx', index=False)
    print('Informações extraídas com sucesso')

# pressed cancel
else:
    df = pd.read_excel('EXTRACTED_BNY.xlsx')
    print('Etapa de atualização ignorada')
    # sys.exit("Error message")

msg = "Na etapa a seguir, você deve importar uma planilha em Excel com o CNPJ dos fundos\
que deseja buscar, lembrando que o título da coluna deve ser 'CNPJ' (Consultar arquivo modelo_consulta.xlsx)"

title = "Importar Serviço"

if ccbox(msg, title):  # show a Continue/Cancel dialog
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    df_search = pd.read_excel(file_path)
    df_search['CHECK'] = 'EXTRACT'

    goal_link = pd.merge(df, df_search, on='CNPJ', how='left')
    links = goal_link[(goal_link['CHECK'] == 'EXTRACT')].copy()

    df_final = GET_NEV(links)
    my_dict = {'data': [], 'cota': []}
    res = [ele for ele in df_final['INFO'] if ele.strip()]

    count = 0
    for i in res:
        resultado = []
        x = i.split('\n')

        for info in x:
            if info.strip():
                resultado.append(info)
                #print(info)

        resultado_clean = [i for i in resultado if i!='nao_encontrada']
        
        today = date.today()
        target_day = today - BDay(1)
        extract_carteiras_day = target_day.strftime("%d/%m/%Y")
        
        '''
        Por algum motivo o site esta apresentando erro
        em algumas solicitações de cota
        
        Verificar posteriormente o motivo
        '''
        
        if len(resultado_clean) > 0:
            my_dict['data'].append(resultado_clean[1])
            my_dict['cota'].append(resultado_clean[3])
            
        else:
            my_dict['data'].append(extract_carteiras_day)
            my_dict['cota'].append('NaN')
            continue

        count += 1

    df_final['DATA'] = my_dict['data']
    df_final['COTA'] = my_dict['cota']
    df_final = df_final.drop(['CHECK', 'INFO'], axis = 1)
    df_final = df_final.reset_index(drop = True)
    
    df_final.to_excel('RESULT.xlsx', index = False)
    print('Script Finalizado')

else:  # user chose Cancel
    print('Favor realizar a importação do seu modelo de consulta')
    sys.exit(0)
