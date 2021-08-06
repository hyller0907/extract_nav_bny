#!/home/hvianna/anaconda3/bin/python

from search_it import GET_NEV

import pandas as pd
import requests
from bs4 import BeautifulSoup
from easygui import *
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from datetime import date
from pandas.tseries.offsets import BDay




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

    df_final.to_excel('output_file.xlsx', index = False)
    print('Script Finalizado')

else:  # user chose Cancel
    print('Favor realizar a importação do seu modelo de consulta')
    sys.exit(0)
