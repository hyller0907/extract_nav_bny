from yesterday import show_yday
import pandas as pd

calendar_file = 'ANBIMA.txt'

def finalstep(df_extracted, file_output):
    df_final = pd.DataFrame(df_extracted)

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

        my_yesterday = show_yday(calendar_file)
        extract_carteiras_day = my_yesterday.strftime("%d/%m/%Y")
        fname = my_yesterday.strftime("%Y%m%d")

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

    file_name = f'{file_output}{fname}.xlsx'
    df_final.to_excel(file_name, index = False)

    return file_name
