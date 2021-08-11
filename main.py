#!/home/hvianna/anaconda3/bin/python

'''

Your script you just need to make your script executable.
Something like chmod a+x [your-script].py should make it
executable and then you can just call ./[your-script.py]
in shell.

'''

from cont_df import jdf
from mellon_links import links_bny
from nav_info import get_nav
from step4 import finalstep

import os

my_files = r'/home/hvianna/Desktop/bny_extract/my_files'

urls = os.path.join(my_files, "bny_urls.xlsx")
finput = os.path.join(my_files, "my_input.xlsx")
final_output = 'CotaDiaria_BNY'

if __name__ == "__main__":
    double_check = os.path.isfile(urls)

    if double_check == False:
        links_bny(name_output=urls, move_to=my_files)

    if double_check == True:
        pre_df = jdf(bny_file=urls, user_file=finput)
        final_dataframe = get_nav(tg_dataframe=pre_df)
        fatality = finalstep(df_extracted=final_dataframe, file_output=final_output)

print('Código executado com sucesso')
