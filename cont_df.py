#!/home/hvianna/anaconda3/bin/python

import pandas as pd


def jdf(bny_file, user_file):
    '''
    Esta função irá concatenar 2 DataFrames
        - O principal, contendo a informações de todos os links da BNY
        - O do usuário, contendo os fundos que este deseja a cota
    '''

    df_search = pd.read_excel(user_file)
    df = pd.read_excel(bny_file)

    df_search['CHECK'] = 'EXTRACT'
    goal_link = pd.merge(df, df_search, on='CNPJ', how='left')
    links = goal_link[(goal_link['CHECK'] == 'EXTRACT')].copy()

    return links
